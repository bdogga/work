#!/bin/bash         

echo "Plotting Tbalde3 3D Output file"

tblade3 3dbgbinput.1.dat dev
python3 2python_airfoil3d_plotter.py
