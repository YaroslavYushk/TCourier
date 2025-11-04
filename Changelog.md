### v2.1.3
* Fixed a bug in 3DEqualizer where geo with same names couln't be saved properly
* Fixed a bug in Nuke where geometry transforms weren't imported for object tracks
* Fixed a bug in Blender where the undistort sequence failed to load if the file or camera name was too long
* Added import validation for object tracks with incompatible project data
* Improved import/export data validation in 3DEqualizer with better error reporting
* Added .obj format validation in Nuke for geo and object track export

### v2.1.2
* Disabling forced scene unit scale is now supported in Blender

### v2.1.1
* Improved old versions of Nuke compatibility

### v2.1.0
* 2d tracks import/export between 3DEqualizer and Nuke
* Fixed an export issue for blender when camera or object were animated in unexpected rotation order
* Fixed an export bug related to relative file paths
* Fixed a bug with wrong scale assigment in Blender
* Fixed a bug in Blender's object track export

### v2.0.1
* Fixed TEMP folder path for MAC compatibility
* Added error message when the file is corrupted or missing

### v2.0.0
* Initial release
