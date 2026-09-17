"""Density dilution as particles expand: preserve young dark exhaust, fade old plume."""
import bpy,json
from pathlib import Path
s=bpy.context.scene;rows=json.loads(Path('outputs/vol-complet-v4/sources/telemetrie.json').read_text(encoding='utf8'))
for p in bpy.data.objects:
 if not p.name.startswith('Volume fumee'):continue
 for fc in p.active_material.node_tree.animation_data.action.fcurves:
  if 'Math.001' not in fc.data_path:continue
  for k in fc.keyframe_points:
   age=max(0,rows[round(k.co.x)-1]['time']-p['birth_s']);factor=(1+.7*age)**2
   k.co.y/=factor;k.handle_left.y/=factor;k.handle_right.y/=factor
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(Path('outputs/vol-complet-v4/chasse-galerie-1-vol-complet.blend').resolve()))
s.frame_start=1;s.frame_end=330;s.render.filepath=str(Path('work/atmosphere-v4/frames/vol-').resolve());bpy.ops.render.render(animation=True)
exec(Path('work/extrait-fumee.py').read_text(encoding='utf8'))
