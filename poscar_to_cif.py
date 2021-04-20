from pymatgen.io.cif import CifWriter
from pymatgen.core.structure import Structure
import os

structs = [i for i in os.listdir() if i[:6] == 'POSCAR']
for s in structs:
    CifWriter(Structure.from_file(s)).write_file(f'{s}.cif')
    os.remove(s)
