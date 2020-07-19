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



plt.plot(foil1['X'],foil1['Y'])
plt.ylim(-0.5, 0.5)
plt.show()
