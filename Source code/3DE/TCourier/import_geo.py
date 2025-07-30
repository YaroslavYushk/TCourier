# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4
from vl_sdv import mat3d, quatd, rot3d

from .utils import call_error
from .utils import load_data


def import_model(pgroup_id, model_id, model_data):
    vertices = model_data['vertices']
    for vertex_index in vertices:
        tde4.add3DModelVertex(pgroup_id, model_id, vertices[vertex_index])

    faces = model_data['faces']
    for face_index in faces:
        vert_list = faces[face_index]
        tde4.add3DModelFace(pgroup_id, model_id, vert_list)
        vert_list.append(vert_list[0])
        tde4.add3DModelLine(pgroup_id, model_id, vert_list)

    tde4.set3DModelPosition3D(
        pgroup_id, model_id, model_data['position'])

    scale_values = model_data['scale']
    scale_matrix = mat3d(
        scale_values[0], 0.0, 0.0,
        0.0, scale_values[1], 0.0,
        0.0, 0.0, scale_values[2])

    quaternion_values = model_data['quaternion']
    quaternion = quatd(quaternion_values[0],
                       quaternion_values[1],
                       quaternion_values[2],
                       quaternion_values[3])
    rotation_matrix = mat3d(rot3d(quaternion))

    r_s_m = rotation_matrix * scale_matrix
    rot_scale_matrix = [[r_s_m[0][0], r_s_m[0][1], r_s_m[0][2]],
                        [r_s_m[1][0], r_s_m[1][1], r_s_m[1][2]],
                        [r_s_m[2][0], r_s_m[2][1], r_s_m[2][2]]]

    tde4.set3DModelRotationScale3D(pgroup_id, model_id, rot_scale_matrix)

    tde4.set3DModelName(pgroup_id, model_id, model_data['name'])
    tde4.set3DModelSurveyFlag(pgroup_id, model_id, 0)
    tde4.set3DModelVisibleFlag(pgroup_id, model_id, 1)
    tde4.set3DModelRenderingFlags(pgroup_id, model_id, 0, 1, 0)
    return


def execute():
    data_import = load_data('geo')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")

    pgroup_id = tde4.getCurrentPGroup()
    if pgroup_id is None:
        call_error('There is no Point group')
    if tde4.getPGroupType(pgroup_id) != 'CAMERA':
        call_error('Current Point Group is not `Camera` type')

    for model_name in data_import['data_models']:
        model_id = tde4.create3DModel(pgroup_id, 0)
        tde4.removeAll3DModelGeometryData(pgroup_id, model_id)
        import_model(pgroup_id, model_id, data_import['data_models'][model_name])
    return True
