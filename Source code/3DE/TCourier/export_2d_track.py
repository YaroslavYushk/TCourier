# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4

from .utils import call_error
from .utils import save_data


def get_point_2d_coords(pgroup_id, point_id, camera_id, frames, frames_offset):
    keyframes = {}
    coords = tde4.getPointPosition2DBlock(
        pgroup_id, point_id, camera_id, 1, frames)
    for i in range(1, frames + 1):
        frame = i + frames_offset - 1
        keyframes[frame] = {}
        keyframes[frame]['x'] = coords[i - 1][0]
        keyframes[frame]['y'] = coords[i - 1][1]
        keyframes[frame]['is_valid'] = bool(
            tde4.isPointPos2DValid(pgroup_id, point_id, camera_id, i))
    return keyframes


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

    frames = tde4.getCameraNoFrames(camera_id)
    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = frame_offset
    frame_end = (tde4.getCameraSequenceAttr(camera_id)[1]
                 - tde4.getCameraSequenceAttr(camera_id)[0]
                 + frame_offset)
    source_width = tde4.getCameraImageWidth(camera_id)
    source_height = tde4.getCameraImageHeight(camera_id)
    points_list = tde4.getPointList(pgroup_id, 1)
    if len(points_list) == 0:
        points_list = tde4.getPointList(pgroup_id, 0)

    data_points = {}
    for point in points_list:
        point_name = tde4.getPointName(pgroup_id, point)
        data_points[point_name] = get_point_2d_coords(
            pgroup_id, point, camera_id, frames, frame_offset)

    data_export = {
        'source_width': source_width,
        'source_height': source_height,
        'frame_start': frame_start,
        'frame_end': frame_end,
        'data_points': data_points,
    }
    save_data(data_export, '2d_track')
    return True
