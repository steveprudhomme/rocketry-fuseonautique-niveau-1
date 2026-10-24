"""Export camera-space vectors and body attitude for a qualitative educational overlay."""
import bpy,json
import numpy as np
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
out=Path('outputs/ath-v10');s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s
body=next(o for o in s.objects if o.name.startswith('Corps - pendule'));root=next(o for o in s.objects if o.name.startswith('CHASSE GALERIE'))
tele=json.loads(Path('outputs/cinematographie-v8/donnees/telemetrie.json').read_text());p=np.genfromtxt('outputs/cinematographie-v8/donnees/vol-h143.csv',delimiter=',',names=True);vx=np.gradient(p['x_m'],p['time_s']);vy=np.gradient(p['y_m'],p['time_s'])
records=[]
for r in tele:
 s.frame_set(r['frame']);s.view_layers[0].update();pos=body.matrix_world.translation+body.matrix_world.to_quaternion()@Vector((0,0,.6));base=world_to_camera_view(s,s.camera,pos)
 velocity=Vector((float(np.interp(r['time'],p['time_s'],vx)),float(np.interp(r['time'],p['time_s'],vy)),float(np.interp(r['time'],p['time_s'],p['vz_m_s']))))
 # Wind used by the source OpenRocket trajectory: westward 2 m/s.
 air=velocity-Vector((-2,0,0));directions={'gravite':Vector((0,0,-1)),'poussee':root.matrix_world.to_quaternion()@Vector((0,0,1)),'trainee':-air.normalized()}
 vectors={}
 for key,direction in directions.items():
  q=world_to_camera_view(s,s.camera,pos+direction*.25);d=Vector(((q.x-base.x)*1920,-(q.y-base.y)*1080));vectors[key]=list(d.normalized()) if d.length>.005 else None
 records.append({'frame':r['frame'],'anchor':[base.x*1920,(1-base.y)*1080],'vectors':vectors,'body_rotation':[list(row) for row in body.matrix_world.to_quaternion().to_matrix()]})
(out/'donnees/projections.json').write_text(json.dumps(records,separators=(',',':')),encoding='utf8');print('PROJECTIONS_EXPORTED',len(records))
