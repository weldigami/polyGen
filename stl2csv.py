from stl import mesh
import numpy as np
import csv

stl_folder = 'stl_test/'
file_name = 'cylinder.stl'
csv_folder = 'stl_test/'

mesh_data = mesh.Mesh.from_file(stl_folder + file_name)
verts = np.unique(mesh_data.vectors.reshape(-1, 3), axis=0).tolist()

edges = []
faces = []
for face in mesh_data.vectors:
    face_edges = []
    for i in range(3):
        v1 = face[i].tolist()
        v2 = face[(i + 1) % 3].tolist()
        fwd_vec = [verts.index(v1), verts.index(v2)]
        bwd_vec = fwd_vec[::-1]
        if fwd_vec not in edges or bwd_vec not in edges:
            edges.append(fwd_vec)
        try: face_edges.append(edges.index(fwd_vec))
        except: face_edges.append(edges.index(bwd_vec))
    faces.append(face_edges)
csv_conversion = [[len(verts), len(edges), len(faces)]] + verts + edges + faces

csv_path = f'{csv_folder + file_name}'.replace('.stl', '.csv')
with open(csv_path, 'w', newline='') as csv_file:
    csv.writer(csv_file).writerows(csv_conversion)
