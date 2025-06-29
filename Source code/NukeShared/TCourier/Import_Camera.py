# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke
from math import pi

from libs.utils import clean_name
from libs.utils import load_data
from libs.utils import find_free_space
from libs.utils import call_error


def apply_camera_keyframes(node_camera, keyframes_camera, is_zoom):
    if is_zoom is True:
        node_camera["focal"].setAnimated()
    if is_zoom is False:
        key = list(keyframes_camera.keys())[0]
        node_camera["focal"].setValue(keyframes_camera[str(key)]['focal_length'])

    node_camera["translate"].setAnimated()
    node_camera["rotate"].setAnimated()
    node_camera["rot_order"].setValue('ZXY')

    for frame in keyframes_camera:
        if is_zoom is True:
            node_camera["focal"].setValueAt(
                keyframes_camera[str(frame)]['focal_length'], int(frame))

        node_camera["translate"].setValueAt(
            keyframes_camera[str(frame)]['position'][0], int(frame), 0)
        node_camera["translate"].setValueAt(
            keyframes_camera[str(frame)]['position'][1], int(frame), 1)
        node_camera["translate"].setValueAt(
            keyframes_camera[str(frame)]['position'][2], int(frame), 2)
        quaternion = nuke.nukemath.Quaternion(
            keyframes_camera[str(frame)]['quaternion'][0],
            keyframes_camera[str(frame)]['quaternion'][1],
            keyframes_camera[str(frame)]['quaternion'][2],
            keyframes_camera[str(frame)]['quaternion'][3])
        matrix = quaternion.matrix()
        euler = matrix.rotationsZXY()
        node_camera["rotate"].setValueAt(euler[0] * 180 / pi, int(frame), 0)
        node_camera["rotate"].setValueAt(euler[1] * 180 / pi, int(frame), 1)
        node_camera["rotate"].setValueAt(euler[2] * 180 / pi, int(frame), 2)


def execute():
    data_import = load_data('camera')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")
        return
    root = nuke.root()

    root['fps'].setValue(data_import['fps'])
    root['first_frame'].setValue(data_import['frame_start'])
    root['last_frame'].setValue(data_import['frame_end'])

    node_scene = None
    selected_nodes = nuke.selectedNodes()
    if (len(selected_nodes) == 1 and selected_nodes[0].Class() == 'Scene'):
        node_scene = selected_nodes[0]
        node_scene.setSelected(False)

    node_camera = nuke.toNode(f"Camera_{clean_name(data_import['camera_name'])}")
    if node_camera is None:
        node_camera = nuke.createNode("Camera2")
        node_camera.setName(f"Camera_{clean_name(data_import['camera_name'])}")
    if node_scene:
        node_scene.connectInput(0, node_camera)
        tile_height = nuke.toNode("preferences")["TileHeight"].value()
        node_camera.setXpos(node_scene.xpos())
        node_camera.setYpos(int(
            node_scene.ypos()
            - tile_height * 6
            - node_camera.screenHeight() / 2
            - node_scene.screenHeight() / 2))
    find_free_space(node_camera)
    node_camera["haperture"].setValue(data_import['filmback_width'])
    node_camera["vaperture"].setValue(data_import['filmback_height'])
    node_camera["near"].setValue(data_import['clipping_near'])
    node_camera["far"].setValue(data_import['clipping_far'])

    keyframes_camera = data_import['keyframes_camera']
    is_zoom = data_import['is_zoom']
    apply_camera_keyframes(node_camera, keyframes_camera, is_zoom)


if __name__ == "__main__":
    execute()
