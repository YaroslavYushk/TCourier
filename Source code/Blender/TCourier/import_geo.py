import bpy
import mathutils

from .utils import load_data


class TCourier_Import_geo(bpy.types.Operator):
    bl_idname = "tcourier.import_geo"
    bl_label = "Import Geo"
    bl_description = "Import geo data from JSON file"

    def execute(self, context):
        data_import = load_data('geo')
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

        data_models = data_import['data_models']
        for model_id in data_models:
            model_info = data_models[f'{model_id}']
            model_name = model_info['name']
            vertices = []
            for vertex in model_info['vertices']:
                vertices.append(model_info['vertices'][f'{vertex}'])
            faces = []
            for face in model_info['faces']:
                faces.append(model_info['faces'][f'{face}'])

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
                model_info['position'][0],
                -model_info['position'][2],
                model_info['position'][1])
            obj.scale = (
                model_info['scale'][0],
                model_info['scale'][1],
                model_info['scale'][2])
            vector = mathutils.Vector([
                model_info['quaternion'][0],
                model_info['quaternion'][1],
                model_info['quaternion'][2],
                model_info['quaternion'][3]])
            quat_fix = mathutils.Quaternion(
                mathutils.Vector([1, 1, 0, 0])).normalized()
            quat_fix_2 = mathutils.Quaternion(
                mathutils.Vector([1, -1, 0, 0])).normalized()
            quaternion = (quat_fix
                          @ mathutils.Quaternion(vector).normalized()
                          @ quat_fix_2)
            obj.rotation_mode = 'XYZ'
            obj.rotation_euler = (quaternion.to_euler('XYZ'))

        self.report({'INFO'},
                    message="3d models data loaded successfully!")

        return {'FINISHED'}
