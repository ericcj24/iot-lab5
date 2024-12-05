import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import make_interp_spline
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

def compute_cdf(data, num_points=200):
    # Sort data
    sorted_data = np.sort(data)
    # CDF values
    sorted_data = np.sort(data)
    unique_data, unique_indices = np.unique(sorted_data, return_index=True)
    cdf = np.linspace(0, 1, len(sorted_data))[unique_indices]  # Handle duplicates
    # Interpolate for a smoother curve
    spline = make_interp_spline(unique_data, cdf, k=3)  # Cubic spline
    smooth_x = np.linspace(sorted_data.min(), sorted_data.max(), num_points)
    smooth_y = spline(smooth_x)
    return smooth_x, smooth_y

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



green_zebra = df[df['color']=='green']
yellow_zebra = df[df['color']=='yellow']
orange_zebra = df[df['color']=='orange']
red_zebra = df[df['color']=='red']
#df_first = df_first.head(5000)

zebras = [('green', green_zebra), ('yellow', yellow_zebra), ('orange', orange_zebra), ('red', red_zebra)]
datasets = []
# calculate speed
for zebra in zebras:
    data = zebra[1]
    color = zebra[0]
    dataset = []
    for i in range(0, len(data) - 1):
        row1 = data.iloc[i]
        row2 = data.iloc[i + 1]

        time_diff = row2['time'] - row1['time']
        distance = math.sqrt((row2['xcoord'] - row1['xcoord'])**2 + (row2['ycoord'] - row1['ycoord'])**2)
        speed = round(distance/time_diff, 2)

        dataset.append(speed)
    datasets.append([f'{color}_Zebra', dataset, color])

plt.figure(figsize=(10, 6))

for label, data, color in datasets:
    smooth_x, smooth_y = compute_cdf(data)
    plt.plot(smooth_x, smooth_y, label=label, color=color)

plt.xlabel("Speed (m/s)")
plt.ylabel("Probability")
plt.title("CDF of Movement Speed of Zebra Herd")
plt.legend()
plt.grid()

# Show the plot
plt.show()
