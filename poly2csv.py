import os
import numpy as np
import csv

data_folder = 'poly_texts/'
csv_folder = 'poly_csvs/'

def convert(text):
    text.pop(0)  # delete the header
    consts = []
    verts = []
    edges = []
    faces = []
    done_with_consts = False
    for line in text:
        line = line.strip()
        line = line.replace(' ', '')

        if not line:
            if len(consts) != 0:
                done_with_consts = True

        elif line[0] == 'C':
            if done_with_consts: 
                continue  # ignores duplicate definitions
            consts.append(float(line.split('=')[1]))

        elif line[0] == 'V':
            clist = line.split('=')[1].strip('()').split(',')
            coords = []
            for c in clist:
                if '-C' in c:
                    coords.append(-consts[int(c[2:])])
                elif 'C' in c:
                    coords.append(consts[int(c[1:])])
                else:
                    coords.append(float(c))
            verts.append(coords)
        
        elif line[0] == '{':
            v_names = line.strip('{').strip('}').split(',')
            face_edges = []
            for v1, v2 in zip(v_names, np.roll(v_names, -1)):
                fwd_vec = [int(v1), int(v2)]
                bwd_vec = [int(v2), int(v1)]
                if fwd_vec not in edges and bwd_vec not in edges:
                    edges.append(fwd_vec)
                    face_edges.append(len(edges) - 1)
                else:
                    try: face_edges.append(edges.index(fwd_vec))
                    except: face_edges.append(edges.index(bwd_vec))
            faces.append(face_edges)
    return [[len(verts), len(edges), len(faces)]] + verts + edges + faces

data_dict = {}
for category in os.listdir(data_folder):
    category_path = os.path.join(data_folder, category)
    if os.path.isdir(category_path):
        poly_names = [polyname for polyname in os.listdir(category_path) if polyname.endswith(".txt")]
        data_dict[category] = poly_names

for folder, files in data_dict.items():
    folder_read_path = data_folder + folder
    folder_write_path = csv_folder + folder
    if not os.path.exists(folder_write_path):
        os.makedirs(folder_write_path)

    for file in files:
        file_name = f'{folder_read_path}/{file}'
        csv_name = f'{folder_write_path}/{file}'.replace('.txt', '.csv')
        with open(file_name, 'r') as file:
            csv_conversion = convert(file.readlines())
            with open(csv_name, 'w', newline='') as new_file:
                csv.writer(new_file).writerows(csv_conversion)
