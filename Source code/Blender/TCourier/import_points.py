import bpy

from .utils import load_data


def create_points(data_points, collection):
    for point_name in data_points:
        if point_name not in bpy.data.objects:
            point_obj = bpy.data.objects.new(f"{point_name}", None)
        else:
            point_obj = bpy.data.objects[f"{point_name}"]

        point_obj.empty_display_type = 'PLAIN_AXES'
        point_obj.location = [
            data_points[f'{point_name}']['position'][0],
            -data_points[f'{point_name}']['position'][2],
            data_points[f'{point_name}']['position'][1]]
        point_obj.empty_display_size = 2

        if point_name not in collection.objects:
            collection.objects.link(point_obj)


class TCourier_Import_points(bpy.types.Operator):
    bl_idname = "tcourier.import_points"
    bl_label = "Import Points"
    bl_description = "Import points data from JSON file"

    def execute(self, context):
        data_import = load_data('points')
        if data_import is None:
            self.report({'ERROR'},
                        message=("Data loading failed. "
                                 "The file may be missing or damaged."))
            return {'CANCELLED'}

        if "Points" not in bpy.data.collections:
            collection_proj = bpy.data.collections.new("Points")
        else:
            collection_proj = bpy.data.collections["Points"]
        if "Points" not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(collection_proj)

        data_points = data_import['data_points']
        create_points(data_points, collection_proj)

        self.report({'INFO'}, message="Points data loaded successfully!")

        return {'FINISHED'}
