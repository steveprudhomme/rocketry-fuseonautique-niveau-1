"""Run from any empty build directory; stage archived inputs for the v8 scripts."""
from pathlib import Path
import shutil
source=Path(__file__).resolve().parent.parent
animation=source.parent
build=Path.cwd()
v8=build/'outputs/cinematographie-v8'
for path in (v8/'sources',v8/'donnees',build/'outputs/eclairage-v7',build/'outputs/vol-complet-v4/sources',build/'work/cinematographie-v8'):
    path.mkdir(parents=True,exist_ok=True)
shutil.copy2(animation/'eclairage/chasse-galerie-1-eclairage.blend',build/'outputs/eclairage-v7/chasse-galerie-1-eclairage.blend')
for name in ('terrain-hybride.json','telemetrie.json','vol-h143.csv'):
    shutil.copy2(source/'donnees'/name,v8/'donnees'/name)
shutil.copy2(source/'donnees/telemetrie.json',build/'outputs/vol-complet-v4/sources/telemetrie.json')
shutil.copy2(source/'donnees/vol-h143.csv',build/'outputs/vol-complet-v4/vol-h143.csv')
for path in (source/'sources').iterdir():
    if path.is_file():shutil.copy2(path,v8/'sources'/path.name)
print('Inputs ready. Run Blender from this build directory with sources/creer-camera.py, then finaliser-optique.py, then corriger-disque.py -- --animation. Run both verifier scripts and encoder-videos.py last. Set the ffmpeg path in encoder-videos.py if necessary.')
