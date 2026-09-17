"""Blender 4.3: native soft-body samples baked into portable mesh shape keys.
Input: existing full-flight scene; args: simulation JSON, telemetry JSON, output dir, work dir.
Canopy shape morph lasts 1.5 physical seconds; whole recovery assembly is never scaled.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
sim=json.loads(Path(args[0]).read_text(encoding='utf8'));tele=json.loads(Path(args[1]).read_text(encoding='utf8'))
out=Path(args[2]).resolve();work=Path(args[3]).resolve();out.mkdir(parents=True,exist_ok=True);work.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene;rocket=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'))
recovery=bpy.data.objects['Recuperation illustrative'];recovery.animation_data_clear();recovery.scale=(1,1,1)
apo=10.245999999999869
def ease(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def sampled(age):
 index=min(600,max(0,age*60));i=int(index);j=min(600,i+1);a=index-i
 return [Vector(p).lerp(Vector(q),a) for p,q in zip(sim['samples'][i]['points'],sim['samples'][j]['points'])]
canopy=next(o for o in bpy.data.objects if o.name.startswith('Parachute 36'))
oldcord=bpy.data.objects['Sangle - representation schematique'];cordmat=oldcord.data.materials[0]
bpy.data.objects.remove(oldcord,do_unlink=True)
# Constant-radius tube around the native solver's centreline.
def tube(points,radius=.006,sides=8):
 verts=[]
 for i,p in enumerate(points):
  tangent=(points[min(len(points)-1,i+1)]-points[max(0,i-1)]).normalized()
  u=tangent.cross(Vector((0,1,0))).normalized();v=tangent.cross(u).normalized()
  for k in range(sides):verts.append(p+radius*(u*math.cos(2*math.pi*k/sides)+v*math.sin(2*math.pi*k/sides)))
 return verts
ps=sampled(0);verts=tube(ps);faces=[]
for i in range(len(ps)-1):
 for k in range(8):faces.append((i*8+k,i*8+(k+1)%8,(i+1)*8+(k+1)%8,(i+1)*8+k))
mesh=bpy.data.meshes.new('Corde calculee - maillage portable');mesh.from_pydata(verts,[],faces);mesh.update()
rope=bpy.data.objects.new('Corde de choc - simulation Soft Body integree',mesh);scene.collection.objects.link(rope);rope.parent=recovery;mesh.materials.append(cordmat)
for p in mesh.polygons:p.use_smooth=True
rope.shape_key_add(name='t 0.000');keys=mesh.shape_keys;keys.use_relative=False;keys.key_blocks[0].interpolation='KEY_LINEAR'
for i,s in enumerate(sim['samples'][1:],1):
 key=rope.shape_key_add(name=f't {s["t"]:.3f}');key.interpolation='KEY_LINEAR'
 for v,p in zip(key.data,tube([Vector(x) for x in s['points']])):v.co=p
rope['solver']=sim['solver'];rope['rest_length_m']=sim['rest_length_m'];rope['sampling_fps']=60
rope['cache']='601 native Soft Body samples embedded as absolute shape keys; no external physics cache needed.'
# Canopy: closed pleated fabric -> full dome. Mesh altitude follows rope top.
canopy.animation_data_clear();canopy.location=(0,0,0)
original=[v.co.copy() for v in canopy.data.vertices]
for v,co in zip(canopy.data.vertices,original):
 radius=math.hypot(co.x,co.y);theta=math.atan2(co.y,co.x);fraction=radius/(.9144/2)
 folded_radius=.028+.015*fraction+.008*math.cos(8*theta)*fraction
 v.co=(folded_radius*math.cos(theta),folded_radius*math.sin(theta),4.57+.74*math.sqrt(max(0,1-fraction*fraction)))
canopy.shape_key_add(name='Voilure pliee');openkey=canopy.shape_key_add(name='Gonflage progressif 1.5 seconde')
for v,co in zip(openkey.data,original):v.co=co
canopy['inflation_duration_s']=1.5;canopy['method']='Pleated-to-dome mesh morph, smoothstep; canopy not fluid-simulated.'
susp=sorted([o for o in bpy.data.objects if o.name.startswith('Suspente')],key=lambda o:o.name)
branch=bpy.data.objects['Lien de section avant']
payload=bpy.data.objects['Section avant separee'];payload.animation_data_clear()
cam=scene.camera
deployment_frame=next(r['frame'] for r in tele if r['time']>=apo)
for o in [canopy,rope,branch]+susp:
 o.hide_render=True;o.hide_viewport=True;o.keyframe_insert('hide_render',frame=1);o.keyframe_insert('hide_viewport',frame=1)
 o.keyframe_insert('hide_render',frame=deployment_frame-1);o.keyframe_insert('hide_viewport',frame=deployment_frame-1)
 o.hide_render=False;o.hide_viewport=False;o.keyframe_insert('hide_render',frame=deployment_frame);o.keyframe_insert('hide_viewport',frame=deployment_frame)
for row in tele:
 f=row['frame'];t=row['time'];age=max(0,t-apo);u=ease(age/1.5);scene.frame_set(f)
 keys.eval_time=min(6000,age*600);keys.keyframe_insert('eval_time',frame=f)
 openkey.value=u;openkey.keyframe_insert('value',frame=f)
 top=sampled(age)[-1];canopy.location.z=top.z-4.1;canopy.keyframe_insert('location',frame=f)
 # Riser ends and canopy hem remain connected throughout inflation.
 for k,o in enumerate(susp):
  angle=k*math.pi/4;closed_radius=.043+.008*math.cos(8*angle);radius=closed_radius*(1-u)+(.9144/2)*u
  coords=[top,top+Vector((radius*math.cos(angle),radius*math.sin(angle),.47))]
  for p,co in zip(o.data.splines[0].points,coords):p.co=(*co,1);p.keyframe_insert('co',frame=f)
 payload.location=(.35*u,0,1.2*u);payload.rotation_euler=(0,.35*u,0);payload.keyframe_insert('location',frame=f);payload.keyframe_insert('rotation_euler',frame=f)
 # Secondary link remains illustrative, with an exact attachment and curved slack.
 attach=Vector((.35*u+math.sin(.35*u)*.5842,0,1.2*u+math.cos(.35*u)*.5842));bottom=Vector((0,0,.5842));middle=(attach+bottom)/2+Vector((.10*(1-u),.10*u,-.10*u))
 for p,co in zip(branch.data.splines[0].points,[bottom,middle,attach]):p.co=(*co,1);p.keyframe_insert('co',frame=f)
 # Zoom anticipates full extension; retain the same trajectory and other scenes.
 if t>=apo-1.2:
  widen=ease((t-apo+1.2)/1.2);distance=4.8+13.2*widen;target=rocket.location+Vector((0,0,.65+2.2*widen))
  cam.location=target+Vector((distance*.48,-distance,.12));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
  cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
for datablock in list(bpy.data.objects)+list(bpy.data.curves)+list(bpy.data.shape_keys):
 if datablock.animation_data and datablock.animation_data.action:
  for fc in datablock.animation_data.action.fcurves:
   for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
scene['recovery_revision']='v2: 1.5s mesh inflation + native Soft Body shock cord, 49 nodes, 60Hz, embedded samples.'
scene['recovery_limitations']='Local frame with gravity, animated pinned endpoints. Artistic material coefficients; no body/cord collision, aerodynamic or load validation. Secondary tether illustrative. After 10s use settled solver state.'
scene.frame_set(1);scene.render.filepath=str(work/'frames'/'vol-');(work/'frames').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-vol-complet.blend'),compress=True)
for age in (.05,.5,1.,1.5,3.):
 f=min(tele,key=lambda r:abs(r['time']-apo-age))['frame'];scene.frame_set(f)
 scene.render.filepath=str(work/f'recuperation-{age:.2f}.png');bpy.ops.render.render(write_still=True)
print('RECOVERY_V2_READY',flush=True)
