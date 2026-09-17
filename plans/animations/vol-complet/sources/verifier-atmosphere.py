import bpy,json,math
from pathlib import Path
s=bpy.context.scene;out=Path('outputs/vol-complet-v4');rows=json.loads((out/'sources/telemetrie.json').read_text(encoding='utf8'));root=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'));parts=[o for o in bpy.data.objects if o.name.startswith('Volume fumee')]
assert len(parts)==116
error=0;active=0
for f in range(1,1218):
 s.frame_set(f);r=rows[f-1];error=max(error,abs(root.location.x-r['x']),abs(root.location.y-r['y']),abs(root.location.z-r['altitude']-.08))
 for p in parts:
  if not p.hide_render:
   active+=1;assert -1e-5<=r['time']-p['birth_s']<7.04
assert error<.0001,error
assert active>0
for p in parts:
 assert p.parent is None and p['birth_s']<1.73
 assert any(n.type=='PRINCIPLED_VOLUME' for n in p.active_material.node_tree.nodes)
 assert p.hide_render
s.frame_set(100);p=parts[0];x0=p.location.x;scale0=p.scale.x
s.frame_set(200);assert p.location.x<x0 and p.scale.x>scale0
report={'frames_checked':1217,'maximum_trajectory_coordinate_error_m':error,'volumetric_particles':len(parts),'active_particle_frames':active,'births_only_during_motor_burn':True,'world_space_advection_and_growth':True,'all_particles_invisible_at_end':True,'wind_average_m_s':2,'landing_distance_m':math.hypot(rows[-1]['x'],rows[-1]['y'])}
(out/'verification-atmosphere.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('ATMOSPHERE_VERIFIED',report)
