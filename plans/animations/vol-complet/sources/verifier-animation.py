import bpy,json,csv,math,sys
from pathlib import Path
base=Path(sys.argv[sys.argv.index('--')+1]);rows=json.loads((base/'work/vol-complet/telemetrie.json').read_text())
scene=bpy.context.scene;rocket=next(o for o in bpy.data.objects if o.name.startswith('CHASSE GALERIE'))
assert scene.frame_end==1035 and scene.render.fps==30
assert (scene.render.resolution_x,scene.render.resolution_y)==(1920,1080)
maxerr=0
for r in rows:
 scene.frame_set(r['frame']);maxerr=max(maxerr,abs(rocket.location.z-(r['altitude']+.08)))
assert maxerr<.0001,maxerr
assert abs(rows[-1]['time']-106.84268527829295)<1e-6
assert rows[-1]['altitude']==0
images=[i for i in bpy.data.images if i.source=='FILE'];assert len(images)>=2 and all(i.packed_file for i in images)
print('VERIFIED',json.dumps(dict(frames=len(rows),max_altitude_error_m=maxerr,packed_textures=len(images),end_time_s=rows[-1]['time'])))
