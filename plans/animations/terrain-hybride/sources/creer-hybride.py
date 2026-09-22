"""Blender 4.3: hybrid orthophoto/PBR terrain integrated into the existing flight."""
import bpy,numpy as np,json,math,random
from pathlib import Path
from mathutils import Vector
out=Path('outputs/terrain-hybride-v6').resolve();w=Path('work/terrain-hybride-v6').resolve();spec=json.loads((out/'donnees/terrain-hybride.json').read_text(encoding='utf8'));data=np.load(out/'donnees/hybride.npz');pad=Vector(data['pad']);land=Vector(data['landing'])
bpy.context.window.scene=bpy.data.scenes['01 — Vol v4 de référence'];bpy.context.view_layer.update();bpy.ops.scene.new(type='FULL_COPY');s=bpy.context.scene;s.name='03 — Vol complet sur terrain hybride';s.view_layers[0].update()
def empty(name):
 o=bpy.data.objects.new(name,None);s.collection.objects.link(o);return o
anchor=empty('VOL — translation vers le site et raccord de contact');static=empty('PAS DE TIR — emplacement illustratif réglable');static.location=pad
roots=[o for o in s.objects if o.parent is None and o not in (anchor,static)]
for o in roots:
 if o.name.startswith(('Champ laboure','Chaumes de mais','Feuillage','Terre horizon','Soleil a travers')):
  o.hide_render=True;o.hide_viewport=True;continue
 o.parent=anchor if o.animation_data or o.name.startswith('Volume fumee') else static
for f in range(1,1218):
 t=max(0,min(1,(f-900)/77));t=t*t*(3-2*t);anchor.location=(pad.x,pad.y,pad.z+(land.z-pad.z)*t);anchor.keyframe_insert('location',frame=f)
for fc in anchor.animation_data.action.fcurves:
 for k in fc.keyframe_points:k.interpolation='LINEAR'
s['terrain_spec']=json.dumps(spec,ensure_ascii=False);s['flight_data_note']='OpenRocket v4 CSV preserved. X/Y translated to provisional pad. Z visually adjusted between frames 900 and 977 to the SRTM landing support; not terrain-aware flight physics.'
# Dense render mesh; original SRTM scene 02 remains unchanged.
xyz=data['patch_xyz'];nr,nc=xyz.shape[:2];verts=xyz.reshape(-1,3);idx=np.arange((nr-1)*(nc-1));j=idx//(nc-1);i=idx%(nc-1);a=j*nc+i;faces=np.stack((a,a+nc,a+nc+1,a+1),axis=1)
mesh=bpy.data.meshes.new('SRTM — interpolation de rendu ×3, appuis visuels');mesh.from_pydata(verts.tolist(),[],faces.tolist());mesh.update();terrain=bpy.data.objects.new('TERRAIN HYBRIDE — orthophoto et terre PBR',mesh);s.collection.objects.link(terrain)
uv=mesh.uv_layers.new(name='MTM8 — orthophoto 2025');loopidx=np.empty(len(mesh.loops),dtype=np.int32);mesh.loops.foreach_get('vertex_index',loopidx);uv.data.foreach_set('uv',data['patch_uv'].reshape(-1,2)[loopidx].ravel());mesh.polygons.foreach_set('use_smooth',np.ones(len(mesh.polygons),dtype=bool))
mat=bpy.data.materials.new('SOL HYBRIDE — orthophoto / terre / chaumes — rayon 30 m');mat.use_nodes=True;mesh.materials.append(mat);ns=mat.node_tree.nodes;ls=mat.node_tree.links;ns.clear()
def node(typ,name,x,y):
 n=ns.new(typ);n.name=name;n.label=name;n.location=(x,y);return n
def connect(a,out,b,inp):ls.new(a.outputs[out],b.inputs[inp])
output=node('ShaderNodeOutputMaterial','Surface finale',1200,180)
tex=node('ShaderNodeTexImage','Orthophoto ouverte 2025 — RGB, 2 m/pixel',-1000,600);tex.image=bpy.data.images.load(str(out/'donnees/orthophoto-2025-2m.jpg'));tex.image.pack();tex.interpolation='Linear';tex.extension='EXTEND'
uvnode=node('ShaderNodeUVMap','Coordonnées MTM8 reprojetées vers UTM18',-1250,600);uvnode.uv_map=uv.name;connect(uvnode,'UV',tex,'Vector')
globalbs=node('ShaderNodeBsdfPrincipled','Vue aérienne — orthophoto',650,400);connect(tex,'Color',globalbs,'Base Color');globalbs.inputs['Roughness'].default_value=.94
geo=node('ShaderNodeNewGeometry','Position en mètres',-1400,-100);sep=node('ShaderNodeSeparateXYZ','Plan horizontal',-1200,-100);connect(geo,'Position',sep,0);xy=node('ShaderNodeCombineXYZ','XY sans altitude',-1000,-100);connect(sep,'X',xy,'X');connect(sep,'Y',xy,'Y')
sub=node('ShaderNodeVectorMath','Centre du pas de tir',-800,-100);sub.operation='SUBTRACT';sub.inputs[1].default_value=(pad.x,pad.y,0);connect(xy,0,sub,0)
length=node('ShaderNodeVectorMath','Distance horizontale au départ',-600,-100);length.operation='LENGTH';connect(sub,0,length,0)
mask=node('ShaderNodeMapRange','MASQUE — fondu doux de 24 à 36 m',-380,0);mask.interpolation_type='SMOOTHSTEP';mask.clamp=True;mask.inputs['From Min'].default_value=24;mask.inputs['From Max'].default_value=36;mask.inputs['To Min'].default_value=1;mask.inputs['To Max'].default_value=0;connect(length,'Value',mask,'Value')
noise=node('ShaderNodeTexNoise','Terre — agrégats de 6 cm',-800,-430);noise.inputs['Scale'].default_value=17;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.7;connect(geo,'Position',noise,'Vector')
fine=node('ShaderNodeTexNoise','Terre — grain millimétrique',-800,-720);fine.inputs['Scale'].default_value=380;fine.inputs['Detail'].default_value=2;connect(geo,'Position',fine,'Vector')
color=node('ShaderNodeValToRGB','Nuances de terre sèche',-480,-300);color.color_ramp.elements[0].color=(.22,.17,.11,1);color.color_ramp.elements[1].color=(.65,.55,.39,1);connect(noise,'Fac',color,'Fac')
tint=node('ShaderNodeMixRGB','Conserver les grandes teintes du champ',-40,390);tint.blend_type='MULTIPLY';tint.inputs[0].default_value=.28;connect(tex,'Color',tint,1);connect(color,'Color',tint,2)
bumpfine=node('ShaderNodeBump','Microrelief — 1,5 mm',-350,-640);bumpfine.inputs['Strength'].default_value=.55;bumpfine.inputs['Distance'].default_value=.0015;connect(fine,'Fac',bumpfine,'Height')
bump=node('ShaderNodeBump','Mottes — 8 mm',-60,-340);bump.inputs['Strength'].default_value=.65;bump.inputs['Distance'].default_value=.008;connect(noise,'Fac',bump,'Height');connect(bumpfine,'Normal',bump,'Normal')
rough=node('ShaderNodeMapRange','Rugosité PBR de 0,78 à 0,98',-350,-880);rough.inputs['To Min'].default_value=.78;rough.inputs['To Max'].default_value=.98;connect(noise,'Fac',rough,'Value')
localbs=node('ShaderNodeBsdfPrincipled','Vue proche — terre PBR',340,-70);connect(tint,0,localbs,'Base Color');connect(rough,0,localbs,'Roughness');connect(bump,'Normal',localbs,'Normal')
mix=node('ShaderNodeMixShader','Fusion des deux surfaces',960,180);connect(mask,0,mix,0);connect(globalbs,0,mix,1);connect(localbs,0,mix,2);connect(mix,0,output,'Surface')
mat['blend_radius_m']=30;mat['blend_inner_m']=24;mat['blend_outer_m']=36
# Stubble is real geometry with metric spacing. Smoothly reduce height and density at edge.
rng=random.Random(20260920);vs=[];fs=[];stalks=0
def ground(x,y):
 # Nearest face on the dense render mesh, queried below through Blender's BVH.
 hit=terrain.ray_cast(Vector((x,y,100)),Vector((0,0,-1)));return hit[1].z if hit[0] else pad.z
straw=bpy.data.materials.new('Chaumes secs — matériau PBR');straw.use_nodes=True;pbs=straw.node_tree.nodes.get('Principled BSDF');pbs.inputs['Base Color'].default_value=(.20,.125,.055,1);pbs.inputs['Roughness'].default_value=.92
for xx in np.arange(-36,36,.75):
 for yy in np.arange(-36,36,.32):
  x=float(xx+rng.uniform(-.07,.07));y=float(yy+rng.uniform(-.10,.10));r=math.hypot(x,y);f=max(0,min(1,(36-r)/12));f=f*f*(3-2*f)
  if r<.7 or rng.random()>f*.78:continue
  x+=pad.x;y+=pad.y;z=ground(x,y);height=rng.uniform(.08,.22)*f;radius=rng.uniform(.005,.010);base=len(vs)
  for zz,rr in [(0,radius),(height,radius*.45)]:
   for k in range(4):ang=k*math.tau/4;vs.append((x+rr*math.cos(ang)+zz*.18,y+rr*math.sin(ang),z+zz))
  fs.extend([(base+k,base+(k+1)%4,base+(k+1)%4+4,base+k+4) for k in range(4)])
  # One broken leaf segment, folded rather than a flat billboard.
  q=len(vs);theta=rng.random()*math.tau;dx=math.cos(theta);dy=math.sin(theta);ll=rng.uniform(.07,.17)*f
  vs.extend([(x,y,z+height*.55),(x+dx*ll*.5-dy*.012,y+dy*ll*.5+dx*.012,z+height*.7),(x+dx*ll,y+dy*ll,z+.014*f),(x+dx*ll*.5+dy*.012,y+dy*ll*.5-dx*.012,z+height*.6)]);fs.append((q,q+1,q+2,q+3));stalks+=1
sm=bpy.data.meshes.new('Chaumes — tiges et feuilles brisées');sm.from_pydata(vs,[],fs);sm.update();ob=bpy.data.objects.new('CHAUMES — détail métrique avec fondu radial',sm);s.collection.objects.link(ob);sm.materials.append(straw);ob['seed']=20260920;ob['stalks']=stalks
# Render settings. Aerial camera includes the real landscape, flight timing stays unchanged.
s.camera.data.clip_end=20000;s.render.engine='BLENDER_EEVEE_NEXT';s.eevee.taa_render_samples=24;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.fps=30;s.frame_start=1;s.frame_end=1217
readme=bpy.data.texts.new('LIRE — Terrain hybride v6');readme.write(json.dumps(spec,ensure_ascii=False,indent=2)+'\nOrthophoto aérienne : © Région Centre-du-Québec, 2025, CC BY 4.0. RGB 20 cm rééchantillonné à 2 m. Chaumes artistiques, pas une observation de la culture actuelle. Scènes 01 et 02 conservées comme références.\n')
s.frame_set(85);s.view_layers[0].update();s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=95;s.render.filepath=str(w/'frames/vol-');(w/'frames').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-terrain-hybride.blend'))
report={'frames':1217,'fps':30,'vertices':len(mesh.vertices),'stalks':stalks,'image_packed':bool(tex.image.packed_file),'uv_min':data['patch_uv'].reshape(-1,2).min(axis=0).tolist(),'uv_max':data['patch_uv'].reshape(-1,2).max(axis=0).tolist(),'blend_at_radii':{'0':1,'24':1,'30':.5,'36':0,'100':0},'native_srtm_reference_preserved':True,'pad':list(pad),'landing':list(land)}
(out/'verification-hybride.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('HYBRID_READY',report,flush=True)
for f in (85,230,650,1217):
 s.frame_set(f);s.view_layers[0].update();s.render.filepath=str(out/f'apercu-vol-{f}.jpg');bpy.ops.render.render(write_still=True)
# Inspection cameras saved in an additional scene sharing the completed terrain.
review=s.copy();review.name='04 — Inspection du terrain hybride';bpy.context.window.scene=review;review.view_layers[0].update();camdata=bpy.data.cameras.new('Optique de contrôle du terrain');cam=bpy.data.objects.new('Caméra de contrôle du terrain',camdata);review.collection.objects.link(cam);review.camera=cam;camdata.clip_end=20000;camdata.lens=45
def look(loc,target):cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
for name,loc,target in [('detail',(pad.x+2,pad.y-3,pad.z+.65),(pad.x,pad.y+2,pad.z+.15)),('transition',(pad.x+45,pad.y-65,pad.z+65),(pad.x,pad.y,pad.z)),('aerien',(pad.x+400,pad.y-550,650),(0,0,0))]:
 look(loc,target);review.render.filepath=str(out/f'apercu-{name}.jpg');bpy.ops.render.render(write_still=True)
bpy.context.window.scene=s;s.view_layers[0].update();s.frame_set(85);s.view_layers[0].update();s.render.filepath=str(w/'frames/vol-');bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-terrain-hybride.blend'))
