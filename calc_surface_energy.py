'''
******************************************************************
coding: utf-8
Author: Yaowei Wang
E-mail: yaowei.wang@sjtu.edu.cn
Function: calcualte surface energy for a intermetallic
Input: mp-id in Material Project, For example, mp-1265 for MgO
Output: Surface energies and coresponding directories
History:
01/01/2021: Created
04/07/2021: Change from ratio = int(dicts['Mg']/dicts[x]) to ratio = dicts['Mg']/dicts[x]

To be chieve:
a. plot the surface energy under Mg-rich and x-rich condition
*******************************************************************
'''

import os
from matminer.data_retrieval.retrieve_MP import MPDataRetrieval

mp_id = input('Please input mp-id of the intermetallic (for example: mp-1265):')
mpdr = MPDataRetrieval(api_key='Bw7HdCARiXvzEWJK')
df = mpdr.get_dataframe(criteria={"material_id": mp_id},
                        properties=['energy_per_atom', 'formation_energy_per_atom',
                                   'unit_cell_formula'])

dicts = df['unit_cell_formula'][mp_id]
total_atoms_in_formula = int(sum(dicts.values()))
fe_formula = df['formation_energy_per_atom'][mp_id]*total_atoms_in_formula
en_formula = df['energy_per_atom'][mp_id]*total_atoms_in_formula
x = [i for i in dicts.keys() if i != 'Mg'][0]

'''DFT energies for pure elements'''
eles = {'La':-4.9266, 'Ce':-5.9343, 'Pr':-4.7837, 'Y':-6.4674,
        'Er':-4.5674, 'Li':-1.9080, 'Sm':-4.7163, 'Ni':-5.7783,
        'Cu':-4.0993, 'Ag':-2.8262, 'Sr':-1.6841, 'Eu':-10.2906,
        'Hg':-0.3016, 'Tm':-4.4782, 'Ho':-4.5781, 'Tb':-4.6275,
        'Lu':-4.5259, 'Dy':-4.5999, 'Ba':-1.9246, 'Nd':-4.7651,
        'Pr':-4.7837, 'F':-1.882, 'Sc':-6.3325,'H':-3.23975,
        'He': -0.0255,'Gd':-14.0834, 'Ca':-1.9995,'Si':-5.4234,
        'Ge':-4.6175,
#         Non-metal element
        'O':-4.927495, 'F':-1.9115,
       }

mu_mg = -1.5908
mu_x = eles[x] + fe_formula/dicts[x]
ratio = dicts['Mg']/dicts[x]

def get_slab_atoms():
    with open('POSCAR','r') as f:
        poscar = f.read().splitlines()
        if poscar[5].split()[0] == "Mg":
            slab_nMg,slab_nx = eval(poscar[6].split()[0]),eval(poscar[6].split()[1])
        else:
            slab_nMg,slab_nx = eval(poscar[6].split()[1]),eval(poscar[6].split()[0])
        return slab_nMg,slab_nx

def get_surface_area():
    with open('POSCAR','r') as f:
        poscar = f.read().splitlines()
        a = poscar[2].split()[0]
        b = poscar[3].split()[1]
        return eval(a)*eval(b)

def get_slab_energy():
    with open('OSZICAR','r') as f:
        oszicar = f.read().splitlines()
        return eval(oszicar[-1].split()[4])

def calc_surf_energy():
    count = 0
    area = get_surface_area()
    slab_energy = get_slab_energy()
    slab_nMg,slab_nx = get_slab_atoms()
    if slab_nMg/slab_nx == ratio:
        surf = slab_energy - slab_nMg/dicts['Mg']*en_formula
    elif slab_nMg/slab_nx > ratio:
        while slab_nMg/slab_nx > ratio:
            slab_nMg -= 1
            count += 1
        surf = (slab_energy - slab_nMg/dicts['Mg']*en_formula - count*mu_mg)
    else:
        while slab_nMg/slab_nx < ratio:
            slab_nx -= 1
            count += 1
        surf = (slab_energy - slab_nMg/dicts['Mg']*en_formula - count*mu_x)

    return (surf/2/area)*16000

# Main part
path = os.getcwd()
min_dir,min_energy = 'No such a dir',1000
print('-------------SURFACE ENERGY CALCULATING START------------------')
for d in os.listdir(path):
    full_path = path+'/'+d
    if os.path.isdir(full_path) and d[0]!='.':
        os.chdir(full_path)
        surf_energy = round(calc_surf_energy(),3)
        if surf_energy < min_energy:
            min_dir,min_energy = d, surf_energy
        print(f"{d} {surf_energy}mj/m2")
print('-------------MINIMUM SURFACE ENERGY AND ITS CORRESPONDING SURFACE------------------')
print(min_dir,min_energy)
print('-------------SURFACE ENERGY CALCULATING END------------------')
os.chdir(path)
