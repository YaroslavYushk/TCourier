import bpy
import mathutils

from .utils import save_data


def get_camera_keyframes(cam_obj):
    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end
    keyframes_camera = {}

    for frame in range(frame_start, frame_end + 1):
        fcurves = cam_obj.animation_data.action.fcurves

        euler = mathutils.Euler((
            fcurves.find('rotation_euler', index=0).evaluate(frame),
            fcurves.find('rotation_euler', index=1).evaluate(frame),
            fcurves.find('rotation_euler', index=2).evaluate(frame)),
            'XYZ')
        quat_fix = mathutils.Quaternion(
            mathutils.Vector([1, -1, 0, 0])).normalized()
        quaternion = quat_fix @ euler.to_quaternion().normalized()

        keyframes_camera[str(frame)] = {
            'position': [fcurves.find('location', index=0).evaluate(frame),
                         fcurves.find('location', index=2).evaluate(frame),
                         -fcurves.find('location', index=1).evaluate(frame)],
            'quaternion': [quaternion[0],
                           quaternion[1],
                           quaternion[2],
                           quaternion[3]],
            'focal_length': cam_obj.data.lens,
        }
    return keyframes_camera


class TCourier_Export_camera(bpy.types.Operator):
    bl_idname = "tcourier.export_camera"
    bl_label = "Export Camera"
    bl_description = "Export camera data as JSON file"

    def execute(self, context):
        cam_obj = bpy.context.active_object
        if cam_obj.type != 'CAMERA':
            cam_obj = bpy.context.scene.camera
            if cam_obj is None:
                self.report({'ERROR'},
                            message=("Can't find Camera for export"))
                return {'CANCELLED'}

        is_zoom = False
        if cam_obj.animation_data and cam_obj.animation_data.action:
            for fcurve in cam_obj.animation_data.action.fcurves:
                if fcurve.data_path == "lens":
                    is_zoom = True

        keyframes_camera = get_camera_keyframes(cam_obj)

        data_export = {
            'camera_name': cam_obj.name,
            'filmback_width': cam_obj.data.sensor_width,
            'filmback_height': cam_obj.data.sensor_height,
            'frame_start': bpy.context.scene.frame_start,
            'frame_end': bpy.context.scene.frame_end,
            'fps': bpy.context.scene.render.fps,
            'is_zoom': is_zoom,
            'clipping_near': cam_obj.data.clip_start,
            'clipping_far': cam_obj.data.clip_end,
            'keyframes_camera': keyframes_camera,
        }

        save_data(data_export, 'camera')
        self.report({'INFO'},
                    message="Camera data saved successfully!")

        return {'FINISHED'}
