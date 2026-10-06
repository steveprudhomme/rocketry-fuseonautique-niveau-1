import bpy,json,math
from mathutils import Vector
from pathlib import Path
out=Path('outputs/eclairage-v7');s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s;s.frame_set(1);s.view_layers[0].update();cfg=json.loads((out/'donnees/eclairage.json').read_text(encoding='utf8'));suns=[o for o in s.objects if o.type=='LIGHT' and o.data.type=='SUN'];assert len(suns)==1
sun=suns[0];direction=(sun.matrix_world.to_quaternion()@Vector((0,0,1))).normalized();az=math.degrees(math.atan2(direction.x,direction.y))%360;el=math.degrees(math.asin(direction.z));assert abs(az-cfg['sun_azimuth_utm_deg'])<.001 and abs(el-50)<.001
tex=s.objects['TERRAIN HYBRIDE — orthophoto et terre PBR'].data.materials[0].node_tree.nodes['Orthophoto ouverte 2025 — RGB, 2 m/pixel'].image;assert tex.packed_file and list(tex.size)==[5000,4000]
report={'sun_count':len(suns),'sun_azimuth_utm_deg':az,'shadow_azimuth_utm_deg':(az+180)%360,'sun_elevation_deg':el,'solar_direction_numeric_error_deg':abs(az-cfg['sun_azimuth_utm_deg']),'visual_estimation_uncertainty_deg':10,'elevation_is_artistic':True,'texture_size':list(tex.size),'texture_packed':True,'fill_light_shadows_disabled':all(not o.data.use_shadow for o in s.objects if o.type=='LIGHT' and o.data.type!='SUN')}
(out/'verification-eclairage.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('SUN_VERIFIED',report,flush=True)
