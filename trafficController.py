import os
import sys
import traci
import traci.constants as tc


# Define the paths to your SUMO configuration files
net_file = "tJunction.net.xml"
sumo_cfg = "tJunction.sumocfg"

# Configure the command to start SUMO with TraCI
sumo_cmd = ["sumo-gui", "-c", sumo_cfg]

# Start the SUMO simulation
traci.start(sumo_cmd)

# Duration of green/yellow phases in seconds
green_phase_duration = 30
yellow_phase_duration = 5

# Initial phase (assuming 0 is the phase where the main road is green)
current_phase = 0

# Start the simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    # Get the current simulation time
    sim_time = traci.simulation.getTime()

    # Switch phases based on the simulation time and phase durations
    if current_phase == 0 and sim_time % (green_phase_duration + yellow_phase_duration) == 0:
    # Switch to yellow phase before changing the main direction
        traci.trafficlight.setPhase("J1", 1)  # Change "yourTrafficLightID" to your actual traffic light ID
        current_phase = 1
    elif current_phase == 1 and sim_time % (green_phase_duration + yellow_phase_duration) == yellow_phase_duration:
        # Switch to the next green phase
        traci.trafficlight.setPhase("J1", 2)  # Adjust phase index as needed
        current_phase = 2
    elif current_phase == 2 and sim_time % (green_phase_duration + yellow_phase_duration) == 0:
            # Switch to yellow phase before changing back to the main direction
            traci.trafficlight.setPhase("J1", 3)  # Adjust phase index as needed
            current_phase = 3
    elif current_phase == 3 and sim_time % (green_phase_duration + yellow_phase_duration) == yellow_phase_duration:
    # Switch back to the initial green phase
        traci.trafficlight.setPhase("J1", 0)
        current_phase = 0

    # Advance the simulation to the next time step
    traci.simulationStep()

# Close the TraCI connection
traci.close()
