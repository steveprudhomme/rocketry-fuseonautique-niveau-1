import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path('outputs/terrain-hybride-v6').resolve();w=Path('work/terrain-hybride-v6').resolve();s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s;s.view_layers[0].update();spec=json.loads((out/'donnees/terrain-hybride.json').read_text(encoding='utf8'));pad=Vector(spec['pad_local_m'])
# Daylight makes the terrain texture and physical microrelief legible.
for o in s.objects:
 if o.type=='LIGHT' and o.data.type=='SUN':
  o.data=o.data.copy();o.data.energy=2.8;o.data.color=(1,.94,.84);o.data.angle=.09;o.rotation_euler=(math.radians(35),math.radians(-25),math.radians(-40))
s.world=s.world.copy();s.world.use_nodes=True
for n in s.world.node_tree.nodes:
 if n.type=='BACKGROUND':n.inputs['Strength'].default_value=.65
review=bpy.data.scenes['04 — Inspection du terrain hybride'];review.world=s.world
# Retain the original shot timing but raise the aerial camera to reveal terrain beneath flight.
root=next(o for o in s.objects if o.name.startswith('CHASSE GALERIE'));cam=s.camera;cam.animation_data.action=cam.animation_data.action.copy()
for f in range(1,1218):
 s.frame_set(f);s.view_layers[0].update();alt=root.location.z-.08;t=max(0,min(1,(alt-8)/50));t=t*t*(3-2*t);target=root.matrix_world.translation+Vector((0,0,.6));loc=cam.matrix_world.translation;dist=(loc-target).length;loc.z+=dist*.8*t;cam.location=cam.parent.matrix_world.inverted()@loc if cam.parent else loc;cam.rotation_euler=(target-loc).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
for f in (1,85,230,650,1217):
 s.frame_set(f);s.view_layers[0].update();s.render.filepath=str(out/f'apercu-vol-{f}.jpg');bpy.ops.render.render(write_still=True)
bpy.context.window.scene=review;review.view_layers[0].update();cam=review.camera;review.frame_set(1);review.view_layers[0].update()
def look(loc,target):cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
for name,loc,target in [('detail',(pad.x+2,pad.y-3,pad.z+.65),(pad.x,pad.y+2,pad.z+.15)),('transition',(pad.x+45,pad.y-65,pad.z+65),(pad.x,pad.y,pad.z)),('aerien',(pad.x+400,pad.y-550,650),(0,0,0))]:
 look(loc,target);review.render.filepath=str(out/f'apercu-{name}.jpg');bpy.ops.render.render(write_still=True)
# A short inspection flight from the stubble to the aerial image demonstrates the blend.
for f in range(1,241):
 t=(f-1)/239;t=t*t*(3-2*t);look((pad.x+2+100*t,pad.y-3-140*t,pad.z+.65+160*t),(pad.x,pad.y+2,pad.z));cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
review.frame_start=1;review.frame_end=240;review.render.filepath=str(w/'detail/terrain-');(w/'detail').mkdir(exist_ok=True)
bpy.context.window.scene=s;s.view_layers[0].update();s.frame_set(1);s.view_layers[0].update();s.render.filepath=str(w/'frames/vol-');bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-terrain-hybride.blend'))
bpy.ops.render.render(animation=True)
bpy.context.window.scene=review;review.view_layers[0].update();review.frame_set(1);review.view_layers[0].update();bpy.ops.render.render(animation=True)
