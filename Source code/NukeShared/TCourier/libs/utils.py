import nuke
import json
import os
import tempfile


def call_error(message: str, title="Error"):
    from PySide2 import QtWidgets
    QtWidgets.QMessageBox.critical(
        None,
        title,
        str(message),
        QtWidgets.QMessageBox.Ok)


def clean_name(name: str) -> str:
    import re
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def load_data(data_type: str) -> dict:
    temp_dir = tempfile.gettempdir()
    if data_type == 'camera':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_camera.json')
    elif data_type == 'geo':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_geo.json')
    elif data_type == 'obj_track':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_obj_track.json')
    elif data_type == '2d_track':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_2d_track.json')
    else:
        call_error("Wrong data type")
        return
    try:
        with open(path_data, 'r') as file_data:
            data_import = json.load(file_data)
        print(f"TCourier: Data loaded successfully - '{data_type}'")
    except Exception:
        print(f"TCourier: An error occurred while loading data - '{data_type}'")
        return None
    return data_import


def save_data(data_export: dict, data_type: str):
    temp_dir = tempfile.gettempdir()
    os.makedirs(temp_dir + r'\TCourier', exist_ok=True)
    if data_type == 'camera':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_camera.json')
    elif data_type == 'geo':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_geo.json')
    elif data_type == 'obj_track':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_obj_track.json')
    elif data_type == '2d_track':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_2d_track.json')
    else:
        call_error("Wrong data type")
        return
    try:
        with open(path_data, 'w+') as file_data:
            json.dump(data_export, file_data, indent=4)
        os.chmod(path_data, 0o666)
        print(f"TCourier: Data saved successfully - '{data_type}'")
    except Exception:
        print(f"TCourier: An error occurred while saving data - '{data_type}'")


def check_space(target):
    tile_width = nuke.toNode("preferences")["TileWidth"].value()
    tile_height = nuke.toNode("preferences")["TileHeight"].value()

    all_nodes = nuke.allNodes()
    target_x = target.xpos() + target.screenWidth() / 2
    target_y = target.ypos() + target.screenHeight() / 2
    is_space_free = True
    for node in all_nodes:
        if node == target:
            continue
        node_x = node.xpos() + node.screenWidth() / 2
        node_y = node.ypos() + node.screenHeight() / 2
        if ((abs(target_x - node_x) < tile_width * 2)
                and (abs(target_y - node_y) < tile_height * 5)):
            is_space_free = False
            break
    return is_space_free


def find_free_space(target):
    nuke.autoplaceSnap(target)
    tile_width = nuke.toNode("preferences")["TileWidth"].value()
    while True:
        is_space_free = check_space(target)
        if is_space_free is False:
            target.setXpos(int(target.xpos() + tile_width))
        if is_space_free is True:
            break


def make_relative_path_absolute(filepath):
    from pathlib import Path
    relative_path = Path(filepath)
    proj_path = Path(nuke.script_directory())
    absolute_path = (proj_path / relative_path).resolve()
    return str(absolute_path)
