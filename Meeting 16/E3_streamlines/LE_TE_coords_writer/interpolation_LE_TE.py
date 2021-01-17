import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv
import itertools
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d



#Import the Coordinates for LE and TE
LE_TE = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/populate-Tbalde3-example-file/LE_TE_coordinates.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["xLE","rLE","xTE","rTE"])
#Be careful wilth the order of coordinates. These start at hub and go down to casing. (Imagine measuring while standing on the ground)
LE_TE.dropna(axis=0,how='any',thresh=None)
LE_TE.astype(float)
#print(LE_TE.tail())

LE = LE_TE.iloc[:,0:2].rename(columns={"xLE": "X", "rLE": "Y"})
LE = LE.sort_values(by=['Y'], ascending=True)
LE = LE.drop_duplicates()
LE_x_coord = LE.iloc[:,0].round(3).tolist()
LE_y_coord = LE.iloc[:,1].round(3).tolist()
LE_z_coord = [0.0] * len(LE['X'])
LE_x_coord_np = np.around(LE.iloc[:,0].tolist(),3)
LE_y_coord_np = np.around(LE.iloc[:,1].tolist(),3)
LE_df = (pd.DataFrame(list(zip(LE_x_coord, LE_y_coord, LE_z_coord)), columns =['X', 'Y', 'Z'], dtype=float).sort_values(by=['Y'], ascending=False).reset_index(drop=True))
#print(LE_df.tail())
#print(LE_x_coord)

TE = LE_TE.iloc[:,2:4].rename(columns={"xTE": "X", "rTE": "Y"})
TE = TE.sort_values(by=['Y'], ascending=True)
TE = TE.drop_duplicates()
TE_x_coord = TE.iloc[:,0].round(3).tolist()
TE_y_coord = TE.iloc[:,1].round(3).tolist()
TE_z_coord = [0.0] * len(TE['X'])
TE_x_coord_np = np.around(TE.iloc[:,0].tolist(),3)
TE_y_coord_np = np.around(TE.iloc[:,1].tolist(),3)
TE_df = (pd.DataFrame(list(zip(TE_x_coord, TE_y_coord, TE_z_coord)), columns =['X', 'Y', 'Z'], dtype=float).sort_values(by=['Y'], ascending=False).reset_index(drop=True))
#print(TE_df.tail())
#print(TE_x_coord)



#print(TE_y_coord_np)

#The x coordinate of the input curve should always be in increasing order. Scipy.interpolate does not accept dupplicate entries in the input. Also, The input has to be numpy array and not pandas series.

def cubic_linear_interp(x_coord, y_coord):
   # The input is switched here because we need to iterate with rest pect to ordinate. 
   x = y_coord
   y = x_coord
   cs = CubicSpline(x, y)
   d_int = interp1d(x, y)
   xs = np.linspace(y_coord.min(), y_coord.max(), 21).round(3)
   #print(xs)
   d_inter_TE_y_coord = d_int(xs).round(3)
   cs_TE_y_coord = cs(xs).round(3)
   #print(d_inter_TE_y_coord)
   #print(cs_TE_y_coord)
   plt.plot(y, x, 'ro', label='data')
   plt.plot(cs_TE_y_coord, xs, 'g^',label='CS')
   plt.plot(d_inter_TE_y_coord, xs, 'bs',label="1d_inter")
   plt.plot(d_inter_TE_y_coord, xs, label="1d_inter")
   plt.plot(y, x, label='true')
   plt.plot(cs_TE_y_coord, xs, label="CS")
   # Uncomment to return cubic spline interpolated coordinates
   #return (pd.DataFrame(list(zip(cs_TE_y_coord, xs, [0.0]*21)), columns =['X', 'Y', 'Z'], dtype=float).sort_values(by=['Y'], ascending=False).reset_index(drop=True))
   # Uncomment to return linear interpolated coordinates
   return (pd.DataFrame(list(zip(d_inter_TE_y_coord, xs, [0.0]*21)), columns =['X', 'Y', 'Z'], dtype=float).sort_values(by=['Y'], ascending=False).reset_index(drop=True))
   

interp_LE_df = cubic_linear_interp(LE_x_coord_np, LE_y_coord_np)
print(interp_LE_df)
interp_TE_df = cubic_linear_interp(TE_x_coord_np, TE_y_coord_np)
print(interp_TE_df)



#Write to file
#interp_LE_df.to_csv('interp_LE_df.dat', sep='\t', index=False)
#interp_TE_df.to_csv('interp_TE_df.dat', sep='\t', index=False)


# We went with linear interpolation because cubic was overshooting and undershooting near the hub. Linear was more closer to the actual data.

#Plot the files
#fig, ax = plt.subplots(figsize=(6.5, 4))
#ax.plot(LE_x_coord, LE_y_coord, 'o', label='data')
#ax.plot(LE_x_coord, LE_y_coord, label='true')
#ax.plot(xs_LE, cs_LE(xs), label="S")


#plt.plot(LE_df['X'],LE_df['Y'], label='LE', color='red')
#plt.plot(TE_df['X'],TE_df['Y'], label='TE', color='blue')
#plt.legend()
#plt.show()
