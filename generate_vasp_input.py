from pymatgen.core.structure import Structure
from pymatgen.io.vasp.sets import MPRelaxSet
import os
import shutil

struct = Structure.from_file('mgo_opt_100.cif')
formula = struct.composition.reduced_formula

root_dir = os.getcwd()
input_dir = os.path.join(root_dir,formula)

def generate_vasp_input(structure):
    vis=MPRelaxSet(struct)
    vis.write_input('.')
    os.remove('INCAR')
    shutil.copyfile(input_dir+'/POSCAR',input_dir+'/POSCAR_ori')
    with open ('/Users/wangyaowei/Desktop/codes/opt/INCAR_opt_slab') as f:
        incar = f.readlines()
    with open('INCAR','w') as f:
        for para in incar:
            f.write(para)

# Main part
os.mkdir(formula)
os.chdir(formula)
generate_vasp_input(struct)
os.chdir('../')
