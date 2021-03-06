# Script to plot meanline slope u (nondimensional chord)
# Written by Sabrina Shrestha (University of Cincinnati)
# Modified by Mayank Sharma (GTSL, University of Cincinnati)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from cycler import cycler
import os
import sys

## THe main issue was with the difference in number of coodrinatesin some of the rows. Wrote a rough code to bypass that issue. 

# Plot (m', \theta) sections
# Stored in the same PDF
with PdfPages('NASA_plot_uv_coordinates.pdf') as pdf:
   for i_sec in range(1, 21):
      print(i_sec)
      def add_page(i_sec):   
            # Read section files
         filename            = 'fan-curve_layer' + str(i_sec) + '.dat'
         f                   = open(filename, "r")
         lines               = f.readlines()
         lines1              = lines[107:197]     # Specify the rows where the coordinates exist
         f.close()
         print(i_sec)
         # numpy arrays for storing blade section coordinates read from the file
         u             = np.zeros(len(lines1))
         v             = np.zeros(len(lines1))

         # Store the blade coordinates read from the file in the arrays defined above
         i                   = 0
         for line in lines1:
            u[i]      = float(line.split()[0])
            v[i]      = float(line.split()[1])
            i         = i + 1
            
         # Plot the 2D blade section
         plt.figure()
         plt.plot(u, v, 'k')
         plt.xlabel(r"$u$", fontsize = 16)
         plt.ylabel(r'$v$',   fontsize = 16)
         plt.title(r"($u, v$) plot for section %d"%int(i_sec), fontsize = 16)
         plt.axis('equal')
         # Save PDF
         pdf.savefig()   

      def add_page_short_ones(i_sec):   
            # Read section files
         filename            = 'fan-curve_layer' + str(i_sec) + '.dat'
         f                   = open(filename, "r")
         lines               = f.readlines()
         lines1              = lines[105:193]     # Specify the rows where the coordinates exist
         f.close()
         # numpy arrays for storing blade section coordinates read from the file
         u             = np.zeros(len(lines1))
         v             = np.zeros(len(lines1))

         # Store the blade coordinates read from the file in the arrays defined above
         i                   = 0
         for line in lines1:
            u[i]      = float(line.split()[0])
            v[i]      = float(line.split()[1])
            i         = i + 1
            
         # Plot the 2D blade section
         plt.figure()
         plt.plot(u, v, 'k')
         plt.xlabel(r"$u$", fontsize = 16)
         plt.ylabel(r'$v$',   fontsize = 16)
         plt.title(r"($u, v$) plot for section %d"%int(i_sec), fontsize = 16)
         plt.axis('equal')

         # Save PDF
         pdf.savefig()      
         
      if int(i_sec) in range(5, 8):
         add_page_short_ones(i_sec)
      else:
         add_page(i_sec)



plt.close()
