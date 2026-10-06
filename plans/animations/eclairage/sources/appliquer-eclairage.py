"""Apply corrected orthophoto and solar direction; retain v6 flight and geometry."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path('outputs/eclairage-v7').resolve();w=Path('work/eclairage-v7').resolve();cfg=json.loads((out/'donnees/eclairage.json').read_text(encoding='utf8'));s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];review=bpy.data.scenes['04 — Inspection du terrain hybride'];bpy.context.window.scene=s;s.view_layers[0].update()
terrain=s.objects['TERRAIN HYBRIDE — orthophoto et terre PBR'];mat=terrain.data.materials[0];tex=mat.node_tree.nodes['Orthophoto ouverte 2025 — RGB, 2 m/pixel'];tex.image=bpy.data.images.load(str(out/'donnees/orthophoto-ombres-attenuees.png'));tex.image.pack();tex.label='Orthophoto 2025 — ombres atténuées dans le compositeur';az=math.radians(cfg['sun_azimuth_utm_deg']);el=math.radians(cfg['sun_elevation_deg']);ray=Vector((-math.sin(az)*math.cos(el),-math.cos(az)*math.cos(el),-math.sin(el)))
sun=[]
for o in s.objects:
 if o.type=='LIGHT' and o.data.type=='SUN':
  o.rotation_euler=ray.to_track_quat('-Z','Y').to_euler();o.data.energy=cfg['sun_energy'];o.data.angle=cfg['sun_angular_size_rad'];sun.append(o.name)
 elif o.type=='LIGHT':o.data.use_shadow=False
for scene in (s,review):scene['lighting_revision']='v7 — masked compositor correction; approximate shadow-derived sun azimuth';scene['lighting_parameters']=json.dumps(cfg,ensure_ascii=False)
s.frame_set(1);s.view_layers[0].update();s.render.filepath=str(w/'frames/vol-');(w/'frames').mkdir(exist_ok=True);(w/'detail').mkdir(exist_ok=True);review.render.filepath=str(w/'detail/terrain-');bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-eclairage.blend'),compress=True)
for f in (1,115,230,650,1217):
 s.frame_set(f);s.view_layers[0].update();s.render.filepath=str(out/f'apercu-vol-{f}.jpg');bpy.ops.render.render(write_still=True)
s.frame_set(1);s.view_layers[0].update();s.render.filepath=str(w/'frames/vol-');bpy.ops.render.render(animation=True)
bpy.context.window.scene=review;review.view_layers[0].update();review.frame_set(1);review.view_layers[0].update();review.render.filepath=str(w/'detail/terrain-');bpy.ops.render.render(animation=True);print('LIGHTING_RENDERED',sun,flush=True)
