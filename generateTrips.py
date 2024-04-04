
#duarouter --net-file tJunction.net.xml --trip-files tJunction.trips.xml --output-file tJunction.rou.xml
import random
import traci
import sys
from helpers import loadParams

if len(sys.argv) > 2:
    filepath = sys.argv[1]
    index = int(sys.argv[2])
else:
    print("Usage: testrun.py filepath, index")
    sys.exit(1)

params = loadParams(filepath, index)
autonomous_weight = float(params["autonomous_weight"])
normal_weight = 1 - autonomous_weight

# Template for the .rou.xml content
rou_content = '''<trips>
    <vType id="normal" accel="2.6" decel="4.5" sigma="0.7" tau="1.2" length="5" maxSpeed="33.33" guiShape="passenger"/>
    <vType id="autonomous" accel="2.6" decel="4.5" sigma="0.0" length="5" maxSpeed="33.33" guiShape="passenger" color="0,255,0" carFollowModel="Krauss" lcStrategic="5.0" lcCooperative="5.0" lcSpeedGain="5.0" lcKeepRight="1.0" />
'''

from_edges = ['A0', 'A7', 'L0', 'L2', 'L4', 'L6', 'L8', 'L10']
to_edges = ['A1', 'A6', 'L1', 'L3', 'L5', 'L7', 'L9', 'L11']
invalid_routes = [{"from": "A0", "to": "A1"}, {"from": "A7", "to": "A6"}, 
                    {"from": "L10", "to": "L11"}, {"from": "L8", "to": "L9"},
                    {"from": "L6", "to": "L7"}, {"from": "L4", "to": "L5"},
                    {"from": "L2", "to": "L3"}, {"from": "L0", "to": "L1"}]
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

# Generate vehicles for each route
vehicle_id = 0
depart_time = 0
def chooseType():
    return random.choices(population=["normal","autonomous"], weights=[normal_weight, autonomous_weight], k=1)[0]

for j in range(1000):
    route = random.choice(routes)
    rou_content += f'    <trip id="veh_{vehicle_id}" type="{chooseType()}" from="{route["from"]}" to="{route["to"]}" depart="{depart_time}"/>\n'
    depart_time += 3
    vehicle_id += 1


rou_content += '</trips>'
# Save to a .rou.xml file
rou_file_path = 'tjunction.trips.xml'
with open(rou_file_path, 'w') as file:
    file.write(rou_content)
