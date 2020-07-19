import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from numpy import savetxt
import csv


#Choose to weight square distances based on distance between points of target airfoil?
#1 = yes, 0 = no
weight = 1
#Set u values at ends of LE and TE
xLE = 0.15
xTE = 0.95

#Read in text files of airfoils
foil1 = pd.read_csv('/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/airfoil_plotter/seligdatfile0012.dat',na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y"])
foil1.dropna(axis=0,how='any',thresh=None)
foil1.astype(float)

# Ensure that target blade's coordinates fit into a 0<u<1 and -1<v<1 range
Xmax = foil1['X'].max()
Xmin = foil1['X'].min()
chord = Xmax-Xmin
foil1['X'] = foil1['X']-Xmin
foil1['X'] = foil1['X']/chord
foil1['Y'] = foil1['Y']/chord

#Calculate average distance between points for faceted airfoil
n = len(foil1['X'])
x_dist = []
y_dist = []
point_dist = []
for i in range(n):
	if i==0:
		x_dist.append((abs(foil1['X'].iloc[i]-foil1['X'].iloc[n-1])+abs(foil1['X'].iloc[i]-foil1['X'].iloc[i+1]))/2) 
		y_dist.append((abs(foil1['Y'].iloc[i]-foil1['Y'].iloc[n-1])+abs(foil1['Y'].iloc[i]-foil1['Y'].iloc[i+1]))/2)
		point_dist.append((x_dist[i]**2+y_dist[i]**2)**0.5)
	elif i==(n-1):
		x_dist.append((abs(foil1['X'].iloc[i]-foil1['X'].iloc[0])+abs(foil1['X'].iloc[i]-foil1['X'].iloc[i-1]))/2) 
		y_dist.append((abs(foil1['Y'].iloc[i]-foil1['Y'].iloc[0])+abs(foil1['Y'].iloc[i]-foil1['Y'].iloc[i-1]))/2)
		point_dist.append((x_dist[i]**2+y_dist[i]**2)**0.5)
	else:
		x_dist.append((abs(foil1['X'].iloc[i]-foil1['X'].iloc[i-1])+abs(foil1['X'].iloc[i]-foil1['X'].iloc[i+1]))/2) 
		y_dist.append((abs(foil1['Y'].iloc[i]-foil1['Y'].iloc[i-1])+abs(foil1['Y'].iloc[i]-foil1['Y'].iloc[i+1]))/2)
		point_dist.append((x_dist[i]**2+y_dist[i]**2)**0.5)

foil1['Point_dist'] = point_dist
for i in range(n):
	if weight==0:
		foil1['Point_dist'].iloc[i] = 1
	else:
		foil1['Point_dist'].iloc[i] = foil1['Point_dist'].iloc[i]
print(sum(foil1['Point_dist']))


foil2 = pd.read_csv('/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/airfoil_plotter/uvblade.1.2.TT', sep = " ", encoding = 'ISO-8859-1',na_values = None,skipinitialspace=True,keep_default_na=False,names=["X","Y"])
foil2.dropna(axis=0,how='any',thresh=None)
foil2.astype(float)
foil2.X = foil2.X+0.25

#split the coordinates into 4 quadrants to fit polynomials to target airfoil

Q1 = foil1.loc[foil1['X'] <= xLE]
Q1 = Q1.sort_values(by = 'Y',ascending = True)
line_1=np.interp(Q1['Y'],Q1['Y'],Q1['X'])
fig, ax = plt.subplots(2,2)
fig.suptitle('Target Airfoil')
ax[0,0].plot(Q1['Y'],Q1['X'],'o',Q1['Y'],line_1,'-')
ax[0,0].set_title('Leading Edge')


Q2 = foil1.loc[(foil1['X'] > xLE) & (foil1['X'] < xTE)]
Q2 = Q2.loc[Q2['Y']>= Q2['Y'].mean()]
Q2 = Q2.sort_values(by = 'X',axis=0,ascending=True)
line_2=np.interp(Q2['X'],Q2['X'],Q2['Y'])
ax[0,1].plot(Q2['X'],Q2['Y'],'o',Q2['X'],line_2,'-')
ax[0,1].set_title('Top')


Q3 = foil1.loc[(foil1['X'] > xLE) & (foil1['X'] < xTE)]
Q3 = Q3.loc[Q3['Y'] < Q3['Y'].mean()]
Q3 = Q3.sort_values(by = 'X',axis=0,ascending=True)
line_3=np.interp(Q3['X'],Q3['X'],Q3['Y'])
ax[1,0].plot(Q3['X'],Q3['Y'],'o',Q3['X'],line_3,'-')
ax[1,0].set_title('Bottom')


Q4 = foil1.loc[foil1['X'] >= xTE]
Q4 = Q4.sort_values(by = 'Y',axis=0,ascending=True)
line_4=np.interp(Q4['Y'],Q4['Y'],Q4['X'])
ax[1,1].plot(Q4['Y'],Q4['X'],'o',Q4['Y'],line_4,'-')#,label = ['Target Airfoil','Target Airfoil Linear Interpolation'])
ax[1,1].set_title('Trailing Edge')

#2nd blade

Q1_2 = foil2.loc[foil2['X'] <= xLE]
Q1_2 = Q1_2.sort_values(by = 'Y',axis=0,ascending=True)
line_1_2=np.interp(Q1['Y'],Q1_2['Y'],Q1_2['X'])
diff1 = Q1['Point_dist']*(line_1_2-Q1['X'])**2
fig, ax = plt.subplots(2,2)
fig.suptitle('Target vs Generated Blades')
ax[0,0].plot(Q1['Y'],Q1['X'],'o',Q1['Y'],line_1_2,'-')
ax[0,0].set_title('Leading Edge')



Q2_2 = foil2.loc[(foil2['X'] > xLE) & (foil2['X'] < xTE)]
Q2_2 = Q2_2.loc[Q2_2['Y']>= Q2_2['Y'].mean()]
Q2_2 = Q2_2.sort_values(by='X',axis=0,ascending=True)
line_2_2=np.interp(Q2['X'],Q2_2['X'],Q2_2['Y'])
diff2 = Q2['Point_dist']*(line_2_2-Q2['Y'])**2
ax[0,1].plot(Q2['X'],Q2['Y'],'o',Q2['X'],line_2_2,'-')
ax[0,1].set_title('Top')


Q3_2 = foil2.loc[(foil2['X'] > xLE) & (foil2['X'] < xTE)]
Q3_2 = Q3_2.loc[Q3_2['Y'] < Q3_2['Y'].mean()]
Q3_2 = Q3_2.sort_values(by = 'X',axis=0,ascending=True)
line_3_2=np.interp(Q3['X'],Q3_2['X'],Q3_2['Y'])
diff3 = Q3['Point_dist']*(line_3_2-Q3['Y'])**2
ax[1,0].plot(Q3['X'],Q3['Y'],'o',Q3['X'],line_3_2,'-')
ax[1,0].set_title('Bottom')
#ax[1,0].legend('Target Airfoil','Generated Airfoil')


Q4_2 = foil2.loc[foil2['X'] >= xTE]
Q4_2 = Q4_2.sort_values(by = 'Y',axis=0,ascending=True)
line_4_2=np.interp(Q4['Y'],Q4_2['Y'],Q4_2['X'])
diff4 = Q4['Point_dist']*(line_4_2-Q4['X'])**2
ax[1,1].plot(Q4['Y'],Q4['X'],'o',Q4['Y'],line_4_2,'-')
ax[1,1].set_title('Trailing Edge')


#plt.show()

diff_total = (diff1.sum() + diff2.sum() + diff3.sum() + diff4.sum())
difference = np.array([diff_total])
print(difference)
diff_total = pd.DataFrame(data=difference)
plt.figure()
plt.plot(foil1['X'],foil1['Y'])
plt.plot(foil2['X'],foil2['Y'])
plt.legend(['Target Airfoil','Generated Airfoil'],loc='upper left')
plt.title('Blade Comparison')
s = "Square distance ={}".format(diff_total)
plt.text(0.7,0.4,s)
plt.ylim(-0.5, 0.5)
plt.savefig('Airfoil_fit.png')
#diff_total.to_csv('/home/christopher/Desktop/Research/openmdao_project-Copy/Square_distance',index=False)
np.savetxt('Sq_diff_out.dat',difference)

