"""Read-only checks of the reopened v3 scene; outputs a JSON QA report."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]);tele=json.loads(Path(args[1]).read_text(encoding='utf8'))
scene=bpy.context.scene;body=bpy.data.objects['Corps - pendule et atterrissage'];payload=bpy.data.objects['Section avant separee'];root=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'));rope=bpy.data.objects['Corde de choc - simulation Soft Body integree'];canopy=next(o for o in bpy.data.objects if o.name.startswith('Parachute 36'));susp=[o for o in bpy.data.objects if o.name.startswith('Suspente')]
terrain=bpy.data.objects['Champ laboure et sillons'];terrain_max=max((terrain.matrix_world@v.co).z for v in terrain.data.vertices)
minimum={'body':float('inf'),'payload':float('inf'),'canopy':float('inf'),'rope':float('inf')};pin_error=0;maxroot=0;lengths=[];tilts=[];yaws=[]
frames=sorted(set(range(369,977,8))|set(range(977,1218)))
for f in frames:
 scene.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();dg.update()
 maxroot=max(maxroot,abs(root.location.z-tele[f-1]['altitude']-.08))
 for name,objects in [('body',body.children),('payload',payload.children),('canopy',[canopy]),('rope',[rope])]:
  for o in objects:
   if o.type!='MESH':continue
   ev=o.evaluated_get(dg)
   minimum[name]=min(minimum[name],min((o.matrix_world@v.co).z for v in ev.data.vertices))
 ev=rope.evaluated_get(dg);pts=[sum((ev.data.vertices[i+k].co for k in range(8)),Vector())/8 for i in range(0,len(ev.data.vertices),8)]
 start=rope.matrix_world@pts[0];end=rope.matrix_world@pts[-1];attachment=body.matrix_world@Vector((0,0,.5842));pin_error=max(pin_error,(start-attachment).length)
 for o in susp:pin_error=max(pin_error,(o.matrix_world@Vector(o.data.splines[0].points[0].co[:3])-end).length)
 if f>=977:lengths.append(sum((a-b).length for a,b in zip(pts,pts[1:])))
 if 440<f<965:
  tilts.append(math.degrees(math.acos(max(-1,min(1,(body.rotation_euler.to_matrix()@Vector((0,0,1))).z)))))
  yaws.append(math.degrees(body.rotation_euler.z))
assert all(v>terrain_max for v in minimum.values()),(minimum,terrain_max)
assert pin_error<1e-4,pin_error
assert maxroot<1e-4,maxroot
assert max(tilts)>3 and max(yaws)-min(yaws)>6
assert min(lengths)>4.57 and max(lengths)<4.572*1.05,(min(lengths),max(lengths))
scene.frame_set(1217);dg=bpy.context.evaluated_depsgraph_get();dg.update();canopy_z=[(canopy.matrix_world@v.co).z for v in canopy.evaluated_get(dg).data.vertices]
assert max(canopy_z)-min(canopy_z)<.06
assert abs((body.matrix_world.to_3x3()@Vector((0,0,1))).z)<.01
assert abs((payload.matrix_world.to_3x3()@Vector((0,0,1))).z)<.01
report={'checked_frames':len(frames),'contact_frame':977,'frames':1217,'fps':30,'duration_s':1217/30,'post_contact_s':8,'terrain_max_vertex_z_m':terrain_max,'minimum_visible_geometry_z_m':minimum,'maximum_attachment_error_m':pin_error,'root_altitude_error_m':maxroot,'impact_cord_length_range_m':[min(lengths),max(lengths)],'observed_airborne_max_tilt_deg':max(tilts),'observed_yaw_range_deg':[min(yaws),max(yaws)],'final_canopy_thickness_m':max(canopy_z)-min(canopy_z),'final_bodies_horizontal':True,'physics_scope':'keyframed landing with geometric support plane; not a physical impact prediction'}
out.write_text(json.dumps(report,indent=2),encoding='utf8');print('LANDING_VERIFIED',json.dumps(report),flush=True)
