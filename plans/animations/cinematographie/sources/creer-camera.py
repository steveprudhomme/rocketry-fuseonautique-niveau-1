"""Blender 4.3: deadband tracker, damped framing, acceleration-weighted camera shake and optics."""
import bpy,json,math,csv
import numpy as np
from pathlib import Path
from mathutils import Vector
out=Path('outputs/cinematographie-v8').resolve();w=Path('work/cinematographie-v8').resolve();s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s;s.view_layers[0].update();cam=s.camera;original_parent=cam.parent
tele=json.loads(Path('outputs/vol-complet-v4/sources/telemetrie.json').read_text(encoding='utf8'));physics=np.genfromtxt('outputs/vol-complet-v4/vol-h143.csv',delimiter=',',names=True);acc=np.gradient(physics['speed_m_s'],physics['time_s']);acc=np.maximum(acc,0);burn=physics['time_s']<1.73;maxacc=float(acc[burn].max());peak=float(physics['time_s'][np.where(burn)[0][np.argmax(acc[burn])]])
root=next(o for o in s.objects if o.name.startswith('CHASSE GALERIE'));body=next(o for o in s.objects if o.name.startswith('Corps - pendule'));payload=next(o for o in s.objects if o.name.startswith('Section avant separee'));canopy=next(o for o in s.objects if o.name.startswith('Parachute 36'));sun=next(o for o in s.objects if o.type=='LIGHT' and o.data.type=='SUN');sunvec=(sun.matrix_world.to_quaternion()@Vector((0,0,1))).normalized()
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def empty(name,parent=None):
 ob=bpy.data.objects.new(name,None);s.collection.objects.link(ob);ob.parent=parent;return ob
records=[]
for f in range(1,1218):
 s.frame_set(f);s.view_layers[0].update();pts=[];dg=bpy.context.evaluated_depsgraph_get()
 for ob in list(body.children)+list(payload.children)+([canopy] if tele[f-1]['time']>=10.1954595315 else []):
  if ob.type!='MESH':continue
  ev=ob.evaluated_get(dg)
  pts.extend([ob.matrix_world@Vector(v) for v in ev.bound_box])
 xyz=np.array([list(v) for v in pts]);lo=xyz.min(axis=0);hi=xyz.max(axis=0)
 records.append({'frame':f,'cam':cam.matrix_world.translation.copy(),'parent_inverse':original_parent.matrix_world.inverted().copy(),'center':Vector((lo+hi)/2),'root':root.matrix_world.translation.copy(),'points':pts,'alt':tele[f-1]['altitude'],'time':tele[f-1]['time']})
rig=empty('CAMÉRA — suivi amorti et zone de tolérance',original_parent);shake=empty('CAMÉRA — secousse moteur native',rig);focus=empty('CAMÉRA — mise au point adaptative');cam.animation_data_clear();cam.data=cam.data.copy();cam.data.animation_data_clear();cam.parent=shake;cam.matrix_parent_inverse.identity();cam.location=(0,0,0);cam.rotation_euler=(0,0,0);cam.data.dof.use_dof=True;cam.data.dof.focus_object=focus;cam.data.dof.aperture_blades=7;cam.data.clip_end=25000
offset=Vector((0,0));tau=.18;alpha=1-math.exp(-1/(30*tau));log=[];previous_euler=None
for rec in records:
 f=rec['frame'];time=rec['time'];pos=rec['cam'];center=rec['center'];deploy=smooth((time-10.1954595315)/1.5)
 # Baseline follows the whole recovery assembly; deadband handles its secondary movements.
 zoffset=.60+2.1*deploy
 if f>=977:zoffset=.6+2.1*deploy*(1-smooth((f-977)/132))
 base=rec['root']+Vector((0,0,zoffset));q=(base-pos).to_track_quat('-Z','Y');right=q@Vector((1,0,0));up=q@Vector((0,1,0));dist=(base-pos).length;halfwidth=dist*(cam.data.sensor_width/(2*cam.data.lens));halfheight=halfwidth*1080/1920;tol=Vector((halfwidth*.044,halfheight*.050));want=Vector(((center-base).dot(right),(center-base).dot(up)))
 for axis in (0,1):
  delta=want[axis]-offset[axis]
  if abs(delta)>tol[axis]:offset[axis]+=alpha*(delta-math.copysign(tol[axis],delta))
  # Limit transient lag so fast recovery deployment cannot escape the frame.
  limit=(halfwidth if axis==0 else halfheight)*.10;offset[axis]=max(want[axis]-limit,min(want[axis]+limit,offset[axis]))
 aim=base+right*offset.x+up*offset.y;orientation=(aim-pos).to_track_quat('-Z','Y');rig.location=rec['parent_inverse']@pos;rotation=orientation.to_euler('XYZ',previous_euler) if previous_euler else orientation.to_euler('XYZ');rig.rotation_euler=rotation;previous_euler=rotation.copy();rig.keyframe_insert('location',frame=f);rig.keyframe_insert('rotation_euler',frame=f)
 focus.location=center;focus.keyframe_insert('location',frame=f);fstop=7.1+(2.8-7.1)*smooth((rec['alt']-8)/100);fstop=max(fstop,2.8+1.2*deploy);cam.data.dof.aperture_fstop=fstop;cam.data.dof.keyframe_insert('aperture_fstop',frame=f)
 a=float(np.interp(time,physics['time_s'],acc));engine=0
 if f>=61 and time<=1.73:engine=smooth(time/.10)*(.25+.75*min(1,a/maxacc))*smooth((1.73-time)/.16)
 log.append({'frame':f,'time':time,'altitude':rec['alt'],'shake_envelope':engine,'acceleration_positive_m_s2':a,'focus_distance_m':(center-pos).length,'fstop':fstop,'tracking_offset_m':list(offset),'tracking_error_fraction':[float((want.x-offset.x)/(2*halfwidth)),float((want.y-offset.y)/(2*halfheight))]})
# Native F-curve Noise + Envelope modifiers: deterministic, limited to motor combustion.
shake.rotation_euler=(0,0,0);shake.keyframe_insert('rotation_euler',frame=1);shake.keyframe_insert('rotation_euler',frame=1217)
for axis,fc in enumerate(shake.animation_data.action.fcurves):
 noise=fc.modifiers.new('NOISE');noise.scale=2.6+axis*.45;noise.strength=1;noise.phase=37+axis*19;noise.use_restricted_range=True;noise.frame_start=61;noise.frame_end=113
 env=fc.modifiers.new('ENVELOPE');env.reference_value=0;env.default_min=-1;env.default_max=1
 for f in [1,60]+list(range(61,115))+[1217]:
  p=env.control_points.add(f);amplitude=math.radians([.22,.16,.12][axis])*log[f-1]['shake_envelope'];p.min=-amplitude;p.max=amplitude
for ob in (rig,focus):
 for fc in ob.animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
# Compositor effects: mild lateral color dispersion; sun-facing ghosts are gated by angle.
s.use_nodes=True;ns=s.node_tree.nodes;ls=s.node_tree.links;ns.clear();render=ns.new('CompositorNodeRLayers');render.location=(-600,120);render.name='Rendu optique v8';lens=ns.new('CompositorNodeLensdist');lens.name='Aberration chromatique subtile';lens.inputs['Dispersion'].default_value=.0007;lens.use_fit=True;lens.location=(-360,120);ls.new(render.outputs['Image'],lens.inputs['Image']);ghost=ns.new('CompositorNodeGlare');ghost.glare_type='GHOSTS';ghost.quality='HIGH';ghost.threshold=2.0;ghost.iterations=2;ghost.color_modulation=.15;ghost.mix=0;ghost.location=(-100,-100);ls.new(lens.outputs['Image'],ghost.inputs['Image']);mix=ns.new('CompositorNodeMixRGB');mix.name='Reflets — conditionnés à la direction solaire';mix.location=(160,120);ls.new(lens.outputs['Image'],mix.inputs[1]);ls.new(ghost.outputs['Image'],mix.inputs[2]);comp=ns.new('CompositorNodeComposite');comp.location=(420,120);ls.new(mix.outputs[0],comp.inputs['Image'])
# Visible solar disc at optical infinity; the Sun lamp alone casts the scene's shadows.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=46.5);disc=bpy.context.object;disc.name='SOLEIL — disque lointain pour les reflets optiques';sm=bpy.data.materials.new('Disque solaire — émission optique');sm.use_nodes=True;sn=sm.node_tree.nodes;sn.clear();em=sn.new('ShaderNodeEmission');em.inputs[0].default_value=(1,.90,.75,1);em.inputs[1].default_value=40;op=sn.new('ShaderNodeOutputMaterial');sm.node_tree.links.new(em.outputs[0],op.inputs[0]);disc.data.materials.append(sm)
for f in range(1,1218):
 s.frame_set(f);s.view_layers[0].update();direction=cam.matrix_world.to_quaternion()@Vector((0,0,-1));dot=direction.dot(sunvec);gate=.10*smooth((dot-math.cos(math.radians(25)))/(1-math.cos(math.radians(25))));mix.inputs[0].default_value=gate;mix.inputs[0].keyframe_insert('default_value',frame=f);disc.location=cam.matrix_world.translation+sunvec*10000;disc.keyframe_insert('location',frame=f);log[f-1]['flare_mix']=gate
cfg={'revision':'v8','fps':30,'frames':1217,'dead_zone_half_fraction':[.022,.025],'damping_time_constant_s':tau,'tracking_lag_limit_fraction':.05,'shake_max_amplitude_deg':[.22,.16,.12],'shake_modifiers':['NOISE','ENVELOPE'],'burnout_physical_s':1.73,'peak_positive_acceleration_time_s':peak,'peak_positive_acceleration_m_s2':maxacc,'dispersion':.0007,'flare_cone_deg':25,'flare_max_mix':.10,'solar_disc_diameter_deg':math.degrees(2*math.atan(46.5/10000)),'fstop_range':[2.8,7.1],'autofocus':'evaluated assembly bounding-box center','frame_count_unchanged':True,'audio':False,'note':'Artistic camera effects; no trajectory or force modification.'}
s['cinematography']=json.dumps(cfg);txt=bpy.data.texts.new('LIRE — Cinématographie v8');txt.write(json.dumps(cfg,indent=2));s.eevee.taa_render_samples=48;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=95;s.frame_set(1);s.view_layers[0].update();(w/'frames').mkdir(exist_ok=True);s.render.filepath=str(w/'frames/vol-')
(out/'donnees/cinematographie.json').write_text(json.dumps(cfg,indent=2),encoding='utf8');(out/'donnees/camera-par-image.json').write_text(json.dumps(log,indent=2),encoding='utf8');bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-cinematographie.blend'),compress=True)
for f in (1,75,95,230,400,650,977,1217):
 s.frame_set(f);s.view_layers[0].update();s.render.filepath=str(out/f'apercu-{f}.jpg');bpy.ops.render.render(write_still=True)
print('CAMERA_V8_READY',cfg,flush=True)
