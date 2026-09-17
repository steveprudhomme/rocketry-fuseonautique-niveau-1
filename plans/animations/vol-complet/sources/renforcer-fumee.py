import bpy,json,math
from pathlib import Path
from mathutils import Vector
s=bpy.context.scene;rows=json.loads(Path('outputs/vol-complet-v4/sources/telemetrie.json').read_text(encoding='utf8'));root=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'));cam=s.camera
for o in bpy.data.objects:
 if not o.name.startswith('Volume fumee'):continue
 ns=o.active_material.node_tree.nodes;vol=next(n for n in ns if n.type=='PRINCIPLED_VOLUME');vol.inputs['Color'].default_value=(.035,.035,.035,1)
 for fc in o.active_material.node_tree.animation_data.action.fcurves:
  if 'Math.001' in fc.data_path:
   for k in fc.keyframe_points:k.co.y*=4;k.handle_left.y*=4;k.handle_right.y*=4
 for fc in o.animation_data.action.fcurves:
  if fc.data_path=='scale' and fc.array_index<2:
   for k in fc.keyframe_points:k.co.y*=1.5;k.handle_left.y*=1.5;k.handle_right.y*=1.5
poses=[]
for f in range(1,151):
 s.frame_set(f);t=rows[f-1]['time'];factor=1.8 if t<=1.73 else 1+.8*max(0,1-(t-1.73)/1.2);target=root.location+Vector((0,0,.6));poses.append(target+(cam.location-target)*factor)
for f,p in enumerate(poses,1):cam.location=p;cam.keyframe_insert('location',frame=f)
s.frame_set(85);s.render.filepath=str(Path('work/atmosphere-v4/smoke-final.png').resolve());bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(Path('outputs/vol-complet-v4/chasse-galerie-1-vol-complet.blend').resolve()))
