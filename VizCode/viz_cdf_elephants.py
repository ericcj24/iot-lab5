import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import math

# Load JSON data from a file
with open('path.json') as f:
    data = json.load(f)

x = []
y = []
z = []
c = []

# Extract timestamp, coordinates, and assign colors for elephants
for animal in data.keys():
    for ts in data[animal]['timestamp']:
        z.append(float(ts))
        if 'Elephant:4d1e37' in animal:
            c.append('blue')
        elif 'Elephant:882e9e' in animal:
            c.append('orange')
        elif 'Elephant:4bf779' in animal:
            c.append('green')
        else:
            c.append('gray')  # unknown

    # Assuming each animal also has GPS coordinates
    if 'gps coordinates' in data[animal]:
        for coord in data[animal]['gps coordinates']:
            x.append(float(coord[0]))
            y.append(float(coord[1]))

# Create DataFrame
df = pd.DataFrame({
    'xcoord': x,
    'ycoord': y,
    'time': z,
    'color': c
})

df.sort_values('time', inplace=True)

# Separate elephant data by color
blue_elephant = df[df['color'] == 'blue']
orange_elephant = df[df['color'] == 'orange']
green_elephant = df[df['color'] == 'green']

elephants = [
    ('blue_Elephant', blue_elephant, 'blue'),
    ('orange_Elephant', orange_elephant, 'orange'),
    ('green_Elephant', green_elephant, 'green')
]

datasets = []

# Calculate speed
for elephant in elephants:
    label, data, color = elephant
    dataset = []
    for i in range(len(data) - 1):
        row1 = data.iloc[i]
        row2 = data.iloc[i + 1]

        time_diff = row2['time'] - row1['time']
        distance = math.sqrt((row2['xcoord'] - row1['xcoord'])**2 + (row2['ycoord'] - row1['ycoord'])**2)
        speed = round(distance / time_diff, 2) if time_diff > 0 else 0

        dataset.append(speed)
    datasets.append([label, dataset, color])

# Compute and plot CDF
def compute_cdf(data, num_points=200):
    sorted_data = np.sort(data)
    unique_data, unique_indices = np.unique(sorted_data, return_index=True)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)  # Properly generate the CDF values
    # Interpolate for a smoother curve
    interp_func = interp1d(sorted_data, cdf, kind='linear', fill_value="extrapolate", bounds_error=False)
    smooth_x = np.linspace(sorted_data.min(), sorted_data.max(), num_points)
    smooth_y = interp_func(smooth_x)
    return smooth_x, smooth_y

plt.figure(figsize=(10, 6))

for label, data, color in datasets:
    if len(data) > 0:
        smooth_x, smooth_y = compute_cdf(data)
        plt.plot(smooth_x, smooth_y, label=label, color=color)

plt.xlabel("Speed (m/s)")
plt.ylabel("Probability")
plt.title("CDF of Movement Speed of Elephants")
plt.legend()
plt.grid()

# Show the plot
plt.show()
