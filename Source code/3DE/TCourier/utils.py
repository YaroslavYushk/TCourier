import tde4
import json
import os
import tempfile


def call_error(text: str):
    tde4.postQuestionRequester(
        "TCourier", text, "Ok")
    raise RuntimeError(text)


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
    elif data_type == 'undistort':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_undistort.json')
    elif data_type == 'points':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_points.json')
    elif data_type == '2d_track':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_2d_track.json')
    else:
        path_data = None
        call_error("Wrong data type")
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
    elif data_type == 'undistort':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_undistort.json')
    elif data_type == 'points':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_points.json')
    elif data_type == '2d_track':
        path_data = (temp_dir + r'\TCourier'
                     + r'\TCourier_data_2d_track.json')
    else:
        path_data = None
        call_error("Wrong data type")
    try:
        with open(path_data, 'w+') as file_data:
            json.dump(data_export, file_data, indent=4)
        os.chmod(path_data, 0o666)
        print(f"TCourier: Data saved successfully - '{data_type}'")
    except Exception:
        print(f"TCourier: An error occurred while saving data - '{data_type}'")
