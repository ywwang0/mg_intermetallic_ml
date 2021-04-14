'''
******************************************************************
coding: utf-8
Author: Yaowei Wang
E-mail: yaowei.wang@sjtu.edu.cn
Function: calcualte workfunction
Input: VASP output
Output: vaccum energy, fermi energy, work function
History: 
04/14/2021: Created

To be chieve:

Note:
How to find certain context in python (get_fermi function)
*******************************************************************
'''


from pymatgen.io.vasp import Locpot
import matplotlib.pyplot as plt
import numpy as np

def e_vaccum():
    slab_locpot = Locpot.from_file("LOCPOT")
    with open('POSCAR','r') as f:
        content = f.readlines()
    z_length = eval(content[4].split()[-1])
    slab_zlp = slab_locpot.get_average_along_axis(2)
    vac_range = int(3/z_length*len(slab_zlp))
    return round(np.average(slab_zlp[:vac_range]),4)

def get_fermi():
    with open ('OUTCAR','r') as f:
        context = f.readlines()
    target_line = []
    for l in context:
        if l.find('E-fermi') == -1:
            continue
        else:
            target_line.append(l)
    fermi = target_line[-1].split()[2]
#     print(f'费米能级为{fermi}')
    return eval(fermi)

def plot_zpotential():
    slab_locpot = Locpot.from_file("LOCPOT")
    slab_zlp = slab_locpot.get_average_along_axis(2)
    plt.plot(slab_zlp)
    plt.savefig('zpotential.pdf',dpi=900)

# Main Function
plot_zpotential()
vaccum_energy = e_vaccum()
fermi_energy = get_fermi()
print(vaccum_energy,fermi_energy,vaccum_energy-fermi_energy)
