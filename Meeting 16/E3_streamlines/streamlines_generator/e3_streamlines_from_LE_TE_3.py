import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv
import itertools
from scipy.interpolate import CubicSpline



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
LE_TE = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_streamlines/unique_LE_TE_coordinates.dat",na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["xLE","rLE","xTE","rTE"])
#Be careful wilth the order of coordinates. These start at hub and go down to casing. (Imagine measuring while standing on the ground)
LE_TE.dropna(axis=0,how='any',thresh=None)
LE_TE.astype(float)
#print(LE_TE.tail())

LE = LE_TE.iloc[:,0:2].rename(columns={"xLE": "X", "rLE": "Y"})
LE_x_coord = LE.iloc[:,0].round(3).tolist()
LE_y_coord = LE.iloc[:,1].round(3).tolist()
LE_z_coord = [0.0] * len(LE['X'])
LE_df = pd.DataFrame(list(zip(LE_x_coord, LE_y_coord, LE_z_coord)), columns =['X', 'Y', 'Z'], dtype=float).sort_values(by=['Y'], ascending=False)
LE_df = LE_df.reset_index(drop=True)
#print(LE_df)
LE_df.to_csv('sorted_LE_df.dat', sep='\t', index=False)

TE = LE_TE.iloc[:,2:4].rename(columns={"xTE": "X", "rTE": "Y"})
TE_x_coord = TE.iloc[:,0].round(3).tolist()
TE_y_coord = TE.iloc[:,1].round(3).tolist()
TE_z_coord = [0.0] * len(TE['X'])
TE_df = pd.DataFrame(list(zip(TE_x_coord, TE_y_coord, TE_z_coord)), columns =['X', 'Y', 'Z'], dtype=float).sort_values(by=['Y'], ascending=False)
TE_df = TE_df.reset_index(drop=True)
#print(TE_df.tail())
TE_df.to_csv('sorted_TE_df.dat', sep='\t', index=False)


# There's beeen a mismatch between the coordinates of LE, TE and Hub. So we will normlaize the hub coordinates and then use the distance been the LE and TE coordinates to estimate a scaling factor for the hub coordnates.
# Then translate the hub coordinates so that the lowest coordinate of TE coinsides with the 128th coordinate of the hub, this number is an estimate for now and could be easily altered when the right constraint is found.
#     We are translating the hub instead of the blade because the LE and TE coordinates are from the NASA-GE E3 document where as the hub is just an export from FINE/TURBO IGG, so the primary source is given more preference.
# The estimation is done using Figure 40: Full-Scale Fan Test Vehicle on Page 45 of ""NASA-GE E3 fan design.pdf"" file
dist_LE0_TE0 = np.sqrt( ((LE_TE.iloc[0,0]-LE_TE.iloc[0,2])**2)+((LE_TE.iloc[0,1]-LE_TE.iloc[0,3])**2) )
#print(dist_LE0_TE0)
norm_hub = hub.copy()
norm_hub = norm_hub/Xdiff_hub
#print(norm_hub.head())
scaled_hub = norm_hub.copy()
scaled_hub = scaled_hub*dist_LE0_TE0*5.5
translated_hub = scaled_hub.copy()
xhub_TE_diff = LE_TE.iloc[0,2] - translated_hub.iloc[127,0]
yhub_TE_diff = LE_TE.iloc[0,3] - translated_hub.iloc[127,1]
#print(xhub_TE_diff)
#print(yhub_TE_diff)
translated_hub['X'] = translated_hub['X'] + xhub_TE_diff
translated_hub['Y'] = translated_hub['Y'] + yhub_TE_diff - 30e-2
translated_hub = translated_hub.round(6)
translated_hub.to_csv('translated_hub.dat', sep='\t', index=False)


# Using LE, TE and the scaled Hub Coordinates, construct the casing.
#  We will construct the casing using three sections, one before the LE, second from LE to TE and finally

casing = translated_hub.copy()
#print(casing.head())
#   Part 1 of casing
casing.iloc[:95,1] = LE_TE.iloc[19,1]+30e-2
casing1 = casing.iloc[0:95,:]
#print(casing1.tail())

#   Part 2 of casing
def intermediates(p1, p2, nb_points=8):
    """"Return a list of nb_points equally spaced points
    between p1 and p2"""
    # If we have 8 intermediate points, we have 8+1=9 spaces
    # between p1 and p2
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

    return [[p1[0] + i * x_spacing, p1[1] +  i * y_spacing, 0.0] 
            for i in range(1, nb_points+1)]
case3_points = intermediates([casing.iloc[93,0]+10e-1, LE_TE.iloc[19,1]+30e-2], [casing.iloc[125,0]-10e-2, LE_TE.iloc[19,3]+1e-2], nb_points=29)
case3_df = pd.DataFrame(case3_points, columns=['X','Y', 'Z'])
caseing1_df = casing1.append(case3_df, ignore_index=True)

#  Part 3 of casing
casing.iloc[124:,1] = LE_TE.iloc[19,3]+10e-2
caseing1_dg = caseing1_df.append(casing.iloc[124:,], ignore_index=True)
caseing1_dg = caseing1_dg.round(6)
caseing1_dg.to_csv('caseing1_dg.dat', sep='\t', index=False)

#This equates the number of points in the casing to the number of points in the hub,
# this can also be achieved by simply making sure that the ending abscissa of both
# the casing and hub are the same

   #final comparison of coordinates:
#print(translated_hub.tail())
#print(caseing1_dg.head())



# Streamline construction: We need to construct 21 streamlines between the hub and casing. Also, we need to make sure that the streamlines include the LE and TE coodinates.
   # This is done in three parts. We start with making a dataframe of all the points on the left of LE and divide them into 21 sections

def streamline_coordinates_construct(x_iloc):
   
   if x_iloc<110:
      #Use the LE coodinates to space the streamlines
      temp_coords=[]
      for i in range(len(LE_df['X'])):
         y20 = translated_hub.iloc[x_iloc,1]+((LE_df.iloc[i,1])*((caseing1_dg.iloc[x_iloc,1]-translated_hub.iloc[x_iloc,1])/(LE_df.iloc[0,1]-LE_df.iloc[19,1])))
         temp_coords.append(y20)
         temp_coords = [round(num, 6) for num in temp_coords]
         sorted(temp_coords, reverse=True)
      #print(temp_coords)
      #print(translated_hub.iloc[x_iloc, 1])
      stream_deav = max(temp_coords) - caseing1_dg.iloc[x_iloc, 1]
      temp_coords = [x-stream_deav for x in temp_coords]
      streamlines_sect_1_y = temp_coords
      # to evenly space the streamlines
      #streamlines_sect_1_y = np.linspace(caseing1_dg.iloc[x_iloc,1],translated_hub.iloc[x_iloc,1],21)
      #print(streamlines_sect_1_y)
      streamlines_sect_1_x = [caseing1_dg.iloc[x_iloc,0]] * len(streamlines_sect_1_y)
      #print(streamlines_sect_1_x)
      streamlines_sect_1_z = [0.0] * len(streamlines_sect_1_x)
      #print(streamlines_sect_1_z)
      streamlines_sect_next_df = pd.DataFrame(list(zip(streamlines_sect_1_x, streamlines_sect_1_y, streamlines_sect_1_z)), columns =['X', 'Y', 'Z'], dtype=float)
      #print(streamlines_sect_next_df.tail())
   else:
      temp_coords=[]
      for i in range(len(TE_df['X'])):
         y20 = translated_hub.iloc[x_iloc,1]+((TE_df.iloc[i,1])*((caseing1_dg.iloc[x_iloc,1]-translated_hub.iloc[x_iloc,1])/(TE_df.iloc[0,1]-TE_df.iloc[19,1])))
         temp_coords.append(y20)
         temp_coords = [round(num, 6) for num in temp_coords]
         sorted(temp_coords, reverse=True)
      stream_deav = max(temp_coords) - caseing1_dg.iloc[x_iloc, 1]
      temp_coords = [x-stream_deav for x in temp_coords]
      streamlines_sect_1_y = temp_coords
      streamlines_sect_1_x = [caseing1_dg.iloc[x_iloc,0]] * len(streamlines_sect_1_y)
      streamlines_sect_1_z = [0.0] * len(streamlines_sect_1_x)
      streamlines_sect_next_df = pd.DataFrame(list(zip(streamlines_sect_1_x, streamlines_sect_1_y, streamlines_sect_1_z)), columns =['X', 'Y', 'Z'], dtype=float)
   return streamlines_sect_next_df

list_x_vals = [np.arange(60, 209, 10)]
#print(list_x_vals)


streamlines_sect01_next_df = streamline_coordinates_construct(60)
#print(streamlines_sect01_next_df.tail())
streamlines_sect02_next_df = streamline_coordinates_construct(70)
streamlines_sect03_next_df = streamline_coordinates_construct(80)
streamlines_sect04_next_df = streamline_coordinates_construct(85)
streamlines_sect05_next_df = streamline_coordinates_construct(98)
streamlines_sect06_next_df = streamline_coordinates_construct(105)
streamlines_sect07_next_df = streamline_coordinates_construct(112)
streamlines_sect08_next_df = streamline_coordinates_construct(120)
streamlines_sect09_next_df = streamline_coordinates_construct(130)
streamlines_sect10_next_df = streamline_coordinates_construct(140)
streamlines_sect11_next_df = streamline_coordinates_construct(150)
streamlines_sect12_next_df = streamline_coordinates_construct(160)
streamlines_sect13_next_df = streamline_coordinates_construct(170)
streamlines_sect14_next_df = streamline_coordinates_construct(180)
streamlines_sect15_next_df = streamline_coordinates_construct(190)
streamlines_sect16_next_df = streamline_coordinates_construct(209)

#print(list_of_coordinates)

""" There is an issue with the current LE and TE coordinates where in they are no uniformly spced and there are duplicated values as well. We replace them with an evenly spaced linear interpolation version using "interpolation_LE_TE.py" file"""

#interp_LE_df = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_streamlines/sorted_LE_df.dat",na_values = None,skipinitialspace=True,sep="\s+")
#print(interp_LE_df)
#interp_TE_df = pd.read_csv("/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_streamlines/sorted_TE_df.dat",na_values = None,skipinitialspace=True,sep="\s+")
#print(interp_TE_df)

streamlines_final_df = streamlines_sect01_next_df.append(streamlines_sect02_next_df, ignore_index = True)
#print(streamlines_final_df.tail())
streamlines_final_df = streamlines_final_df.append(streamlines_sect03_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect04_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(LE_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect05_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect06_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect07_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect08_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(TE_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect09_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect10_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect11_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect12_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect13_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect14_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect15_next_df, ignore_index = True)
streamlines_final_df = streamlines_final_df.append(streamlines_sect16_next_df, ignore_index = True)
#print(streamlines_final_df.head())
#print(streamlines_final_df.tail())

#df.iloc[::5, :]

streamline_01_coordiantes = streamlines_final_df.iloc[::20, :].reset_index(drop=True)
#print(streamline_01_coordiantes.tail())
streamline_02_coordiantes = streamlines_final_df.iloc[1::20, :].reset_index(drop=True)
streamline_03_coordiantes = streamlines_final_df.iloc[2::20, :].reset_index(drop=True)
streamline_04_coordiantes = streamlines_final_df.iloc[3::20, :].reset_index(drop=True)
streamline_05_coordiantes = streamlines_final_df.iloc[4::20, :].reset_index(drop=True)
streamline_06_coordiantes = streamlines_final_df.iloc[5::20, :].reset_index(drop=True)
streamline_07_coordiantes = streamlines_final_df.iloc[6::20, :].reset_index(drop=True)
streamline_08_coordiantes = streamlines_final_df.iloc[7::20, :].reset_index(drop=True)
streamline_09_coordiantes = streamlines_final_df.iloc[8::20, :].reset_index(drop=True)
streamline_10_coordiantes = streamlines_final_df.iloc[9::20, :].reset_index(drop=True)
streamline_11_coordiantes = streamlines_final_df.iloc[10::20, :].reset_index(drop=True)
streamline_12_coordiantes = streamlines_final_df.iloc[11::20, :].reset_index(drop=True)
streamline_13_coordiantes = streamlines_final_df.iloc[12::20, :].reset_index(drop=True)
streamline_14_coordiantes = streamlines_final_df.iloc[13::20, :].reset_index(drop=True)
streamline_15_coordiantes = streamlines_final_df.iloc[14::20, :].reset_index(drop=True)
streamline_16_coordiantes = streamlines_final_df.iloc[15::20, :].reset_index(drop=True)
streamline_17_coordiantes = streamlines_final_df.iloc[16::20, :].reset_index(drop=True)
streamline_18_coordiantes = streamlines_final_df.iloc[17::20, :].reset_index(drop=True)
streamline_19_coordiantes = streamlines_final_df.iloc[18::20, :].reset_index(drop=True)
streamline_20_coordiantes = streamlines_final_df.iloc[19::20, :].reset_index(drop=True)

#print(streamline_18_coordiantes.tail())

caseing1_dg = caseing1_dg.iloc[59:,:] #This chops off the casing extesnion and provides a more realistic view of the geometry.

"""
streamlines_sect_1_y = np.linspace(caseing1_dg.iloc[60,1],translated_hub.iloc[60,1],21)
print(streamlines_sect_1_y)
streamlines_sect_1_x = [caseing1_dg.iloc[60,0]] * len(streamlines_sect_1_y)
print(streamlines_sect_1_x)
streamlines_sect_1_z = [0.0] * len(streamlines_sect_1_x)
print(streamlines_sect_1_z)
streamlines_sect_1_df = pd.DataFrame(list(zip(streamlines_sect_1_x, streamlines_sect_1_y, streamlines_sect_1_z)), columns =['X', 'Y', 'Z'], dtype=float)
print(streamlines_sect_1_df.head())
"""



#Plot the files
plt.plot(translated_hub['X'],translated_hub['Y'], label='Translated Hub Coordinates', color='Violet')
plt.plot(LE_TE['xLE'],LE_TE['rLE'], label='LE', color='red')
plt.plot(LE_TE['xTE'],LE_TE['rTE'], label='TE', color='blue')
plt.plot(caseing1_dg['X'],caseing1_dg['Y'], label='Generated Casing', color='black')
plt.plot(streamlines_final_df['X'], streamlines_final_df['Y'], 'g^', label='Streamline Coordinates')

# Plot Streamlines
plt.plot(streamline_01_coordiantes['X'],streamline_01_coordiantes['Y'], label='Streamlines', color='grey')
plt.plot(streamline_02_coordiantes['X'],streamline_02_coordiantes['Y'], color='grey')
plt.plot(streamline_03_coordiantes['X'],streamline_03_coordiantes['Y'], color='grey')
plt.plot(streamline_04_coordiantes['X'],streamline_04_coordiantes['Y'], color='grey')
plt.plot(streamline_05_coordiantes['X'],streamline_05_coordiantes['Y'], color='grey')
plt.plot(streamline_06_coordiantes['X'],streamline_06_coordiantes['Y'], color='grey')
plt.plot(streamline_07_coordiantes['X'],streamline_07_coordiantes['Y'], color='grey')
plt.plot(streamline_08_coordiantes['X'],streamline_08_coordiantes['Y'], color='grey')
plt.plot(streamline_09_coordiantes['X'],streamline_09_coordiantes['Y'], color='grey')
plt.plot(streamline_10_coordiantes['X'],streamline_10_coordiantes['Y'], color='grey')
plt.plot(streamline_11_coordiantes['X'],streamline_11_coordiantes['Y'], color='grey')
plt.plot(streamline_12_coordiantes['X'],streamline_12_coordiantes['Y'], color='grey')
plt.plot(streamline_13_coordiantes['X'],streamline_13_coordiantes['Y'], color='grey')
plt.plot(streamline_14_coordiantes['X'],streamline_14_coordiantes['Y'], color='grey')
plt.plot(streamline_15_coordiantes['X'],streamline_15_coordiantes['Y'], color='grey')
plt.plot(streamline_16_coordiantes['X'],streamline_16_coordiantes['Y'], color='grey')
plt.plot(streamline_17_coordiantes['X'],streamline_17_coordiantes['Y'], color='grey')
plt.plot(streamline_18_coordiantes['X'],streamline_18_coordiantes['Y'], color='grey')
plt.plot(streamline_19_coordiantes['X'],streamline_19_coordiantes['Y'], color='grey')
plt.plot(streamline_20_coordiantes['X'],streamline_20_coordiantes['Y'], color='grey')
#plt.plot(streamline_21_coordiantes['X'],streamline_21_coordiantes['Y'], color='grey')




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


