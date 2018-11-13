# -*- coding: utf-8 -*-

import bpy
import sys

# blender --python PATH/openBlender.py PATH/animation.ext
try:
    anim_path = sys.argv[3]
    
    def openAnimation(anim_path):
        if anim_path.endswith('.blend'):
            bpy.ops.wm.open_mainfile( filepath = anim_path)
        if anim_path.endwith('.fbx'):
            bpy.ops.import_scene.fbx( filepath = anim_path)
        if anim_path.endswith('.3ds'):
            bpy.ops.import_scene.autodesk_3ds( filepath = anim_path )
        if anim_path.endswith('.dae'):
            bpy.wm.collada_import( filepath = anim_path )
        if anim_path.endswith('.abc'):
            bpy.wm.alembic_import( filepath = anim_path )
            
    openAnimation(anim_path)
    
    print('openBlender.py executed successfully')

except: print('ERROR OPENING: ' + anim_path)