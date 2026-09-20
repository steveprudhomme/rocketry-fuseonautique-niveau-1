"""Blender 4.3: native SRTM terrain and BlenderGIS georeference, plus intact v4 scene."""
import bpy,numpy as np,json,math,sys,os,importlib
from pathlib import Path
from mathutils import Vector
w=Path('work/topographie-v5').resolve();out=Path('outputs/topographie-v5').resolve();m=json.loads((out/'donnees/georeferencement.json').read_text(encoding='utf8'));d=np.load(out/'donnees/terrain-srtm.npz');verts=d['vertices'];rows,cols=d['heights'].shape
# Load official addon locally; keep its cache in this project's temporary directory.
os.environ['PYTHONHTTPSVERIFY']='1';os.environ['IMAGEIO_USERDIR']=str(w/'cache/imageio');os.environ['IMAGEIO_NO_INTERNET']='1';sys.path.insert(0,str(w/'addons'));bgis=importlib.import_module('BlenderGIS-master');GeoScene=importlib.import_module('BlenderGIS-master.geoscene').GeoScene;UTM=importlib.import_module('BlenderGIS-master.core.proj.utm').UTM;proj=UTM(18,True)
reference=bpy.context.scene;reference.name='01 — Vol v4 de référence';reference['topography_note']='Animation v4 retained intact; terrain is in scene 02. No terrain-aware trajectory calculation performed.'
s=bpy.data.scenes.new('02 — Site SRTM géoréférencé');bpy.context.window.scene=s;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
geo=GeoScene(s);geo.crs='EPSG:32618';geo.setOriginGeo(m['longitude'],m['latitude']);assert geo.isGeoref
s['vertical_datum']='EGM96 EPSG:5773';s['origin_elevation_m']=m['origin_elevation_egm96_m'];s['vertical_exaggeration']=1.;s['source']='NASA/NGA SRTM GL1 v3 / OpenTopography';s['reference_only']='Intersection is the geographic origin. Actual launch pad has not been surveyed.'
terrain_collection=bpy.data.collections.new('TOPO — Maillage SRTM natif');s.collection.children.link(terrain_collection)
guides=bpy.data.collections.new('TOPO — Repères et routes OSM');s.collection.children.link(guides)
def material(name,color,emission=False):
 mat=bpy.data.materials.new(name);mat.diffuse_color=(*color,1);mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.88
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=.2
 return mat
faces=[(j*cols+i,(j+1)*cols+i,(j+1)*cols+i+1,j*cols+i+1) for j in range(rows-1) for i in range(cols-1)]
mesh=bpy.data.meshes.new('SRTM — 1 seconde d’arc — sommets natifs');mesh.from_pydata(verts.tolist(),[],faces);mesh.update();terrain=bpy.data.objects.new('Terrain SRTM réel — 57 200 sommets',mesh);terrain_collection.objects.link(terrain)
terrain['native_spacing_arcsec']=1.;terrain['elevation_offset_m']=m['origin_elevation_egm96_m'];terrain['modified_heights']=False
mat=material('Teintes altimétriques — aucune texture satellite',(.42,.48,.39));terrain.data.materials.append(mat);ns=mat.node_tree.nodes;ls=mat.node_tree.links;geoNode=ns.new('ShaderNodeNewGeometry');sep=ns.new('ShaderNodeSeparateXYZ');ls.new(geoNode.outputs['Position'],sep.inputs[0]);rng=ns.new('ShaderNodeMapRange');rng.inputs['From Min'].default_value=10-m['origin_elevation_egm96_m'];rng.inputs['From Max'].default_value=59-m['origin_elevation_egm96_m'];ls.new(sep.outputs['Z'],rng.inputs[0]);ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1]);colors=[(0,(.07,.18,.23,1)),(.25,(.12,.29,.28,1)),(.55,(.30,.43,.34,1)),(.8,(.58,.60,.42,1)),(1,(.84,.75,.56,1))]
for i,(t,c) in enumerate(colors):
 e=ramp.color_ramp.elements[0] if i==0 else ramp.color_ramp.elements.new(t);e.position=t;e.color=c
ls.new(rng.outputs[0],ramp.inputs[0]);ls.new(ramp.outputs[0],ns.get('Principled BSDF').inputs['Base Color'])
for p in mesh.polygons:p.use_smooth=True
def height(x,y):
 lon,lat=proj.utm_to_lonlat(x+m['origin_easting_m'],y+m['origin_northing_m']);u=(lon-d['lons'][0])*3600;v=(d['lats'][0]-lat)*3600;i=max(0,min(cols-2,int(u)));j=max(0,min(rows-2,int(v)));a=max(0,min(1,u-i));b=max(0,min(1,v-j));z=d['heights'];return float((z[j,i]*(1-a)+z[j,i+1]*a)*(1-b)+(z[j+1,i]*(1-a)+z[j+1,i+1]*a)*b)-m['origin_elevation_egm96_m']
def curve(name,points,width,mat):
 data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=1;data.bevel_depth=width;data.bevel_resolution=2;sp=data.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,data);guides.objects.link(ob);ob.data.materials.append(mat);return ob
roadmat=material('Routes OSM — repères blancs',(.90,.88,.76),True);accent=material('Intersection — corail',(.95,.16,.075),True)
roads=json.loads((out/'donnees/routes-locales.json').read_text(encoding='utf8'))
for road in roads:
 points=[]
 for a,b in zip(road['vertices'],road['vertices'][1:]):
  a,b=Vector(a),Vector(b);count=max(2,math.ceil((b-a).length/15))
  for i in range(count):
   p=a.lerp(b,i/count)
   if abs(p.x)>3100 or abs(p.y)>3100:continue
   points.append((p.x,p.y,height(p.x,p.y)+2))
 ob=curve(road['name']+' — axe OSM',points,5,roadmat);ob['osm_way_id']=road['osm_way_id'];ob['display_width_m']=10;ob['width_is_symbolic']=True
origin=bpy.data.objects.new('Origine — rang Letendre × 10e Rang',None);guides.objects.link(origin);origin.empty_display_type='PLAIN_AXES';origin.empty_display_size=100;origin['latitude']=m['latitude'];origin['longitude']=m['longitude'];origin['osm_node']=540514913
curve('Repère vertical de l’intersection',[(0,0,1),(0,0,125)],4,accent)
curve('Cercle de localisation',[(60*math.cos(t*math.tau/64),60*math.sin(t*math.tau/64),height(60*math.cos(t*math.tau/64),60*math.sin(t*math.tau/64))+3) for t in range(65)],3,accent)
# Camera and lights for an eight-second topographic overview, true vertical scale.
camdata=bpy.data.cameras.new('Caméra topographique');cam=bpy.data.objects.new('Caméra topographique',camdata);s.collection.objects.link(cam);s.camera=cam;camdata.clip_end=30000;camdata.lens=48
target=Vector((0,0,-20))
for f in range(1,241):
 angle=math.radians(-115+32*(f-1)/239);cam.location=(5100*math.cos(angle),5100*math.sin(angle),4200);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
sunData=bpy.data.lights.new('Soleil topographique','SUN');sunData.energy=2.8;sun=bpy.data.objects.new('Soleil topographique',sunData);s.collection.objects.link(sun);sun.rotation_euler=(math.radians(48),math.radians(-25),math.radians(-40))
s.world=bpy.data.worlds.new('Fond topographique');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.16,.20,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.7
s.render.engine='BLENDER_EEVEE_NEXT';s.eevee.taa_render_samples=32;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=30;s.frame_start=1;s.frame_end=240;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG';s.render.filepath=str(w/'frames/topo-');s.frame_set(120)
text=bpy.data.texts.new('LIRE — Géoréférencement et limites');text.write(json.dumps(m,ensure_ascii=False,indent=2)+'\n\nScene 01: preserved v4 animation. Scene 02: true-scale SRTM base ready for terrain shading. No satellite imagery or surveyed pad included. Road widths are symbolic.\n')
# Set a useful opening viewport.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.clip_end=30000
all_errors=np.array([tuple(v.co) for v in mesh.vertices])-verts;assert abs(all_errors).max()<.001
report={'blendergis_version':list(bgis.bl_info['version']),'georeferenced':geo.isGeoref,'crs':geo.crs,'origin':[geo.crsx,geo.crsy],'vertices':len(mesh.vertices),'faces':len(mesh.polygons),'mesh_float_precision_error_m':float(abs(all_errors).max()),'height_samples_modified':False,'scale':1,'scene_v4_preserved':reference.frame_end==1217,'scene_topography_frames':240}
(out/'verification-topographie.json').write_text(json.dumps(report,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-topographie.blend'));s.render.filepath=str(out/'apercu-topographie.png');bpy.ops.render.render(write_still=True);s.render.filepath=str(w/'frames/topo-');bpy.ops.render.render(animation=True)
print('TOPOGRAPHY_READY',report,flush=True)
