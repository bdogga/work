import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv



#Import the Coordinates for LE and TE
LE_TE = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_streamlines/unique_LE_TE_coordinates.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["xLE","rLE","xTE","rTE"])
#Be careful wilth the order of coordinates. These start at hub and go down to casing. (Imagine measuring while standing on the ground)
LE_TE.dropna(axis=0,how='any',thresh=None)
LE_TE = LE_TE.round(3)
LE_TE.astype(float)
#print(LE_TE.tail())

LE = LE_TE.iloc[:,0:2]#.rename(columns={"xLE": "X", "rLE": "Y"})
LE = LE.sort_values(by=['rLE'], ascending=True)
LE = LE.drop_duplicates()
LE_x_coord = LE.iloc[:,0].round(3).tolist()
LE_y_coord = LE.iloc[:,1].round(3).tolist()
LE_z_coord = [0.0] * len(LE['xLE'])
LE_x_coord_np = np.around(LE.iloc[:,0].tolist(),3)
LE_y_coord_np = np.around(LE.iloc[:,1].tolist(),3)
LE_df = (pd.DataFrame(list(zip(LE_x_coord, LE_y_coord, LE_z_coord)), columns =['xLE', 'rLE', 'thetaLE'], dtype=float).sort_values(by=['rLE'], ascending=False).reset_index(drop=True))
print(LE_df.tail())
#print(LE_x_coord)
#LE_df.to_csv('sorted_LE_df.dat', sep='\t', index=False)

TE = LE_TE.iloc[:,2:4]#.rename(columns={"xTE": "X", "rTE": "Y"})
TE = TE.sort_values(by=['rTE'], ascending=True)
TE = TE.drop_duplicates()
TE_x_coord = TE.iloc[:,0].round(3).tolist()
TE_y_coord = TE.iloc[:,1].round(3).tolist()
TE_z_coord = [0.0] * len(TE['xTE'])
TE_x_coord_np = np.around(TE.iloc[:,0].tolist(),3)
TE_y_coord_np = np.around(TE.iloc[:,1].tolist(),3)
TE_df = (pd.DataFrame(list(zip(TE_x_coord, TE_y_coord, TE_z_coord)), columns =['xTE', 'rTE', 'thetaTE'], dtype=float).sort_values(by=['rTE'], ascending=False).reset_index(drop=True))
print(TE_df.tail())
#print(TE_x_coord)
#TE_df.to_csv('sorted_TE_df.dat', sep='\t', index=False)

LE_TE1 = pd.concat([LE_df['xLE'], LE_df['rLE'], TE_df['xTE'], TE_df['rTE']], axis=1)
LE_TE_2 = LE_TE1.sort_values(by=['rTE'], ascending=True)
LE_TE_2 = LE_TE_2.reset_index(drop=True)
print(LE_TE_2.tail())

plt.plot(LE_df['xLE'], LE_df['rLE'], 'ro', label='LE points')
plt.plot(TE_df['xTE'], TE_df['rTE'], 'g^',label='TE points')
plt.plot(LE_df['xLE'], LE_df['rLE'], label="LE")
plt.plot(TE_df['xTE'], TE_df['rTE'], label="TE")
#plt.legend(loc='lower left', ncol=2)

# Labels for the points
for a,b in zip(LE_df['xLE']+0.5, LE_df['rLE']):
   plt.text(a, b, str(b))
for a,b in zip(TE_df['xTE']-1.5, TE_df['rTE']):
   plt.text(a, b, str(b))
plt.show()



#Write to file
#interp_LE_df.to_csv('interp_LE_df.dat', sep='\t', index=False)
#interp_TE_df.to_csv('interp_TE_df.dat', sep='\t', index=False)
#LE_TE1.to_csv('unique_LE_TE_coordinates.dat', sep='\t', index=False)
LE_TE_2.to_csv('unique_LE_TE_coordinates_Tblade3_format.dat', sep='\t', index=False)

