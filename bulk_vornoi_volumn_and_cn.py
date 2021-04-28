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
from collections import Counter

'''
tol (float) – tolerance parameter for near-neighbor finding. Faces that are smaller than tol fraction of the largest face are not included in the tessellation. (default: 0).
targets (Element or list of Elements) – target element(s).
cutoff (float) – cutoff radius in Angstrom to look for near-neighbor atoms. Defaults to 13.0.
allow_pathological(病态的) (bool) – whether to allow infinite vertices in determination of Voronoi coordination.
weight (string) – available in get_voronoi_polyhedra)
extra_nn_info (bool) –
compute_adj_neighbors (bool) – adjacent. Turn off for faster performance
'''
cn = VoronoiNN(tol=0.5, targets=None, cutoff=13.0, allow_pathological=True, 
               weight='solid_angle', extra_nn_info=True, compute_adj_neighbors=False)

# 更改成当前文件下需要分析的文件
struct = Structure.from_file("mgf2.vasp")

'''
solid_angle - Solid angle subtended(对向的) by face
angle_normalized - Solid angle normalized such that the faces with the largest
area - Area of the facet
face_dist - Distance between site n and the facet
volume - Volume of Voronoi cell for this face
n_verts - Number of vertices(顶点数) on the facet
'''
print(f"结构的原子数为：{len(cn.get_all_nn_info(struct))}")
print(f"结构中第一个原子的配位数为：{len(cn.get_all_nn_info(struct)[1])}")

atom_index = []
ele = []
nn = []
x = []
y = []
z = []
vol = []
nn_ele = []

# 保存原子序数，元素符号，元素坐标和配位数
for i in range(len(struct)):
    print(i,str(struct[i]).split()[-1],str(struct[i])[:-3])
    atom_index.append(i)
    ele.append(str(struct[i]).split()[-1])
    if len(str(struct[i]).split()[-1]) == 2:
        position_info = str(struct[i])[:-3][1:-1]
        x.append(position_info.split()[0])
        y.append(position_info.split()[1])
        z.append(position_info.split()[2])
    else:
        position_info = str(struct[i])[:-3][1:]
        x.append(position_info.split()[0])
        y.append(position_info.split()[1])
        z.append(position_info.split()[2])

# 求和计算vornoi体积
for i in range(len(struct)):
    sum = 0.0
    dic = cn.get_all_voronoi_polyhedra(struct)[i]
    for key in dic.keys():
        sum = sum + dic[key]['volume']
    vol.append(sum)

nn_ele = []
# 求配位数中的元素种类
for i in range(len(struct)):
    elments = []
    for a in cn.get_all_voronoi_polyhedra(struct)[i]:
        info = cn.get_all_voronoi_polyhedra(struct)[i][a]['site']
        elment = str(info).split()[-1]
        elments.append(elment)

    nn_ele.append(dict(Counter(elments)))
    
c = {
    "atom_index":atom_index,
    'element':ele,
    'x':x,
    'y':y,
    'z':z,
    'vor_volumn':vol
}

df = pd.DataFrame(c)
df.to_csv('test.csv',index=None)
