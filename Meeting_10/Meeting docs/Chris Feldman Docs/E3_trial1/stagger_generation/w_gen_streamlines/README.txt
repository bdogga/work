#############################################################
geomturbo.exe [WINDOWS EXECUTABLE]

Kiran Siddappaji
Ahmed Nemnem
Gas Turbine Simulation Lab
University of Cincinnati
############################################################

Creates a geomturbo file 'row.1.geomTurbo' to go into
Autgorid (Numeca-Fine/TURBO's gridding tool) using 3D
bladesections and hub and tip streamlines obtained
from 3DBGB (http://gtsl.ase.uc.edu/3DBGB). The geomturbo
file is the native format for AUTOGRID.

# Need to run 3DBGB first to have the 3D sections.
# The blade scale factor in 3dbgbinput file should be in mm.

# Currently it works for only ODD number of coordinates in the airfoil.

#So if your airfoil has say 66 coordinates make it 67 or 65.
 Make sure the coordinates run from TE to LE to TE counter-clockwise with the TE point repeating.

#############################################################

EXAMPLE:

Input  : 3dbgbinput.1.dat
No. of points on each blade section : 241

step 1 : > 3dbgb 3dbgbinput.1.dat
    
         This creates the 3D bladesections needed for geomturbo.
	 Obtain 3dbgb executable from http://gtsl.ase.uc.edu/3DBGB .

step 2 : > geomturbo 3dbgbinput.1.dat 241

         Creates a geomturbo file, 'row.1.geomTurbo' in meters.



# This also can create geomturbo file for the splitter blade in the same row as the main blade.
STEPS:
1. Add 'S' at the end of the casename in the 3dbgbinput file (2nd line).
2. Make the filename of the splitter blade as 3dbgbinput.bladerowS.dat
3. Keep both the main blade and splitter blade inputs in the same directory and run them.
4. You will get files for both cases in the same directory.
5. You only have to run the geomturbo with the main blade file name as explained in the above process.
6. A single geomturbo file 'row_wth_splitter.geomTurbo' is created which includes both main blade and the splitter blade coordinates.