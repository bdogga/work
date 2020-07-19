import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv



#Import the Coordinates for LE and TE
streamllines = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_streamlines/streamlines_tblade_example_case.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["x_s","r_s"])
#Be careful wilth the order of coordinates. These start at hub and go down to casing. (Imagine measuring while standing on the ground)
streamllines.dropna(axis=0,how='any',thresh=None)
streamllines.astype(float)
print(streamllines.tail())


plt.plot(streamllines['x_s'], streamllines['r_s'], 'g^', label='Streamline points')
for a,b in zip(streamllines['x_s'], streamllines['r_s']):
   plt.text(a, b, str(b))
#plt.plot(streamllines['x_s'], streamllines['r_s'], label="Streamlines")
#plt.legend(loc='lower left', ncol=2)
plt.show()

#Write to file
#streamllines.to_csv('streamllines.dat', sep='\t', index=False)


