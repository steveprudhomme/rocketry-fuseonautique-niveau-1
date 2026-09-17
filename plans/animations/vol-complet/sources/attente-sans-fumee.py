import bpy
from pathlib import Path
s=bpy.context.scene;p=bpy.data.objects['Volume fumee 000'];p.hide_render=True;p.keyframe_insert('hide_render',frame=1);p.hide_render=False;p.keyframe_insert('hide_render',frame=61)
for fc in p.animation_data.action.fcurves:
 if fc.data_path=='hide_render':
  for k in fc.keyframe_points:k.interpolation='CONSTANT'
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(Path('outputs/vol-complet-v4/chasse-galerie-1-vol-complet.blend').resolve()));s.frame_start=1;s.frame_end=60;s.render.filepath=str(Path('work/atmosphere-v4/frames/vol-').resolve());bpy.ops.render.render(animation=True)
