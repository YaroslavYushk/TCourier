# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke

from libs.utils import call_error
from libs.utils import save_data
from libs.utils import make_relative_path_absolute

from libs.matrix_operations import multiply_matrices_4x4
from libs.matrix_operations import build_matrix_4x4_from_list
from libs.matrix_operations import get_translation_from_matrix_4x4
from libs.matrix_operations import get_scale_from_matrix_4x4
from libs.matrix_operations import get_rotation_matrix_from_matrix_4x4
from libs.matrix_operations import get_quaternion_from_rotation_matrix_4x4


def get_mesh_data_from_file(file_path):
    vertices = {}
    vert_index = 0
    faces = {}
    face_index = 0
    with open(file_path, 'r') as f:
        file_data = f.read()
    for line in file_data.splitlines():
        if line.startswith("#"):
            continue
        if line.startswith("v "):
            vertices[str(vert_index)] = [float(line.split()[1]),
                                         float(line.split()[2]),
                                         float(line.split()[3])]
            vert_index = vert_index + 1
        if line.startswith("f "):
            faces[str(face_index)] = []
            for a in line.split():
                if a == 'f':
                    continue
                faces[str(face_index)].append(int(a.split('/')[0]) - 1)
            face_index = face_index + 1
    return vertices, faces


def get_model_data(node_ReadGeo):
    model_filepath = nuke.filename(node_ReadGeo)
    if model_filepath.startswith("."):
        model_filepath = make_relative_path_absolute(model_filepath)

    if model_filepath.endswith(".obj"):
        vertices, faces = get_mesh_data_from_file(model_filepath)
    else:
        call_error("One of your models is not in .obj format and was not exported")
        return None

    geo_matrix = node_ReadGeo["matrix"].getValueAt(nuke.frame())
    geo_matrix = build_matrix_4x4_from_list(geo_matrix)

    for node_child in node_ReadGeo.dependent():
        if ((node_child.input(0) == node_ReadGeo)
                and (node_child.Class() == 'TransformGeo')):
            child_matrix = node_child["matrix"].getValueAt(nuke.frame())
            child_matrix = build_matrix_4x4_from_list(child_matrix)
            geo_matrix = multiply_matrices_4x4(geo_matrix, child_matrix)
            break

    position = get_translation_from_matrix_4x4(geo_matrix)
    scale = get_scale_from_matrix_4x4(geo_matrix)
    rotation_mat = get_rotation_matrix_from_matrix_4x4(geo_matrix)
    quaternion = get_quaternion_from_rotation_matrix_4x4(rotation_mat)

    data_model = {
        'name': node_ReadGeo.name(),
        'position': position,
        'quaternion': quaternion,
        'scale': scale,
        'model_filepath': model_filepath,
        'vertices': vertices,
        'faces': faces,
    }
    return data_model


def execute():
    selected_nodes = nuke.selectedNodes()
    if len(selected_nodes) == 0:
        call_error("There are no selected nodes")
        return
    geo_nodes = []
    for node in selected_nodes:
        if node.Class() in ["ReadGeo", "ReadGeo2"]:
            geo_nodes.append(node)

    data_models = {}
    for node in geo_nodes:
        data = get_model_data(node)
        if data is not None:
            data_models[str(node.name())] = data
    if data_models == {}:
        call_error("No data were exported")
        return

    data_export = {
        'data_models': data_models,
    }

    save_data(data_export, 'geo')
    return


if __name__ == "__main__":
    execute()
