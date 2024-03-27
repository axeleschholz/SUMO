# testrun.py

from helpers import loadParams
import sys
import json

if len(sys.argv) > 2:
    filepath = sys.argv[1]
    index = int(sys.argv[2])
else:
    print("Usage: testrun.py filepath, index")
    sys.exit(1)

parameters = loadParams(filepath, index)
print(parameters)
