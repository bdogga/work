import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
#from scipy.optimize import curve_fit
#from scipy.optimize import minimize
#from scipy.interpolate import interp1d
from numpy import savetxt
import csv

#Read in text files of airfoils
foil1 = pd.read_csv('/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/populate-Tbalde3-example-file/input-for-sort.dat',na_values = None,skipinitialspace=True,skiprows=[0],sep="\s+",keep_default_na=False,names = ["J","in_Beta","out_Beta","mrel_in","chord","t/c_max","Incidence","Deviation","Sec. Flow Angle"])
#foil1.dropna(axis=0,how='any',thresh=None)
print(foil1.head())
potato = foil1.sort_index(ascending=False)
potato = potato.round(6)
del potato['J']
potato.reset_index(drop=True, inplace=True)
print(potato.head())
potato.index += 1
potato.index.names = ['J']
print(potato.head())
#potato.to_csv('/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/populate-Tbalde3-example-file/output-from-sort.dat', sep = "\t", index=True)
