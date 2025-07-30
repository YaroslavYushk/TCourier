# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke

from .libs.utils import call_error
from .libs.utils import save_data
from .libs.utils import make_relative_path_absolute

from .libs.matrix_operations import build_matrix_4x4_from_list
from .libs.matrix_operations import get_translation_from_matrix_4x4
from .libs.matrix_operations import get_scale_from_matrix_4x4
from .libs.matrix_operations import get_rotation_matrix_from_matrix_4x4
from .libs.matrix_operations import get_quaternion_from_rotation_matrix_4x4


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
    geo_matrix = node_ReadGeo["matrix"].getValueAt(nuke.frame())
    geo_matrix = build_matrix_4x4_from_list(geo_matrix)

    position = get_translation_from_matrix_4x4(geo_matrix)
    scale = get_scale_from_matrix_4x4(geo_matrix)
    rotation_mat = get_rotation_matrix_from_matrix_4x4(geo_matrix)
    quaternion = get_quaternion_from_rotation_matrix_4x4(rotation_mat)

    model_filepath = nuke.filename(node_ReadGeo)
    if model_filepath.startswith("."):
        model_filepath = make_relative_path_absolute(model_filepath)

    vertices, faces = get_mesh_data_from_file(model_filepath)

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


def get_obj_track_keyframes(node_transformGeo):
    frame_start = int(nuke.root()['first_frame'].value())
    frame_end = int(nuke.root()['last_frame'].value())

    data_keyframes = {}
    warning_scale_diff = False
    for frame in range(frame_start, frame_end + 1):
        transform_matrix = node_transformGeo["matrix"].getValueAt(frame)
        transform_matrix = build_matrix_4x4_from_list(transform_matrix)
        position = get_translation_from_matrix_4x4(transform_matrix)
        scale = get_scale_from_matrix_4x4(transform_matrix)
        if ((abs(scale[0] - scale[1]) / scale[0] > 0.001)
                or (abs(scale[0] - scale[2]) / scale[0] > 0.001)):
            warning_scale_diff = True
        rotation_mat = get_rotation_matrix_from_matrix_4x4(transform_matrix)
        quaternion = get_quaternion_from_rotation_matrix_4x4(rotation_mat)

        data_keyframes[str(frame)] = {
            'position': position,
            'quaternion': quaternion,
            'scale': scale[0],
        }
    if warning_scale_diff is True:
        call_error("Warning: Axis have a scale difference, "
                   "it will not be transferred")
    return data_keyframes


def execute():
    selected_nodes = nuke.selectedNodes()
    if len(selected_nodes) == 0:
        call_error("There are no selected nodes")
        return
    if len(selected_nodes) > 1:
        call_error("Please select TransformGeo node only")
        return

    node_transformGeo = selected_nodes[0]
    if node_transformGeo.Class() != "TransformGeo":
        call_error("Please select TransformGeo node")
        return

    node_readGeo = None
    data_models = {}
    if node_transformGeo.input(0):
        if node_transformGeo.input(0).Class() in ["ReadGeo", "ReadGeo2"]:
            node_readGeo = node_transformGeo.input(0)
            data = get_model_data(node_readGeo)
            data_models[str(node_readGeo.name())] = data

    if node_readGeo is not None:
        pgroup_name = node_readGeo.name()
    else:
        pgroup_name = "object_track"

    data_export = {
        'frame_start': int(nuke.root()['first_frame'].value()),
        'frame_end': int(nuke.root()['last_frame'].value()),
        'pgroup_name': pgroup_name,
        'pgroup_keyframes': get_obj_track_keyframes(node_transformGeo),
        'data_models': data_models,
    }

    save_data(data_export, 'obj_track')
    return


if __name__ == "__main__":
    execute()
