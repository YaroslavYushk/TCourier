import bpy

from .utils import load_data


class TCourier_Import_undistort(bpy.types.Operator):
    bl_idname = "tcourier.import_undistort"
    bl_label = "Import Undistorted footage"
    bl_description = "Load undistort and import data from JSON file"

    def execute(self, context):
        data_import = load_data('undistort')

        bpy.ops.image.open(
            filepath=data_import['filepath'],
            directory=data_import['directory'],
            files=[{"name": data_import['files_name']}],
            show_multiview=False, use_udim_detecting=False)
        undistort_seq = bpy.data.images[f'{data_import["files_name"]}']
        undistort_seq.source = 'SEQUENCE'

        scene = bpy.context.scene
        scene.render.fps = int(round(data_import['fps']))
        scene.render.resolution_x = (
            round(data_import['source_width'] * data_import['pixel_aspect']))
        scene.render.resolution_y = data_import['source_height']

        cam_name = data_import['camera_name']
        if cam_name not in bpy.data.cameras:
            self.report(
                {'ERROR'},
                message=("There is no appropriate Camera. "
                         "Try to import scene first"))
            return {'CANCELLED'}
        cam_data = bpy.data.cameras[cam_name]
        cam_data.show_background_images = True
        if len(cam_data.background_images) == 0:
            cam_data.background_images.new()

        bg_sequence = cam_data.background_images[0]
        bg_sequence.source = 'IMAGE'
        bg_sequence.image = undistort_seq
        bg_sequence.image_user.frame_duration = (
            data_import['frame_end'] - data_import['frame_start'] + 1)
        bg_sequence.image_user.frame_start = data_import['frame_start']
        bg_sequence.image_user.frame_offset = data_import['frame_start'] - 1
        bg_sequence.frame_method = 'STRETCH'
        bg_sequence.alpha = 1
        bg_sequence.display_depth = 'BACK'

        self.report({'INFO'}, message="Undistort data loaded successfully!")

        return {'FINISHED'}
