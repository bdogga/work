#!/bin/bash         

echo "Running Plotting Tbalde3"

tblade3 3dbgbinput.1.dat dev
python3 2python_airfoil3d_plotter.py
