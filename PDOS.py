#!/usr/bin/env python
"""
Extract PDOS from DOSCAR

IMPORTANT - in a geometry optimization, DOSCAR is averaged over the steps
 of the optimization. DOS plots must therefore come from single points with
 larger NEDOS values
"""

import sys

import linecache

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Set a large font size for DOS plots for figures/papers

font = {'family' : 'normal',
    'weight' : 'bold',
    'size'   : 30}

plt.rc('font', **font)

# Set the size of the plot in inches (Larger than default)
plt.rcParams["figure.figsize"] = [10,10]

#import sys

doscar = 'DOSCAR'
ion_number = int(sys.argv[1])

#first_parameters = linecache.getline(doscar,1)

#n_ions,n_real_ions,PDOS_bool,ncdij = first_parameters.split()

name = linecache.getline(doscar,5)

energy_params = linecache.getline(doscar,6).split()

NEDOS = int(energy_params[2])
E_f = float(energy_params[3])


"""
Create lists of zeros to store data
"""
energies = [0] * NEDOS

total_s_up = [0] * NEDOS
total_s_down = [0] * NEDOS

total_py_up = [0] * NEDOS
total_py_down = [0] * NEDOS
total_pz_up = [0] * NEDOS
total_pz_down = [0] * NEDOS
total_px_up = [0] * NEDOS
total_px_down = [0] * NEDOS

total_dxy_up = [0] * NEDOS
total_dxy_down = [0] * NEDOS
total_dyz_up = [0] * NEDOS
total_dyz_down = [0] * NEDOS
total_dz2_up = [0] * NEDOS
total_dz2_down = [0] * NEDOS
total_dxz_up = [0] * NEDOS
total_dxz_down = [0] * NEDOS
total_dx2_up = [0] * NEDOS
total_dx2_down = [0] * NEDOS




def get_ion_PDOS(file,ion_number,points,energies,Ef):
# Identify the part of the file corresponding to the ion
    first_line_no = 7 + (NEDOS + 1) * ion_number
# Loop through the NEDOS lines describing the ion
    for E_point in range(first_line_no,first_line_no+NEDOS):
# E_index starts counting at 0 wherever we are in the file
        E_index = E_point - first_line_no
# Break the line up into spin-orbital components
        all_PDOS = linecache.getline(file,E_point).split()

# Set zero of energy scale at the Fermi level by subtracting
# Ef from each point
        energies[E_index] = (float(all_PDOS[0])) - Ef


# Add s PDOS contributions from this atom to the total
        s_up = float(all_PDOS[1])
        total_s_up[E_index] += s_up
        s_down = float(all_PDOS[2])
        total_s_down[E_index] += s_down

# p PDOS        
        py_up = float(all_PDOS[3])
        total_py_up[E_index] += py_up
        py_down = float(all_PDOS[4])
        total_py_down[E_index] += py_down
        pz_up = float(all_PDOS[5])
        total_pz_up[E_index] += pz_up
        pz_down = float(all_PDOS[6])
        total_pz_down[E_index] += pz_down
        px_up = float(all_PDOS[7])
        total_px_up[E_index] += px_up
        px_down = float(all_PDOS[8])
        total_px_down[E_index] += px_down

# d PDOS        
        dxy_up = float(all_PDOS[9])
        total_dxy_up[E_index] += dxy_up
        dxy_down = float(all_PDOS[10])
        total_dxy_down[E_index] = dxy_down
        dyz_up = float(all_PDOS[11])
        total_dyz_up[E_index] += dyz_up
        dyz_down = float(all_PDOS[12])
        total_dyz_down[E_index] += dyz_down
        dz2_up = float(all_PDOS[13])
        total_dz2_up[E_index] += dz2_up
        dz2_down = float(all_PDOS[14])
        total_dz2_down[E_index] += dz2_down
        dxz_up = float(all_PDOS[15])
        total_dxz_up[E_index] += dxz_up
        dxz_down = float(all_PDOS[16])
        total_dxz_down[E_index] += dxz_down
        dx2_up = float(all_PDOS[17])
        total_dx2_up[E_index] += dx2_up
        dx2_down = float(all_PDOS[18])
        total_dx2_down[E_index] += dx2_down
        
    return np.asarray((energies,total_s_up,total_s_down,total_py_up,total_py_down,total_px_up,total_px_down,total_pz_up,total_pz_down,total_dxy_up,total_dxy_down,total_dyz_up,total_dyz_down,total_dz2_up,total_dz2_down,total_dxz_up,total_dxz_down,total_dx2_up,total_dx2_down))


dos_array = get_ion_PDOS(doscar,ion_number,NEDOS,energies,E_f)

def plot_d_PDOS(data_array,fermi_energy,E_lower,E_upper):
    # Set range of energy axis
    # Set energy data as a variable for neatness
    E = data_array[0]
    """
    # Plot s orbital projection
    plt.plot(data_array[1],E,color='black') # s up
    plt.plot((-1*data_array[2]),E,color='black') # s down
    """
    
    
    # Plot all the d orbital projections
    plt.plot(data_array[9],E,color='red', linewidth=2.5) # xy up
    plt.plot((-1*data_array[10]),E,color='red', linewidth=2.5) # xy down
    plt.plot(data_array[11],E,color='green', linewidth=2.5) # yz up
    plt.plot((-1*data_array[12]),E,color='green', linewidth=2.5) # yz down
    plt.plot(data_array[13],E,color='blue', linewidth=2.5) # z2 up
    plt.plot((-1*data_array[14]),E,color='blue', linewidth=2.5) # z2 down
    plt.plot(data_array[15],E,color='purple', linewidth=2.5) # xz up
    plt.plot((-1*data_array[16]),E,color='purple', linewidth=2.5) # xz down
    plt.plot(data_array[17],E,color='orange', linewidth=2.5) # x2-y2 up
    plt.plot((-1*data_array[18]),E,color='orange', linewidth=2.5) # x2-y2 down
    
    """
    Use this version if the ion is spin-down
    but you want it to look spin-up!
    """
    """
    plt.plot(-1*data_array[9],E,color='red', linewidth=2.5) # xy up
    plt.plot((data_array[10]),E,color='red', linewidth=2.5) # xy down
    plt.plot(-1*data_array[11],E,color='green', linewidth=2.5) # yz up
    plt.plot((data_array[12]),E,color='green', linewidth=2.5) # yz down
    plt.plot(-1*data_array[13],E,color='blue', linewidth=2.5) # z2 up
    plt.plot((data_array[14]),E,color='blue', linewidth=2.5) # z2 down
    plt.plot(-1*data_array[15],E,color='purple', linewidth=2.5) # xz up
    plt.plot((data_array[16]),E,color='purple', linewidth=2.5) # xz down
    plt.plot(-1*data_array[17],E,color='orange', linewidth=2.5) # x2-y2 up
    plt.plot((data_array[18]),E,color='orange', linewidth=2.5) # x2-y2 down
    """
    
    plt.ylim(E_lower,E_upper)
#    xmin,xmax = plt.xlim(-3,3)
    
# Add a dotted line across the plot to mark the Fermi energy    
    xmin,xmax = plt.xlim(-2,2)
    plt.hlines(0,xmin,xmax,linestyle='--')
    
    # Create legend

#    black_patch = mpatches.Patch(color='black', label='s')
    red_patch = mpatches.Patch(color='red', label='$d_{xy}$')
    green_patch = mpatches.Patch(color='green', label='$d_{yz}$')
    blue_patch = mpatches.Patch(color='blue', label='$d_{z^2}$')
    purple_patch = mpatches.Patch(color='purple', label='$d_{xz}$')
    orange_patch = mpatches.Patch(color='orange', label='$d_{x^2-y^2}$')
    plt.legend(handles=[red_patch,green_patch,blue_patch,purple_patch,orange_patch],loc='upper right')


    # Labels, annotations etc    
#    plt.xlabel('DOS')
#    plt.ylabel('Energy / eV')
#    plt.annotate("$E_F$",xy=(xmin,fermi_energy),xytext=((xmin-0.15),(fermi_energy-0.3)))
#    plt.yticks([-2,0,2,4,6])
#    plt.xticks([])
    
    
    plt.savefig("Co2H_Mo18_PDOS.pdf",dpi=1000)
    plt.savefig("Co2H_Mo18_PDOS.png",dpi=1000)
    plt.show()

plot_d_PDOS(dos_array,E_f,-8,4)

doscar.close()