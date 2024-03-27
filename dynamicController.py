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
simulation_type = params["control_type"]

YELLOW_LIGHT_DURATION = 3
MIN_LIGHT_DURATION = 20
STATIC_LIGHT_DURATION=42

def setState(junction_id, state):
    traci.trafficlight.setRedYellowGreenState(junction_id, state)
    return state
    
class Junction:
    def __init__(self, junction_id, state, static_state=None):
        self.junction_id = junction_id
        self.state = state
        self.queue = [] #queue of objects with {"state": "duration":}
        self.wait = 0
        self.static_state = static_state
        
    def step(self):
        if self.wait > 0:
            self.wait -= 1
            return
        else:
            if len(self.queue) > 0:
                action = self.queue.pop(0)
                self.state = setState(self.junction_id, action['state'])
                self.wait = action['duration']
                return
        return
        
    def addAction(self, state, duration):
        self.queue.append({"state": state, "duration":duration})
    


def transitionState(state):
    new_state = ''
    for val in state:
        if val in ['g', 'G']:
            new_state += 'y'
        else:
            new_state += val
    
    return new_state

def transition(junction, new_state, duration=None):
    if len(junction.queue) > 0:
        return False
    transition_state = transitionState(junction.state)
    junction.addAction(transition_state, YELLOW_LIGHT_DURATION)
    if duration is None:
        duration=MIN_LIGHT_DURATION
    junction.addAction(new_state, duration)
    return True
    

def classify_lanes(incLanes):
    # Placeholder logic: adjust based on your actual network setup
    # For example, main road lanes might have specific naming conventions
    main_road_lanes = [lane for lane in incLanes if "A" in lane]
    side_road_lanes = [lane for lane in incLanes if "L" in lane]
    return main_road_lanes, side_road_lanes

# Function to get the total queue length for main and side roads at a junction
def get_queue_length_by_road_type(junction_id):
    incLanes = traci.trafficlight.getControlledLanes(junction_id)
    main_road_lanes, side_road_lanes = classify_lanes(incLanes)
    main_queue_length = sum([traci.lane.getLastStepHaltingNumber(lane) for lane in main_road_lanes])
    side_queue_length = sum([traci.lane.getLastStepHaltingNumber(lane) for lane in side_road_lanes])
    return main_queue_length, side_queue_length
    
def evaluate_junction(junction):
    queue_length_main, queue_length_side = get_queue_length_by_road_type(junction.junction_id)  
    
    # Decide new state based on queue lengths
    if queue_length_side > queue_length_main:
        new_state = "GGgrrrrGGgrrrr"  # Favor side road
    else:
        new_state = "rrrGGGgrrrGGGg"  # Favor main road
    
    transition(junction, new_state)


def control_traffic_lights_dynamic():
    step = 0
    initial_state = "rrrGGGgrrrGGGg"
    junction_ids = ['J0', 'J1', 'J2']
    junctions = [Junction(junction_id, initial_state) for junction_id in junction_ids]
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        for junction in junctions:
            evaluate_junction(junction)
            junction.step()
                
        step += 1

def check_static_junction(junction, states):
    if len(junction.queue) > 0:
        return False
    
    junction.static_state = (junction.static_state + 1) % len(states)
    new_state = states[junction.static_state]
    transition(junction, new_state["state"], news_state["duration"])
    return True
    
    
def control_traffic_lights_static():
    step = 0
    states = [{'state': "GGgrrrrGGgrrrr", 'duration': 40}, 
            {'state': "rrrrrrGrrrrrrG", 'duration': 20}, 
            {'state': "rrrGGGgrrrGGGg", 'duration': 100}]
    junction_ids = ['J0', 'J1', 'J2']
    junctions = [Junction(junction_id, initial_state, -1) for junction_id in junction_ids]
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        for junction in junctions:
            check_static_junction(junction, states)
            junction.step()
                
        step += 1
        
    
def run():
    sumoCmd = ['sumo-gui', '-c', 'tJunction.sumocfg']
    traci.start(sumoCmd)
    if(simulation_type == "basic"):
        control_traffic_lights_dynamic() 
    elif(simulation_type == "intelligent"):
        control_traffic_lights_static()
    else:
        print("Something went VERY wrong")
    traci.close()

if __name__ == "__main__":
    run()