import random

num_sensors = 10  # number of sensors
num_laps = 4     # number of laps
track_length = 1000  # length of the track

# Generate sensor positions as integer x and y coordinates
sensors = []
for i in range(num_sensors):
    x = random.randint(0, track_length)
    y = random.randint(0, track_length)
    sensors.append((x, y, []))

time = 0

for j in range(num_laps):
    for i in range(num_sensors):
        time += random.uniform(3, 9)
        sensors[i][2].append(time)

for i in range(num_sensors):
    print(sensors[i][0], end=', ')
    print(sensors[i][1], end=', ')
    for lap_time in sensors[i][2]:
        print(lap_time, end = ', ')
    print("")


