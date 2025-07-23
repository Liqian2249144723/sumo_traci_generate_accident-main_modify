import random

# 定义可用的起点和终点边（都必须经过 B1）
incoming_edges = ['A1B1', 'B0B1', 'C1B1', 'B2B1']
outgoing_edges = {
    'A1B1': ['B1B0', 'B1B2', 'B1C1'],
    'B0B1': ['B1A1', 'B1C1', 'B1B2'],
    'C1B1': ['B1A1', 'B1B0', 'B1B2'],
    'B2B1': ['B1A1', 'B1B0', 'B1C1']
}

with open("generated_routes.rou.xml", "w") as f:
    f.write("""<routes>
    <vType id="car" accel="2.0" decel="4.5" sigma="0.5" length="5" maxSpeed="13.89" guiShape="passenger"/>
""")

    for i in range(3600):
        depart_time = i  # 每秒一辆
        from_edge = random.choice(incoming_edges)
        to_edge = random.choice([e for e in outgoing_edges[from_edge]])

        f.write(f'    <vehicle id="veh{i}" type="car" depart="{depart_time}">\n')
        f.write(f'        <route edges="{from_edge} {to_edge}"/>\n')
        f.write(f'    </vehicle>\n')

    f.write("</routes>")
