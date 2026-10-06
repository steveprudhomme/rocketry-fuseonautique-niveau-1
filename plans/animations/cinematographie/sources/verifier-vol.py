"""Reopen final scene and check terrain/material structure, flight and contacts."""
import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
out=Path('outputs/cinematographie-v8');s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s;s.view_layers[0].update();spec=json.loads((out/'donnees/terrain-hybride.json').read_text(encoding='utf8'));tele=json.loads(Path('outputs/vol-complet-v4/sources/telemetrie.json').read_text(encoding='utf8'));pad=Vector(spec['pad_local_m']);land=Vector(spec['landing_local_m'])
terrain=s.objects['TERRAIN HYBRIDE — orthophoto et terre PBR'];ns=terrain.data.materials[0].node_tree.nodes;mask=ns['MASQUE — fondu doux de 24 à 36 m'];assert mask.interpolation_type=='SMOOTHSTEP' and mask.inputs['From Min'].default_value==24 and mask.inputs['From Max'].default_value==36
assert ns['Orthophoto ouverte 2025 — RGB, 2 m/pixel'].image.packed_file
root=next(o for o in s.objects if o.name.startswith('CHASSE GALERIE'));body=next(o for o in s.objects if o.name.startswith('Corps - pendule'));payload=next(o for o in s.objects if o.name.startswith('Section avant separee'));canopy=next(o for o in s.objects if o.name.startswith('Parachute 36'));rope=next(o for o in s.objects if o.name.startswith('Corde de choc - simulation'))
maximum=0;minimum={'body':1e9,'payload':1e9,'canopy':1e9,'rope':1e9};clearance=1e9
for f in range(1,1218):
 s.frame_set(f);s.view_layers[0].update();t=max(0,min(1,(f-900)/77));t=t*t*(3-2*t);r=tele[f-1];expected=Vector((r['x']+pad.x,r['y']+pad.y,r['altitude']+.08+pad.z+(land.z-pad.z)*t));maximum=max(maximum,(root.matrix_world.translation-expected).length)
 hit=terrain.ray_cast(Vector((expected.x,expected.y,2000)),Vector((0,0,-1)));assert hit[0];clearance=min(clearance,expected.z-hit[1].z)
 if f>=977:
  dg=bpy.context.evaluated_depsgraph_get()
  for key,obs in [('body',body.children),('payload',payload.children),('canopy',[canopy]),('rope',[rope])]:
   for ob in obs:
    if ob.type!='MESH':continue
    ev=ob.evaluated_get(dg);coords=np.empty(len(ev.data.vertices)*3);ev.data.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3);mw=np.array(ob.matrix_world);world=coords@mw[:3,:3].T+mw[:3,3];minimum[key]=min(minimum[key],float(world[:,2].min()-land.z))
    # All post-contact parts fit inside the flat rendered landing support.
    assert np.hypot(world[:,0]-land.x,world[:,1]-land.y).max()<12
assert maximum<.001,maximum
assert min(minimum.values())>0,minimum
assert clearance>.03,clearance
native=next(o for o in bpy.data.scenes['02 — Site SRTM géoréférencé'].objects if o.name.startswith('Terrain SRTM'))
v=np.array([list(v.co) for v in native.data.vertices]);original=np.load('outputs/topographie-v5/donnees/terrain-srtm.npz')['vertices'];err=float(abs(v-original).max());assert err<.001
report={'checked_flight_frames':1217,'checked_post_contact_frames':241,'maximum_transformed_trajectory_error_m':maximum,'minimum_root_clearance_m':clearance,'minimum_post_contact_clearance_m':minimum,'native_srtm_reference_error_m':err,'packed_orthophoto':True,'smoothstep_mask_24_36m':True,'support_flat_radius_m':16,'support_visual_max_height_edit_m':spec['render_support_max_height_change_m'],'physics_note':'Checks include the documented visual Z contact adjustment, not a new OpenRocket terrain simulation.'}
(out/'verification-vol-terrain.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('VERIFIED',report,flush=True)
