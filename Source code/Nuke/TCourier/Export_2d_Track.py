# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke
import re

from .libs.utils import call_error
from .libs.utils import save_data


def get_dimensions(node):
    width = nuke.root().format().width()
    height = nuke.root().format().height()
    return (width, height)


def turn_curves_into_keyframes(curve_x, curve_y, source_width, source_height):
    curve_list_x = curve_x[1:-1].split()
    curve_list_y = curve_y[1:-1].split()

    keyframes = {}
    frame_start = nuke.root().firstFrame()
    frame_end = nuke.root().lastFrame()
    for i in range(frame_start, frame_end + 1):
        keyframes[i] = {
            'x': -1,
            'y': -1,
            'is_valid': False,
        }

    frame = frame_start
    for i in range(len(curve_list_x)):
        if curve_list_x[i] == 'curve':
            continue
        elif curve_list_x[i].startswith('x'):
            frame = int(curve_list_x[i][1:])
        else:
            keyframes[frame]['x'] = float(curve_list_x[i]) / source_width
            keyframes[frame]['y'] = float(curve_list_y[i]) / source_height
            keyframes[frame]['is_valid'] = True
            frame = frame + 1
    return keyframes


def get_2d_tracks(node_tracker):
    source_width, source_height = get_dimensions(node_tracker)

    data_points = {}

    script_full = node_tracker['tracks'].toScript()
    script_lines = script_full.split('\n')
    tracks_amount = int(script_lines[0].split()[3])
    tracks_line_index = 34

    for track in range(tracks_amount):
        line = script_lines[tracks_line_index + track]

        track_name = re.search('\".*\"', line).group()
        if len(track_name) > 2:
            track_name = track_name[1:-1]
        else:
            track_name = str(track + 1)

        line_postname = line.split('"')[2]
        curves = re.findall(r'{curve [^{}]*}', line_postname)
        if len(curves) == 0:
            continue
        curve_x = curves[0]
        curve_y = curves[1]
        data_points[track_name] = turn_curves_into_keyframes(
            curve_x, curve_y, source_width, source_height)
    return data_points


def execute():
    frame_start = nuke.root().firstFrame()
    frame_end = nuke.root().lastFrame()

    selected_nodes = nuke.selectedNodes()
    if len(selected_nodes) == 0:
        call_error("No nodes selected. You should select Tracker node")
        return
    if len(selected_nodes) > 1:
        call_error("More than 1 node selected. You should select Tracker node")
        return
    node_tracker = selected_nodes[0]
    if node_tracker.Class() != "Tracker4":
        call_error("You should select Tracker node")
        return

    source_width, source_height = get_dimensions(node_tracker)

    data_points = get_2d_tracks(node_tracker)
    data_export = {
        'source_width': source_width,
        'source_height': source_height,
        'frame_start': frame_start,
        'frame_end': frame_end,
        'data_points': data_points,
    }

    save_data(data_export, '2d_track')
    return


if __name__ == "__main__":
    execute()
