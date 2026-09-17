"""Check the reopened delivery scene against the native-solver data and flight telemetry."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
base=Path(sys.argv[sys.argv.index('--')+1]);sim=json.loads((base/'work/recuperation-v2/corde-simulation.json').read_text());rows=json.loads((base/'outputs/vol-complet/sources/telemetrie.json').read_text())
scene=bpy.context.scene;rope=bpy.data.objects['Corde de choc - simulation Soft Body integree'];canopy=next(o for o in bpy.data.objects if o.name.startswith('Parachute 36'));root=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'))
assert len(rope.data.shape_keys.key_blocks)==601
assert sim['max_pin_error_m']<1e-4
assert sim['max_length_m']/sim['rest_length_m']<1.03
assert all(math.isfinite(v) for s in sim['samples'] for p in s['points'] for v in p)
apo=10.245999999999869;prev=0;maxerr=0;maxflight=0;first=None;last=None
for r in rows:
 scene.frame_set(r['frame']);age=max(0,r['time']-apo);value=canopy.data.shape_keys.key_blocks[1].value
 assert value>=prev-1e-5;prev=value
 maxflight=max(maxflight,abs(root.location.z-r['altitude']-.08))
 if value>0 and first is None:first=r['time']
 if value>=.99999 and last is None:last=r['time']
 if r['time']<apo:assert rope.hide_render
 else:
  assert not rope.hide_render
  dg=bpy.context.evaluated_depsgraph_get();ev=rope.evaluated_get(dg)
  bot=sum((v.co for v in ev.data.vertices[:8]),Vector())/8;top=sum((v.co for v in ev.data.vertices[-8:]),Vector())/8
  ix=min(600,age*60);i=int(ix);j=min(600,i+1);alpha=ix-i
  for p,k in [(bot,0),(top,-1)]:
   expected=Vector(sim['samples'][i]['points'][k]).lerp(Vector(sim['samples'][j]['points'][k]),alpha);maxerr=max(maxerr,(p-expected).length)
  if r['frame']%5==0:
   ce=canopy.evaluated_get(dg)
   for v in ce.data.vertices:
    q=world_to_camera_view(scene,scene.camera,ce.matrix_world@v.co)
    assert .01<q.x<.99 and .01<q.y<.99,(r['frame'],tuple(q))
assert maxerr<.0001,maxerr
assert maxflight<.0001,maxflight
assert 1.45<last-first<1.55,(first,last)
report={'native_solver':sim['solver'],'samples':601,'nodes':sim['nodes'],'rest_length_m':sim['rest_length_m'],'maximum_length_m':sim['max_length_m'],'maximum_extension_percent':100*(sim['max_length_m']/sim['rest_length_m']-1),'maximum_pin_error_m':sim['max_pin_error_m'],'baked_endpoint_error_m':maxerr,'flight_altitude_error_m':maxflight,'inflation_duration_s':1.5,'first_inflation_sample_s':first,'first_full_sample_s':last,'canopy_framing':'passed every fifth frame after deployment'}
(base/'outputs/vol-complet-v2/verification-recuperation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('RECOVERY_VERIFIED',json.dumps(report))
