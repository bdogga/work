#!/bin/bash


#clean:
rm tblade.log spancontrolinputs.2.log T-Blade3_run.log square_distance.log uvblade.1.2.TT Airfoil_fit.png 


tblade3 3dbgbinput.2.dat dev> tblade.log
#/home/christopher/Desktop/Research/T-Blade3-master/bin/techop blade.1.2.TT 20 > techop.log
#/home/christopher/Desktop/Research/Mises/bin/iset 1.2.TT << EOF > iset.log
python '/home/bharadwaj/work/Meeting_10/Meeting docs/Chris Feldman Docs/E3_trial1/E3_fan_layer05_te_altered/Blade_comparison_openmdao.py' > square_distance.log
#python '/home/christopher/Desktop/Research/T-Blade3-master/scripts/plot_thickness_data.py' > thickness_plot.log
#python '/home/christopher/Desktop/Research/T-Blade3-master/scripts/plot_2D_sections.py' > section_plot.log
#1

#2

#3
#4
#0
#EOF
#cp ises.1.2.TT_inv ises.1.2.TT 
#/home/christopher/Desktop/Research/Mises/bin/ises 1.2.TT << EOF > ises_inv.log
#6
#0
#EOF
#cp ises.1.2.TT_Re ises.1.2.TT 
#/home/christopher/Desktop/Research/Mises/bin/ises 1.2.TT << EOF > ises_visc.log
#-200
#0
#EOF
#/home/christopher/Desktop/Research/Mises/bin/iplot 1.2.TT << EOF > iplot.log
#1
#11
#0
#0
#EOF


#grep Zeta iplot.log | cut -d'=' -f 2 > zeta_out.dat
#grep S2 iplot.log | awk {'print $5'} > S2_out.dat
#grep rms\(dR\) ises_visc.log | tail -n 1 | awk {'print $1'} > cases_out.dat
#grep Square_distance.dat  > Sq_diff_out.dat



