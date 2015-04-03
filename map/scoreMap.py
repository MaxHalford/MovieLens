from __future__ import print_function
import zipfile
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import pandas as pd

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
# Calculate average score per state
df = pd.read_csv('mapData')
scores = df.groupby('state')['score'].mean()
scores = scores.to_dict()
# Open shapefile
shp_info = m.readshapefile('st99_d00', 'states', drawbounds=True)
# Set a color for each state according to score
colors = {}
statenames = []
# Choose color range
cmap = plt.cm.YlGn
# Define extreme values
vmin = min(scores.values())
vmax = max(scores.values())
# Define the list colormap array
for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia','Puerto Rico']:
        score = scores[statename]
        colors[statename] = cmap((score - vmin) / (vmax - vmin))
    statenames.append(statename)
# Loop through each state and color it
ax = plt.gca()
for nshape, seg in enumerate(m.states):
    # skip DC and Puerto Rico.
    if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)

colorBar = np.zeros((1, 10))
ticks = np.linspace(vmin, vmax, 10)
for i, tick in enumerate(ticks):
    colorBar[0, i] = tick
plt.imshow(colorBar, cmap=plt.get_cmap('YlGn'), aspect=1)
plt.colorbar()

plt.title('Note moyenne par état')
plt.show()
