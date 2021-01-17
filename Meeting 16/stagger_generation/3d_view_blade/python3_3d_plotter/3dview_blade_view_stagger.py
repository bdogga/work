####################################################################
# 3D AIRFOILPLOT v0.1
####################################################################
# Plots the 3D airfoil from 'blade3d.casename' files created from T-Blade3
# in the same dimensions as the files and animates the 360 degree view of the plot
# Can plot multiple rows by giving the correct blade3d data files and hub and casing 3d data.
#
# Kiran Siddappaji
# University of Cincinnati

#
###########################################################

# Inputs: 'blade3d.casename.dat' files from T-Blade3 which contain the dimensional XYZ coordinates
#             hub and casing 3d curves
#             nfiles in line 83 
#             filenames in line 87
#             plotcolors in line 88
# The above line numbers might increase based on more comments being added in the future     
# To run:
# > 3dview_blade.py 
#

###########################################################

# The Zoom icon in the viewer does not work for 3D plots. A better library is needed.
# To Rotate  : left mouse + move the mouse
# To ZoomIN  : right mouse + move the mouse down.
# To ZoomOUT : right mouse + move the mouse up.
#
###########################################################
###########################################################

from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import sys
import math
import numpy as np
from matplotlib.ticker import LinearLocator, FormatStrFormatter
# import pylab as py


####################################################
##FUNCTIONS
####################################################	
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
nskip =  1 #Number of lines to skip at the top
npt   = -1 #enter # of points or -1 to read to the end of the file
ndim  = -1 #number of dimensions to read
pltcoord = [-1] #coordinates to plot [0,1] for x,y or [0,2] for x,z ... [-1] for all
coordnames  = ['x','y','z']

# casename1 = str(sys.argv[1])
# casename2 = str(sys.argv[2])
# nsect  = int(sys.argv[3]) 
# nsect2 = 2*nsect
pi = math.pi

nfiles = 4
nskips = [1]*nfiles
npts = [-1]*nfiles

#fnames = ["blade3d.GE_E3_Fan_rotor.dat"]
#plotcolors = ['green']

fnames = ["blade3d.GE_E3_Fan_rotor.dat","blade3d.nasafanstator.dat","hub.nasafanrotor.sldcrv","casing.nasafanrotor.sldcrv"]
plotcolors = ['green', 'blue', 'black','black']

# Combining both rows
print
print 'Number of files: ', len(fnames)
print
# fnames = dict(fnames.items() + gnames.items())
#converting Dict to List	
# fnames = fnames.values()
# print fnames	
def file_dim(fname, nskip):
  f = open(fname, 'r')
  for i in range(nskip+1):
    datastr = f.readline()

  f.close()
  return len(datastr.split())


def file_len(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

# For looping over files  
#fname = fnames[i]
fig = plt.figure(figsize=(14,6))
ax = fig.add_subplot(1,1,1,projection='3d')

for k in xrange(len(fnames)): 
  fname = fnames[k]
  npt = npts[k]
  nskip = nskips[k]
  print k,len(fnames),fname
  
  #Determine npt, ndim and pltcoord
  if npt < 0:
   npt = file_len(fname) - nskip

  if ndim < 0:
   ndim = file_dim(fname, nskip)

  if pltcoord[0] < 0:
   pltcoord = []
   for i in range(ndim):
     pltcoord.append(i)
    
  nplt = len(pltcoord)

  # print "fname: ", fname
  if k == 0:
	print "npt: ", npt, "   nplt: ", nplt, "   ndim: ", ndim
  x3d = np.zeros(npt)
  y3d = np.zeros(npt)
  z3d = np.zeros(npt)
  
  #Read file
  f = open(fname, 'r')

  for i in range(nskip):
   datastr = f.readline()

  line = np.zeros((nplt,npt))
  for i in range(npt):
   datastr = f.readline()
   data    = datastr.split()
   for j in range(nplt):
    line[j][i] = data[pltcoord[j]]
   #
  ##### 
  for i in range(npt):
   x3d[i] = line[0][i]
   # print x3d[i]
   y3d[i] = line[1][i]
   # print y3d[i]
   z3d[i] = line[2][i]
   # print z3d[i]
   # print x3d[i],y3d[i],z3d[i]
  # max_range = np.array([x3d.max()-x3d.min(), y3d.max()-y3d.min(), z3d.max()-z3d.min()]).max() / 2.0
  # mean_x = x3d.mean()
  # mean_y = y3d.mean()
  # mean_z = z3d.mean()
  # ax.set_xlim(mean_x - max_range, mean_x + max_range)
  # ax.set_ylim(mean_y - max_range, mean_y + max_range)
  # ax.set_zlim(mean_z - max_range, mean_z + max_range)
  ax.set_aspect('equal')
  
  # Plotting\ 
  ax.plot_wireframe(y3d,x3d,z3d,color =plotcolors[k],lw=1.5) #, rstride=4, cstride=4, linewidth=0)
  #ax.plot_trisurf(y3d,x3d,z3d, cmap=cm.jet, linewidth=0)
  
plt.xlabel("Y dim")
plt.ylabel("X dim")
set_aspect_equal_3d(ax)
# ax.view_init(90, -45)
plt.title("3D airfoil in x,y,z dimensional coordinates")
plt.legend(["3D Airfoil (x,y,z)"], loc='upper center', bbox_to_anchor=(0.9, 1.10),
          fancybox=True, shadow=True, ncol=2)  
		  
		  
		  
#plt.show()
 # rotate the axes and update
for angle in range(0, 360):
    ax.view_init(50, angle)
    plt.draw()
    plt.pause(0.25) 
