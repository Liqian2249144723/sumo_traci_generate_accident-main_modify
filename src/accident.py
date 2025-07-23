from random import choice
from src.config import traci, settings


def create_accident(mode='auto', lane_type=None):
    """
    创建交通事故。
    mode: 'auto' 表示自动随机选一个车道；'manual' 表示手动选择 lane_type。
    lane_type: 0（右转），1（直行），2（左转）
    """
    # 所有进口道车道ID（右、直、左）
    all_lanes = {
        0: ["B0B1_0", "C1B1_0", "A1B1_0", "B2B1_0"],  # 右转
        1: ["B0B1_1", "C1B1_1", "A1B1_1", "B2B1_1"],  # 直行
        2: ["B0B1_2", "C1B1_2", "A1B1_2", "B2B1_2"],  # 左转
    }

    # 自动模式：从所有 lane 随机选
    if mode == 'auto':
        lane_ids = sum(all_lanes.values(), [])  # 展开所有 lane
        lane_id = choice(lane_ids)

    # 手动模式：根据 lane_type 选择对应方向
    elif mode == 'manual':
        if lane_type not in [0, 1, 2]:
            print("错误：lane_type 必须是 0（右转）、1（直行）、2（左转）")
            return
        lane_id = choice(all_lanes[lane_type])  # 从对应方向中随机选一个车道

    else:
        print("错误：mode 必须为 'auto' 或 'manual'")
        return

    # 获取该车道上的车辆
    vehicle_ids = traci.lane.getLastStepVehicleIDs(lane_id)
    for vehicle_id in vehicle_ids:
        if not vehicle_is_in_a_valid_position_lane(vehicle_id):
            continue

        create_vehicle_accidented(vehicle_id, lane_id)
        return  # 成功创建一个就退出


def vehicle_is_in_a_valid_position_lane(vehicle_id: str):
    position = traci.vehicle.getLanePosition(vehicle_id)
    return 0.2 * settings.lane_length < position > 0.4 * settings.lane_length


def create_vehicle_accidented(vehicle_id: str, lane_id: str):
    speed_road_accidented: float = settings.speed_road_accidented
    edge_id = traci.lane.getEdgeID(lane_id)  # 用lane接口获取对应edge ID
    traci.edge.setMaxSpeed(edge_id, speed_road_accidented)  # 传入edge ID
    traci.vehicle.slowDown(
        vehicle_id,
        slow_down_vehicle_speed(vehicle_id),
        settings.timing_to_slow_down_vehicle,
    )
    try:
        traci.vehicle.setStop(
            vehicle_id,
            edgeID=edge_id,
            pos=get_position_vehicle_will_stop(vehicle_id),
            laneIndex=traci.vehicle.getLaneIndex(vehicle_id),
            duration=settings.accident_duration_timeout,
        )
    except Exception as e:
        print(f"Error setting stop for vehicle {vehicle_id}: {e}")
        return
    set_highlight_accident(vehicle_id)
    print(
        f"{traci.simulation.getTime()} - Vehicle {vehicle_id} has been accidented in road {edge_id}"
    )



def get_road_ids_except_internals():
    road_ids: list[str] = traci.edge.getIDList()
    return [road_id for road_id in road_ids if not road_id.startswith(':')]

def slow_down_vehicle_speed(vehicle_id: str):
    return 0.2 * traci.vehicle.getAllowedSpeed(vehicle_id)


def get_position_vehicle_will_stop(vehicle_id: str):
    lane_id = traci.vehicle.getLaneID(vehicle_id)
    lane_length = traci.lane.getLength(lane_id)
    pos = traci.vehicle.getLanePosition(vehicle_id) + (0.1 * lane_length)
    pos = max(0.1, min(pos, lane_length - 0.1))
    return pos



def set_highlight_accident(vehicle_id: str):
    traci.vehicle.highlight(vehicle_id, settings.color_accident)
