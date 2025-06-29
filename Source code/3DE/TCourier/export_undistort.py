# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/


import tde4
import os
from pathlib import Path
import re

from .utils import call_error
from .utils import save_data


def prepareImagePath(path, frame):
    path = path.replace("\\", "/")
    if '#' not in path:
        return path
    n = path.count('#')  # count '#' symbols
    i = path.index('#')  # look for first '#' symbol

    return f'{path[:i]}{frame:0{n}d}{path[i+n:]}'  # change '####' to 0001


def execute(scale=1):
    # Variables
    camera_id = tde4.getCurrentCamera()
    if camera_id is None: call_error('There is no active Camera')
    if tde4.getCameraType(camera_id) == 'REF_FRAME':
        call_error('Active camera is Reference camera')
    camera_name = tde4.getCameraName(camera_id)
    camera_fps = tde4.getCameraFPS(camera_id)
    frame_offset = tde4.getCameraFrameOffset(camera_id)
    frame_start = frame_offset
    frame_end = (tde4.getCameraSequenceAttr(camera_id)[1]
                 - tde4.getCameraSequenceAttr(camera_id)[0]
                 + frame_offset)
    lens_pixel_aspect = tde4.getLensPixelAspect(tde4.getCameraLens(camera_id))

    if tde4.getCameraPath(camera_id) == '':
        call_error('There is no Footage in camera')
    source_width = int(tde4.getCameraImageWidth(camera_id))
    source_height = int(tde4.getCameraImageHeight(camera_id))
    if scale == 1080:
        scale = 1080 / source_height
    cache_width = round(source_width * scale)
    cache_height = round(source_height * scale)

    # Pathes and names
    path_project_file = Path(tde4.getProjectPath())
    if path_project_file is None: call_error('Save your project first')
    path_project_folder = path_project_file.parent

    project_name_full = path_project_file.stem
    project_ver = re.search(r'_v[0-9][0-9][0-9].*', str(project_name_full))
    if project_ver is None:
        project_ver = '_v001'
    else:
        project_ver = project_ver.group()
    project_name = (
        str(project_name_full)
        .split(project_ver)[0]
        .replace('_track', ''))

    path_cache_folder = path_project_folder / 'undistort'
    path_cache_pattern = (
        path_cache_folder / f'{camera_name}_undistort{project_ver}_####.jpg')

    #
    #  Render cache sequence
    #

    # apply render settings

    if tde4.get3DEVersion() == '3DEqualizer4 Release 8.0':
        tde4.setRenderCacheFlags(
            0,  # show_fov
            0,  # show_fov_crop_mask
            0,  # show_2d_points
            0,  # show_3d_models
            0,  # show_geo_lines
            0,  # show_horizon
            0,  # render_mblur
            0,  # remove_rs
            1,  # undistort
            0,  # foreground_rendering
            0,  # anaglyph_rendering
            0,  # show_3d_points
            0,  # show_tracked_3d_points_only
        )
    else:  # assuming '3DEqualizer4 Release 7.1'
        tde4.setRenderCacheFlags(
            0,  # show_fov
            0,  # show_fov_crop_mask
            0,  # show_2d_points
            0,  # show_3d_models
            0,  # show_geo_lines
            0,  # show_horizon
            0,  # render_mblur
            0,  # remove_rs
            1,  # undistort
            0,  # foreground_rendering
            0,  # anaglyph_rendering
        )

    # start rendering cache
    tde4.postProgressRequesterAndContinue(
        'Save out Rendered Frames...',
        '...',
        frame_end - frame_start + 1,  # max progress
        'Cancel')
    i = 0  # i - progress bar
    for f in range(frame_start, frame_end + 1):
        i = i + 1
        cont = tde4.updateProgressRequester(i, f'Saving Frame {f}...')
        if not cont: break

        filename = prepareImagePath(str(path_cache_pattern), f)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        ok = tde4.saveRenderCacheFrame(
            camera_id,
            f - frame_offset + 1,  # frame
            filename,
            'IMAGE_JPEG',
            scale,  # Image scale
            0,  # overscan
            0,  # reapply_distortion
            0,  # offset_x
            0,  # offset_y
            cache_width,
            cache_height)
        if not ok:
            ret = tde4.postQuestionRequester(
                'Save out Rendered Frames...',
                f'Error, can\'t save file: \"{filename}\".',
                'Continue',
                'Cancel')
            if ret == 2: break
    tde4.unpostProgressRequester()

    #
    # Post-render
    #

    frame_start_formatted = str(frame_start).zfill(4)
    files_name = f'{camera_name}_undistort{project_ver}_{frame_start_formatted}.jpg'
    filepath = str(path_cache_folder / files_name)

    data_undistort = {
        'camera_name': f'{camera_name}',
        'filepath': filepath,
        'directory': str(path_cache_folder),
        'files_name': files_name,
        'frame_start': frame_start,
        'frame_end': frame_end,
        'fps': camera_fps,
        'pixel_aspect': lens_pixel_aspect,
        'source_width': source_width,
        'source_height': source_height,
    }
    save_data(data_undistort, 'undistort')
    return True
