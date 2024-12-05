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
for animal in data.keys():
    for ts in data[animal]['timestamp']:
        z.append(float(ts))
        if 'Zebra:44dc78' in animal:
            c.append('green')
        elif 'Zebra:23d306' in animal:
            c.append('yellow')
        elif 'Zebra:da2a6c' in animal:
            c.append('orange')
        elif 'Zebra:123956' in animal:
            c.append('red')
        else:
            c.append('black')
        #elif 'Elephant' in animal:
        #    c.append('yellow')
        #elif 'Lion' in animal:
        #    c.append('red')
        #else:
            #unknown
        #    c.append('gray')
        
    for coord in data[animal]['gps coordinates']:
        x.append(float(coord[0]))
        y.append(float(coord[1]))



df = pd.DataFrame({
    'xcoord': x,
    'ycoord': y,
    'time': z,
    'color': c
})

df.sort_values('time')



df_first = df[df['color']!='black']
#df_first = df_first.head(5000)

# Create a simple line plot
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(df_first['xcoord'], df_first['ycoord'], df_first['time'], c = df_first['color'])
ax.set_xlabel('X coord')
ax.set_ylabel('Y coord')
ax.set_zlabel('Time')

plt.title("zebra herd movement")

plt.show()