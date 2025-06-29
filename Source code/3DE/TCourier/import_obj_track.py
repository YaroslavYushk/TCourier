# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4
from vl_sdv import mat3d, quatd, rot3d

from .utils import load_data
from .utils import call_error


def apply_pgroup_keyframes(
        data_keyframes, pgroup_id, camera_id,
        frame_offset, frame_start, frame_end):
    for frame in range(frame_start, frame_end + 1):
        position = data_keyframes[str(frame)]['position']
        scale = data_keyframes[str(frame)]['scale']
        quaternion = quatd(data_keyframes[str(frame)]['quaternion'][0],
                           data_keyframes[str(frame)]['quaternion'][1],
                           data_keyframes[str(frame)]['quaternion'][2],
                           data_keyframes[str(frame)]['quaternion'][3])
        rot_mat = mat3d(rot3d(quaternion))
        rotation_matrix = [[rot_mat[0][0], rot_mat[0][1], rot_mat[0][2]],
                           [rot_mat[1][0], rot_mat[1][1], rot_mat[1][2]],
                           [rot_mat[2][0], rot_mat[2][1], rot_mat[2][2]]]

        rotation_conv, position_conv = (
            tde4.convertObjectPGroupTransformationWorldTo3DE(
                camera_id, frame - frame_offset + 1,
                rotation_matrix, position, scale))

        tde4.setPGroupPosition3D(
            pgroup_id, camera_id, frame - frame_offset + 1, position_conv)
        tde4.setPGroupRotation3D(
            pgroup_id, camera_id, frame - frame_offset + 1, rotation_conv)
        tde4.setPGroupScale3D(pgroup_id, scale)
    tde4.copyPGroupEditCurvesToFilteredCurves(pgroup_id, camera_id)

    return


def build_model(model_data, pgroup_id, model_id):
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
    data_import = load_data('obj_track')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")
        return

    pgroup_id = tde4.createPGroup('OBJECT')
    tde4.setPGroupName(pgroup_id, data_import['pgroup_name'])

    camera_id = tde4.getCurrentCamera()
    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = data_import['frame_start']
    frame_end = data_import['frame_end']

    apply_pgroup_keyframes(
        data_import['pgroup_keyframes'], pgroup_id, camera_id,
        frame_offset, frame_start, frame_end)

    for model_name in data_import['data_models']:
        model_id = tde4.create3DModel(pgroup_id, 0)
        tde4.removeAll3DModelGeometryData(pgroup_id, model_id)
        build_model(
            data_import['data_models'][model_name], pgroup_id, model_id)

    return True
