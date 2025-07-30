# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4

from .utils import call_error
from .utils import load_data


def apply_2d_point_coords(data_import, point_name, pgroup_id, camera_id,
                          frame_start, frame_end, frame_offset):
    data_point = data_import['data_points'][point_name]
    point_id = tde4.createPoint(pgroup_id)
    tde4.setPointName(pgroup_id, point_id, point_name)
    frames = frame_end - frame_start + 1
    curve = []
    for frame in range(1, frames + 1):
        curve.append([-1, -1])
    for frame in data_point:
        if data_point[frame]['is_valid']:
            curve[int(frame) - frame_offset] = [
                data_point[frame]['x'], data_point[frame]['y']]
    tde4.setPointPosition2DBlock(pgroup_id, point_id, camera_id, 1, curve)
    return


def execute():
    data_import = load_data('2d_track')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")

    camera_id = tde4.getCurrentCamera()
    pgroup_id = tde4.getCurrentPGroup()
    if (camera_id is None) or (pgroup_id is None):
        call_error("There is no Current Camera or Point Group")
    if tde4.getCameraType(camera_id) == 'REF_FRAME':
        call_error("Active camera has `Reference` type")

    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = frame_offset
    frame_end = (tde4.getCameraSequenceAttr(camera_id)[1]
                 - tde4.getCameraSequenceAttr(camera_id)[0]
                 + frame_offset)
    if ((frame_start != data_import['frame_start']) or
            (frame_end != data_import['frame_end'])):
        call_error("Frame range mismatch")

    set_id = tde4.createSet(pgroup_id)
    tde4.setSetName(pgroup_id, set_id, 'Imported')

    for point_name in data_import['data_points']:
        apply_2d_point_coords(data_import, point_name, pgroup_id, camera_id,
                              frame_start, frame_end, frame_offset)

    return True
