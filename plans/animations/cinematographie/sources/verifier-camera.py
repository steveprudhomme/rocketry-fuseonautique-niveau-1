import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
out=Path('outputs/cinematographie-v8');s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s;s.view_layers[0].update();cam=s.camera;shake=s.objects['CAMÉRA — secousse moteur native'];focus=s.objects['CAMÉRA — mise au point adaptative'];tele=json.loads(Path('outputs/vol-complet-v4/sources/telemetrie.json').read_text(encoding='utf8'));body=next(o for o in s.objects if o.name.startswith('Corps - pendule'));payload=next(o for o in s.objects if o.name.startswith('Section avant separee'));canopy=next(o for o in s.objects if o.name.startswith('Parachute 36'));bounds=[];cocs=[];background=[];amplitudes=[];outside=[]
for f in range(1,1218):
 s.frame_set(f);s.view_layers[0].update();dg=bpy.context.evaluated_depsgraph_get();points=[]
 for o in list(body.children)+list(payload.children)+([canopy] if tele[f-1]['time']>=10.1954595315 else []):
  if o.type=='MESH':points.extend([o.matrix_world@Vector(v) for v in o.evaluated_get(dg).bound_box])
 projection=[world_to_camera_view(s,cam,p) for p in points];bounds.append([min(p.x for p in projection),min(p.y for p in projection),max(p.x for p in projection),max(p.y for p in projection)]);assert all(p.z>0 for p in projection)
 inv=cam.matrix_world.inverted();distance=-(inv@focus.matrix_world.translation).z;focal=cam.data.lens/1000;n=cam.data.dof.aperture_fstop
 c=[focal*focal*abs(p.z-distance)/(n*p.z*(distance-focal))*1920/(cam.data.sensor_width/1000) for p in projection];cocs.append(max(c));background.append(focal*focal/(n*(distance-focal))*1920/(cam.data.sensor_width/1000));a=max(abs(v) for v in shake.rotation_euler);amplitudes.append(math.degrees(a))
 if f<61 or f>113:outside.append(a)
b=np.array(bounds);assert b[:,:2].min()>.025 and b[:,2:].max()<.975,(b.min(axis=0),b.max(axis=0));assert max(outside)<1e-7;assert .001<max(amplitudes)<.5,max(amplitudes);assert max(cocs)<4,max(cocs)
fcs=shake.animation_data.action.fcurves;assert all([m.type for m in fc.modifiers]==['NOISE','ENVELOPE'] for fc in fcs)
report={'frames_checked':1217,'subject_bounds_min_xy':b[:,:2].min(axis=0).tolist(),'subject_bounds_max_xy':b[:,2:].max(axis=0).tolist(),'minimum_frame_margin':min(float(b[:,:2].min()),float(1-b[:,2:].max())),'maximum_shake_component_deg':max(amplitudes),'shake_outside_burn_max_rad':max(outside),'subject_max_circle_of_confusion_px':max(cocs),'background_infinity_blur_diameter_px_range':[min(background),max(background)],'native_noise_and_envelope':True,'flare_gate_max_in_flight':max(r['flare_mix'] for r in json.loads((out/'donnees/camera-par-image.json').read_text())),'note':'Optical blur estimates use thin-lens formula, not a pixel-level MTF measurement.'}
(out/'verification-camera.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('CAMERA_VERIFIED',report,flush=True)
