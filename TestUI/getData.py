# -*- coding: utf-8 -*-

import bpy

import os
import csv
import math
import sys


output_path = sys.argv[4]

anim_path = sys.argv[5]

bpy.ops.wm.open_mainfile( filepath = anim_path )

"""
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

#openAnimation(anim_path)
"""

sce = bpy.context.scene

#Takes moments to complete

def roundUp(n, d=8):
    d = int('1' + ('0' * d))
    return math.floor(n*d)/d

def timestampIt(n):
    n_floor = math.floor(n)
    n_ms = str(roundUp(n - n_floor,6))
    n_h = "00"
    n_m = "00"
    n_s = "00"
    if n_floor >=3600:
        n_h = str(math.floor((n_floor - 3600)/3600))
        n_floor = n_floor - n_h*3600
    if (n_floor >=60) and (n_floor < 3600):
        n_m = str(math.floor((n_floor - 60)/60))
        n_floor = n_floor - n_m*60
    if (n_floor >=1) and (n_floor < 60):
        n_s = str(n_floor)
        
    if len(n_h) < 2:
        n_h = "0"+n_h
    if len(n_m) < 2:
        n_m = "0"+n_m
    if len(n_s) < 2:
        n_s = "0"+n_s

    #get rid of the leading 0 on the n_ms string
    n_ms = n_ms[2:]
    
    #add zeros
    while len(n_ms) < 6:
        n_ms = n_ms+'0'
        
    timestamp = (n_h+":"+n_m+":"+n_s+":"+n_ms)
    return timestamp

#print("Writing to: " + output_path + "\n\n")
outputfile = os.path.join(output_path, 'bone_data.csv')
with open(outputfile, 'w', newline='') as w_file:
    filewriter = csv.writer(w_file, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #filewriter.writerow(['Port'])
    for obj in bpy.data.objects:
        # won't return if there isn't a viable rigging in the scene
        if obj.type == 'ARMATURE':
            arm = obj.data
            
            nBones = len(arm.bones)
            boneNames = [None] * nBones 
            frames = list(range(sce.frame_start-1,sce.frame_end))

            fps = sce.render.fps
            spf = 1/fps 
            
            i = 0
            for bone in arm.bones:
                boneNames[i] = bone.name
                i+=1
                

            header = ['Frame','Time']
            for name in boneNames:
                header.extend([name + ' / localX', name + ' / localY', name +' / localZ',name + ' / localDistChanged',name + ' / local ThetaX', name + ' / local ThetaY', name + ' / local ThetaZ'])
                    
            
            filewriter.writerow((header))
            
            for f in frames:
                
                i=0
                
                time = f * spf
                
                sce.frame_set(f)
                row = []
                
                row.extend(['Frame ' + str(f),timestampIt(time)+':'+str(f)+'f'])
                localDistChange = 0.0
                for bone in arm.bones:   
                    #get bone frame data
                    poseBone = bpy.data.objects[obj.name].pose.bones[bone.name]
                    
                    # Arrays indexed by frame in parent order. Frame 2 is at index [0+nBones]
                    index = f+i+(nBones*f-nBones)
                    
                    #globalXYZ[index] = poseBone.matrix.decompose()[0]
                    #globalThetaXYZ[index] = poseBone.matrix.decompose()[1].to_euler()
                    
                    localXYZ = poseBone.matrix_basis.decompose()[0]
                    localThetaXYZ = poseBone.matrix_basis.decompose()[1].to_euler()
                     
                    row.extend([roundUp(localXYZ[0]),roundUp(localXYZ[1]),roundUp(localXYZ[2])])
                    if f > sce.frame_start:
                        #globalDistChange[index] = math.sqrt((globalXYZ[index][0]-globalXYZ[index-1][0])^2+(globalXYZ[index][1]-globalXYZ[index-1][1])^2+(globalXYZ[index][2]-globalXYZ[index-1][2])^2)
                       localDistChange = math.sqrt(math.pow((localXYZ[0]-row[2+i*7]),2)+math.pow((localXYZ[1]-row[3+i*7]),2)+math.pow((localXYZ[2]-row[4+i*7]),2))
                    
                    row.extend([roundUp(localDistChange)])
                    row.extend([roundUp(math.degrees(localThetaXYZ[0])),roundUp(math.degrees(localThetaXYZ[1])),roundUp(math.degrees(localThetaXYZ[2]))])
              
                    i+=1
                    
                filewriter.writerow(row)
    
           
            # Array:
            # Bone1 Frames 1-N,
            # Bone2 Frames 1-N
            # Etc..
            
            # CSV Array:
            # Frame 1, Time 1, Bone1 Frame 1 data, Bone 2 Frame 1 data... 
            # Frame 2, Time 2...
            
# create atexit script.
print('OK!') 