"""Blender 4.3: OpenRocket wind trajectory and procedural volumetric exhaust.
Load v3 scene. Run from project directory. No external simulation cache required.
Smoke is an artistic Lagrangian particle approximation, not a CFD solution.
"""
import bpy,csv,json,math,bisect
from pathlib import Path
from mathutils import Vector
base=Path.cwd();out=base/'outputs/vol-complet-v4';work=base/'work/atmosphere-v4';src=out/'sources'
scene=bpy.context.scene;root=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'))
old=json.loads((base/'outputs/vol-complet-v3/sources/telemetrie.json').read_text(encoding='utf8'))
flight=[{k:float(v) for k,v in r.items()} for r in csv.DictReader((out/'vol-h143.csv').open())];times=[r['time_s'] for r in flight]
events={r['event']:float(r['time_s']) for r in csv.DictReader((out/'evenements-h143.csv').open())}
apo=events['RECOVERY_DEVICE_DEPLOYMENT'];end=events['GROUND_HIT']
def interp(x,xs,ys):
 i=max(0,min(len(xs)-2,bisect.bisect_right(xs,x)-1));a=max(0,min(1,(x-xs[i])/(xs[i+1]-xs[i])));return ys[i]*(1-a)+ys[i+1]*a
def sample(t):return {k:interp(t,times,[r[k] for r in flight]) for k in flight[0]}
anchors=[0,1.73,10.245999999999869,11.745999999999869,12.245999999999869,103.84268527829295,106.84268527829295]
targets=[0,1.73,apo,apo+1.5,apo+2,end-3,end]
# Preserve baked recovery and landing, while replacing world-space flight path.
cache=[];followers=[scene.camera]+[o for o in bpy.data.objects if o.name.startswith('Ciel reflechi')]
for f in range(1,1218):
 scene.frame_set(f);cache.append((root.location.copy(),[o.location.copy() for o in followers]))
rows=[];positions=[]
for f,r0 in enumerate(old,1):
 r=dict(r0);t=interp(r['time'],anchors,targets);s=sample(t);pos=Vector((s['x_m'],s['y_m'],max(0,s['altitude_m'])+.08));positions.append(pos.copy())
 delta=pos-cache[f-1][0];root.location=pos;root.keyframe_insert('location',frame=f)
 for o,p in zip(followers,cache[f-1][1]):o.location=p+delta;o.keyframe_insert('location',frame=f)
 r.update(time=t,altitude=max(0,s['altitude_m']),speed=s['speed_m_s'],x=s['x_m'],y=s['y_m']);rows.append(r)
for i,r in enumerate(rows):
 if 'post_contact_s' not in r:
  rate=(rows[min(i+1,len(rows)-1)]['time']-r['time'])*30
  r['rate']='ATTENTE' if rate<.001 else ('TEMPS RÉEL' if abs(rate-1)<.01 else f'TEMPS ×{rate:.2f}')
(src/'telemetrie.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf8')
# Add the same detailed soil at the calculated landing area.
landing=positions[-1]
for name in ['Champ laboure et sillons','Chaumes de mais coupes et feuilles seches']:
 o=bpy.data.objects.get(name)
 if o:
  cp=o.copy();cp.data=o.data;cp.name=name+' — zone de retour';scene.collection.objects.link(cp);cp.location.x+=landing.x;cp.location.y+=landing.y
for o in list(bpy.data.objects):
 if o.name.startswith('Fumee animee'):bpy.data.objects.remove(o,do_unlink=True)
# Mesh containers with volume-only materials. Radial falloff prevents hard shells.
collection=bpy.data.collections.new('Fumée volumétrique — particules advectées');scene.collection.children.link(collection)
for n in range(116):
 birth=n*1.73/116;s=sample(birth);origin=Vector((s['x_m'],s['y_m'],s['altitude_m']+.075));seed=n*2.39996
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);p=bpy.context.object;p.name=f'Volume fumee {n:03d}'
 for c in list(p.users_collection):c.objects.unlink(p)
 collection.objects.link(p)
 mat=bpy.data.materials.new(p.name);mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear();links=mat.node_tree.links
 output=nodes.new('ShaderNodeOutputMaterial');vol=nodes.new('ShaderNodeVolumePrincipled');vol.inputs['Color'].default_value=(.23,.22,.20,1);vol.inputs['Anisotropy'].default_value=.15;links.new(vol.outputs['Volume'],output.inputs['Volume'])
 tex=nodes.new('ShaderNodeTexCoord');sub=nodes.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=(.5,.5,.5);links.new(tex.outputs['Generated'],sub.inputs[0])
 length=nodes.new('ShaderNodeVectorMath');length.operation='LENGTH';links.new(sub.outputs[0],length.inputs[0])
 fade=nodes.new('ShaderNodeMapRange');fade.clamp=True;fade.inputs['From Min'].default_value=.20;fade.inputs['From Max'].default_value=.49;fade.inputs['To Min'].default_value=1;fade.inputs['To Max'].default_value=0;links.new(length.outputs['Value'],fade.inputs['Value'])
 noise=nodes.new('ShaderNodeTexNoise');noise.noise_dimensions='4D';noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.7;links.new(tex.outputs['Generated'],noise.inputs['Vector'])
 mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(fade.outputs[0],mul.inputs[0]);links.new(noise.outputs['Fac'],mul.inputs[1])
 density=nodes.new('ShaderNodeMath');density.operation='MULTIPLY';links.new(mul.outputs[0],density.inputs[0]);links.new(density.outputs[0],vol.inputs['Density']);p.data.materials.append(mat)
 p['birth_s']=birth;p['lifetime_s']=7;p['wind_m_s']='(-2, 0, 0), model coordinates';p['method']='procedural volumetric particle, not CFD'
 for f,r in enumerate(rows,1):
  age=r['time']-birth;visible=0<=age<7 and f>=61
  # Only transition visibility keys; motion and density sampled during lifetime.
  if f==1 or visible!=previous:
   p.hide_render=not visible;p.keyframe_insert('hide_render',frame=f)
  previous=visible
  if not visible:continue
  a=age;wind=-2*(a-.35*(1-math.exp(-a/.35)));eddy=.16*a
  p.location=origin+Vector((wind+eddy*math.sin(seed+a*2),eddy*math.cos(seed+a*1.7),.22*a+eddy*.5*math.sin(seed+a*2.3)))
  radius=.13+.24*a;p.scale=(radius,radius,max(radius,.09+s['speed_m_s']*1.73/116*.65));p.rotation_euler=(.12*math.sin(seed+a),.12*math.cos(seed+a),seed+a*.18)
  for prop in ['location','scale','rotation_euler']:p.keyframe_insert(prop,frame=f)
  density.inputs[1].default_value=22*(1-a/7)**2/(1+a*.7);density.inputs[1].keyframe_insert('default_value',frame=f)
  noise.inputs['W'].default_value=seed+a*.65;noise.inputs['W'].keyframe_insert('default_value',frame=f)
 for datablock in [p,mat.node_tree]:
  if datablock.animation_data and datablock.animation_data.action:
   for curve in datablock.animation_data.action.fcurves:
    for k in curve.keyframe_points:k.interpolation='CONSTANT' if curve.data_path=='hide_render' else 'LINEAR'
scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.resolution_percentage=100
scene['atmosphere']='OpenRocket 2 m/s, turbulence 10%, seed 20260912; procedural volumetric smoke'
scene.frame_set(90);scene.render.filepath=str(work/'frames/vol-');bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-vol-complet.blend'))
info={'revision':'v4','frames':1217,'duration':1217/30,'contact_frame':977,'post_contact_duration':8,'flight_duration':end,'deployment':apo,'apogee':max(r['altitude_m'] for r in flight),'wind_average_m_s':2,'wind_turbulence_intensity':.1,'wind_direction_parameter_deg':90,'random_seed':20260912,'landing_xy_m':list(landing)[:2],'smoke_particles':116,'smoke_model':'procedural volume particles, not CFD','timing':'v3 landmarks preserved; physical time remapped and playback rate displayed'}
(src/'animation-info.json').write_text(json.dumps(info,indent=2),encoding='utf8')
for f in [85,110,150,650,1150]:
 scene.frame_set(f);scene.render.filepath=str(work/f'apercu-{f}.png');bpy.ops.render.render(write_still=True)
print('ATMOSPHERE_READY',json.dumps(info),flush=True)
