# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke
from pathlib import Path
from math import pi
import re

from libs.utils import call_error
from libs.utils import clean_name
from libs.utils import load_data
from libs.utils import find_free_space


def create_obj_from_json(data_model):
    proj_folder = nuke.script_directory()
    if not proj_folder:
        call_error("Save project first")
        return
    Path(proj_folder).mkdir(exist_ok=True)
    (Path(proj_folder) / 'geo').mkdir(exist_ok=True)
    proj_name = str(Path(nuke.root().name()).stem)
    proj_name = clean_name(proj_name)
    proj_name = re.sub(r'_v[0-9][0-9][0-9].*', '', proj_name)  # cut version
    proj_name = re.sub(r'_scene', '', proj_name)  # cut suffix

    is_file_exist = True
    num = 0
    clean_model_name = clean_name(data_model['name'])
    while is_file_exist:
        filename = f"{proj_name}_geo_{clean_model_name}_v001_{num:02d}.obj"
        path_file = Path(proj_folder) / 'geo' / filename
        if path_file.exists():
            num = num + 1
        else:
            is_file_exist = False

    with path_file.open("w") as file:
        file.write(f"o {data_model['name']}\n")
        for v in data_model['vertices']:
            vert = data_model['vertices'][v]
            file.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
        for f in data_model['faces']:
            face = data_model['faces'][f]
            file.write("f " + " ".join(str(v + 1) for v in face) + "\n")

    print("TCourier: .obj file was created successfully from model data")
    return path_file


def execute():
    data_import = load_data('geo')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")
        return

    tile_height = nuke.toNode("preferences")["TileHeight"].value()
    tile_width = nuke.toNode("preferences")["TileWidth"].value()

    selected_nodes = nuke.selectedNodes()
    if (len(selected_nodes) == 1 and selected_nodes[0].Class() == 'Scene'):
        node_scene = selected_nodes[0]
        node_scene.setSelected(False)
    else:
        node_scene = None
    if node_scene is not None:
        last_node_xpos = node_scene.xpos()
        last_node_ypos = node_scene.ypos() - tile_height * 8
    else:
        last_node_xpos = None
        last_node_ypos = None

    data_models = data_import['data_models']
    for m in data_models:
        model = data_models[m]
        if ((model['model_filepath'] is not None)
                and (Path(model['model_filepath']).exists())):
            path_obj = model['model_filepath']
        else:
            path_obj = create_obj_from_json(model)
        if path_obj is None:
            call_error("No obj data or can't create obj file")
            return

        # region ReadGeo
        node_readGeo = nuke.createNode("ReadGeo2")
        node_readGeo.setName(f"Geo_{clean_name(m)}_01")
        node_readGeo["file"].setValue(str(path_obj).replace('\\', '/'))
        if last_node_xpos is not None:
            node_readGeo.setXpos(int(
                last_node_xpos
                + tile_width * 2
                + node_readGeo.screenWidth()))
        if last_node_ypos is not None:
            node_readGeo.setYpos(int(last_node_ypos))
        find_free_space(node_readGeo)
        last_node_xpos = node_readGeo.xpos()
        last_node_ypos = node_readGeo.ypos()

        # region Wireframe
        wframe = nuke.createNode("Wireframe")
        wframe.setXpos(node_readGeo.xpos())
        wframe.setYpos(int(
            node_readGeo.ypos()
            - tile_height * 4
            - node_readGeo.screenHeight() / 2
            - wframe.screenHeight() / 2))
        nuke.autoplaceSnap(wframe)
        node_readGeo.setInput(0, wframe)

        # region node_transformGeo
        node_transformGeo = nuke.createNode("TransformGeo")
        node_transformGeo.setXpos(node_readGeo.xpos())
        node_transformGeo.setYpos(int(
            node_readGeo.ypos()
            + tile_height * 4
            + node_readGeo.screenHeight() / 2
            + node_transformGeo.screenHeight() / 2))
        nuke.autoplaceSnap(node_transformGeo)
        node_transformGeo.setInput(0, node_readGeo)
        # position
        node_transformGeo["translate"].setValue(data_models[m]['position'][0], 0)
        node_transformGeo["translate"].setValue(data_models[m]['position'][1], 1)
        node_transformGeo["translate"].setValue(data_models[m]['position'][2], 2)
        # rotation
        node_transformGeo["rot_order"].setValue('ZXY')

        if (((nuke.NUKE_VERSION_MAJOR == 13) and (nuke.NUKE_VERSION_MINOR < 2))
                or (nuke.NUKE_VERSION_MAJOR <= 12)):
            quaternion = nuke.math.Quaternion(
                data_models[m]['quaternion'][0],
                data_models[m]['quaternion'][1],
                data_models[m]['quaternion'][2],
                data_models[m]['quaternion'][3])
        else:
            quaternion = nuke.nukemath.Quaternion(
                data_models[m]['quaternion'][0],
                data_models[m]['quaternion'][1],
                data_models[m]['quaternion'][2],
                data_models[m]['quaternion'][3])

        matrix = quaternion.matrix()
        euler = matrix.rotationsZXY()
        node_transformGeo["rotate"].setValue(euler[0] * 180 / pi, 0)
        node_transformGeo["rotate"].setValue(euler[1] * 180 / pi, 1)
        node_transformGeo["rotate"].setValue(euler[2] * 180 / pi, 2)
        # scale
        node_transformGeo["scaling"].setValue(data_models[m]['scale'][0], 0)
        node_transformGeo["scaling"].setValue(data_models[m]['scale'][1], 1)
        node_transformGeo["scaling"].setValue(data_models[m]['scale'][2], 2)

        if node_scene is not None:
            node_scene.connectInput(0, node_transformGeo)


if __name__ == "__main__":
    execute()
