"""Read-only verification of the reopened Blender deliverable."""
import bpy,json,numpy as np
from pathlib import Path
out=Path('outputs/topographie-v5');meta=json.loads((out/'donnees/georeferencement.json').read_text(encoding='utf8'));data=np.load(out/'donnees/terrain-srtm.npz')
scene=bpy.data.scenes['02 — Site SRTM géoréférencé'];ref=bpy.data.scenes['01 — Vol v4 de référence'];ob=next(o for o in scene.objects if o.name.startswith('Terrain SRTM réel'))
actual=np.array([tuple(v.co) for v in ob.data.vertices]);error=float(np.max(np.abs(actual-data['vertices'])))
assert error<.001 and len(ob.data.polygons)==56715
assert scene['SRID']=='EPSG:32618'
assert abs(scene['crs x']-meta['origin_easting_m'])<1e-6
assert abs(scene['crs y']-meta['origin_northing_m'])<1e-6
assert scene.unit_settings.scale_length==1 and scene['vertical_exaggeration']==1
assert ref.frame_end==1217 and scene.frame_end==240
root=next(o for o in ref.objects if o.name.startswith('CHASSE GALERIE'));tele=json.loads(Path('outputs/vol-complet-v4/sources/telemetrie.json').read_text(encoding='utf8'));flight_error=0
bpy.context.window.scene=ref
ref.view_layers[0].update()
for f in [1,85,369,650,977,1217]:
 ref.frame_set(f);ref.view_layers[0].update();r=tele[f-1];flight_error=max(flight_error,abs(root.location.x-r['x']),abs(root.location.y-r['y']),abs(root.location.z-r['altitude']-.08))
assert flight_error<.001
assert all(i.packed_file is not None for i in bpy.data.images if i.source=='FILE' and i.filepath)
report={'reopened_blend':True,'native_vertices_checked':len(actual),'mesh_error_m':error,'reference_flight_samples_checked':6,'reference_flight_error_m':flight_error,'georeference_matches_metadata':True,'vertical_exaggeration':1,'all_file_textures_packed':True,'topography_animation_frames':240}
(out/'verification-reouverture.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('REOPENED_VERIFIED',report)
