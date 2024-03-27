#!/bin/bash

PARAMS_FILE="simulation_params.csv"
# Calculate the number of lines in the CSV, subtracting the header
NUM_LINES=$(wc -l < "$PARAMS_FILE")
NUM_LINES=$(($NUM_LINES - 1)) # subtract the header line
echo $NUM_LINES
# Loop through each line of the CSV file by index
for (( INDEX=0; INDEX<NUM_LINES; INDEX++ ))
do
    python testrun.py $PARAMS_FILE $INDEX
    #python generateTrips.py $PARAMS_FILE $INDEX
    #duarouter --net-file tJunction.net.xml --trip-files tJunction.trips.xml --output-file tJunction.rou.xml
    #python dynamicController.py $PARAMS_FILE $INDEX
    #python store_results.py $PARAMS_FILE $INDEX
done

$SHELL

