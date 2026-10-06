"""Correct compositor mask dimensions; optionally render the optical control."""
import bpy, sys, json
from pathlib import Path
out=Path('outputs/cinematographie-v8').resolve()
work=Path('work/cinematographie-v8').resolve()
main=bpy.data.scenes['03 — Vol complet sur terrain hybride']
test=bpy.data.scenes['05 — Contrôle optique face au soleil']
for scene in (main,test):
    mask=scene.node_tree.nodes['Soleil — disque projeté sans géométrie']
    mask.mask_width=.011625
    mask.mask_height=.011625
    assert abs(mask.mask_width-mask.mask_height)<.01
bpy.context.window.scene=main
main.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'chasse-galerie-1-cinematographie.blend'),compress=True)
bpy.context.window.scene=test
for frame in (1,58,75):
    test.frame_set(frame)
    test.render.filepath=str(out/f'controle-optique-{frame}.jpg')
    bpy.ops.render.render(write_still=True)
if '--animation' in sys.argv:
    test.render.filepath=str(work/'optique-corrigee/optique-')
    (work/'optique-corrigee').mkdir(exist_ok=True)
    bpy.ops.render.render(animation=True)
print('SOLAR_MASK_CORRECTED',flush=True)
