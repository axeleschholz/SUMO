# Define the number of vehicles to generate for each route
import random
import traci
import sys

if len(sys.argv) > 1:
    weights_str = sys.argv[1]
    normal_weight, autonomous_weight = map(float, weights_str.split(','))
else:
    print("Usage: routeGeneration.py normal_weight,autonomous_weight")
    sys.exit(1)

# Template for the .rou.xml content
rou_content = '''<routes>
    <vType id="normal" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="33.33" guiShape="passenger"/>
    <vType id="autonomous" accel="2.6" decel="4.5" sigma="0.0" length="5" maxSpeed="33.33" guiShape="passenger" color="0,255,0" carFollowModel="Krauss" lcStrategic="5.0" lcCooperative="5.0" lcSpeedGain="5.0" lcKeepRight="1.0" />
'''

from_edges = ['A0', 'A7', 'L0', 'L2', 'L4', 'L6', 'L8', 'L10']
to_edges = ['A1', 'A6', 'L1', 'L3', 'L5', 'L7', 'L9', 'L11']
invalid_routes = [{"from": "A0", "to": "A1"}, {"from": "A7", "to": "A6"}]
preferred_routes = [{"from": "A0", "to": "A7"}, {"from": "A1", "to": "A6"}]  # Routes to be weighted higher

# Generate all possible routes, excluding the specified invalid routes
# Weight preferred routes higher by adding them extra times
routes = []
for from_edge in from_edges:
    for to_edge in to_edges:
        route = {"from": from_edge, "to": to_edge}
        if route not in invalid_routes:
            routes.append(route)
            # If the route is preferred, duplicate its entry to increase its weight
            if route in preferred_routes:
                routes.extend([route] * 2)  # Add 2 more instances for a total of 3


depart_time = 0

sumoCmd = ['sumo-gui', '-c', 'tJunction.sumocfg']
traci.start(sumoCmd)
# Generate vehicles for each route
vehicle_id = 0
for i, route in enumerate(routes):
    edges = route = traci.simulation.findRoute(route["from"], route["to"]).edges
    rou_content += f'    <route id="route_{i}" edges="{edges}" />\n'

def chooseType():
    return random.choices(population=["normal","autonomous"], weights=[0.8, 0.2], k=1)[0]

for j in range(1000):
    rou_content += f'    <vehicle id="veh_{vehicle_id}" type="{chooseType()}" route="route_{random.randrange(0, len(routes))}" depart="{depart_time}"/>\n'
    depart_time += random.randrange(1, 6)
    vehicle_id += 1


rou_content += '</routes>'
# Save to a .rou.xml file
rou_file_path = 'tjunction.rou.xml'
with open(rou_file_path, 'w') as file:
    file.write(rou_content)

traci.close()