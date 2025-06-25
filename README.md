# TCourier
Fast cross-software import-export bridge for tracking data

## Supported programs
* 3DEqualizer
* Blender
* Nuke

## Export/Import options
* Camera
* 3D Points
* Undistorted footage
* Geo
* Object track

## Installation
### 3DE
Copy script files to one of your scripts folder:
* Your custom scripts folder defined in 3DE Preferences
* C:\Users\\\<Username>\AppData\Roaming\.3dequalizer\py_scripts  (default user's scripts folder)
* <3DE installation folder>\sys_data\py_scripts  (not recommended)

### Blender
Automatic installation:
Open Blender and go to Edit - Preferences - Get Extensions - Press the arrow at the top-right corner - Install from Disk...
And select .zip archive 

Manual installation:
Unzip archive and copy files to the directory:
C:\Users\\\<Username>\AppData\Roaming\Blender Foundation\Blender\\\<Blender version>\extensions\user_default\TCourier

### Nuke
#### Nukeshared
If you are using NukeShared, copy the files to:
* ...\NukeShared\Repository\Nodes\ - *(if you want scripts appear on the left panel)*
* ...\NukeShared\Repository\Nuke\ - *(if you want scripts appear on the header)*

#### Nuke (basic)
If you are not using NukeShared, copy files in your plugins folder instead:
C:\Users\\\<Username>\.nuke\TCourier
Then open (or create) menu.py file and add next lines of code to create menu at the header:

```
import nuke
import TCourier.Export_Camera
import TCourier.Export_Geo
import TCourier.Export_Obj_Track
import TCourier.Import_Camera
import TCourier.Import_Geo
import TCourier.Import_Obj_Track
import TCourier.Import_Scene
nuke.menu("Nuke").addCommand("TCourier/Export Camera", TCourier.Export_Camera.execute, icon="Export_Camera.png")
nuke.menu("Nuke").addCommand("TCourier/Export Geo", TCourier.Export_Geo.execute, icon="Export_Geo.png")
nuke.menu("Nuke").addCommand("TCourier/Export Obj Track", TCourier.Export_Obj_Track.execute, icon="Export_Obj_Track.png")
nuke.menu("Nuke").addCommand("TCourier/Import Camera", TCourier.Import_Camera.execute, icon="Import_Camera.png")
nuke.menu("Nuke").addCommand("TCourier/Import Geo", TCourier.Import_Geo.execute, icon="Import_Geo.png")
nuke.menu("Nuke").addCommand("TCourier/Import Obj Track", TCourier.Import_Obj_Track.execute, icon="Import_Obj_Track.png")
nuke.menu("Nuke").addCommand("TCourier/Import Scene", TCourier.Import_Scene.execute, icon="Import_Scene.png")
```
