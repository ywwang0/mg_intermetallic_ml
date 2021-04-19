'''
******************************************************************
coding: utf-8
Author: Yaowei Wang
E-mail: yaowei.wang@sjtu.edu.cn
Function: calcualte vornoi volumn and coordinate number for a structure
Input: pymatgen structure class
Output: csv file containing all necessary dictionary(c dictionary)
History: 
04/18/2021: Created

To be chieve:
None
*******************************************************************
'''

from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.core.structure import Structure
import pandas as pd

'''
tol (float) – tolerance parameter for near-neighbor finding. Faces that are smaller than tol fraction of the largest face are not included in the tessellation. (default: 0).
targets (Element or list of Elements) – target element(s).
cutoff (float) – cutoff radius in Angstrom to look for near-neighbor atoms. Defaults to 13.0.
allow_pathological(病态的) (bool) – whether to allow infinite vertices in determination of Voronoi coordination.
weight (string) – available in get_voronoi_polyhedra)
extra_nn_info (bool) –
compute_adj_neighbors (bool) – adjacent. Turn off for faster performance
'''
cn = VoronoiNN(tol=0, targets=None, cutoff=13.0, allow_pathological=True, 
               weight='solid_angle', extra_nn_info=True, compute_adj_neighbors=True)

# 更改成当前文件下需要分析的文件
struct = Structure.from_file("Al-111-0001.cif")

atom_index = []
ele = []
nn = []
pos = []
vol = []

# 保存原子序数，元素符号，元素坐标和配位数
for i in range(len(struct)):
    print(i,str(struct[i]).split()[-1],str(struct[i])[:-3],len(cn.get_all_nn_info(struct)[i]))
    atom_index.append(i)
    ele.append(str(struct[i]).split()[-1])
    if len(str(struct[i]).split()[-1]) == 2:
        pos.append(str(struct[i])[:-3][1:-1])
    else:
        pos.append(str(struct[i])[:-3][1:])
    nn.append(len(cn.get_all_nn_info(struct)[i]))

# 求和计算vornoi体积
for i in range(len(struct)):
    sum = 0.0
    dic = cn.get_all_voronoi_polyhedra(struct)[i]
    for key in dic.keys():
        sum = sum + dic[key]['volume']
    vol.append(sum)

c = {
    "atom_index":atom_index,
    'ele':ele,
    'nn':nn,
    'vor_volumn':vol,
    'position':pos
}

df = pd.DataFrame(c)
df.to_csv('vornoi_output.csv',index=None)
