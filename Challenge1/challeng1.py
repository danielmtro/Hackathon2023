from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from pprint import pprint


filename = 'splits.txt'
try:
    f = open(filename, 'r')
except:
    raise FileNotFoundError(f"The data file {filename} doesn't currently exist")

input_lines = [line.strip() for line in f.readlines()]
#print(input_lines)

f.close()

if len(input_lines) < 1:
    raise ValueError("Data file doesn't have enough data!")

try:
    summary_data = input_lines[0].split(',')
    numlaps = int(summary_data[0])
    numsensors = int(summary_data[1])
except:
    raise ValueError("Data is of the wrong type")

sensor_data = []

for line in input_lines[1:]:
    try:
        lst = line.split(',')
        coords = [int(x) for x in lst[0:2]]
        times = [float(x) for x in lst[2:] if len(x) != 0 ]
        combined = coords + times
        sensor_data.append(tuple([x for x in combined]))
    except:
        raise ValueError("Input data is of the wrong type")
    
#error checking - are the times negative or in wrong order
if len(sensor_data) != numsensors:
    raise ValueError(f"Incorrect number of values. Should be {numlaps} laps and {numsensors} sensors")

for line in range(len(sensor_data)):
    if len(sensor_data[line]) != numlaps + 2:
        raise ValueError(f"Incorrect number of values. Should be {numlaps} laps and {numsensors} sensors")
    for num in range(2, len(sensor_data[line])):
        if sensor_data[line][num] < 0:
            raise ValueError ("Times should not be negative")
        
        if num == 2:
            continue

        if sensor_data[line][num] < sensor_data[line][num - 1]:
            raise ValueError("Times should be increasing")
        try:
            if sensor_data[line][num] < sensor_data[line - 1][num]:
                raise ValueError("Times should be increasing")
        except:
            continue


times = [[]]
ind = 0
for lap in range(2, numlaps + 2):
    for sensor in range(1, len(sensor_data)):
        times[ind].append(sensor_data[sensor][lap] - sensor_data[sensor - 1][lap])
    
    if lap != numlaps + 1:
        times.append([])
    ind += 1

timearray = np.asarray(times)

#an array containing the fastest times for each split
fastest_splits = np.amin(timearray, axis = 0)

#an array containing the total time for each lap
laptimes = np.sum(timearray, axis = 1)
fastest_lap_time = min(laptimes)

#the index of the fastest lap
for i in range(numlaps):
    if laptimes[i] == fastest_lap_time:
        fastest_lap = i


#plotting
nparray = np.asarray(sensor_data)
xlocs, ylocs = nparray[:, 0], nparray[:, 1]
plt.scatter(xlocs, ylocs, color = 'red')
plt.plot(xlocs, ylocs, color = 'green')
plt.xlabel("X Distance (m)")
plt.ylabel("Y Distance (m)")
plt.title("Map of Sensor Locations")
#plt.show()
plt.savefig('map.png')
plt.clf


fig, ax = plt.subplots()
ax.set_xlim(min(xlocs), max(xlocs))
ax.set_ylim(min(ylocs), max(ylocs))
line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = xlocs[:i+1]
    y = ylocs[:i+1] 
    line.set_data(x, y)
    return line,

def animateplot(speed):
    anim = FuncAnimation(fig, animate, init_func=init,frames=len(xlocs), interval=500)
    
    pass

