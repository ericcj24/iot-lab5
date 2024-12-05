import json
import numpy as np
import matplotlib.pyplot as plt
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

# Extract timestamp, coordinates, and assign colors for lions
for animal in data.keys():
    for ts in data[animal]['timestamp']:
        z.append(float(ts))
        if 'Lion:5a8049' in animal:
            c.append('blue')
        elif 'Lion:7c0573' in animal:
            c.append('orange')
        elif 'Lion:860e77' in animal:
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

# Separate lion data by color
blue_lion = df[df['color'] == 'blue']
orange_lion = df[df['color'] == 'orange']
green_lion = df[df['color'] == 'green']

lions = [
    ('blue_Lion', blue_lion, 'blue'),
    ('orange_Lion', orange_lion, 'orange'),
    ('green_Lion', green_lion, 'green')
]

datasets = []

# Calculate speed
for lion in lions:
    label, data, color = lion
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
    cdf = np.linspace(0, 1, len(sorted_data))[unique_indices]
    spline = make_interp_spline(unique_data, cdf, k=3)
    smooth_x = np.linspace(sorted_data.min(), sorted_data.max(), num_points)
    smooth_y = spline(smooth_x)
    return smooth_x, smooth_y

plt.figure(figsize=(10, 6))

for label, data, color in datasets:
    if len(data) > 0:
        smooth_x, smooth_y = compute_cdf(data)
        plt.plot(smooth_x, smooth_y, label=label, color=color)

plt.xlabel("Speed (m/s)")
plt.ylabel("Probability")
plt.title("CDF of Movement Speed of Lions")
plt.legend()
plt.grid()

# Show the plot
plt.show()
