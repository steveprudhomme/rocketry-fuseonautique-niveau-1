"""Blender 4.3 / Cycles : Chasse Galerie 1, champ de maïs récolté, heure dorée.
blender --background --factory-startup --python rendre-decollage-blender.py -- --preview
Sans --preview : rendu final et scène .blend autonome avec textures embarquées.
Unités : mètres. La fusée reprend les cotes du SCAD; le paysage est artistique.
"""
import bpy, math, random, re, sys, json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rendus-artistiques';OUT.mkdir(exist_ok=True)
PREVIEW='--preview' in sys.argv
random.seed(140926)
source=(ROOT/'loc-iv-4po.scad').read_text(encoding='utf-8')
def mm(key):return float(re.search(r'^'+key+r'\s*=\s*([\d.]+)\s*;',source,re.M)[1])/1000
R=mm('body_d')/2;B=mm('booster_l');P=mm('payload_l');N=mm('total_l')-B-P
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC'
scene.render.engine='CYCLES';scene.cycles.samples=40 if PREVIEW else 192
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.035 if PREVIEW else .012
scene.cycles.max_bounces=8;scene.cycles.volume_bounces=2
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
    prefs.compute_device_type='OPTIX';prefs.get_devices()
    gpu=False
    for d in prefs.devices:
        d.use=d.type=='OPTIX';gpu|=d.use
    scene.cycles.device='GPU' if gpu else 'CPU'
except Exception:scene.cycles.device='CPU'
scene.render.resolution_x=1800;scene.render.resolution_y=2400
scene.render.resolution_percentage=50 if PREVIEW else 100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.image_settings.color_depth='8';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
scene.view_settings.exposure=-.25

def linear(hexvalue):
    values=[int(hexvalue[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values)+(1,)
def material(name,color,rough=.5,metal=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=linear(color)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m
def mesh(name,verts,faces,mat,uv=None):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    o=bpy.data.objects.new(name,data);scene.collection.objects.link(o)
    if mat:o.data.materials.append(mat)
    if uv:
        layer=data.uv_layers.new(name='Developpe')
        for poly,coords in zip(data.polygons,uv):
            for loop,coord in zip(poly.loop_indices,coords):layer.data[loop].uv=coord
    return o
def smooth(o):
    for p in o.data.polygons:p.use_smooth=True
def orient(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def rod(name,a,b,r,mat,r2=None,sides=8):
    a,b=Vector(a),Vector(b);delta=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=sides,radius1=r,radius2=r if r2 is None else r2,depth=delta.length,location=(a+b)/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat);return o
def sphere(name,loc,scale,mat,sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mat);smooth(o);return o

navy=material('Peinture bleu Quebec satinee','082A55',.38)
navy.node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value=.10
black=material('Boutons noirs','16181B',.45)
steel=material('Aluminium brosse','737C83',.29,.8)

# Ensemble mobile, même azimut du raccord à 60 degrés que les autres modèles.
rocket=bpy.data.objects.new('CHASSE GALERIE 1 - dimensions du plan',None);scene.collection.objects.link(rocket)
rocket.location=(0,0,.88);rocket.rotation_euler=(math.radians(-2),math.radians(-4),math.radians(56.565))
def parent(o):o.parent=rocket;return o
def tube(name,z,length,tex):
    mat=material(name+' / vinyle satine','FFFFFF',.43)
    nodes=mat.node_tree.nodes;p=nodes.get('Principled BSDF')
    p.inputs['Coat Weight'].default_value=.08;p.inputs['Coat Roughness'].default_value=.38
    t=nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(ROOT/'decalques/sillage'/tex));t.image.pack()
    t.interpolation='Linear';t.extension='REPEAT';mat.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
    verts=[];faces=[];uv=[];segments=256
    for zz in (z,z+length):
        for i in range(segments+1):
            angle=math.radians(60)+2*math.pi*i/segments;verts.append((R*math.cos(angle),R*math.sin(angle),zz))
    for i in range(segments):
        faces.append((i,i+1,i+segments+2,i+segments+1));uv.append(((i/segments,0),((i+1)/segments,0),((i+1)/segments,1),(i/segments,1)))
    o=parent(mesh(name,verts,faces,mat,uv));smooth(o)
    return o
tube('Tube inferieur 584.2 mm',0,B,'texture-booster.png')
tube('Payload 279.4 mm',B,P,'texture-payload.png')

verts=[];faces=[];rings=64;segments=128
for j in range(rings+1):
    a=j/rings*math.pi/2;radius=max(1e-6,R*math.cos(a));z=B+P+N*math.sin(a)
    for i in range(segments):
        theta=2*math.pi*i/segments;verts.append((radius*math.cos(theta),radius*math.sin(theta),z))
for j in range(rings):
    for i in range(segments):
        faces.append((j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i))
smooth(parent(mesh('Ogive ellipsoidale du plan',verts,faces,navy)))

outline=[(0,mm('fin_root')),(mm('fin_span'),mm('fin_root')-mm('fin_leading_sweep')),
         (mm('fin_span'),mm('fin_root')-mm('fin_aft_extent')),
         (mm('fin_aft_kink'),mm('fin_root')-mm('fin_aft_extent')),(0,0)]
for a in (0,120,240):
    vs=[(R+x,y,z) for y in (-mm('fin_t')/2,mm('fin_t')/2) for x,z in outline]
    fs=[tuple(range(4,-1,-1)),tuple(range(5,10))]+[(i,(i+1)%5,(i+1)%5+5,i+5) for i in range(5)]
    o=parent(mesh('Aileron LOC '+str(a),vs,fs,navy));o.rotation_euler.z=math.radians(a)
    bevel=o.modifiers.new('Bord peint legerement adouci','BEVEL');bevel.width=.00035;bevel.segments=2
    o.modifiers.new('Normales des faces','WEIGHTED_NORMAL')
for z in (.07,.43):
    a=math.radians(60);v=Vector((math.cos(a),math.sin(a),0))
    for rr,l,start in ((.006,.003,R),(.0035,.003,R+.003),(.006,.003,R+.006)):
        parent(rod('Bouton de rail',v*start+Vector((0,0,z)),v*(start+l)+Vector((0,0,z)),rr,black,sides=24))
parent(rod('Enveloppe arriere moteur', (0,0,-.006),(0,0,.014),.019,steel,sides=48))

# Sol et rangs de culture : relief et détail procéduraux, aucun décor photographique.
soil=material('Terre seche apres recolte','56402B',.94)
nodes=soil.node_tree.nodes;links=soil.node_tree.links;p=nodes.get('Principled BSDF')
coord=nodes.new('ShaderNodeTexCoord');noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=22;noise.inputs['Detail'].default_value=4
links.new(coord.outputs['Object'],noise.inputs['Vector'])
ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=linear('30251E')
ramp.color_ramp.elements[1].position=.78;ramp.color_ramp.elements[1].color=linear('9C8061')
links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],p.inputs['Base Color'])
bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.55;bump.inputs['Distance'].default_value=.016
links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],p.inputs['Normal'])
verts=[];faces=[];nx,ny=200,200
for j in range(ny+1):
    y=-12+j*.6
    for i in range(nx+1):
        x=-60+i*.6;z=.012*math.sin(x*2*math.pi/.72)+random.uniform(-.012,.012)
        verts.append((x,y,z))
for j in range(ny):
    for i in range(nx):
        k=j*(nx+1)+i;faces.append((k,k+1,k+nx+2,k+nx+1))
smooth(mesh('Champ laboure et sillons',verts,faces,soil))
fieldback=mesh('Terre horizon',[(-300,-30,-.04),(300,-30,-.04),(300,400,-.04),(-300,400,-.04)],[(0,1,2,3)],soil)
strawmats=[material('Chaume '+str(i),col,.87) for i,col in enumerate(('BDA16A','927448','D4B982','795A35','AD8851'))]

# Un maillage commun pour les milliers de tiges coupées et feuilles recourbées.
v=[];f=[];mi=[]
def stalk(x,y,height,radius,lean):
    start=len(v)
    for j in range(3):
        z=j*height/2;rr=radius*(1-.2*j)
        for k in range(6):
            a=k*math.pi/3;v.append((x+rr*math.cos(a)+lean[0]*j/2,y+rr*math.sin(a)+lean[1]*j/2,z))
    for j in range(2):
        for k in range(6):f.append((start+j*6+k,start+j*6+(k+1)%6,start+(j+1)*6+(k+1)%6,start+(j+1)*6+k));mi.append(random.randrange(5))
    f.append(tuple(start+12+k for k in range(6)));mi.append(2)
def leaf(x,y,z,angle,length,width,curl):
    start=len(v)
    for j in range(6):
        t=j/5;w=width*math.sin(math.pi*t)*.5
        for side in (-1,1):
            v.append((x+math.cos(angle)*length*t+side*w*math.sin(angle),y+math.sin(angle)*length*t-side*w*math.cos(angle),z+curl*math.sin(math.pi*t)+.009*t))
    for j in range(5):f.append((start+2*j,start+2*j+1,start+2*j+3,start+2*j+2));mi.append(random.randrange(5))
for row in range(-24,25):
    for k in range(180):
        x=row*.72+random.uniform(-.075,.075);y=-5+k*.29+random.uniform(-.06,.06)
        if abs(x)<.4 and abs(y)<.45:continue
        h=random.uniform(.075,.22);stalk(x,y,h,random.uniform(.006,.011),(random.uniform(-.035,.035),random.uniform(-.03,.03)))
        if random.random()<.95:leaf(x,y,.01,random.uniform(0,6.28),random.uniform(.12,.37),.045,random.uniform(.02,.08))
        if random.random()<.75:leaf(x+random.uniform(-.2,.2),y+random.uniform(-.12,.12),.006,random.uniform(0,6.28),random.uniform(.09,.24),.04,random.uniform(.005,.025))
        if random.random()<.35:leaf(x,y,h*.65,random.uniform(0,6.28),.16,.02,-.04)
obj=mesh('Chaumes de mais coupes et feuilles seches',v,f,None)
for mat in strawmats:obj.data.materials.append(mat)
for face,index in zip(obj.data.polygons,mi):face.material_index=index

# Lisière agricole lointaine, adoucie par la brume.
treemats=[material('Lisiere automnale '+str(i),c,.9) for i,c in enumerate(('535439','62543A','826242','534635'))]
for i in range(85):
    x=-85+i*2.2;y=random.uniform(95,125);height=random.uniform(2,4.5)
    rod('Tronc lointain',(x,y,0),(x,y,height*.7),.10,treemats[3],r2=.035,sides=5)
    for branch in range(18):
        a=random.uniform(0,6.28);rad=random.uniform(0,1.0)
        pos=(x+math.cos(a)*rad,y+math.sin(a)*rad,height*.45+random.random()*height*.45)
        o=sphere('Feuillage de la lisiere',pos,(random.uniform(.3,.65),random.uniform(.3,.65),random.uniform(.35,.75)),random.choice(treemats),1)
        # Contour irrégulier, sans grandes ellipses lisses sur l'horizon.
        for vert in o.data.vertices:vert.co*=random.uniform(.78,1.20)

# Soleil bas Nishita : lumière atmosphérique dorée réelle dans Cycles.
world=bpy.data.worlds.new('Heure doree - ciel Nishita');scene.world=world;world.use_nodes=True
wn=world.node_tree.nodes;wn.clear();output=wn.new('ShaderNodeOutputWorld');bg=wn.new('ShaderNodeBackground');sky=wn.new('ShaderNodeTexSky')
sky.sky_type='NISHITA';sky.sun_elevation=math.radians(6);sky.sun_rotation=2.20;sky.sun_size=math.radians(1.0)
sky.sun_disc=False;sky.sun_intensity=.75;sky.air_density=1.1;sky.dust_density=2.4;sky.ozone_density=1
bg.inputs['Strength'].default_value=.20;world.node_tree.links.new(sky.outputs['Color'],bg.inputs['Color']);world.node_tree.links.new(bg.outputs[0],output.inputs[0])
sunpos=Vector((-45,126,12))
bpy.ops.object.light_add(type='SUN',location=sunpos);sun=bpy.context.object;sun.name='Soleil rasant, contre-jour chaud'
sun.data.energy=2.0;sun.data.color=(1,.65,.32);sun.data.angle=math.radians(1);orient(sun,(0,0,0))
sunmat=material('Disque du soleil','FFD58B',.4)
sunshader=sunmat.node_tree.nodes.get('Principled BSDF');sunshader.inputs['Emission Color'].default_value=(1,.62,.22,1);sunshader.inputs['Emission Strength'].default_value=10
sphere('Soleil a travers la brume',sunpos,(1.5,1.5,1.5),sunmat,3)

# Perspective atmosphérique : la lisière se fond doucement dans la lumière.
haze=bpy.data.materials.new('Brume atmospherique legere');haze.use_nodes=True
hn=haze.node_tree.nodes;hn.clear();ho=hn.new('ShaderNodeOutputMaterial');hv=hn.new('ShaderNodeVolumePrincipled')
hv.inputs['Density'].default_value=.003;hv.inputs['Color'].default_value=(.65,.69,.73,1);hv.inputs['Anisotropy'].default_value=.45
haze.node_tree.links.new(hv.outputs['Volume'],ho.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,55,12));fog=bpy.context.object;fog.name='Volume de brume du paysage';fog.scale=(240,220,26);fog.data.materials.append(haze)

# Léger débouchage photographique pour garder le bleu et le nom lisibles.
bpy.ops.object.light_add(type='AREA',location=(1,-3,3.8));light=bpy.context.object;light.name='Ciel reflechi - debouchage doux'
light.data.energy=75;light.data.shape='DISK';light.data.size=4;light.data.color=(.85,.9,1);orient(light,(0,0,1.4))

def smoke_material():
    m=bpy.data.materials.new('Fumee volumetrique non simulee');m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear();links=m.node_tree.links
    out=nodes.new('ShaderNodeOutputMaterial');vol=nodes.new('ShaderNodeVolumePrincipled');vol.inputs['Color'].default_value=(.4,.36,.30,1);vol.inputs['Anisotropy'].default_value=.3
    tc=nodes.new('ShaderNodeTexCoord')
    length=nodes.new('ShaderNodeVectorMath');length.operation='LENGTH';links.new(tc.outputs['Object'],length.inputs[0])
    edge=nodes.new('ShaderNodeMapRange');edge.clamp=True;edge.inputs['From Min'].default_value=.15;edge.inputs['From Max'].default_value=1;edge.inputs['To Min'].default_value=1;edge.inputs['To Max'].default_value=0;links.new(length.outputs['Value'],edge.inputs['Value'])
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=3;links.new(tc.outputs['Object'],noise.inputs['Vector'])
    mult=nodes.new('ShaderNodeMath');mult.operation='MULTIPLY';links.new(noise.outputs['Fac'],mult.inputs[0]);links.new(edge.outputs['Result'],mult.inputs[1])
    density=nodes.new('ShaderNodeMath');density.operation='MULTIPLY';density.inputs[1].default_value=30;links.new(mult.outputs[0],density.inputs[0]);links.new(density.outputs[0],vol.inputs['Density'])
    links.new(vol.outputs[0],out.inputs['Volume']);return m
smoke=smoke_material()
bpy.context.view_layer.update()
tail=rocket.matrix_world@Vector((0,0,-.007))
axis=rocket.rotation_euler.to_matrix()@Vector((0,0,1))
for i in range(17):
    t=i/16;center=tail-axis*(.09+.9*t)+Vector((.20*t*t,.08*t*t,0))
    size=.022+.15*t;center.z=max(.04,center.z)
    o=sphere('Panache '+str(i),center,(size*(1+random.random()*.2),size,size*1.5),smoke,2);o.rotation_euler.z=random.random()*6.28
for i in range(22):
    x=random.uniform(-.35,.8);y=random.uniform(-.08,.7);z=random.uniform(.045,.18);s=random.uniform(.11,.3)
    sphere('Fumee au sol '+str(i),(x,y,z),(s,s*.8,s*.7),smoke,2)

# Coeur lumineux stylisé, court et aligné sur l'axe, sans modifier le modèle moteur.
fire=material('Coeur lumineux du jet','FFC376',.4)
bsdf=fire.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Emission Color'].default_value=(1,.25,.025,1);bsdf.inputs['Emission Strength'].default_value=14
rod('Jet lumineux',tail-axis*.17,tail,.002,fire,r2=.014,sides=32)
bpy.ops.object.light_add(type='POINT',location=tail-axis*.08);bpy.context.object.name='Lueur du jet';bpy.context.object.data.energy=11;bpy.context.object.data.color=(1,.26,.035);bpy.context.object.data.shadow_soft_size=.08

# Rail et petit trépied au sol, volontairement discrets derrière le panache.
direction=Vector((math.cos(math.pi/3),math.sin(math.pi/3),0))
bottom=rocket.matrix_world@(direction*(R+.025)+Vector((0,0,-.88)))
top=rocket.matrix_world@(direction*(R+.025)+Vector((0,0,.70)))
rod('Rail de lancement en arriere-plan',bottom,top,.006,steel,sides=4)
for a in (0,120,240):
    foot=bottom+Vector((.35*math.cos(math.radians(a)),.35*math.sin(math.radians(a)),0));foot.z=.025
    rod('Pied de la rampe',bottom+Vector((0,0,.14)),foot,.012,steel,sides=8)

# Caméra portrait à hauteur du champ, profondeur de champ modérée.
bpy.ops.object.camera_add(location=(1.4,-2.8,.68));cam=bpy.context.object;cam.name='Camera hero - depart dans les chaumes'
orient(cam,(0,0,1.10));cam.data.lens=57;cam.data.sensor_width=36
cam.data.dof.use_dof=True;cam.data.dof.focus_distance=(cam.location-Vector((0,0,1.4))).length;cam.data.dof.aperture_fstop=7.1
scene.camera=cam

# Halo optique discret, sans dessin ajouté après le rendu.
scene.use_nodes=True;nodes=scene.node_tree.nodes;nodes.clear()
rl=nodes.new('CompositorNodeRLayers');glare=nodes.new('CompositorNodeGlare');glare.glare_type='FOG_GLOW';glare.quality='HIGH';glare.threshold=2;glare.size=7
comp=nodes.new('CompositorNodeComposite');scene.node_tree.links.new(rl.outputs['Image'],glare.inputs['Image']);scene.node_tree.links.new(glare.outputs['Image'],comp.inputs['Image'])

# Les textures sont incluses dans le .blend; aucun chemin externe indispensable.
groups={name:bpy.data.collections.new(name) for name in ('01 - Fusee','02 - Champ','03 - Lisiere','04 - Lumiere et camera','05 - Panache et rampe')}
for group in groups.values():scene.collection.children.link(group)
for o in list(scene.collection.objects):
    if o==rocket or o.parent==rocket:key='01 - Fusee'
    elif o.name.startswith(('Feuillage','Tronc')):key='03 - Lisiere'
    elif o.type in ('CAMERA','LIGHT') or o.name.startswith(('Soleil','Volume de brume')):key='04 - Lumiere et camera'
    elif o.name.startswith(('Panache','Fumee','Jet','Rail','Pied')):key='05 - Panache et rampe'
    else:key='02 - Champ'
    groups[key].objects.link(o);scene.collection.objects.unlink(o)
scene['projet']='Chasse Galerie 1 / Le sillage fleurdelise'
scene['statut']='Image artistique; cotes nominales SCAD, panache et paysage non simules.'
scene['sources']='plans/loc-iv-4po.scad et plans/decalques/sillage/texture-*.png'
scene.render.filepath=str(OUT/('apercu-decollage.png' if PREVIEW else 'chasse-galerie-1-golden-hour.png'))
if not PREVIEW:
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'chasse-galerie-1-golden-hour.blend'),compress=True)
bpy.ops.render.render(write_still=True)
print('RENDU TERMINE :',scene.render.filepath)
