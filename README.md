VASP DOS scripts

PDOS.py - d PDOS for a spin-polarized calculation

H_PDOS.py - s PDOS for a spin-polarized calculation, intended for H atoms

Unpolarized_PDOS.py - d PDOS for a spin-unpolarized calculation

Unpolarized_total_DOS.py - total DOS for a spin-unpolarized calculation

These scripts all require a certain amount of editing to get them to work with your calculations, most notably the atom for which the PDOS should be plotted (given as an argument) and the energy range. The x limits can also be set manually.