#############################################################
# Plots 2d airfoil with showing the passage
# Inputs: filename and blade count in lines 19 and 24
#############################################################
import sys
import math
import numpy as np
import pylab as py


nskip =  2 #Number of lines to skip at the top
npt   = -1 #enter # of points or -1 to read to the end of the file
ndim  = -1 #number of dimensions to read
pltcoord = [0,1] #coordinates to plot [0,1] for x,y or [0,2] for x,z ... [-1] for all
coordnames  = ['x','y','z']

nskips = [2]*1
npts = [-1]*1
nblades = 32
pitch  = (2.*math.pi/nblades) 
print
print "pitch:",pitch
print
fnames = ["blade.1.1.GE_E3_Fan_rotor"]

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

#print "fname: ", fname
#print "npt: ", npt, "   nplt: ", nplt, "   ndim: ", ndim

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

  pltname = []
  for j in range(nplt):
   pltname.append(coordnames[pltcoord[j]])

  f.close()
      
#Plot stuff
  fignum = 1
  pairs = []
  if nplt == 2:
   pairs.append([0,1])
  elif nplt == 3:
   pairs.append([0,1])
   pairs.append([0,2])
   pairs.append([1,2])
    
  npair = len(pairs)
  yp = []
  py.figure(fignum)
  for i in range(npair):
   pair = pairs[i]
   yp = line[1] + pitch
   # print yp, pair[1]
   py.subplot(npair,1,i)
   py.plot(line[pair[0]],line[pair[1]])
   py.plot(line[pair[0]],yp)
   py.xlabel(pltname[pair[0]]); py.ylabel(pltname[pair[1]]) 
   py.axis("equal")
  
py.show()

 
