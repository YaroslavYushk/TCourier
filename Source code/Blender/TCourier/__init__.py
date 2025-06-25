import bpy
import bpy.utils.previews
import os

from . import import_camera
from . import import_points
from . import import_geo
from . import import_undistort
from . import import_obj_track
from . import export_camera
from . import export_geo
from . import export_obj_track


icon = None


def load_preview_icon():
    path = os.path.dirname(__file__) + r"\TCourier.png"
    if "3DE" not in icon:
        if os.path.exists(path):
            icon.load("3DE", path, "IMAGE")
        else: return 0
    return icon["3DE"].icon_id


class TCOURIER_PT_main_panel(bpy.types.Panel):
    bl_label = "TCourier"
    bl_idname = "TCOURIER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'INSTANCED'}

    def draw(self, context):
        self.layout.label(text="Import:")
        self.layout.operator("tcourier.import_camera", icon='CAMERA_DATA')
        self.layout.operator("tcourier.import_points", icon='EMPTY_AXIS')
        self.layout.operator("tcourier.import_geo", icon='CUBE')
        self.layout.operator("tcourier.import_undistort", icon='IMAGE_PLANE')
        self.layout.separator()
        self.layout.operator("tcourier.import_obj_track", icon='GP_SELECT_POINTS')
        self.layout.operator("tcourier.duplicate", icon='NONE')
        self.layout.separator()
        self.layout.label(text="Export:")
        self.layout.operator("tcourier.export_camera", icon='CAMERA_DATA')
        self.layout.operator("tcourier.export_geo", icon='CUBE')
        self.layout.operator("tcourier.export_obj_track",
                             icon='OUTLINER_DATA_GREASEPENCIL')


def draw_TCourier_popover(self, context):
    self.layout.popover("TCOURIER_PT_main_panel",
                        icon_value=load_preview_icon())


class TCOURIER_MT_menu_import(bpy.types.Menu):
    bl_label = "TCourier"
    bl_idname = "TCOURIER_MT_menu_import"

    def draw(self, context):
        self.layout.operator("tcourier.import_camera", icon='CAMERA_DATA')
        self.layout.operator("tcourier.import_points", icon='EMPTY_AXIS')
        self.layout.operator("tcourier.import_geo", icon='CUBE')
        self.layout.operator("tcourier.import_undistort", icon='IMAGE_PLANE')
        self.layout.separator()
        self.layout.operator("tcourier.import_obj_track", icon='GP_SELECT_POINTS')


def draw_TCourier_menu_import(self, context):
    self.layout.menu("TCOURIER_MT_menu_import", text="TCourier")


class TCOURIER_MT_menu_export(bpy.types.Menu):
    bl_label = "TCourier"
    bl_idname = "TCOURIER_MT_menu_export"

    def draw(self, context):
        self.layout.operator("tcourier.export_camera", icon='CAMERA_DATA')
        self.layout.operator("tcourier.export_geo", icon='CUBE')
        self.layout.operator("tcourier.export_obj_track",
                             icon='OUTLINER_DATA_GREASEPENCIL')


def draw_TCourier_menu_export(self, context):
    self.layout.menu("TCOURIER_MT_menu_export", text="TCourier")


def register():
    global icon
    icon = bpy.utils.previews.new()

    bpy.utils.register_class(import_camera.TCourier_Import_camera)
    bpy.utils.register_class(import_points.TCourier_Import_points)
    bpy.utils.register_class(import_geo.TCourier_Import_geo)
    bpy.utils.register_class(import_undistort.TCourier_Import_undistort)
    bpy.utils.register_class(import_obj_track.TCourier_Import_obj_track)
    bpy.utils.register_class(import_obj_track.TCourier_Duplicate)
    bpy.utils.register_class(export_camera.TCourier_Export_camera)
    bpy.utils.register_class(export_geo.TCourier_Export_geo)
    bpy.utils.register_class(export_obj_track.TCourier_Export_obj_track)

    bpy.utils.register_class(TCOURIER_PT_main_panel)

    bpy.types.VIEW3D_HT_tool_header.append(draw_TCourier_popover)
    bpy.utils.register_class(TCOURIER_MT_menu_import)
    bpy.types.TOPBAR_MT_file_import.append(draw_TCourier_menu_import)
    bpy.utils.register_class(TCOURIER_MT_menu_export)
    bpy.types.TOPBAR_MT_file_export.append(draw_TCourier_menu_export)


def unregister():
    global icon

    bpy.types.VIEW3D_HT_tool_header.remove(draw_TCourier_popover)
    bpy.utils.previews.remove(icon)
    bpy.utils.unregister_class(TCOURIER_MT_menu_import)
    bpy.types.TOPBAR_MT_file_import.remove(draw_TCourier_menu_import)
    bpy.utils.unregister_class(TCOURIER_MT_menu_export)
    bpy.types.TOPBAR_MT_file_export.remove(draw_TCourier_menu_export)

    bpy.utils.unregister_class(TCOURIER_PT_main_panel)

    bpy.utils.unregister_class(import_camera.TCourier_Import_camera)
    bpy.utils.unregister_class(import_points.TCourier_Import_points)
    bpy.utils.unregister_class(import_geo.TCourier_Import_geo)
    bpy.utils.unregister_class(import_undistort.TCourier_Import_undistort)
    bpy.utils.unregister_class(import_obj_track.TCourier_Import_obj_track)
    bpy.utils.unregister_class(import_obj_track.TCourier_Duplicate)
    bpy.utils.unregister_class(export_camera.TCourier_Export_camera)
    bpy.utils.unregister_class(export_geo.TCourier_Export_geo)
    bpy.utils.unregister_class(export_obj_track.TCourier_Export_obj_track)


if __name__ == "__main__":
    register()
