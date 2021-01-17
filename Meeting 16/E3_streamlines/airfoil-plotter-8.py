import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv


#Read in text files of airfoils
foil1 = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/airfoil_plotter/fan-curve_layer05_edited-te_2D.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y"])
foil1.dropna(axis=0,how='any',thresh=None)
foil1.astype(float)

Xmax = foil1['X'].max()
Xmin = foil1['X'].min()
Ymax = foil1['Y'].max()
Ymin = foil1['Y'].min()
Xdiff = Xmax-Xmin
Ydiff = Ymax-Ymin

#The author is a bit skeptical about this normalization method. Kept it for the time being.
foil1['X'] = foil1['X']-Xmin
foil1['X'] = foil1['X']-Xdiff
foil1['X'] = foil1['X']/Xdiff
foil1['Y'] = foil1['Y']-Ymin
foil1['Y'] = foil1['Y']/Ydiff


angle = -135
stggr_ang = np.deg2rad(angle)


def rotate(x, y, rad):
       xx = round(math.cos(rad)*x - math.sin(rad)*y,6)
       yy = round(math.sin(rad)*x + math.cos(rad)*y,6)
       return xx, yy

# Code Source: "https://stackoverflow.com/questions/35905550/python-rotating-a-point-counterclockwise-by-an-angle"
# Math Source: "https://en.wikipedia.org/wiki/Rotation_(mathematics)"
# Code troubleshoot help: "Kiran Dogiparthi (dogipakr@mail.uc.edu), UC MEngg CS Fall 2019 admit" 

x_new=[]
y_new=[]
for i in range(len(foil1)):
    xx,yy = rotate(foil1.iloc[i,0], foil1.iloc[i,1], stggr_ang)
    x_new.append(xx)
    y_new.append(yy)
    
dataset = pd.DataFrame(list(zip(x_new, y_new)), 
               columns =['X', 'Y']) 

foil1_chord_length = math.sqrt( (((foil1['X'].min())-(foil1['X'].max()))**2)+(((foil1['Y'].min())-(foil1['Y'].max()))**2) )
dataset_chord_length = math.sqrt( (((dataset['X'].min())-(dataset['X'].max()))**2)+(((dataset['Y'].min())-(dataset['Y'].max()))**2) )
print(foil1_chord_length)
print(dataset_chord_length)
dataset_norm = dataset.copy()
dataset_norm['X'] = dataset_norm['X']/dataset_chord_length
dataset_norm['Y'] = dataset_norm['Y']/dataset_chord_length
print(dataset_norm['X'].max())


#plot: "matplotlib is very notorious for making plots that make no sense. It has his limiations due to topology issues. Alwasys make sure that the plot is a square and that the axes limits match when comparing plots."
#fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30,30))
fig = plt.figure(figsize=(15,15))
fig.suptitle('Horizontally stacked subplots', size=32)
ax1 = plt.subplot(122)
ax2 = plt.subplot(223)
ax3 = plt.subplot(221)

ax1.plot(foil1['X'],foil1['Y'], label='Original Coordinates', color='red')
ax1.set_ylim([-0.1, 1.1])
ax1.set_xlim([-1.1, 0.1])
ax1.grid(True)
ax1.set(adjustable='box', aspect='equal')
ax1.legend(fontsize=14)

ax2.plot(dataset['X'],dataset['Y'], label=f'rotated dataset, angle={angle}$^\circ$', color='orange')
ax2.set_ylim([-0.1, 0.5])
ax2.set_xlim([-0.1, 1.6])
ax2.grid(True)
ax2.set(adjustable='box', aspect='equal')
ax2.legend(fontsize=14)

ax3.plot(dataset_norm['X'],dataset_norm['Y'], label=f'Normalized dataset, rotated {angle}$^\circ$', color='green')
ax3.set_ylim([-0.1, 0.4])
ax3.set_xlim([-0.1, 1.2])
ax3.grid(True)
ax3.set(adjustable='box', aspect='equal')
ax3.legend(fontsize=14)

plt.show()

#Write Coordinates to File
dataset_norm.to_csv('normalized_airfoil.dat', sep='\t', index=False)
