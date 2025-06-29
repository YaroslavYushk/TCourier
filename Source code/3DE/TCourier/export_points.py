# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4


from .utils import call_error
from .utils import save_data


def get_points_data(pgroup_id):
    points_list = tde4.getPointList(pgroup_id, 1)
    if len(points_list) == 0:
        points_list = tde4.getPointList(pgroup_id, 0)
    if len(points_list) == 0:
        return None

    data_points = {}
    for point_id in points_list:
        point_name = tde4.getPointName(pgroup_id, point_id)
        point_pos = tde4.getPointCalcPosition3D(pgroup_id, point_id)
        if (tde4.getPointCalcMode(pgroup_id, point_id) != 'CALC_OFF'
           and tde4.getPointSurveyMode(pgroup_id, point_id) != 'SURVEY_LINEUP'):
            data_points[f'{point_name}'] = {
                'position': point_pos,
            }
    print('TCourier: Points data obtained successfully')
    return data_points


def execute():
    camera_id = tde4.getCurrentCamera()
    if camera_id is None: call_error('There is no active Camera')
    if tde4.getCameraType(camera_id) == 'REF_FRAME':
        call_error('Active camera is Reference camera')

    pgroup_id = tde4.getCurrentPGroup()
    if pgroup_id == 0: call_error('There is no Point group')
    if tde4.getPGroupType(pgroup_id) != 'CAMERA':
        call_error('Current Point Group is not `Camera` type')

    data_points = get_points_data(pgroup_id)
    if data_points is None: call_error('There are no points')

    data_export = {
        'data_points': data_points,
    }
    save_data(data_export, 'points')
    return True
