import random

routes = [
    ("B0B1", "B1B2"),  # 南→北
    ("B2B1", "B1B0"),  # 北→南
    ("A1B1", "B1C1"),  # 西→东
    ("C1B1", "B1A1"),  # 东→西
    ("C1B1", "B1B0"),  # 东→南
    ("B0B1", "B1C1"),  # 南→东
    ("A1B1", "B1B2"),  # 西→北
    ("B2B1", "B1A1")   # 北→西
]

with open("single_intersection_routes.xml", "w") as f:
    f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    f.write('        xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')
    for i in range(100):
        depart = i
        edge_from, edge_to = random.choice(routes)
        f.write(f'    <vehicle id="{i}" depart="{depart}">\n')
        f.write(f'        <route edges="{edge_from} {edge_to}"/>\n')
        f.write(f'    </vehicle>\n')
    f.write('</routes>\n')
