# processdata.py

import sys
import pandas
from helpers import loadParams
import os

if len(sys.argv) > 2:
    filepath = sys.argv[1]
    index = int(sys.argv[2])
else:
    print("Usage: testrun.py filepath, index")
    sys.exit(1)


params = loadParams(filepath, index)

params_df = pandas.DataFrame([params])

df = pandas.read_xml("tripinfo.xml")
df.to_csv(f'run{params["run_id"]}_tripinfo', index=False)

throughput_overall = len(df)/(max(df['arrival'])/60)

average_waiting_time = df['waitingTime'].mean()

# Append results to the results.csv file
results_df = pandas.DataFrame([[params["run_id"], throughput_overall, average_waiting_time]],
                                columns=['run_id', 'throughput', 'average_waiting_time'])
                              
results_df = pandas.merge(params_df, results_df, on='run_id')
    
# Check if results.csv exists and is not empty, then append without header; otherwise, write with header
if os.path.exists('results.csv') and os.path.getsize('results.csv') > 0:
    results_df.to_csv('results.csv', mode='a', header=False, index=False)
else:
    results_df.to_csv('results.csv', mode='w', header=True, index=False)