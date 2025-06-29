import bpy
import mathutils

from .utils import load_data
from .utils import center_timeline


def apply_camera_keyframes(cam_obj, keyframes_camera, is_zoom):
    cam_data = cam_obj.data

    if is_zoom is False:
        key = list(keyframes_camera.keys())[0]
        cam_data.lens = keyframes_camera[str(key)]['focal_length']

    for frame in keyframes_camera:
        cam_obj.location = (keyframes_camera[f'{frame}']['position'][0],
                            -keyframes_camera[f'{frame}']['position'][2],
                            keyframes_camera[f'{frame}']['position'][1])
        cam_obj.keyframe_insert(data_path='location', frame=int(frame))

        vector = mathutils.Vector([
            keyframes_camera[f'{frame}']['quaternion'][0],
            keyframes_camera[f'{frame}']['quaternion'][1],
            keyframes_camera[f'{frame}']['quaternion'][2],
            keyframes_camera[f'{frame}']['quaternion'][3]])
        quat_fix = mathutils.Quaternion(
            mathutils.Vector([1, 1, 0, 0])).normalized()
        quaternion = quat_fix @ mathutils.Quaternion(vector).normalized()

        cam_obj.rotation_euler = (quaternion.to_euler('XYZ'))
        cam_obj.keyframe_insert(data_path='rotation_euler', frame=int(frame))
        if is_zoom is True:
            cam_data.lens = keyframes_camera[f'{frame}']['focal_length']
            cam_data.keyframe_insert(data_path='lens', frame=int(frame))


class TCourier_Import_camera(bpy.types.Operator):
    bl_idname = "tcourier.import_camera"
    bl_label = "Import Camera"
    bl_description = "Import camera data from JSON file"

    def execute(self, context):
        data_import = load_data('camera')
        if data_import is None:
            self.report({'ERROR'},
                        message=("Data loading failed. "
                                 "The file may be missing or damaged."))
            return {'CANCELLED'}

        # region Collection
        if "Scene_Import" not in bpy.data.collections:
            collection_proj = bpy.data.collections.new("Scene_Import")
        else:
            collection_proj = bpy.data.collections["Scene_Import"]
        if "Scene_Import" not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(collection_proj)

        # region Scene
        scene = bpy.context.scene
        scene.frame_start = data_import['frame_start']
        scene.frame_end = data_import['frame_end']
        if not (scene.frame_start
                <= scene.frame_current
                <= scene.frame_end):
            scene.frame_current = data_import['frame_start']
        scene.render.fps = int(round(data_import['fps']))
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = 0.01
        bpy.context.space_data.clip_start = 10
        bpy.context.space_data.clip_end = 100000

        center_timeline()

        # region Camera
        cam_name = data_import['camera_name']
        if cam_name not in bpy.data.cameras:
            cam_data = bpy.data.cameras.new(cam_name)
        else:
            cam_data = bpy.data.cameras[cam_name]
        cam_data.display_size = 50
        cam_data.sensor_fit = 'HORIZONTAL'
        cam_data.sensor_height = data_import['filmback_height']
        cam_data.sensor_width = data_import['filmback_width']
        cam_data.clip_start = data_import['clipping_near']
        cam_data.clip_end = data_import['clipping_far']

        if cam_name not in bpy.data.objects:
            cam_obj = bpy.data.objects.new(cam_name, cam_data)
        else:
            cam_obj = bpy.data.objects[cam_name]
        if cam_name not in collection_proj.objects:
            collection_proj.objects.link(cam_obj)

        keyframes_camera = data_import['keyframes_camera']
        is_zoom = data_import['is_zoom']
        cam_obj.rotation_mode = 'XYZ'
        apply_camera_keyframes(cam_obj, keyframes_camera, is_zoom)

        self.report({'INFO'},
                    message="Camera data loaded successfully!")

        return {'FINISHED'}
