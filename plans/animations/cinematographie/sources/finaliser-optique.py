"""Project a shadow-free solar disc in the compositor and add a controlled optical test scene."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
out=Path('outputs/cinematographie-v8').resolve();w=Path('work/cinematographie-v8').resolve();s=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=s;s.view_layers[0].update();s.objects['SOLEIL — disque lointain pour les reflets optiques'].hide_render=True;s.objects['SOLEIL — disque lointain pour les reflets optiques'].hide_viewport=True
sun=next(o for o in s.objects if o.type=='LIGHT' and o.data.type=='SUN');sunvec=(sun.matrix_world.to_quaternion()@Vector((0,0,1))).normalized()
ns=s.node_tree.nodes;ls=s.node_tree.links;ellipse=ns.new('CompositorNodeEllipseMask');ellipse.name='Soleil — disque projeté sans géométrie';ellipse.location=(-900,-300);ellipse.mask_width=.011625;ellipse.mask_height=.011625
visible=ns.new('CompositorNodeMath');visible.name='Soleil — visibilité devant la caméra';visible.operation='MULTIPLY';visible.location=(-650,-300);ls.new(ellipse.outputs['Mask'],visible.inputs[0]);solar=ns.new('CompositorNodeMixRGB');solar.name='Disque solaire optique sans ombre portée';solar.blend_type='ADD';solar.location=(-500,300);solar.inputs[2].default_value=(10,9,7.5,1);ls.new(visible.outputs[0],solar.inputs[0]);ls.new(ns['Rendu optique v8'].outputs['Image'],solar.inputs[1]);ls.new(solar.outputs[0],ns['Aberration chromatique subtile'].inputs['Image'])
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def set_sun(sc,f):
 cam=sc.camera;nodes=sc.node_tree.nodes;mask=nodes['Soleil — disque projeté sans géométrie'];vis=nodes['Soleil — visibilité devant la caméra'];mix=nodes['Reflets — conditionnés à la direction solaire'];direction=cam.matrix_world.to_quaternion()@Vector((0,0,-1));dot=direction.dot(sunvec);p=world_to_camera_view(sc,cam,cam.matrix_world.translation+sunvec*10000);mask.x=max(-1,min(2,p.x));mask.y=max(-1,min(2,p.y));mask.keyframe_insert('x',frame=f);mask.keyframe_insert('y',frame=f);vis.inputs[1].default_value=1 if p.z>0 and -.02<p.x<1.02 and -.02<p.y<1.02 else 0;vis.inputs[1].keyframe_insert('default_value',frame=f);mix.inputs[0].default_value=.10*smooth((dot-math.cos(math.radians(25)))/(1-math.cos(math.radians(25))));mix.inputs[0].keyframe_insert('default_value',frame=f)
for f in range(1,1218):s.frame_set(f);s.view_layers[0].update();set_sun(s,f)
s.frame_set(1);s.view_layers[0].update();test=s.copy();test.name='05 — Contrôle optique face au soleil';test.node_tree.animation_data_clear();bpy.context.window.scene=test;test.view_layers[0].update();cdata=s.camera.data.copy();cdata.animation_data_clear();cdata.dof.use_dof=False;c=bpy.data.objects.new('Caméra — essai optique directionnel',cdata);test.collection.objects.link(c);test.camera=c;c.location=s.camera.matrix_world.translation.copy();test.frame_start=1;test.frame_end=150;az=math.atan2(sunvec.x,sunvec.y);el=math.asin(sunvec.z)
for f in range(1,151):
 delta=math.radians(-35+70*(f-1)/149);look=Vector((math.sin(az+delta)*math.cos(el),math.cos(az+delta)*math.cos(el),math.sin(el)));c.rotation_euler=look.to_track_quat('-Z','Y').to_euler();c.keyframe_insert('rotation_euler',frame=f);test.frame_set(f);test.view_layers[0].update();set_sun(test,f)
test.render.filepath=str(w/'optique/optique-');(w/'optique').mkdir(exist_ok=True)
for f in (1,58,75):
 test.frame_set(f);test.view_layers[0].update();test.render.filepath=str(out/f'controle-optique-{f}.jpg');bpy.ops.render.render(write_still=True)
test.render.filepath=str(w/'optique/optique-');bpy.context.window.scene=s;s.view_layers[0].update();s.frame_set(1);s.view_layers[0].update();s.render.filepath=str(w/'frames/vol-')
cfg=json.loads((out/'donnees/cinematographie.json').read_text());cfg['solar_disc']='Compositor projection of solar direction; no shadow-casting geometry';cfg['optical_test_frames']=150;cfg['flare_note']='Main flight cameras face away from sun; flare mix remains zero there. Scene 05 demonstrates sun-facing response.';(out/'donnees/cinematographie.json').write_text(json.dumps(cfg,indent=2),encoding='utf8');s['cinematography']=json.dumps(cfg);bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-cinematographie.blend'),compress=True)
for f in (1,75,95,230,400,650,977,1217):
 s.frame_set(f);s.view_layers[0].update();s.render.filepath=str(out/f'apercu-{f}.jpg');bpy.ops.render.render(write_still=True)
s.render.filepath=str(w/'frames/vol-');bpy.ops.render.render(animation=True);bpy.context.window.scene=test;test.view_layers[0].update();test.render.filepath=str(w/'optique/optique-');bpy.ops.render.render(animation=True);print('V8_RENDERED',flush=True)
