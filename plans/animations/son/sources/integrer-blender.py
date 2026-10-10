"""Add packed sound to the existing flight scene, preserving camera and physics."""
import bpy,json
from pathlib import Path
out=Path('outputs/son-v9').resolve();scene=bpy.data.scenes['03 — Vol complet sur terrain hybride'];bpy.context.window.scene=scene
editor=scene.sequence_editor_create();strip=editor.sequences.new_sound('V9 — Sept sillages et bruitages synchronisés',str(out/'audio/bande-son.wav'),channel=1,frame_start=1);strip.sound.pack();strip.volume=1
scene.render.use_sequencer=False
scene.sync_mode='AUDIO_SYNC';scene.frame_set(1)
report=json.loads((out/'donnees/son.json').read_text(encoding='utf8'))
for event in report['events']:scene.timeline_markers.new('SON — '+event['event'],frame=round(event['video_s']*30)+1)
text=bpy.data.texts.new('LIRE — Bande sonore v9');text.write('Bande sonore originale synthétisée, 48 kHz stéréo. Lecture avec audio dans la scène 03. MP4 final assemblé sans réencodage des images v8. Bruitages illustratifs, non mesurés.\n'+json.dumps(report,ensure_ascii=False,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-son.blend'),compress=True)
assert strip.sound.packed_file and scene.frame_end==1217
print('PACKED_AUDIO_VERIFIED',len(strip.sound.packed_file.data),flush=True)
