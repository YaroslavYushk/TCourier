import bpy
import mathutils

from .utils import load_data


def apply_keyframes_import(data_import, null_data):
    data_keyframes = data_import['pgroup_keyframes']
    for frame in range(data_import['frame_start'], data_import['frame_end'] + 1):
        null_data.location = (data_keyframes[f'{frame}']['position'][0],
                              -data_keyframes[f'{frame}']['position'][2],
                              data_keyframes[f'{frame}']['position'][1])
        null_data.keyframe_insert(data_path='location', frame=frame)

        vector = mathutils.Vector([
            data_keyframes[f'{frame}']['quaternion'][0],
            data_keyframes[f'{frame}']['quaternion'][1],
            data_keyframes[f'{frame}']['quaternion'][2],
            data_keyframes[f'{frame}']['quaternion'][3]])
        quat_fix = mathutils.Quaternion(
            mathutils.Vector([1, 1, 0, 0])).normalized()
        quat_fix_2 = mathutils.Quaternion(
            mathutils.Vector([1, -1, 0, 0])).normalized()
        quaternion = (quat_fix
                      @ mathutils.Quaternion(vector).normalized()
                      @ quat_fix_2)
        null_data.rotation_euler = (quaternion.to_euler('XYZ'))
        null_data.keyframe_insert(data_path='rotation_euler', frame=frame)

        null_data.scale = (
            data_keyframes[f'{frame}']['scale'],
            data_keyframes[f'{frame}']['scale'],
            data_keyframes[f'{frame}']['scale'])
        null_data.keyframe_insert(data_path='scale', frame=frame)

    return


def build_geo_import(data_import, null_data):
    collection_proj = bpy.data.collections["Scene_Import"]
    for model_id in data_import:
        data_model = data_import[f'{model_id}']

        model_name = data_model['name']
        vertices = []
        for vertex in data_model['vertices']:
            vertices.append(data_model['vertices'][f'{vertex}'])
        faces = []
        for face in data_model['faces']:
            faces.append(data_model['faces'][f'{face}'])

        mesh = bpy.data.meshes.new(model_id)
        obj = bpy.data.objects.new(model_name, mesh)
        collection_proj.objects.link(obj)

        mesh.clear_geometry()
        mesh.from_pydata(vertices, [], faces)
        mesh.transform(
            mathutils.Quaternion(
                mathutils.Vector([1, 1, 0, 0])
            ).normalized().to_matrix().to_4x4())
        mesh.validate()
        mesh.update()

        obj.location = (
            data_model['position'][0],
            -data_model['position'][2],
            data_model['position'][1])
        obj.scale = (
            data_model['scale'][0],
            data_model['scale'][1],
            data_model['scale'][2])
        vector = mathutils.Vector([
            data_model['quaternion'][0],
            data_model['quaternion'][1],
            data_model['quaternion'][2],
            data_model['quaternion'][3]])
        quat_fix = mathutils.Quaternion(
            mathutils.Vector([1, 1, 0, 0])).normalized()
        quat_fix_2 = mathutils.Quaternion(
            mathutils.Vector([1, -1, 0, 0])).normalized()
        quaternion = (quat_fix
                      @ mathutils.Quaternion(vector).normalized()
                      @ quat_fix_2)
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler = (quaternion.to_euler('XYZ'))
        obj.parent = null_data

    return


class TCourier_Import_obj_track(bpy.types.Operator):
    bl_idname = "tcourier.import_obj_track"
    bl_label = "Import Object track"
    bl_description = "Import object track data from JSON file"

    def execute(self, context):
        data_import = load_data('obj_track')

        if "Scene_Import" not in bpy.data.collections:
            collection_proj = bpy.data.collections.new("Scene_Import")
        else:
            collection_proj = bpy.data.collections["Scene_Import"]
        if "Scene_Import" not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(collection_proj)

        null_name = data_import['pgroup_name']
        if null_name not in bpy.data.objects:
            bpy.data.objects.new(f"{null_name}", None)
        if bpy.data.objects[null_name].type != 'EMPTY':
            self.report({'ERROR'},
                        message=(f'Something went wrong. Object "{null_name}" '
                                 'expected to be an Empty object type. '
                                 'Change the name or make another import'))
            return {'CANCELLED'}

        null_data = bpy.data.objects[null_name]
        null_data.empty_display_type = 'PLAIN_AXES'
        null_data.empty_display_size = 10
        null_data.rotation_mode = 'XYZ'

        if null_name not in collection_proj.objects:
            collection_proj.objects.link(null_data)

        apply_keyframes_import(data_import, null_data)
        build_geo_import(data_import['data_models'], null_data)

        return {'FINISHED'}


class TCourier_Duplicate(bpy.types.Operator):
    bl_idname = "tcourier.duplicate"
    bl_label = "Linked copy to World Origin"
    bl_description = ("Create linked copy at the world origin for easier "
                      "modeling. (You can just delete the copy after you "
                      "don't need it anymore)")

    def execute(self, context):
        if bpy.context.active_object is None:
            self.report({'ERROR'}, message="Select an object first")

        obj = bpy.context.active_object
        obj_copy = bpy.data.objects.new(obj.name, obj.data)
        for user in obj.users_collection:
            user.objects.link(obj_copy)
        obj_copy.rotation_euler = mathutils.Euler(
            mathutils.Quaternion(
                mathutils.Vector([1, 0, 0, 0]))
            .to_euler('XYZ'))

        return {'FINISHED'}
