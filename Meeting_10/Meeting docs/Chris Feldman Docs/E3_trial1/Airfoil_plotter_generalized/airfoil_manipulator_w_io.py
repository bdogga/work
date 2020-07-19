# Script to manipulate Airfoil sections
# Guide: Dr. Mark Turner (GTSL Lab, University of Cincinnati)
# Codeing: Bharadwaj "Ben" Dogga (GTSL, University of Cincinnati)
# Testing: Adam Ringheisen (GTSL, University of Cincinnati)

import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv


#Read in text files of airfoils
def getfile():
   fileinput = input("File:\n")
   foil1 = pd.read_csv(fileinput,na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["X","Y"])
   foil1.dropna(axis=0,how='any',thresh=None)
   foil1.astype(float)
   return foil1

#Compare the plots of new and old Airfoil
def plot_airfoil(foil1, dataset, angle=0):
   selection_foil = input("""
   
            Y: Yes
            N: No
               
   Do you want to plot the new airfoil? : """)
   
   selection_foil = selection_foil.upper()
   
   if selection_foil == "Y":
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
   elif selection_foil == "N":
      return 0
   else:
      print("Error. You must enter a valid Alphabet")
      plot_airfoil()
   
#Write changes to a new airfoil file.
def write_new_airfoil(foil1_new, iteration=0):
   iteration = str(iteration)
   selection_foil = input("""
   
            Y: Yes
            N: No
               
   Do you want to write the new airfoil Coordinates? : """)
   
   selection_foil = selection_foil.upper()
   
   if selection_foil == "Y":
      output_file_name = str(input("Enter output file name: \n"))
      foil1_new.to_csv(output_file_name+'.dat', sep='\t', index=False)
      print("\n Your new coodinates have been written. \n")
      return 0
   elif selection_foil == "N":
      return 0
   else:
      print("Error. You must enter a valid Alphabet")
      write_new_airfoil()



#remember that variables in functions are self contained which means that the variables declared in a function do not pass on to other funcitons.

#Function to Scale the airfoil
def scale(foil1):
   print("\n This is option A: Scale")
   scale_fact = float(input("\n Please enter the scale factor: "))
   foil1_new = foil1*(scale_fact)
   return foil1_new


#Function to Rotate the airfoil
def rotate(foil1):
   print("\n This is option B: Rotate")
   
   angle = float(input("\n Please enter the rotation angle in degrees: "))
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
   print("\n This is option C: X Offset")
   x_offset_fact = float(input("\n Please enter the X offset factor: "))
   foil1_new = foil1.copy()
   foil1_new['X'] = foil1['X']-x_offset_fact
   return x_offset_fact, foil1_new


#Function to Offset the airfoil in the Y Axis
def y_offset(foil1):
   print("\n This is option D: Y Offset")
   y_offset_fact = float(input("\n Please enter the Y offset factor: "))
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
   #print(menu.counter)
   choice = input("""
   *********Main Menu*********
               
   UC GTSL Lab Airfoil Manipulator: 
       
            A: Scale an Airfoil
            B: Rotate an Airfoil
            C: X offset
            D: Y offset
            Q: Quit
               
   Please make a selection from the menu: """)
   
   choice = choice.upper()
   
   if choice == "A":
      foil1 = getfile()
      foil1_scaled = scale(foil1)
      print("\n Your Scaled airfoil coordinates are: \n", foil1_scaled)
      plot_airfoil(foil1, foil1_scaled)
      write_new_airfoil(foil1_scaled, menu.counter)
      print("\n Starting a new case... \n")
      menu()
   elif choice == "B":
      foil1 = getfile()
      angle, foil1_rotated = rotate(foil1)
      print("\n Your airfoil coordinates after rotation are: \n", foil1_rotated)
      plot_airfoil(foil1, foil1_rotated, angle)
      write_new_airfoil(foil1_rotated, menu.counter)
      print("\n Starting a new case... \n")
      menu()
   elif choice == "C":
      foil1 = getfile()
      x_offset_fact, foil1_x_offset = x_offset(foil1)
      print("\n Your airfoil coordinates after rotation are: \n", foil1_x_offset)
      plot_airfoil(foil1, foil1_x_offset)
      write_new_airfoil(foil1_x_offset, menu.counter)
      print("\n Starting a new case... \n")
      menu()
   elif choice == "D":
      foil1 = getfile()
      y_offset_fact, foil1_y_offset = y_offset(foil1)
      print("\n Your airfoil coordinates after rotation are: \n", foil1_y_offset)
      plot_airfoil(foil1, foil1_y_offset)
      write_new_airfoil(foil1_y_offset, menu.counter)
      print("\n Starting a new case... \n")
      time.sleep(4)
      menu()
   elif choice == "Q":
      quit()
   else:
      print("Error. You must enter a valid Alphabet")
      menu()

#Counts the number of times the menu has been accessed in a single run
menu.counter = 0
#Calls the menu function
menu()

   
