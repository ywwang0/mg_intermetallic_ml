from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.core.structure import Structure
import pandas as pd
from collections import Counter
import numpy as np
import shutil
import os

def get_struct():
    try:
        struct = Structure.from_file("POSCAR.orig")
    except:
        try:
            struct = Structure.from_file("POSCAR0")
        except:
            struct = Structure.from_file("POSCAR")
    return struct

def target_atom_number():
    struct = get_struct()
    for i in range(len(struct)):
        if str(struct[i]).split()[-1] == 'H':
            return i

root = os.getcwd()

total_dirs = [i for i in os.listdir() if os.path.isdir(os.path.join(os.getcwd(),i))]
for phase_dir in total_dirs:
    os.chdir(phase_dir)
    if 'H' in os.listdir():
        target_dir = 'H'
    else:
        target_dir = [i for i in os.listdir() if i[:5] =='block'][0]
    os.chdir(target_dir)
     
        
        
    dirs = [i for i in os.listdir() if (os.path.isdir(os.path.join(os.getcwd(),i)) and i[0] != '.')]
    cn = VoronoiNN(tol=0, targets=None, cutoff=13.0, allow_pathological=True,
                   weight='solid_angle', extra_nn_info=True, compute_adj_neighbors=True)
    nn = []
    vol = []
    nn_ele = []
    file_path = []
    min_atom_distance = []
    sum_atom_distance = []
    all_atom_distance = []
    for d in dirs:
        os.chdir(d)
        struct = get_struct()
        target_nn = cn.get_nn_info(struct,target_atom_number())
        nn.append(len(target_nn))
        target_vornoi = cn.get_voronoi_polyhedra(struct,target_atom_number())
        sum = 0.0
        elments = []
        atom_distance = []
        for key in target_vornoi.keys():
            sum = sum + target_vornoi[key]['volume']
            info = target_vornoi[key]['site']
            elment = str(info).split()[-1]
            elments.append(elment)
            atom_distance.append(target_vornoi[key]['face_dist']*2)
        vol.append(sum)
        nn_ele.append(dict(Counter(elments)))
        min_atom_distance.append(min(atom_distance))
        sum_atom_distance.append(np.sum(atom_distance))
        all_atom_distance.append(atom_distance)

        file_path.append(d.split('-')[-2])
        os.chdir('../')

    c={
        'dir':file_path,
        'nn':nn,
        'nn_ele':nn_ele,
        'vor_volumn':vol,
        'min_atom_distance':min_atom_distance,
        'sum_atom_distance':sum_atom_distance,
        'all_atom_distance':all_atom_distance

    }

    df = pd.DataFrame(c)
    df = df.sort_values(by="dir",ascending=True)
    f = (os.getcwd().split('/')[-2])
    df.to_csv(f+'.csv',index=None)
    shutil.move(f+'.csv','../../../csv_results')
    print(f+'  calculated over!')
    os.chdir(root)
