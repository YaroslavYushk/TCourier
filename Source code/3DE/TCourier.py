#
# 3DE4.script.name:  ~ TCourier panel ~
# 3DE4.script.comment:  Fast cross-software tracking data exchange
#
# 3DE4.script.gui:  Lineup Controls::TCourier
# 3DE4.script.gui:  Orientation Controls::TCourier
# 3DE4.script.gui.config_menus: true
#
# 3DE4.script.addlabel: Export Camera
# 3DE4.script.addlabel: Export Points
# 3DE4.script.addlabel: Export Geo
# 3DE4.script.addlabel: Export Undistort
# 3DE4.script.addlabel: Export Obj track
# 3DE4.script.addlabel: Import Camera
# 3DE4.script.addlabel: Import Geo
# 3DE4.script.addlabel: Import Obj track
#
# Version - 2.0.0
# Author - Yaroslav Yushkevich
# Bugs, ideas, feedback - https://github.com/YaroslavYushk/
#


import tde4

import TCourier.export_camera
import TCourier.export_points
import TCourier.export_geo
import TCourier.export_undistort
import TCourier.export_obj_track
import TCourier.import_camera
import TCourier.import_geo
import TCourier.import_obj_track


def tcourier_export_scene(requester, widget, action):
    TCourier.export_scene.execute()
    return


def tcourier_export_camera(requester, widget, action):
    result = TCourier.export_camera.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_export_camera",
            "+       Export Camera       +")
    return


def tcourier_export_points(requester, widget, action):
    result = TCourier.export_points.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_export_points",
            "+       Export Points       +")
    return


def tcourier_export_undistort(requester, widget, action):
    if widget == "btn_export_undistort": scale = 1.0
    elif widget == "btn_export_undistort_1/2": scale = 0.5
    elif widget == "btn_export_undistort_1/4": scale = 0.25
    elif widget == "btn_export_undistort_1080p": scale = 1080
    result = TCourier.export_undistort.execute(scale=scale)
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_export_undistort",
            "+       Export Undistorted footage       +")
    return


def tcourier_export_geo(requester, widget, action):
    result = TCourier.export_geo.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_export_geo",
            "+       Export Geo       +")
    return


def tcourier_export_obj_track(requester, widget, action):
    result = TCourier.export_obj_track.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_export_obj_track",
            "+       Export Object track       +")
    return


def tcourier_import_camera(requester, widget, action):
    result = TCourier.import_camera.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_import_camera",
            "+       Import Camera       +")
    return


def tcourier_import_geo(requester, widget, action):
    result = TCourier.import_geo.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_import_geo",
            "+       Import Geo       +")
    return


def tcourier_import_obj_track(requester, widget, action):
    result = TCourier.import_obj_track.execute()
    if result is True:
        tde4.setWidgetLabel(
            requester, "btn_import_obj_track",
            "+       Import Object track       +")
    return


def _TCourier_update(requester):
    return


#
# region UI
#
def draw_panel():
    try:
        requester = TCourier_requester
    except (ValueError, NameError, TypeError):
        requester = tde4.createCustomRequester()

        # Label "Export"
        tde4.addLabelWidget(
            requester, "label_01", "Export:", "ALIGN_LABEL_CENTER")
        tde4.setWidgetOffsets(
            requester, "label_01", 0, 100, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "label_01", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WINDOW", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "label_01", "", "", "", "")
        tde4.setWidgetSize(
            requester, "label_01", 60, 20)

        # Button "Export camera"
        tde4.addButtonWidget(
            requester, "btn_export_camera", "Export Camera")
        tde4.setWidgetOffsets(
            requester, "btn_export_camera", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_camera", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_camera", "", "", "label_01", "")
        tde4.setWidgetSize(
            requester, "btn_export_camera", 140, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_camera", "tcourier_export_camera")

        # Button "Export points"
        tde4.addButtonWidget(
            requester, "btn_export_points", "Export Points")
        tde4.setWidgetOffsets(
            requester, "btn_export_points", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_points", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_points", "", "", "btn_export_camera", "")
        tde4.setWidgetSize(
            requester, "btn_export_points", 140, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_points", "tcourier_export_points")

        # Button "Export undistort"
        tde4.addButtonWidget(
            requester, "btn_export_undistort", "Export Undistorted footage")
        tde4.setWidgetOffsets(
            requester, "btn_export_undistort", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_undistort", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_undistort",
            "", "", "btn_export_points", "")
        tde4.setWidgetSize(
            requester, "btn_export_undistort", 140, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_undistort", "tcourier_export_undistort")

        # Button "1/2 res"
        tde4.addButtonWidget(
            requester, "btn_export_undistort_1/2", "1/2 res")
        tde4.setWidgetOffsets(
            requester, "btn_export_undistort_1/2", 10, 35, 8, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_undistort_1/2", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_undistort_1/2", "",
            "", "btn_export_undistort", "")
        tde4.setWidgetSize(
            requester, "btn_export_undistort_1/2", 80, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_undistort_1/2", "tcourier_export_undistort")

        # Button "1/4 res"
        tde4.addButtonWidget(
            requester, "btn_export_undistort_1/4", "1/4 res")
        tde4.setWidgetOffsets(
            requester, "btn_export_undistort_1/4", 38, 62, 8, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_undistort_1/4", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_undistort_1/4", "",
            "", "btn_export_undistort", "")
        tde4.setWidgetSize(
            requester, "btn_export_undistort_1/4", 80, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_undistort_1/4", "tcourier_export_undistort")

        # Button "1080p"
        tde4.addButtonWidget(
            requester, "btn_export_undistort_1080p", "1080p")
        tde4.setWidgetOffsets(
            requester, "btn_export_undistort_1080p", 65, 90, 8, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_undistort_1080p", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_undistort_1080p", "",
            "", "btn_export_undistort", "")
        tde4.setWidgetSize(
            requester, "btn_export_undistort_1080p", 80, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_undistort_1080p", "tcourier_export_undistort")

        # Button "Export geo"
        tde4.addButtonWidget(
            requester, "btn_export_geo", "Export Geo")
        tde4.setWidgetOffsets(
            requester, "btn_export_geo", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_geo", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_geo",
            "", "", "btn_export_undistort_1/2", "")
        tde4.setWidgetSize(
            requester, "btn_export_geo", 140, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_geo", "tcourier_export_geo")

        # Button "Export obj track"
        tde4.addButtonWidget(
            requester, "btn_export_obj_track", "Export Object track")
        tde4.setWidgetOffsets(
            requester, "btn_export_obj_track", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_export_obj_track", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_export_obj_track",
            "", "", "btn_export_geo", "")
        tde4.setWidgetSize(
            requester, "btn_export_obj_track", 140, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_export_obj_track", "tcourier_export_obj_track")

        # Label "Import"
        tde4.addLabelWidget(
            requester, "label_02", "Import:", "ALIGN_LABEL_CENTER")
        tde4.setWidgetOffsets(
            requester, "label_02", 0, 100, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "label_02", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "label_02", "", "", "btn_export_obj_track", "")
        tde4.setWidgetSize(requester, "label_02", 60, 20)

        # Button "Import camera"
        tde4.addButtonWidget(
            requester, "btn_import_camera", "Import Camera")
        tde4.setWidgetOffsets(
            requester, "btn_import_camera", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_import_camera", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_import_camera", "", "", "label_02", "")
        tde4.setWidgetSize(
            requester, "btn_import_camera", 160, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_import_camera", "tcourier_import_camera")

        # Button "Import geo"
        tde4.addButtonWidget(
            requester, "btn_import_geo", "Import Geo")
        tde4.setWidgetOffsets(
            requester, "btn_import_geo", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_import_geo", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_import_geo", "", "", "btn_import_camera", "")
        tde4.setWidgetSize(
            requester, "btn_import_geo", 160, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_import_geo", "tcourier_import_geo")

        # Button "Import obj track"
        tde4.addButtonWidget(
            requester, "btn_import_obj_track", "Import Object track")
        tde4.setWidgetOffsets(
            requester, "btn_import_obj_track", 10, 90, 20, 0)
        tde4.setWidgetAttachModes(
            requester, "btn_import_obj_track", "ATTACH_POSITION",
            "ATTACH_POSITION", "ATTACH_WIDGET", "ATTACH_NONE")
        tde4.setWidgetLinks(
            requester, "btn_import_obj_track",
            "", "", "btn_import_geo", "")
        tde4.setWidgetSize(
            requester, "btn_import_obj_track", 160, 20)
        tde4.setWidgetCallbackFunction(
            requester, "btn_import_obj_track", "tcourier_import_obj_track")

        _TCourier_requester = requester

#
# End of UI
#

    if tde4.isCustomRequesterPosted(_TCourier_requester) == "REQUESTER_UNPOSTED":
        if tde4.getCurrentScriptCallHint() == "CALL_GUI_CONFIG_MENU":
            tde4.postCustomRequesterAndContinue(
                _TCourier_requester, "TCourier", 0, 0, "_TCourier_update")
        else:
            tde4.postCustomRequesterAndContinue(
                _TCourier_requester, "TCourier", 340, 470, "_TCourier_update")
    else: tde4.postQuestionRequester(
        "TCourier",
        "Window/Pane is already posted, close manually first!",
        "Ok")


# region Main
if __name__ == "__main__":
    label = tde4.getLastScriptMenuLabel()
    if label == '~ TCourier panel ~':
        draw_panel()

    if label == 'Export Camera':
        result = TCourier.export_camera.execute()
        msg = "Camera data saved successfully"
    if label == 'Export Points':
        result = TCourier.export_points.execute()
        msg = "Points data saved successfully"
    if label == 'Export Geo':
        result = TCourier.export_geo.execute()
        msg = "Geo data saved successfully"
    if label == 'Export Undistort':
        result = TCourier.export_undistort.execute()
        msg = "Undistort data saved successfully"
    if label == 'Export Obj track':
        result = TCourier.export_obj_track.execute()
        msg = "Object track data saved successfully"

    if label == 'Import Camera':
        result = TCourier.import_camera.execute()
        msg = "Camera data loaded successfully"
    if label == 'Import Geo':
        result = TCourier.import_geo.execute()
        msg = "Geo data loaded successfully"
    if label == 'Import Obj track':
        result = TCourier.import_obj_track.execute()
        msg = "Object track data loaded successfully"

    if result is True:
        tde4.postQuestionRequester(
            "TCourier", msg, "Ok")
        result = False
