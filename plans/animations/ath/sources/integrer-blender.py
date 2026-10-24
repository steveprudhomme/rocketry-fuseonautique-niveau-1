"""Keep the editable 3D scenes and add a sequence containing the delivered HUD film."""
import bpy,json
from pathlib import Path
out=Path('outputs/ath-v10').resolve();base=bpy.data.scenes['03 — Vol complet sur terrain hybride'];scene=base.copy();scene.name='06 — Vol avec ATH et son';bpy.context.window.scene=scene
scene.sequence_editor.sequences.new_movie('ATH v10 — composition issue des données',str(out/'chasse-galerie-1-ath.mp4'),channel=2,frame_start=1)
scene.render.use_compositing=False;scene.view_settings.view_transform="Standard";scene.view_settings.look="None";scene.view_settings.exposure=0;scene.view_settings.gamma=1;scene.render.use_sequencer=True;scene.frame_set(200);scene.render.filepath='//rendu-ath.mp4';scene.render.image_settings.file_format='FFMPEG';scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.audio_codec='AAC'
txt=bpy.data.texts.new('LIRE — ATH v10');txt.write('Scène 06 : montage final avec ATH, vidéo externe dans le même dossier et son intégré. Scène 03 : caméra et animation 3D v9 conservées. Les panneaux ATH sont composés par sources/creer-ath.py; modifier ce script et régénérer le MP4 pour changer leur disposition. Les vecteurs sont qualitatifs.\n')
path=out/'chasse-galerie-1-ath.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
movie=next(s for s in scene.sequence_editor.sequences_all if s.type=='MOVIE');movie.filepath='//chasse-galerie-1-ath.mp4';bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
assert path.stat().st_size<100*1024*1024
print('HUD_BLEND_SAVED',path.stat().st_size,flush=True)
