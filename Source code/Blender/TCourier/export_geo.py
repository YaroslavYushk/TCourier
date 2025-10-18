import bpy
import mathutils

from .utils import save_data


class TCourier_Export_geo(bpy.types.Operator):
    bl_idname = "tcourier.export_geo"
    bl_label = "Export Geo"
    bl_description = "Export geo data as JSON file"

    def execute(self, context):
        scene_scale_fix = 0.01 / bpy.context.scene.unit_settings.scale_length
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) == 0:
            self.report({'ERROR'},
                        message=("There are no selected objects for export"))
            return {'CANCELLED'}

        data_models = {}
        for obj in selected_objects:
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
            data_models[f'{obj.name}'] = model_info

        data_export = {
            'data_models': data_models,
        }

        save_data(data_export, 'geo')

        self.report({'INFO'},
                    message="3d models data saved successfully!")

        return {'FINISHED'}
