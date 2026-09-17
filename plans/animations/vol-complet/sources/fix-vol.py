import bpy
from pathlib import Path
s=bpy.context.scene
for o in bpy.data.objects:
 if not o.name.startswith('Volume fumee'):continue
 ns=o.active_material.node_tree.nodes;ls=o.active_material.node_tree.links;tex=next(n for n in ns if n.type=='TEX_COORD');sub=next(n for n in ns if n.type=='VECT_MATH' and n.operation=='SUBTRACT');sub.inputs[1].default_value=(0,0,0);ls.new(tex.outputs['Object'],sub.inputs[0]);noise=next(n for n in ns if n.type=='TEX_NOISE');ls.new(tex.outputs['Object'],noise.inputs['Vector']);noise.inputs['Scale'].default_value=3
 fade=next(n for n in ns if n.type=='MAP_RANGE');fade.inputs['From Min'].default_value=.4;fade.inputs['From Max'].default_value=.99
s.eevee.volumetric_tile_size='2';s.eevee.volumetric_samples=128;s.eevee.use_volumetric_shadows=True;s.eevee.clamp_volume_indirect=0
s.frame_set(85);s.render.filepath=str(Path('work/atmosphere-v4/smoke-test.png').resolve());bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(Path('outputs/vol-complet-v4/chasse-galerie-1-vol-complet.blend').resolve()))
