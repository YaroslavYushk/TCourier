# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4
from vl_sdv import mat3d, vec3d, rot3d, quatd

from .utils import call_error
from .utils import save_data


def get_pgroup_keyframes(
        pgroup_id, camera_id, frame_offset, frame_start, frame_end):

    pgroup_keyframes = {}
    for frame in range(frame_start - frame_offset + 1,
                       frame_end - frame_offset + 1 + 1):
        pgroup_rot = tde4.getPGroupRotation3D(pgroup_id, camera_id, frame)
        quaternion = quatd(rot3d(mat3d(pgroup_rot)))
        pgroup_keyframes[frame + frame_offset - 1] = {
            'position': tde4.getPGroupPosition3D(pgroup_id, camera_id, frame),
            'quaternion': [quaternion[0],
                           quaternion[1][0],
                           quaternion[1][1],
                           quaternion[1][2]],
            'scale': tde4.getPGroupScale3D(pgroup_id)
        }
    return pgroup_keyframes


def get_model_rotation_scale(pgroup_id, model_id):
    rot_scale_matrix = mat3d(
        tde4.get3DModelRotationScale3D(pgroup_id, model_id)
    ).trans()
    scale_values_from_matrix = vec3d(
        rot_scale_matrix[0].norm2(),
        rot_scale_matrix[1].norm2(),
        rot_scale_matrix[2].norm2())
    # scale_matrix = mat3d(
    #   scale_values_from_matrix[0], 0.0, 0.0,
    #   0.0, scale_values_from_matrix[1], 0.0,
    #   0.0, 0.0, scale_values_from_matrix[2])
    rotation_matrix = mat3d(
        rot_scale_matrix[0].unit(),
        rot_scale_matrix[1].unit(),
        rot_scale_matrix[2].unit()
    ).trans()
    return rotation_matrix, scale_values_from_matrix


def get_model_data(pgroup_id, model_id, camera_id, frame):
    model_name = tde4.get3DModelName(pgroup_id, model_id)
    model_pos = tde4.get3DModelPosition3D(
        pgroup_id, model_id, camera_id, frame)
    rot_matrix, scale_values = get_model_rotation_scale(pgroup_id, model_id)
    quaternion = quatd(rot3d(rot_matrix))
    model_vertices_amount = int(tde4.get3DModelNoVertices(pgroup_id, model_id))
    model_vertices = {}
    for vertex in range(0, model_vertices_amount):
        vertex_pos = tde4.get3DModelVertex(
            pgroup_id, model_id, vertex, camera_id, frame)
        model_vertices[f'{vertex}'] = vertex_pos
    model_faces_amount = int(tde4.get3DModelNoFaces(pgroup_id, model_id))
    model_faces = {}
    for face_index in range(0, model_faces_amount):
        face_points = tde4.get3DModelFaceVertexIndices(
            pgroup_id, model_id, face_index)
        model_faces[f'{face_index}'] = face_points

    model_filepath = tde4.get3DModelFilepath(pgroup_id, model_id)
    if model_filepath == '':
        model_filepath = None

    model_info = {
        'name': model_name,
        'position': model_pos,
        'quaternion': [quaternion[0],
                       quaternion[1][0],
                       quaternion[1][1],
                       quaternion[1][2]],
        'scale': [scale_values[0],
                  scale_values[1],
                  scale_values[2]],
        'model_filepath': model_filepath,
        'vertices': model_vertices,
        'faces': model_faces,
    }
    return (model_info)


def execute():
    camera_id = tde4.getCurrentCamera()
    if camera_id is None:
        call_error("There is no active Camera")
    if tde4.getCameraType(camera_id) == 'REF_FRAME':
        call_error("Active camera is Reference camera")
    if tde4.getCameraNoFrames(camera_id) == 0:
        call_error("Active camera has 0 frames")

    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = frame_offset
    frame_end = (tde4.getCameraSequenceAttr(camera_id)[1]
                 - tde4.getCameraSequenceAttr(camera_id)[0]
                 + frame_offset)

    pgroup_id = tde4.getCurrentPGroup()
    if pgroup_id == 0:
        call_error('There is no Point group')
    if tde4.getPGroupType(pgroup_id) != 'OBJECT':
        call_error('Current Point Group is not `Object` type')
    pgroup_name = tde4.getPGroupName(pgroup_id)

    data_models = {}
    model_list = tde4.get3DModelList(pgroup_id, 0)
    if len(model_list) > 0:
        for model_id in model_list:
            if tde4.get3DModelVisibleFlag(pgroup_id, model_id) == 0:
                continue
            data = get_model_data(
                pgroup_id, model_id, camera_id, frame_start - frame_offset + 1)
            data_models[f'{model_id}'] = data

    data_export = {
        'frame_start': frame_start,
        'frame_end': frame_end,
        'pgroup_name': pgroup_name,
        'pgroup_keyframes': get_pgroup_keyframes(
            pgroup_id, camera_id, frame_offset, frame_start, frame_end),
        'data_models': data_models,
    }

    save_data(data_export, 'obj_track')
    return True
