# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import nuke

from libs.utils import call_error
from libs.utils import load_data


def apply_2d_track(node_tracker, data_import):
    data_points = data_import['data_points']
    source_width = data_import['source_width']
    source_height = data_import['source_height']

    script = (
        '''{ 1 31 %d }
{ { 5 1 20 enable e 1 }
{ 3 1 75 name name 1 }
{ 2 1 58 track_x track_x 1 }
{ 2 1 58 track_y track_y 1 }
{ 2 1 63 offset_x offset_x 1 }
{ 2 1 63 offset_y offset_y 1 }
{ 4 1 27 T T 1 }
{ 4 1 27 R R 1 }
{ 4 1 27 S S 1 }
{ 2 0 45 error error 1 }
{ 1 1 0 error_min error_min 1 }
{ 1 1 0 error_max error_max 1 }
{ 1 1 0 pattern_x pattern_x 1 }
{ 1 1 0 pattern_y pattern_y 1 }
{ 1 1 0 pattern_r pattern_r 1 }
{ 1 1 0 pattern_t pattern_t 1 }
{ 1 1 0 search_x search_x 1 }
{ 1 1 0 search_y search_y 1 }
{ 1 1 0 search_r search_r 1 }
{ 1 1 0 search_t search_t 1 }
{ 2 1 0 key_track key_track 1 }
{ 2 1 0 key_search_x key_search_x 1 }
{ 2 1 0 key_search_y key_search_y 1 }
{ 2 1 0 key_search_r key_search_r 1 }
{ 2 1 0 key_search_t key_search_t 1 }
{ 2 1 0 key_track_x key_track_x 1 }
{ 2 1 0 key_track_y key_track_y 1 }
{ 2 1 0 key_track_r key_track_r 1 }
{ 2 1 0 key_track_t key_track_t 1 }
{ 2 1 0 key_centre_offset_x key_centre_offset_x 1 }
{ 2 1 0 key_centre_offset_y key_centre_offset_y 1 }
}
{
''') % (len(data_points))

    for point_name in data_points:
        point = data_points[point_name]
        curve_x = 'curve '
        curve_y = 'curve '
        for frame in point:
            if point[frame]['is_valid']:
                curve_x = curve_x + f"x{frame} {point[frame]['x'] * source_width} "
                curve_y = curve_y + f"x{frame} {point[frame]['y'] * source_height} "
        script_point = (
            ' { {} "%s" '
            '{%s} {%s} {} {} 1 0 0 {} '
            '1 0 -32 -32 32 32 -22 -22 22 22 '
            '{} {}  {}  {}  {}  {}  {}  {}  {}  {}  {}   } \n'
        ) % (point_name, curve_x, curve_y)
        script = script + script_point
    script = script + '}'

    node_tracker['tracks'].fromScript(script)
    return


def execute():
    data_import = load_data('2d_track')
    if data_import is None:
        call_error("Data loading failed. The file may be missing or damaged.")
        return
    current_frame = nuke.frame()

    node_tracker = nuke.createNode("Tracker4")
    apply_2d_track(node_tracker, data_import)
    nuke.autoplaceSnap(node_tracker)
    nuke.frame(current_frame)
    return


if __name__ == "__main__":
    execute()
