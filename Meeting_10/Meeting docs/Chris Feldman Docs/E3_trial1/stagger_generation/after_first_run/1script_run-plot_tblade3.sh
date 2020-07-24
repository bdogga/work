#!/bin/bash         

echo "Running Plotting Tbalde3"

tblade3 3dbgbinput.1.dat dev
python3 python3_airfoil3d_plotter.py
