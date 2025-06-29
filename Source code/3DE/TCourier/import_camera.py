# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4
from vl_sdv import mat3d, quatd, rot3d

from .utils import call_error
from .utils import load_data


def apply_camera_keyframes(pgroup_id, camera_id, keyframes_camera, is_zoom):
    frame_offset = tde4.getCameraFrameOffset(camera_id)

    if is_zoom is False:
        tde4.setCameraZoomingFlag(camera_id, 0)
        key = list(keyframes_camera.keys())[0]
        tde4.setCameraFocalLength(
            camera_id,
            int(key) - frame_offset + 1,
            keyframes_camera[str(key)]['focal_length'] / 10)  # mm to cm

    for frame in keyframes_camera:
        tde4.setPGroupPosition3D(
            pgroup_id,
            camera_id,
            int(frame) - frame_offset + 1,
            keyframes_camera[str(frame)]['position'])

        quaternion_values = keyframes_camera[str(frame)]['quaternion']
        quaternion = quatd(quaternion_values[0],
                           quaternion_values[1],
                           quaternion_values[2],
                           quaternion_values[3])
        rot_mat = mat3d(rot3d(quaternion.unit()))
        rotation_matrix = [[rot_mat[0][0], rot_mat[0][1], rot_mat[0][2]],
                           [rot_mat[1][0], rot_mat[1][1], rot_mat[1][2]],
                           [rot_mat[2][0], rot_mat[2][1], rot_mat[2][2]]]
        tde4.setPGroupRotation3D(
            pgroup_id, camera_id, int(frame) - frame_offset + 1, rotation_matrix)

        if is_zoom is True:
            tde4.setCameraZoomingFlag(camera_id, 1)
            tde4.setCameraFocalLength(
                camera_id,
                int(frame) - frame_offset + 1,
                keyframes_camera[str(frame)]['focal_length'] / 10)  # mm to cm
    tde4.copyPGroupEditCurvesToFilteredCurves(pgroup_id, camera_id)
    return


def execute():
    data_import = load_data('camera')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")
        return

    pgroup_list = tde4.getPGroupList()
    pgroup_id = None
    for pgroup_check in pgroup_list:
        if tde4.getPGroupType(pgroup_check) == 'CAMERA':
            pgroup_id = pgroup_check
    if pgroup_id is None:
        call_error("There is no Point group woth `Camera` type")

    camera_list = tde4.getCameraList()
    if len(camera_list) == 0:
        call_error("You have no cameras")
    camera_id = tde4.getCurrentCamera()
    if tde4.getCameraType(camera_id) != 'SEQUENCE':
        call_error('Your current camera is not `Sequence` type')
    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = frame_offset
    frame_end = (tde4.getCameraSequenceAttr(camera_id)[1]
                 - tde4.getCameraSequenceAttr(camera_id)[0]
                 + frame_offset)
    if ((frame_start != data_import['frame_start'])
            or (frame_end != data_import['frame_end'])):
        call_error('Start or End frame range mismatch!')

    keyframes_camera = data_import['keyframes_camera']
    is_zoom = data_import['is_zoom']
    apply_camera_keyframes(pgroup_id, camera_id, keyframes_camera, is_zoom)

    tde4.setCameraFPS(camera_id, float(data_import['fps']))
    tde4.setNearClippingPlane(data_import['clipping_near'])
    tde4.setFarClippingPlane(data_import['clipping_far'])

    return True
