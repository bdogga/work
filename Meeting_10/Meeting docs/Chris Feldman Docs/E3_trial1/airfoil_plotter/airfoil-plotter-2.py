import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
#from scipy.optimize import curve_fit
#from scipy.optimize import minimize
#from scipy.interpolate import interp1d
from numpy import savetxt
import csv


#Read in text files of airfoils
foil1 = pd.read_csv('/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/airfoil_plotter/seligdatfile0012.dat',na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y"])
#foil1.dropna(axis=0,how='any',thresh=None)
foil1.astype(float)

# Ensure that target blade's coordinates fit into a 0<u<1 and -1<v<1 range

Xmax = foil1['X'].max()
Xmin = foil1['X'].min()
Ymax = foil1['Y'].max()
Ymin = foil1['Y'].min()
Xdiff = Xmax-Xmin
Ydiff = Ymax-Ymin

#foil1['X'] = foil1['X']-Xmin
#foil1['X'] = foil1['X']-Xdiff
#foil1['X'] = foil1['X']/Xdiff
#foil1['Y'] = foil1['Y']-Ymin


stggr_ang = 10

foil2 = foil1.copy()
print(foil2.shape)


def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return ((R @ (p.T-o.T) + o.T).T)

origin=(Xmax,Ymin)
new_points = rotate(foil1, origin=origin, degrees=stggr_ang)
dataset = pd.DataFrame({'X': new_points[:, 0], 'Y': new_points[:, 1]})
print(dataset)
print(dataset.shape)

plt.plot(dataset['X'],dataset['Y'])
plt.plot(foil1['X'],foil1['Y'])
#plt.ylim(-1.8, 1.8)
plt.show()
