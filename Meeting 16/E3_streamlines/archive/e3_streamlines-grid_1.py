import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv
from scipy.interpolate import interp1d

#Import the Coordinates for Hub
hub = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_streamlines/hub_export.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y","Z"])
hub.dropna(axis=0,how='any',thresh=None)
hub.astype(float)
#print(hub.head())

Xmax_hub = hub['X'].max()
Xmin_hub = hub['X'].min()
Ymax_hub = hub['Y'].max()
Ymin_hub = hub['Y'].min()

hub['X'] = hub['X']-Xmin_hub
Xdiff_hub = Xmax_hub-Xmin_hub
Ydiff_hub = Ymax_hub-Ymin_hub
#print(Xdiff_hub)


#Import the Coordinates for LE and TE
LE_TE = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/populate-Tbalde3-example-file/LE_TE_coordinates.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["xLE","rLE","xTE","rTE"])
#Be careful wilth the order of coordinates. These start at hub and go down to casing. (Imagine measuring while standing on the ground)
LE_TE.dropna(axis=0,how='any',thresh=None)
LE_TE.astype(float)
#print(LE_TE.head())

# There's beeen a mismatch between the coordinates of LE, TE and Hub. So we will normlaize the hub coordinates and then use the distance been the LE and TE coordinates to estimate a scaling factor for the hub coordnates.
# Then translate the hub coordinates so that the lowest coordinate of TE coinsides with the 128th coordinate of the hub, this number is an estimate for now and could be easily altered when the right constraint is found.
#     We are translating the hub instead of the blade because the LE and TE coordinates are from the NASA-GE E3 document where as the hub is just an export from FINE/TURBO IGG, so the primary source if given more preference.
# The estimation is done using Figure 40: Full-Scale Fan Test Vehicle on Page 45 of ""NASA-GE E3 fan design.pdf"" file
dist_LE0_TE0 = np.sqrt( ((LE_TE.iloc[0,0]-LE_TE.iloc[0,2])**2)+((LE_TE.iloc[0,1]-LE_TE.iloc[0,3])**2) )
#print(dist_LE0_TE0)
norm_hub = hub.copy()
norm_hub = norm_hub/Xdiff_hub
#print(norm_hub.head())
scaled_hub = norm_hub.copy()
scaled_hub = scaled_hub*dist_LE0_TE0*5
translated_hub = scaled_hub.copy()
xhub_TE_diff = LE_TE.iloc[0,2] - translated_hub.iloc[127,0]
yhub_TE_diff = LE_TE.iloc[0,3] - translated_hub.iloc[127,1]
#print(xhub_TE_diff)
#print(yhub_TE_diff)
translated_hub['X'] = translated_hub['X'] + xhub_TE_diff
translated_hub['Y'] = translated_hub['Y'] + yhub_TE_diff


# Using LE, TE and the scaled Hub Coordinates, construct the casing.
#  We will construct the casing using three sections, one before the LE, second from LE to TE and finally

casing = translated_hub.copy()
#print(casing.head())
# Part 1 of casing
casing.iloc[:95,1] = LE_TE.iloc[20,1]+10e-2
casing1 = casing.iloc[0:95,:]
#print(casing1.tail())

# Part 2 of casing
def intermediates(p1, p2, nb_points=8):
    """"Return a list of nb_points equally spaced points
    between p1 and p2"""
    # If we have 8 intermediate points, we have 8+1=9 spaces
    # between p1 and p2
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

    return [[p1[0] + i * x_spacing, p1[1] +  i * y_spacing, 0.0] 
            for i in range(1, nb_points+1)]
case3_points = intermediates([casing.iloc[93,0]+10e-2, LE_TE.iloc[20,1]+10e-2], [casing.iloc[125,0]-10e-2, LE_TE.iloc[20,3]+1e-2], nb_points=29)
case3_df = pd.DataFrame(case3_points, columns=['X','Y', 'Z'])
caseing1_df = casing1.append(case3_df, ignore_index=True)

# Part 3 of casing
casing.iloc[124:,1] = LE_TE.iloc[20,3]+10e-2
caseing1_dg = caseing1_df.append(casing.iloc[124:,], ignore_index=True)

#final comparison of coordinates:
#print(translated_hub.tail())
#print(caseing1_dg.tail())





#Plot the files
plt.plot(translated_hub['X'],translated_hub['Y'], label='Translated Hub Coordinates', color='Violet')
plt.plot(LE_TE['xLE'],LE_TE['rLE'], label='LE', color='green')
plt.plot(LE_TE['xTE'],LE_TE['rTE'], label='TE', color='grey')
plt.plot(caseing1_dg['X'],caseing1_dg['Y'], label='Generated Casing', color='blue')
#plt.plot(case3_df['X'],case3_df['Y'], label='slant Casing', color='red')
plt.legend()
plt.show()

#Write to file
#caseing1_df.to_csv('caseing1_df.dat', sep='\t', index=False)

#Debugging
#plt.plot(foil_level05['X'],foil_level05['Y'], label='Blade Level 05', color='blue')
#plt.plot(r_div, casing['Y'], label='r_div', marker='o')
#plt.plot(hub['X'],hub['Y'], label='Hub Coordinates', color='red')
#plt.plot(scaled_hub['X'],scaled_hub['Y'], label='Scaled Hub Coordinates', color='red')
#plt.plot(norm_hub['X'],norm_hub['Y'], label='Norm Hub Coordinates', color='pink')
#print(intermediates([casing.iLoc[127,1]+10e-4, 2+10e-4], [10+10e-4, 6.5+10e-4], nb_points=34))
#print(casing.iloc[127,1]+10e-4)
#print(casing.iloc[91,1]+10e-4)
#plt.plot(casing['X'],casing['Y'], label='Generated Casing', color='blue')


