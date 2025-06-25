# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke

from .libs.utils import call_error
from .libs.utils import save_data

from .libs.matrix_operations import build_matrix_4x4_from_list
from .libs.matrix_operations import get_rotation_matrix_from_matrix_4x4
from .libs.matrix_operations import get_quaternion_from_rotation_matrix_4x4


def get_camera_keyframes(camera):
    root = nuke.root()
    frame_start = root['first_frame'].value()
    frame_end = root['last_frame'].value()
    curent_frame = nuke.frame()

    data_camera = {}

    for frame in range(int(frame_start), int(frame_end) + 1):
        wm = camera["world_matrix"].getValueAt(frame)
        matrix = build_matrix_4x4_from_list(wm)
        rot_matrix = get_rotation_matrix_from_matrix_4x4(matrix)
        quaternion = get_quaternion_from_rotation_matrix_4x4(rot_matrix)

        data_camera[frame] = {
            'position': [wm[3], wm[7], wm[11]],
            'quaternion': [quaternion[0],
                           quaternion[1],
                           quaternion[2],
                           quaternion[3]],
            'focal_length': camera["focal"].valueAt(frame),
        }

    nuke.frame(curent_frame)
    return data_camera


def execute():
    selected_nodes = nuke.selectedNodes()
    if len(selected_nodes) > 1:
        call_error("More than 1 node selected")
        return
    if len(selected_nodes) == 0:
        call_error("There are no selected nodes")
        return
    camera = selected_nodes[0]
    if camera.Class() not in ["Camera", "Camera2", "Camera3", "Camera4"]:
        call_error("Selected node is not a `Camera` class")
        return

    keyframes_camera = get_camera_keyframes(camera)

    is_zoom = camera["focal"].isAnimated()

    data_export = {
        'camera_name': camera.name(),
        'filmback_width': camera["haperture"].value(),
        'filmback_height': camera["vaperture"].value(),
        'frame_start': nuke.root().firstFrame(),
        'frame_end': nuke.root().lastFrame(),
        'fps': nuke.root().fps(),
        'is_zoom': is_zoom,
        'clipping_near': camera["near"].value(),
        'clipping_far': camera["far"].value(),
        'keyframes_camera': keyframes_camera,
    }

    save_data(data_export, 'camera')
    return


if __name__ == "__main__":
    execute()
