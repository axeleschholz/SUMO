import traci

YELLOW_LIGHT_DURATION = 3

def getQueueLength(edgeID):
    return traci.edge.getLastStepHaltingNumber(edgeID)

def setPhase(phase):
    return traci.trafficlight.setPhase('J1', phase)

def setState(state, duration=0):
    traci.trafficlight.setRedYellowGreenState('J1', state)


def transitionState(state):
    new_state = ''
    for val in state:
        if val in ['g', 'G']:
            new_state += 'y'
        else:
            new_state += val
    
    return new_state

def transition(current_state, new_state):
    transition_state = transitionState(current_state)
    setState(transitionState, YELLOW_LIGHT_DURATION)
    setState(new_state)
    return new_state
    
def main():
    sumoCmd = ['sumo-gui', '-c', 'tJunction.sumocfg']
    traci.start(sumoCmd)
    state = 'rrrrrrrrrrrr'

    while traci.simulation.getMinExpectedNumber() > 0:
        # Checking queue lengths on incoming edges
        queue0 = getQueueLength('L2')
        queue1 = getQueueLength('L4')
        queue2 = getQueueLength('L6')
        queue3 = getQueueLength('L0')

        # Determine which edge has the highest demand
        maxQueue = max(queue0, queue1, queue2, queue3)
        if maxQueue == queue0:
            state = transition(state, 'GGgrrrrrrrrr')
        elif maxQueue == queue1:
            state = transition(state, 'rrrGGgrrrrrr')
        elif maxQueue == queue2:
            state = transition(state, 'rrrrrrGGgrrr')
        elif maxQueue == queue3:
            state = transition(state, 'rrrrrrrrrGGg')


        traci.simulationStep()

    traci.close()

if __name__ == "__main__":
    main()