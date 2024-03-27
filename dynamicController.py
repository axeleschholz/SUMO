import traci

YELLOW_LIGHT_DURATION = 3
MIN_LIGHT_DURATION = 20

def setState(junction_id, state):
    traci.trafficlight.setRedYellowGreenState(junction_id, state)
    return state
    
class Junction:
    def __init__(self, junction_id, state):
        self.junction_id = junction_id
        self.state = state
        self.queue = [] #queue of objects with {"state": "duration":}
        self.wait = 0
        
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

def transition(junction, new_state):
    if len(junction.queue) > 0:
        return
    transition_state = transitionState(junction.state)
    junction.addAction(transition_state, YELLOW_LIGHT_DURATION)
    junction.addAction(new_state, MIN_LIGHT_DURATION)
    return
    

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
        
def densityAlgorithm():
    pass

def greenWaveAlgorithm():
    pass
    
def run():
    sumoCmd = ['sumo-gui', '-c', 'tJunction.sumocfg']
    traci.start(sumoCmd)
    control_traffic_lights_dynamic()    
    traci.close()

if __name__ == "__main__":
    run()