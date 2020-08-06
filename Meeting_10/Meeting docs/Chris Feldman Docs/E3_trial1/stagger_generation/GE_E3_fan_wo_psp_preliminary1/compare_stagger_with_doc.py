# Script to plot meanline slope u (nondimensional chord)
# Written by Sabrina Shrestha (University of Cincinnati)
# Modified by Mayank Sharma (GTSL, University of Cincinnati)
# Guidance from Dr. Mark turner



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from cycler import cycler
import os
import sys


# Read the stagger angle file and convert to degrees
stagger_file                    = 'stagger_angles.dat'
stag                            = np.loadtxt(stagger_file,dtype=float,unpack=True)
stagger                         = list(stag*(180/np.pi))
stagger                         = np.round(stagger, 3)

# Read the stagger angle file and convert to degrees
nasa_doc_stagger_file           = 'stagger_from_nasa_doc.dat'
nasa_doc_stag                   = list(np.loadtxt(nasa_doc_stagger_file,dtype=float,unpack=True))

x_axis = list(np.arange(18)+1)
print(stagger)
print(x_axis)
print(nasa_doc_stag)

diff_in_stagger = list(stagger-nasa_doc_stag)
diff_in_stagger = np.round(diff_in_stagger, 3)
print(diff_in_stagger)

plt.plot(x_axis, stagger, color='red', label='Tblade3_stagger')
plt.plot(x_axis, stagger, 'ro')
plt.plot(x_axis, nasa_doc_stag, color='green', label='NASA_doc_stagger')
#plt.plot(x_axis, diff_in_stagger, color='blue', label='diff_in_stagger')
plt.plot(x_axis, nasa_doc_stag, 'g^')

for x,y in zip(x_axis,nasa_doc_stag):
   y_label = diff_in_stagger[x-1]
   plt.annotate(y_label, # this is the text
   (x,y), # this is the point to label
   textcoords="offset points", # how to position the text
   xytext=(0,10), # distance from text to points (x,y)
   ha='center') # horizontal alignment can be left, right or center

plt.ylabel('Stagger angle in Degrees')
plt.xlabel('Streamline Number')
plt.xticks(np.arange(min(x_axis), max(x_axis)+1, 1.0))
plt.legend(loc='lower right')
plt.show()
