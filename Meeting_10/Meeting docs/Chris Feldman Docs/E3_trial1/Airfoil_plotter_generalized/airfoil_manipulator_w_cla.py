# Script to manipulate a 2D Geometry
# Guide: Dr. Mark Turner (GTSL Lab, University of Cincinnati)
# Codeing: Bharadwaj "Ben" Dogga (GTSL, University of Cincinnati)
# Testing: Adam Ringheisen (GTSL, University of Cincinnati)

"""Readme:
Command line argument syntax: python3 script_filename.py "input_file_name_or_path" function_to_perform magnitude_of_function output_filename plot_option
Example: python3 airfoil_manipulator_w_cla.py "/home/naca0012_selig" s 40 airfoil_scaled_40.dat YP


Argument Name                 Options for Arguments: Comments      

function_to_perform           s: Scale a Geometry
                              r: Rotate a Geometry
                              x: X Offset a Geometry
                              y: Y Offset a Geometry
magnitude_of_function         Any real number
output_filename               0: Do not write to file, any other value will write to file. Use quotes if your filename contians a space
plot_option                   0: Do not plot
                              yp: Show plot
              

"""

import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv


#Read in text files of airfoils
def getfile():
   fileinput = str(sys.argv[1])
   foil1 = pd.read_csv(fileinput,na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y"])
   foil1.dropna(axis=0,how='any',thresh=None)
   foil1.astype(float)
   return foil1

#Compare the plots of new and old Airfoil
def plot_airfoil(foil1, dataset, angle=0):
   selection_foil = plot_option
   selection_foil = sys.argv[5]
   selection_foil = selection_foil.upper()
   
   if selection_foil == "YP":
      fig = plt.figure(figsize=(15,15))
      fig.suptitle('Horizontally stacked subplots', size=32)
      ax1 = plt.subplot(121)
      ax2 = plt.subplot(122)
      ax1.plot(foil1['X'],foil1['Y'], label='Original Coordinates', color='red')
      ax1.grid(True)
      ax1.set(adjustable='box', aspect='equal')
      ax1.legend(fontsize=14)

      ax2.plot(dataset['X'],dataset['Y'], label='New airfoil Plot', color='orange')
      ax2.grid(True)
      ax2.set(adjustable='box', aspect='equal')
      ax2.legend(fontsize=14)      
      plt.legend()
      plt.draw()
      plt.show()
      return 0
   elif selection_foil == "0":
      return 0
   else:
      print("Error. You must enter a valid plot argument")
      quit()
   
#Write changes to a new airfoil file.
def write_new_airfoil(foil1_new, iteration=0):
   iteration = str(iteration)
   output_filename = sys.argv[4]
   selection_foil = output_filename
   
   if selection_foil != "0":
      output_file_name = selection_foil
      foil1_new.to_csv(output_file_name, sep='\t', index=False)
      print("\n Your new coodinates have been written. \n")
      return 0
   elif selection_foil == "0":
      return 0
   else:
      print("Error. You must enter a valid write argument")
      quit()



#remember that variables in functions are self contained which means that the variables declared in a function do not pass on to other funcitons.

#Function to Scale the airfoil
def scale(foil1):
   print("\n This is option S: Scale")
   scale_fact = unit_change
   scale_fact = float(sys.argv[3])
   foil1_new = foil1*(scale_fact)
   return foil1_new


#Function to Rotate the airfoil
def rotate(foil1):
   print("\n This is option R: Rotate")
   angle = unit_change
   angle = float(sys.argv[3])
   stggr_ang = np.deg2rad(angle)

   def rotate_algo(x, y, rad):
       xx = round(math.cos(rad)*x - math.sin(rad)*y,6)
       yy = round(math.sin(rad)*x + math.cos(rad)*y,6)
       return xx, yy

# Code Source: "https://stackoverflow.com/questions/35905550/python-rotating-a-point-counterclockwise-by-an-angle"
# Math Source: "https://en.wikipedia.org/wiki/Rotation_(mathematics)"
# Code troubleshoot help: "Kiran Dogiparthi (dogipakr@mail.uc.edu), UC MEngg CS Fall 2019 Admit" 

   x_new=[]
   y_new=[]
   for i in range(len(foil1)):
      xx,yy = rotate_algo(foil1.iloc[i,0], foil1.iloc[i,1], stggr_ang)
      x_new.append(xx)
      y_new.append(yy)
    
   dataset = pd.DataFrame(list(zip(x_new, y_new)), 
               columns =['X', 'Y']) 
   
   return angle, dataset


#Function to Offset the airfoil in the X Axis
def x_offset(foil1):
   print("\n This is option X: X Offset")
   x_offset_fact = unit_change
   x_offset_fact = float(sys.argv[3])
   foil1_new = foil1.copy()
   foil1_new['X'] = foil1['X']-x_offset_fact
   return x_offset_fact, foil1_new


#Function to Offset the airfoil in the Y Axis
def y_offset(foil1):
   print("\n This is option Y: Y Offset")
   y_offset_fact = unit_change
   y_offset_fact = float(sys.argv[3])
   foil1_new = foil1.copy()
   foil1_new['Y'] = foil1['Y']-y_offset_fact
   return y_offset_fact, foil1_new


#Function to quit the code
def quit():
   print("\n The system will now exit...")
   time.sleep(1)
   sys.exit()



#Function to run the menu
def menu():
   menu.counter += 1
   #time.sleep(1)
   print(menu.counter)
   choice = function
   choice = str(sys.argv[2])
   choice = choice.upper()
   
   if choice == "S":
      foil1 = getfile()
      foil1_scaled = scale(foil1)
      print("\n Your Scaled airfoil coordinates are: \n", foil1_scaled)
      plot_airfoil(foil1, foil1_scaled)
      write_new_airfoil(foil1_scaled, menu.counter)
   elif choice == "R":
      foil1 = getfile()
      angle, foil1_rotated = rotate(foil1)
      print("\n Your airfoil coordinates after rotation are: \n", foil1_rotated)
      plot_airfoil(foil1, foil1_rotated, angle)
      write_new_airfoil(foil1_rotated, menu.counter)
   elif choice == "X":
      foil1 = getfile()
      x_offset_fact, foil1_x_offset = x_offset(foil1)
      print("\n Your airfoil coordinates after rotation are: \n", foil1_x_offset)
      plot_airfoil(foil1, foil1_x_offset)
      write_new_airfoil(foil1_x_offset, menu.counter)
   elif choice == "Y":
      foil1 = getfile()
      y_offset_fact, foil1_y_offset = y_offset(foil1)
      print("\n Your airfoil coordinates after rotation are: \n", foil1_y_offset)
      plot_airfoil(foil1, foil1_y_offset)
      write_new_airfoil(foil1_y_offset, menu.counter)
   else:
      print("Error. You must enter a valid operaton argument")
      quit()



#Assigning default values for all the inputs
function = str('q')
unit_change = float(0)
plot_option = str('np')
output_filename = str('new_airfoil.dat')



#Counts the number of times the menu has been accessed in a single run
menu.counter = 0
#Calls the menu function
menu()
