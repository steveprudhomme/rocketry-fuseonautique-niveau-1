"""Blender 4.3 native Soft Body solver, local recovery reference frame.
Exports vertex samples; no aerodynamic or strength-validation claim.
blender -b --factory-startup --python simuler-corde.py -- output-directory
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1]).resolve();out.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene;scene.render.fps=60;scene.frame_start=1;scene.frame_end=601
N=49;length=4.572;bottom=.5842;top0=3.20;top1=4.98
def points(a):return [(a*math.sin(math.pi*i/(N-1)),.06*math.sin(2*math.pi*i/(N-1)),bottom+(top0-bottom)*i/(N-1)) for i in range(N)]
def arclen(p):return sum((Vector(b)-Vector(a)).length for a,b in zip(p,p[1:]))
lo,hi=0.,3.
for _ in range(50):
 mid=(lo+hi)/2
 if arclen(points(mid))>length:hi=mid
 else:lo=mid
verts=points((lo+hi)/2)
m=bpy.data.meshes.new('Corde 49 masses et 48 ressorts');m.from_pydata(verts,[(i,i+1) for i in range(N-1)],[]);m.update()
o=bpy.data.objects.new('CORDE - solveur corps souple natif',m);scene.collection.objects.link(o)
bpy.context.view_layer.objects.active=o;o.select_set(True)
o.shape_key_add(name='Base');key=o.shape_key_add(name='Mise en tension')
for i,p in enumerate(key.data):p.co.z+=(top1-top0)*i/(N-1)
for f,v in ((1,0),(91,1),(601,1)):
 key.value=v;key.keyframe_insert('value',frame=f)
group=o.vertex_groups.new(name='Extremites fixees');group.add(list(range(N)),0,'REPLACE');group.add([0,N-1],1,'REPLACE')
mod=o.modifiers.new('Physique corps souple','SOFT_BODY');s=mod.settings
s.use_goal=True;s.vertex_group_goal=group.name;s.goal_min=0;s.goal_max=1;s.goal_default=1;s.goal_spring=.9;s.goal_friction=10
s.use_edges=True;s.pull=.8;s.push=.8;s.damping=.5;s.bend=.5;s.mass=.3
s.step_min=20;s.step_max=300;s.error_threshold=.001;s.use_self_collision=False
mod.point_cache.frame_start=1;mod.point_cache.frame_end=601
scene.gravity=(0,0,-9.81)
samples=[];maxlen=0;maxpin=0
for f in range(1,602):
 scene.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();dg.update();ev=o.evaluated_get(dg)
 p=[list(v.co) for v in ev.data.vertices];l=arclen(p);maxlen=max(maxlen,l)
 expectedtop=top0+(top1-top0)*key.value
 maxpin=max(maxpin,(Vector(p[0])-Vector((0,0,bottom))).length,(Vector(p[-1])-Vector((0,0,expectedtop))).length)
 samples.append({'t':(f-1)/60,'points':p,'length':l,'top':expectedtop})
assert all(math.isfinite(v) for sample in samples for p in sample['points'] for v in p)
assert maxpin < 1e-4, maxpin
assert maxlen < length*1.03, maxlen
result={'solver':'Blender 4.3 native SOFT_BODY','fps':60,'rest_length_m':length,'nodes':N,'max_length_m':maxlen,'max_pin_error_m':maxpin,'samples':samples}
(out/'corde-simulation.json').write_text(json.dumps(result),encoding='utf8')
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'corde-solveur.blend'),compress=True)
print('SOFT_BODY_RESULT',json.dumps({k:v for k,v in result.items() if k!='samples'}),flush=True)
