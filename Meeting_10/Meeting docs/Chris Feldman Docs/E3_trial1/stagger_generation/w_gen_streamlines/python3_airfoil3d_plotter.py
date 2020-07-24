import sys
import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

#Read in text files of airfoils
E3_fan = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/stagger_generation/without_spancontrol_inputs/blade3d.GE_E3_Fan_rotor.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y","Z"])
E3_fan.dropna(axis=0,how='any',thresh=None)
E3_fan.astype(float)
print(E3_fan.head())

fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.plot_trisurf(E3_fan['X'], E3_fan['Y'], E3_fan['Z'])
#ax.plot_trisurf(E3_fan['X'], E3_fan['Y'], E3_fan['Z'])
surf = ax.plot(E3_fan['X'], E3_fan['Y'], E3_fan['Z'])
plt.show()
