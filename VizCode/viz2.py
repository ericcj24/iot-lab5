import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Load JSON data from a file
with open('../Data/path.json') as f:
    data = json.load(f)

x = []
y = []
z = []
c = []

print(data.keys())

# Extract x and y values from the JSON data
for zebra in data.keys():
    for ts in data[zebra]['timestamp']:
        z.append(float(ts))
        if 'Zebra' in zebra:
            c.append('green')
        elif 'Elephant' in zebra:
            c.append('yellow')
        elif 'Lion' in zebra:
            c.append('red')
        else:
            #unknown
            c.append('gray')
        
    for coord in data[zebra]['gps coordinates']:
        x.append(float(coord[0]))
        y.append(float(coord[1]))

#    print(len(data[zebra]['timestamp']))
#    print(len(data[zebra]['gps coordinates']))

df = pd.DataFrame({
    'xcoord': x,
    'ycoord': y,
    'time': z,
    'color': c
})

df.sort_values('time')



df_first = df.head(len(df))

# Create a simple line plot
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(df_first['xcoord'], df_first['ycoord'], df_first['time'], c = df_first['color'])
ax.set_xlabel('X coord')
ax.set_ylabel('Y coord')
ax.set_zlabel('Time')

plt.show()