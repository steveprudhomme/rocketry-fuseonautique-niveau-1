"""Blender 4.3 / v3: visual pendulum, yaw, cushioned contact and canopy collapse.
Load v2 blend. Arguments: telemetry JSON, native cord JSON, output dir, work dir.
Root flight trajectory is retained. Post-contact motion is illustrative, not OpenRocket data.
"""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector,Matrix
args=sys.argv[sys.argv.index('--')+1:];rows=json.loads(Path(args[0]).read_text(encoding='utf8'));native=json.loads(Path(args[1]).read_text(encoding='utf8'))
out=Path(args[2]).resolve();work=Path(args[3]).resolve();out.mkdir(parents=True,exist_ok=True);work.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene;root=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'))
payload=bpy.data.objects['Section avant separee'];rec=bpy.data.objects['Recuperation illustrative'];canopy=next(o for o in bpy.data.objects if o.name.startswith('Parachute 36'));rope=bpy.data.objects['Corde de choc - simulation Soft Body integree'];branch=bpy.data.objects['Lien de section avant'];susp=sorted([o for o in bpy.data.objects if o.name.startswith('Suspente')],key=lambda o:o.name);cam=scene.camera
apo=10.245999999999869;end=106.84268527829295;start=apo+1.5;B=.5842;floor=.032
contact=next(r['frame'] for r in rows if r['time']>=end-1e-7);total=contact+240;scene.frame_end=total
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def rotation(x,y,z):return Matrix.Rotation(z,3,'Z')@Matrix.Rotation(y,3,'Y')@Matrix.Rotation(x,3,'X')
def native_points(age):
 n=max(0,min(600,age*60));i=int(n);j=min(600,i+1);a=n-i
 return [Vector(p).lerp(Vector(q),a) for p,q in zip(native['samples'][i]['points'],native['samples'][j]['points'])]
# Cache original poses before writing any new animation, including all recovery shapes.
poses=[]
for f in range(1,total+1):
 scene.frame_set(min(f,1035));poses.append({'root':root.location.copy(),'payloadloc':payload.location.copy(),'payloadrot':payload.rotation_euler.copy(),'canopyloc':canopy.location.copy(),'open':canopy.data.shape_keys.key_blocks[1].value,'camloc':cam.location.copy(),'camrot':cam.rotation_euler.copy()})
body=bpy.data.objects.new('Corps - pendule et atterrissage',None);scene.collection.objects.link(body);body.parent=root
for o in list(root.children):
 if o not in (body,payload,rec) and o.type=='MESH' and not o.name.startswith('Fumee'):o.parent=body
bodyverts=[o.matrix_basis@v.co for o in body.children if o.type=='MESH' for v in o.data.vertices]
payloadverts=[o.matrix_basis@v.co for o in payload.children if o.type=='MESH' for v in o.data.vertices]
rootrot=root.rotation_euler.to_matrix()
def clearance(loc,R,verts,rootloc):
 # Conservative horizontal support plane: above the highest local soil relief.
 return min((rootrot@(loc+R@p)).z+rootloc.z for p in verts)
def tube(points,r=.006,sides=8):
 v=[]
 for i,p in enumerate(points):
  axis=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized();u=axis.cross(Vector((0,1,0))).normalized();w=axis.cross(u).normalized()
  for k in range(sides):v.append(p+r*(u*math.cos(k*2*math.pi/sides)+w*math.sin(k*2*math.pi/sides)))
 return v
def absolute_keys(obj,initial):
 obj.shape_key_clear()
 for v,p in zip(obj.data.vertices,initial):v.co=p
 obj.shape_key_add(name='Initial');obj.data.shape_keys.use_relative=False;obj.data.shape_keys.key_blocks[0].interpolation='KEY_LINEAR'
def shape(obj,name,coords):
 key=obj.shape_key_add(name=name);key.interpolation='KEY_LINEAR'
 for v,p in zip(key.data,coords):v.co=p
 return key.frame
# Retain folded/open canopy geometry from v2, then bake collapse into the same mesh.
closed=[v.co.copy() for v in canopy.data.shape_keys.key_blocks[0].data];opened=[v.co.copy() for v in canopy.data.shape_keys.key_blocks[1].data]
absolute_keys(canopy,closed);absolute_keys(rope,tube(native_points(0)))
for obj in (payload,canopy):
 # Visibility keys on canopy must remain; location is overwritten every frame below.
 pass
trace=[];cord_errors=[];minimum_body=10;minimum_payload=10
for f in range(1,total+1):
 old=poses[f-1];r=dict(rows[min(f-1,len(rows)-1)]);post=max(0,(f-contact)/30)
 if f>=contact:
  r.update(frame=f,time=end,altitude=0,speed=0,phase=('CONTACT ET AMORTISSEMENT' if post<.8 else ('BASCULEMENT' if post<2.2 else ('DEGONFLAGE DU PARACHUTE' if post<5.5 else 'FUSEE AU REPOS'))),rate='ANIMATION VISUELLE APRES CONTACT',post_contact_s=post)
 else:r['frame']=f
 t=r['time'];age=max(0,t-apo);u=smooth((t-start)/1.0);rootloc=old['root']
 # A small two-axis pendulum about the upper booster attachment, with gentle yaw.
 elapsed=max(0,t-start);decay=.65+.35*math.exp(-elapsed/18)
 ax=math.radians(7)*u*decay*math.sin(2*math.pi*elapsed/3.7)
 ay=math.radians(4)*u*decay*math.sin(2*math.pi*elapsed/4.9)
 az=math.radians(6)*u*math.sin(2*math.pi*elapsed/11)
 R=rotation(ax,ay,az);loc=Vector((0,0,B))-R@Vector((0,0,B))
 if f>=contact:
  fall=smooth(post/1.9);settle=math.radians(3)*math.exp(-max(0,post-1.9)*3)*math.sin(max(0,post-1.9)*8)
  R=rotation(ax*(1-fall),ay*(1-fall)+(math.pi/2+settle)*fall,az*(1-fall)+math.radians(-18)*fall)
  loc=loc.lerp(Vector((.85,-.2,0)),fall)
  bounce=.035*math.sin(math.pi*min(1,post/.45))*math.exp(-post*3) if post<.45 else 0
  loc.z+=floor-clearance(loc,R,bodyverts,rootloc)+bounce
 else:loc.z+=max(0,floor-clearance(loc,R,bodyverts,rootloc)) if t>start else 0
 body.location=loc;body.rotation_euler=R.to_euler();body.keyframe_insert('location',frame=f);body.keyframe_insert('rotation_euler',frame=f)
 minbody=clearance(loc,R,bodyverts,rootloc);minimum_body=min(minimum_body,minbody)
 base=loc+R@Vector((0,0,B))
 # Section avant has its own modest sway; it lands slightly after the booster.
 pr=old['payloadrot'].to_matrix()@rotation(ax*.7,-ay*.7,-az*.6);pl=old['payloadloc'].copy()
 if f>=contact:
  drop=smooth(post/1.1);fall=smooth((post-.4)/1.8)
  pr=rotation(0,.35*(1-fall)+math.pi/2*fall,math.radians(25)*fall)
  pl=pl.lerp(Vector((.5,.38,-B)),drop)
  pl.z+=max(0,floor-clearance(pl,pr,payloadverts,rootloc))
 payload.location=pl;payload.rotation_euler=pr.to_euler();payload.keyframe_insert('location',frame=f);payload.keyframe_insert('rotation_euler',frame=f)
 minimum_payload=min(minimum_payload,clearance(pl,pr,payloadverts,rootloc));pa=pl+pr@Vector((0,0,B))
 # Canopy descends to the terrain and wrinkles flat; its fabric never penetrates the support plane.
 collapse=smooth((post-.3)/4.4) if f>=contact else 0
 canloc=old['canopyloc'].copy();fabric=[a.lerp(b,old['open']) for a,b in zip(closed,opened)]
 if f>=contact:
  canloc=Vector((2.45*collapse,.45*collapse,0))
  high=poses[contact-1]['canopyloc'].z+4.57
  zhem=(high*(1-collapse)+(floor-rootloc.z+.014)*collapse)
  for i,p in enumerate(fabric):
   theta=math.atan2(p.y,p.x);rho=math.hypot(p.x,p.y)
   p.x*=1+.20*collapse*math.sin(3*theta+.3);p.y*=1-.32*collapse
   p.z=zhem+(p.z-4.57)*(1-collapse)+collapse*(.015+.018*math.sin(theta*7+rho*20)**2)
  top=Vector((canloc.x,canloc.y,zhem+canloc.z-.47*(1-collapse)))
  top.z=max(floor-rootloc.z+.008,top.z)
 else:top=native_points(age)[-1]
 # Shape keys contain the entire geometry; canopy local translation only supplies x/y late in landing.
 canopy.location=canloc;canopy.keyframe_insert('location',frame=f)
 k=shape(canopy,f'Image {f}',fabric);canopy.data.shape_keys.eval_time=k;canopy.data.shape_keys.keyframe_insert('eval_time',frame=f)
 # Existing native cord shape follows its attachments. Ground slack is explicitly visual.
 pts=native_points(age);a0=pts[0].copy();b0=pts[-1].copy()
 for i,p in enumerate(pts):
  q=i/(len(pts)-1);p+=(base-a0)*(1-q)+(top-b0)*q
  if f>=contact:
   p.y+=1.05*collapse*math.sin(math.pi*q)*math.sin(2*math.pi*q)
   p.x+=.65*collapse*math.sin(math.pi*q)
   p.z-=.8*collapse*math.sin(math.pi*q)
   p.z=max(floor-rootloc.z+.009,p.z)
 pts[0]=base;pts[-1]=top
 if f>=contact:
  targetlength=sum((a-b).length for a,b in zip(native_points(age),native_points(age)[1:]))
  def loosen(amplitude):
   return [p+Vector((0,amplitude*math.sin(2*math.pi*i/(len(pts)-1))*math.sin(math.pi*i/(len(pts)-1)),0)) for i,p in enumerate(pts)]
  def length(ps):return sum((a-b).length for a,b in zip(ps,ps[1:]))
  if length(pts)<targetlength:
   lo,hi=0.,3.
   for _ in range(28):
    mid=(lo+hi)/2
    if length(loosen(mid))<targetlength:lo=mid
    else:hi=mid
   pts=loosen((lo+hi)/2)
 k=shape(rope,f'Image {f}',tube(pts));rope.data.shape_keys.eval_time=k;rope.data.shape_keys.keyframe_insert('eval_time',frame=f)
 for n,o in enumerate(susp):
  # Exact hem mesh sample at each suspension azimuth (48 radial segments).
  hem=fabric[12*48+(n*6)%48]+canloc
  for p,co in zip(o.data.splines[0].points,[top,hem]):p.co=(*co,1);p.keyframe_insert('co',frame=f)
 mid=(base+pa)/2+Vector((.04,.08,-.08));mid.z=max(floor-rootloc.z+.008,mid.z)
 for p,co in zip(branch.data.splines[0].points,[base,mid,pa]):p.co=(*co,1);p.keyframe_insert('co',frame=f)
 # Hold a wide view until the canopy is down, then approach the resting assembly.
 if f>=contact:
  zoom=smooth((post-2.7)/3.6);distance=18-12*zoom;target=rootloc+rootrot@Vector((1.15*zoom,.20*zoom,2.85*(1-zoom)+.22*zoom))
  cam.location=target+Vector((distance*.48,-distance,.12+1.8*zoom));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
 trace.append(r)
for block in list(bpy.data.objects)+list(bpy.data.curves)+list(bpy.data.shape_keys):
 if block.animation_data and block.animation_data.action:
  for fc in block.animation_data.action.fcurves:
   for key in fc.keyframe_points:key.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
scene['landing_revision']='v3: damped visual pendulum and yaw; cushioned impact, tip-over, canopy collapse. Post-contact artistic animation.'
scene['landing_support_plane_m']=floor
scene['landing_limits']='Kinematic visual animation; no rigid-body/aerodynamic impact solver. Native v2 cord samples warped to moving anchors; post-contact slack is illustrative.'
(work/'telemetrie.json').write_text(json.dumps(trace),encoding='utf8')
(out/'verification-atterrissage.json').write_text(json.dumps({'frames':total,'contact_frame':contact,'post_contact_duration_s':8,'support_plane_m':floor,'minimum_body_vertex_world_z_m':minimum_body,'minimum_payload_vertex_world_z_m':minimum_payload,'pendulum_max_deg':[7,4],'yaw_max_deg':6,'method':'visual keyframes, conservative geometry-ground contact'},indent=2),encoding='utf8')
scene.frame_set(1);scene.render.filepath=str(work/'frames'/'vol-');(work/'frames').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-vol-complet.blend'),compress=True)
for offset in (-1,0,.5,1.5,3.5,6.5):
 f=max(1,min(total,contact+round(offset*30)));scene.frame_set(f);scene.render.filepath=str(work/f'atterrissage-{offset:.1f}.png');bpy.ops.render.render(write_still=True)
print('LANDING_READY',total,contact,flush=True)
