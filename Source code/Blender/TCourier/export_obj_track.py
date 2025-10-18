import bpy
import mathutils

from .utils import save_data


def get_pgroup_keyframes(pgroup_null, frame_start, frame_end):
    pgroup_keyframes = {}
    rotation_mode = pgroup_null.rotation_mode
    scene_scale_fix = 0.01 / bpy.context.scene.unit_settings.scale_length

    for frame in range(frame_start, frame_end + 1):
        fcurves = pgroup_null.animation_data.action.fcurves

        quat_fix = mathutils.Quaternion(
            mathutils.Vector([1, -1, 0, 0])).normalized()
        quat_fix_2 = mathutils.Quaternion(
            mathutils.Vector([1, 1, 0, 0])).normalized()

        if rotation_mode in ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']:
            euler = mathutils.Euler((
                fcurves.find('rotation_euler', index=0).evaluate(frame),
                fcurves.find('rotation_euler', index=1).evaluate(frame),
                fcurves.find('rotation_euler', index=2).evaluate(frame)),
                'XYZ')
            quaternion = (quat_fix
                          @ euler.to_quaternion().normalized()
                          @ quat_fix_2)
        elif rotation_mode == 'QUATERNION':
            quat_orig = mathutils.Quaternion((
                fcurves.find('rotation_quaternion', index=0).evaluate(frame),
                fcurves.find('rotation_quaternion', index=1).evaluate(frame),
                fcurves.find('rotation_quaternion', index=2).evaluate(frame),
                fcurves.find('rotation_quaternion', index=3).evaluate(frame)))
            quaternion = (quat_fix
                          @ quat_orig.normalized()
                          @ quat_fix_2)
        else:
            return None

        pgroup_keyframes[str(frame)] = {
            'position': [
                fcurves.find('location', index=0).evaluate(frame) / scene_scale_fix,
                fcurves.find('location', index=2).evaluate(frame) / scene_scale_fix,
                -fcurves.find('location', index=1).evaluate(frame) / scene_scale_fix],
            'quaternion': [quaternion[0],
                           quaternion[1],
                           quaternion[2],
                           quaternion[3]],
            'scale': fcurves.find('scale', index=0).evaluate(frame),
        }
    return pgroup_keyframes


def get_obj_data(obj_list):
    data_obj_export = {}
    scene_scale_fix = 0.01 / bpy.context.scene.unit_settings.scale_length

    for obj in obj_list:
        quat_fix = mathutils.Quaternion(
            mathutils.Vector([1, -1, 0, 0])).normalized()
        quat_fix_2 = mathutils.Quaternion(
            mathutils.Vector([1, 1, 0, 0])).normalized()
        quaternion = (quat_fix
                      @ obj.rotation_euler.to_quaternion().normalized()
                      @ quat_fix_2)

        mesh = obj.data

        mesh.transform(
            mathutils.Quaternion(
                mathutils.Vector([1, -1, 0, 0])
            ).normalized().to_matrix().to_4x4())

        mesh_vertices = {}
        for vertex in mesh.vertices:
            index = vertex.index
            mesh_vertices[f'{index}'] = [vertex.co[0] / scene_scale_fix,
                                         vertex.co[1] / scene_scale_fix,
                                         vertex.co[2] / scene_scale_fix]
        mesh_faces = {}
        for face in mesh.polygons:
            index = face.index
            vert_list = face.vertices
            mesh_faces[f'{index}'] = []
            for vert in vert_list:
                mesh_faces[f'{index}'].append(vert)

        mesh.transform(
            mathutils.Quaternion(
                mathutils.Vector([1, 1, 0, 0])
            ).normalized().to_matrix().to_4x4())

        model_info = {
            'name': obj.name,
            'position': [obj.location[0] / scene_scale_fix,
                         obj.location[2] / scene_scale_fix,
                         -obj.location[1] / scene_scale_fix],
            'quaternion': [quaternion[0],
                           quaternion[1],
                           quaternion[2],
                           quaternion[3]],
            'scale': [obj.scale[0],
                      obj.scale[2],
                      obj.scale[1]],
            'model_filepath': None,
            'vertices': mesh_vertices,
            'faces': mesh_faces,
        }
        data_obj_export[f'{obj.name}'] = model_info

    return data_obj_export


class TCourier_Export_obj_track(bpy.types.Operator):
    bl_idname = "tcourier.export_obj_track"
    bl_label = "Export Object track"
    bl_description = "Export object track data as JSON file"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) == 0:
            self.report({'ERROR'},
                        message=("There are no selected objects for export"))
            return {'CANCELLED'}
        if len(selected_objects) > 1:
            self.report({'ERROR'},
                        message=("Too many objects selected"))
            return {'CANCELLED'}

        pgroup_null = None
        if bpy.context.active_object.type == 'EMPTY':
            pgroup_null = bpy.context.active_object
        elif bpy.context.active_object.type == 'MESH':
            if bpy.context.active_object.parent.type != 'EMPTY':
                self.report({'ERROR'}, message=(
                    "Something went wrong. "
                    "Probably, you selected wrong object. "
                    "Select the 'Empty' object or one of it's child"))
            else:
                pgroup_null = bpy.context.active_object.parent

        obj_list = pgroup_null.children

        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end

        pgroup_keyframes = get_pgroup_keyframes(
            pgroup_null, frame_start, frame_end)
        if pgroup_keyframes is None:
            self.report({'ERROR'},
                        message=("Something went wrong"))
            return {'CANCELLED'}

        data_export = {
            'frame_start': frame_start,
            'frame_end': frame_end,
            'pgroup_name': pgroup_null.name,
            'pgroup_keyframes': pgroup_keyframes,
            'data_models': get_obj_data(obj_list),
        }

        save_data(data_export, 'obj_track')
        self.report({'INFO'},
                    message="Object track data saved successfully!")

        return {'FINISHED'}
