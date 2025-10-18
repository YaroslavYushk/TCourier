import bpy


class TCOURIER_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    force_scene_scale: bpy.props.BoolProperty(
        name="Force scene Unit scale to 0.01",
        default=True,
    )  # type: ignore

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "force_scene_scale")
        layout.label(text="This helps to avoid problem of different scales "
                          "in different softwares")
        layout.label(text="(Disable this if you have problems with "
                          "rigged animations or simulations)")


def register():
    bpy.utils.register_class(TCOURIER_Preferences)


def unregister():
    bpy.utils.unregister_class(TCOURIER_Preferences)
