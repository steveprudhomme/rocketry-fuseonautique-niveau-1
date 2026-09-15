"""Blender 4.3: animate the exported OpenRocket H143 ideal-apogee flight.
Usage: blender -b source.blend --python animer-vol.py -- data.csv events.csv output-dir work-dir
All positions use CSV metres; canopy inflation, separation and smoke are illustrative.
"""
import bpy, csv, math, sys, json
from pathlib import Path
from mathutils import Vector
import numpy as np
a=sys.argv[sys.argv.index('--')+1:]; data=np.genfromtxt(a[0],delimiter=',',names=True)
events={r['event']:float(r['time_s']) for r in csv.DictReader(open(a[1]))}
out=Path(a[2]).resolve();work=Path(a[3]).resolve();out.mkdir(parents=True,exist_ok=True);work.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT';scene.eevee.taa_render_samples=16
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.render.fps=30;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.use_nodes=False
scene.world.color=(.2,.25,.35)
wn=scene.world.node_tree.nodes;wn.clear();wo=wn.new('ShaderNodeOutputWorld');bg=wn.new('ShaderNodeBackground')
bg.inputs['Color'].default_value=(.32,.46,.7,1);bg.inputs['Strength'].default_value=.5
scene.world.node_tree.links.new(bg.outputs[0],wo.inputs[0])
# Remove still-image effects; dynamic effects below are synchronized to flight events.
for o in list(bpy.data.objects):
 if o.name.startswith(('Panache','Fumee','Jet','Lueur','Volume de brume')):bpy.data.objects.remove(o,do_unlink=True)
rocket=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'))
rocket.rotation_euler=(0,0,math.radians(56.565))
cam=scene.camera;cam.data.dof.use_dof=False;cam.data.lens=45;cam.data.clip_end=10000
# Extend the agricultural ground so it remains visible from altitude.
ground=bpy.data.objects.get('Terre horizon');ground.scale=(1000,1000,1)
for o in bpy.data.objects:
 if o.name.startswith('Rail de lancement'):
  o.location=(.07,.04,1.2);o.rotation_euler=(0,0,0);o.scale.z=2.4/o.dimensions.z
# Merge distant foliage to reduce per-frame scene overhead.
bpy.ops.object.select_all(action='DESELECT')
trees=[o for o in bpy.data.objects if o.name.startswith(('Feuillage','Tronc'))]
for o in trees:o.select_set(True)
if trees:bpy.context.view_layer.objects.active=trees[0];bpy.ops.object.join()
def mat(name,color,emission=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.6
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=1
 return m
blue=mat('Parachute bleu',(.025,.12,.42));white=mat('Parachute blanc',(.9,.93,1));cordmat=mat('Suspentes',(.8,.8,.72));smokemat=mat('Fumee illustrative',(.15,.14,.13))
recovery=bpy.data.objects.new('Recuperation illustrative',None);scene.collection.objects.link(recovery);recovery.parent=rocket
# 36 inch nominal canopy shown inflated as a hemisphere (illustrative geometry).
verts=[];faces=[];segments=48;rings=12;r=.9144/2
for j in range(rings+1):
 th=(.015+j/rings*(math.pi/2-.015))
 for k in range(segments):
  ang=2*math.pi*k/segments;verts.append((r*math.sin(th)*math.cos(ang),r*math.sin(th)*math.sin(ang),4.57+r*math.cos(th)))
for j in range(rings):
 for k in range(segments):faces.append((j*segments+k,j*segments+(k+1)%segments,(j+1)*segments+(k+1)%segments,(j+1)*segments+k))
mesh=bpy.data.meshes.new('Voilure');mesh.from_pydata(verts,[],faces);mesh.update()
canopy=bpy.data.objects.new('Parachute 36 pouces - forme illustrative',mesh);scene.collection.objects.link(canopy);canopy.parent=recovery
mesh.materials.append(blue);mesh.materials.append(white)
for p in mesh.polygons:p.material_index=(p.index%segments//6)%2;p.use_smooth=True
def line(name,points,radius,material,parent):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=1;s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,v in zip(s.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);scene.collection.objects.link(o);o.parent=parent;o.data.materials.append(material);return o
for k in range(8):
 ang=k*math.pi/4;line('Suspente',[(0,0,4.1),(r*math.cos(ang),r*math.sin(ang),4.57)],.0015,cordmat,recovery)
line('Lien de section avant',[(0,0,.6),(.25,0,1.3),(.62,0,1.98)],.004,cordmat,recovery)
line('Sangle - representation schematique',[(0,0,.6),(.15,0,2.1),(0,0,4.1)],.006,cordmat,recovery)
payload=bpy.data.objects.new('Section avant separee',None);scene.collection.objects.link(payload);payload.parent=rocket
for o in list(rocket.children):
 if o.name.startswith(('Payload','Ogive')):o.parent=payload
# Compact, dark exhaust for the Smoky Sam; no plume after burnout.
puffs=[]
for i in range(12):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1)
 o=bpy.context.object;o.name='Fumee animee';o.parent=rocket;o.data.materials.append(smokemat);puffs.append(o)
fill=next(o for o in bpy.data.objects if o.name.startswith('Ciel reflechi'))
fill.data.energy=400
apo=events['RECOVERY_DEVICE_DEPLOYMENT'];end=events['GROUND_HIT'];burn=events['BURNOUT']
# 2 s introduction; real-time ascent and deployment; descent x6; final 3 s real-time.
slow_end=apo+2;late=end-3
def flight_time(v):
 if v<2:return 0
 v-=2
 if v<=slow_end:return v
 v-=slow_end
 if v<=(late-slow_end)/6:return slow_end+6*v
 return min(end,late+v-(late-slow_end)/6)
duration=2+slow_end+(late-slow_end)/6+3+2
scene.frame_start=1;scene.frame_end=round(duration*30)
def sample(t,key):return float(np.interp(t,data['time_s'],data[key]))
telemetry=[]
for f in range(1,scene.frame_end+1):
 v=(f-1)/30;t=flight_time(v);z=max(0,sample(t,'altitude_m'));pos=Vector((sample(t,'x_m'),sample(t,'y_m'),z+.08))
 rocket.location=pos;rocket.keyframe_insert('location',frame=f)
 opened=max(0,min(1,(t-apo)/.8));recovery.scale=(max(.001,opened),)*3;recovery.keyframe_insert('scale',frame=f)
 payload.location=(.35*opened,0,1.2*opened);payload.rotation_euler=(0,.35*opened,0);payload.keyframe_insert('location',frame=f);payload.keyframe_insert('rotation_euler',frame=f)
 for i,o in enumerate(puffs):
  active=t>.04 and t<burn;size=(.025+.015*i) if active else .00001
  o.location=(.02*math.sin(t*16+i)*i/12,0,-.05-i*.12);o.scale=(size,size,size*1.7);o.keyframe_insert('location',frame=f);o.keyframe_insert('scale',frame=f)
 # Wider framing under canopy, with a stable tracking view throughout.
 distance=4.8+10.7*opened
 target=pos+Vector((0,0,.65+1.85*opened))
 cam.location=target+Vector((distance*.48,-distance,.12))
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
 fill.location=pos+Vector((2,-3,4));fill.keyframe_insert('location',frame=f)
 phase='SUR LA RAMPE' if v<2 else ('PROPULSION' if t<burn else ('MONTEE BALISTIQUE' if t<apo else ('DESCENTE SOUS PARACHUTE' if t<end else 'RETOUR AU SOL')))
 rate='DESCENTE ACCELEREE x6' if slow_end<t<late else 'TEMPS REEL'
 telemetry.append(dict(frame=f,time=t,altitude=z,speed=sample(t,'speed_m_s'),phase=phase,rate=rate))
for o in bpy.data.objects:
 if o.animation_data and o.animation_data.action:
  for fc in o.animation_data.action.fcurves:
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
scene['simulation']='OpenRocket 24.12 / H143 apogee IDEALE [A] / vent nul'
scene['limites']='Masses estimees; trajectoire CSV; separation, parachute et fumee illustratifs. Descente x6.'
scene['csv_source']=Path(a[0]).name
(work/'telemetrie.json').write_text(json.dumps(telemetry),encoding='utf8')
(work/'animation-info.json').write_text(json.dumps(dict(duration=duration,frames=scene.frame_end,flight_duration=end,apogee=max(data['altitude_m']),deployment=apo)),encoding='utf8')
scene.render.filepath=str(work/'frames'/'vol-');(work/'frames').mkdir(exist_ok=True)
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-vol-complet.blend'),compress=True)
# Three independent stage previews before the full render.
for f in (25,200,round((2+apo+1)*30)):
 scene.frame_set(f);scene.render.filepath=str(work/f'apercu-{f}.png');bpy.ops.render.render(write_still=True)
print('ANIMATION_READY',scene.frame_end,flush=True)

