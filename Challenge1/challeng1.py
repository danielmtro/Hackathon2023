from matplotlib import pyplot as plt


filename = 'splits.txt'
try:
    f = open(filename, 'r')
except:
    raise FileNotFoundError(f"The data file {filename} doesn't currently exist")

input_lines = f.readlines()
f.close()

if len(input_lines < 1):
    raise ValueError("Data file doesn't have enough data!")

sensor_data = []

try:
    summary_data = input_lines[0].split(',')
    numlaps = int(summary_data[0])
    numsensors = int(summary_data[1])
except:
    raise ValueError("Data is of the wrong type")

#automatic running + check for 
for line in input_lines[1:]:
    try:
        lst = line.split(',')
        coords = [int(x) for x in lst[0:2]]
        times = [float(x) for x in lst[2:]]
        combined = coords + times
        sensor_data.append((x for x in combined))
    except:
        raise ValueError("Input data is of the wrong type")
    
#error checking - are the times negative or in wrong order
if len(sensor_data) != numlaps:
    raise ValueError(f"Incorrect number of values. Should be {numlaps} laps and {numsensors} sensors")
for line in sensor_data:
    if len(line) != numlaps + 2:
        raise ValueError(f"Incorrect number of values. Should be {numlaps} laps and {numsensors} sensors")
    for num in range(2, len(line)):
        if line[num] < 0:
            raise ValueError ("Times should not be negative")
        
        if num == 2:
            continue

        if line[num] < line[num - 1]:
            raise ValueError("Times should be increasing")
