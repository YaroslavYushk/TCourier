# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4
from vl_sdv import quatd, rot3d, mat3d

from .utils import call_error
from .utils import save_data


def get_camera_data(pgroup_id, camera_id, frame_start, frame_end, frame_offset):
    keyframes_camera = {}
    #  Weird calculations because 3DE calс frames starting from 1, not 1001
    for frame in range(frame_start - frame_offset + 1,
                       frame_end - frame_offset + 1 + 1):
        quaternion = quatd(rot3d(mat3d(
            tde4.getPGroupRotation3D(pgroup_id, camera_id, frame))))
        keyframes_camera[frame + frame_offset - 1] = {
            'position': tde4.getPGroupPosition3D(pgroup_id, camera_id, frame),
            'quaternion': [quaternion[0],
                           quaternion[1][0],
                           quaternion[1][1],
                           quaternion[1][2]],
            'focal_length': tde4.getCameraFocalLength(camera_id, frame) * 10,
            # We multiply by 10 because convert cm to mm
        }
    return keyframes_camera


def execute():
    camera_id = tde4.getCurrentCamera()
    if camera_id is None:
        call_error("There is no active Camera")
    if tde4.getCameraType(camera_id) == 'REF_FRAME':
        call_error("Active camera is Reference camera")
    if tde4.getCameraNoFrames(camera_id) == 0:
        call_error("Active camera has 0 frames")

    pgroup_id = tde4.getCurrentPGroup()
    if pgroup_id is None:
        call_error("There is no Point Group")
    if tde4.getPGroupType(pgroup_id) != 'CAMERA':
        call_error('Current Point Group is not `Camera` type')

    camera_name = tde4.getCameraName(camera_id)
    camera_fps = tde4.getCameraFPS(camera_id)
    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = frame_offset
    frame_end = (tde4.getCameraSequenceAttr(camera_id)[1]
                 - tde4.getCameraSequenceAttr(camera_id)[0]
                 + frame_offset)
    keyframes_camera = get_camera_data(
        pgroup_id, camera_id, frame_start, frame_end, frame_offset)
    if keyframes_camera is not None:
        print('TCourier: Camera data obtained successfully')

    lens_id = tde4.getCameraLens(camera_id)
    if lens_id is None: call_error('There is no Lens')
    lens_fback_width = tde4.getLensFBackWidth(lens_id) * 10
    lens_fback_height = tde4.getLensFBackHeight(lens_id) * 10
    print('TCourier: Lens data obtained successfully')

    if tde4.getCameraZoomingFlag(camera_id) == 1:
        is_zoom = True
    else:
        is_zoom = False
    clipping_near = tde4.getNearClippingPlane()
    clipping_far = tde4.getFarClippingPlane()

    data_export = {
        'camera_name': camera_name,
        'filmback_width': lens_fback_width,
        'filmback_height': lens_fback_height,
        'frame_start': frame_start,
        'frame_end': frame_end,
        'fps': camera_fps,
        'is_zoom': is_zoom,
        'clipping_near': clipping_near,
        'clipping_far': clipping_far,
        'keyframes_camera': keyframes_camera,
    }

    save_data(data_export, 'camera')
    return True
