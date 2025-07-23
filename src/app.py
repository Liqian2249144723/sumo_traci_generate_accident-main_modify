from src.config import (
    traci,
    checkBinary,
    settings,
)
import traceback
import matplotlib.pyplot as plt
import matplotlib
from src.accident import create_accident

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
matplotlib.rcParams['axes.unicode_minus'] = False    # 显示负号


def shouldContinueSim():
    return traci.simulation.getMinExpectedNumber() > 0


def get_avg_queue_length():
    edge_ids = traci.edge.getIDList()
    total_queue = 0
    count = 0
    for edge_id in edge_ids:
        if edge_id.startswith(":"):
            continue
        total_queue += traci.edge.getLastStepHaltingNumber(edge_id)
        count += 1
    return total_queue / count if count > 0 else 0


def get_avg_delay():
    edge_ids = traci.edge.getIDList()
    total_waiting_time = 0
    vehicle_count = 0
    for edge_id in edge_ids:
        if edge_id.startswith(":"):
            continue
        total_waiting_time += traci.edge.getWaitingTime(edge_id)
        vehicle_count += traci.edge.getLastStepVehicleNumber(edge_id)
    return total_waiting_time / vehicle_count if vehicle_count > 0 else 0


def get_halting_vehicle_count():
    vehicle_ids = traci.vehicle.getIDList()
    halting_count = sum(1 for v in vehicle_ids if traci.vehicle.getSpeed(v) < 0.1)
    return halting_count


def run():
    step = 0
    print("Running simulation...")

    # ✅ 初始化数据容器
    times = []
    queues = []
    delays = []
    halts = []

    try:
        while shouldContinueSim():
            current_time = traci.simulation.getTime()
            traci.simulationStep()

            # ✅ 获取三项指标
            avg_queue = get_avg_queue_length()
            avg_delay = get_avg_delay()
            halt_count = get_halting_vehicle_count()

            # ✅ 保存数据
            times.append(current_time)
            queues.append(avg_queue)
            delays.append(avg_delay)
            halts.append(halt_count)

            # ✅ 可选触发事故
            if current_time == 300:
                create_accident(mode='manual', lane_type=0)

            step += 1

    except Exception:
        print(traceback.format_exc())

    finally:
        traci.close()

        # ✅ 仿真结束后绘图并保存三张图
        plot_metric(times, queues, "平均排队长度（辆）", "avg_queue.png", "blue")
        plot_metric(times, delays, "平均延误时间（秒）", "avg_delay.png", "green")
        plot_metric(times, halts, "停车车辆数（辆）", "halting_vehicles.png", "red")

        print("仿真完成，图像已保存。")


def plot_metric(times, values, ylabel, filename, color):
    plt.figure()
    plt.plot(times, values, color=color)
    plt.xlabel("仿真时间（秒）")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} 随时间变化图")
    plt.grid(True)
    plt.savefig(filename, dpi=300)
    plt.close()


def start_simulation():
    sumoBinary = checkBinary("sumo-gui")
    traci.start([sumoBinary, "-c", settings.sumocfg_filepath, "-S", "-Q"])
    run()
