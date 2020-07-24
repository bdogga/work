import sys
import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

####################################################
##FUNCTIONS
####################################################
# This bought up as is from Kiran's 3dplotter. It helps fix a bug where 
def set_aspect_equal_3d(ax):
    """Fix equal aspect bug for 3D plots."""
    # http://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
	
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()

    from numpy import mean
    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([abs(lim - mean_)
                       for lims, mean_ in ((xlim, xmean),
                                           (ylim, ymean),
                                           (zlim, zmean))
                       for lim in lims])

    ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])	
	
#######################################################	

#Read in text files of airfoils
E3_fan = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/stagger_generation/3d_view_blade/python3_3d_plotter/blade3d.GE_E3_Fan_rotor_w_og_coordinates.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y","Z"])
E3_fan.dropna(axis=0,how='any',thresh=None)
E3_fan.astype(float)
print(E3_fan.head())

fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.plot_trisurf(E3_fan['X'], E3_fan['Y'], E3_fan['Z'])
#ax.plot_trisurf(E3_fan['X'], E3_fan['Y'], E3_fan['Z'])
surf = ax.plot(E3_fan['X'], E3_fan['Y'], E3_fan['Z'])
#set_aspect_equal_3d(ax)
plt.show()
