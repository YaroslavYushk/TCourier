import bpy
import json
import os


def load_data(data_type: str) -> dict:
    if data_type == 'camera':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_camera.json')
    elif data_type == 'geo':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_geo.json')
    elif data_type == 'obj_track':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_obj_track.json')
    elif data_type == 'undistort':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_undistort.json')
    elif data_type == 'points':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_points.json')
    else:
        path_data = None
    try:
        with open(path_data, 'r') as file_data:
            data_import = json.load(file_data)
        print(f"TCourier: Data loaded successfully - '{data_type}'")
    except Exception:
        print(f"TCourier: Something went wrong "
              f"when was trying to load data - '{data_type}'")
    return data_import


def save_data(data_export: dict, data_type: str):
    os.makedirs(os.getenv('TEMP') + r'\TCourier', exist_ok=True)
    if data_type == 'camera':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_camera.json')
    elif data_type == 'geo':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_geo.json')
    elif data_type == 'obj_track':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_obj_track.json')
    elif data_type == 'undistort':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_undistort.json')
    elif data_type == 'points':
        path_data = (os.getenv('TEMP') + r'\TCourier'
                     + r'\TCourier_data_points.json')
    else:
        path_data = None
    try:
        with open(path_data, 'w+') as file_data:
            json.dump(data_export, file_data, indent=4)
        os.chmod(path_data, 0o666)
        print(f"TCourier: Data saved successfully - '{data_type}'")
    except Exception:
        print(f"TCourier: Something went wrong "
              f"when was trying to save  data - '{data_type}'")


def center_timeline():
    for area in bpy.context.window.screen.areas:
        if area.ui_type == 'TIMELINE':
            for region in area.regions:
                if region.type == 'WINDOW':
                    with bpy.context.temp_override(
                            screen=bpy.context.window.screen,
                            area=area,
                            region=region):
                        bpy.ops.action.view_all()
