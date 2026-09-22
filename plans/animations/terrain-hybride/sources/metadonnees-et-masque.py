import bpy,json,math
from pathlib import Path
out=Path('outputs/terrain-hybride-v6').resolve();s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];ref=bpy.data.scenes['02 — Site SRTM géoréférencé'];spec=json.loads((out/'donnees/terrain-hybride.json').read_text(encoding='utf8'));pad=spec['pad_local_m']
for sc in (s,bpy.data.scenes['04 — Inspection du terrain hybride']):
 for k in ref.keys():
  if k in ('SRID','crs x','crs y','longitude','latitude','scale'):sc[k]=ref[k]
 sc['simulation']='OpenRocket 24.12 / H143 apogée idéale / vent moyen 2 m/s / CSV v4';sc['statut']='Animation illustrative v6 sur relief SRTM et orthophoto aérienne 2025';sc['crs']='EPSG:32618';sc['origin_elevation_m']=ref['origin_elevation_m'];sc['vertical_datum']='EGM96 EPSG:5773';sc['topography_note']='Hybrid terrain v6 integrated with visually adjusted v4 flight; original scenes 01 and 02 retained.'
bpy.context.window.scene=s;s.view_layers[0].update();s.frame_set(1);s.view_layers[0].update();bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-terrain-hybride.blend'))
# A diagnostic render evaluates the actual material mask through an emission surface.
debug=bpy.data.scenes.new('Contrôle temporaire du masque');bpy.context.window.scene=debug;debug.view_layers[0].update();bpy.ops.mesh.primitive_plane_add(size=90,location=(pad[0],pad[1],pad[2]));plane=bpy.context.object;mat=s.objects['TERRAIN HYBRIDE — orthophoto et terre PBR'].data.materials[0].copy();plane.data.materials.append(mat);ns=mat.node_tree.nodes;links=mat.node_tree.links;em=ns.new('ShaderNodeEmission');links.new(ns['MASQUE — fondu doux de 24 à 36 m'].outputs[0],em.inputs['Color']);links.new(em.outputs[0],ns['Surface finale'].inputs['Surface'])
camdata=bpy.data.cameras.new('Masque — vue orthographique');camdata.type='ORTHO';camdata.ortho_scale=90;cam=bpy.data.objects.new('Caméra masque',camdata);debug.collection.objects.link(cam);cam.location=(pad[0],pad[1],pad[2]+100);debug.camera=cam
debug.render.engine='BLENDER_EEVEE_NEXT';debug.eevee.taa_render_samples=16;debug.render.resolution_x=1000;debug.render.resolution_y=1000;debug.render.resolution_percentage=100;debug.view_settings.view_transform='Standard';debug.render.image_settings.file_format='PNG';debug.render.filepath=str(out/'masque-fusion.png');bpy.ops.render.render(write_still=True)
print('GEOREFERENCE',dict(s.items()),flush=True)
