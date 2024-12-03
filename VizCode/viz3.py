import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import math

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
        if 'Zebra:63d0e8' in animal:
            c.append('green')
        elif 'Zebra:34a602' in animal:
            c.append('yellow')
        elif 'Zebra:87145b' in animal:
            c.append('orange')
        elif 'Zebra:52da41' in animal:
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



df_first = df[df['color']=='green']
#df_first = df_first.head(5000)

result = []
# calculate speed
for i in range(0, len(df_first) - 1):
    row1 = df_first.iloc[i]
    row2 = df_first.iloc[i + 1]

    time_diff = row2['time'] - row1['time']
    distance = math.sqrt((row2['xcoord'] - row1['xcoord'])**2 + (row2['ycoord'] - row1['ycoord'])**2)
    speed = round(distance/time_diff, 2)

    result.append(speed)



# Create a simple line plot
fig, ax = plt.subplots(figsize=(8, 4))
n, bins, patches = ax.hist(result, 500, histtype='step',
                           cumulative=True, label='Empirical')


plt.title("green zebra herd movement")

plt.show()