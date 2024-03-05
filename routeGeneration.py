# Define the number of vehicles to generate for each route
import random

num_vehicles_per_route = 30  # Adjust based on the intersection capacity

# Template for the .rou.xml content
rou_content = '''<routes>
    <vType id="normal" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="33.33" guiShape="passenger"/>
    <vType id="autonomous" accel="2.6" decel="4.5" sigma="0.0" length="5" maxSpeed="33.33" guiShape="passenger" color="0,255,0" carFollowModel="Krauss" lcStrategic="5.0" lcCooperative="5.0" lcSpeedGain="5.0" lcKeepRight="1.0" />
'''

# Routes
routes = [
    {"from": "L0", "to": "L3"},
    {"from": "L0", "to": "L5"},
    {"from": "L0", "to": "L7"},
    {"from": "L2", "to": "L1"},
    {"from": "L2", "to": "L5"},
    {"from": "L2", "to": "L7"},
    {"from": "L4", "to": "L1"},
    {"from": "L4", "to": "L3"},
    {"from": "L4", "to": "L7"},
    {"from": "L6", "to": "L1"},
    {"from": "L6", "to": "L3"},
    {"from": "L6", "to": "L5"},
]

depart_time = 0

# Generate vehicles for each route
vehicle_id = 0
for i, route in enumerate(routes):
    rou_content += f'    <route id="route_{i}" edges="{route["from"]} {route["to"]}" />\n'

def chooseType():
    return random.choices(population=["normal","autonomous"], weights=[0.8, 0.2], k=1)[0]

for j in range(200):
    rou_content += f'    <vehicle id="veh_{vehicle_id}" type="{chooseType()}" route="route_{random.randrange(0, len(routes))}" depart="{depart_time}"/>\n'
    depart_time += random.randrange(1, 11)
    vehicle_id += 1


rou_content += '</routes>'
# Save to a .rou.xml file
rou_file_path = 'tjunction.rou.xml'
with open(rou_file_path, 'w') as file:
    file.write(rou_content)

rou_file_path