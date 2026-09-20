"""Prepare a project-local BlenderGIS copy from the archived official ZIP."""
from pathlib import Path
import zipfile,shutil
w=Path('work/topographie-v5');w.mkdir(parents=True,exist_ok=True)
archive=Path('outputs/topographie-v5/sources/BlenderGIS-original.zip')
shutil.copy2(archive,w/'BlenderGIS.zip')
for name in ['letendre-osm.json','rang10-osm.json']:
    shutil.copy2(Path('outputs/topographie-v5/donnees')/name,w/name)
with zipfile.ZipFile(archive) as z:
    root=(w/'addons').resolve()
    for member in z.namelist():
        if not (root/member).resolve().is_relative_to(root):
            raise ValueError('Unsafe archive path')
    z.extractall(root)
for name in ['__init__.py','prefs.py']:
    p=root/'BlenderGIS-master'/name
    s=p.read_text(encoding='utf8').replace(
        "home = os.path.expanduser('~')",
        "home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'cache'))\n\tos.makedirs(home, exist_ok=True)")
    p.write_text(s,encoding='utf8')
print('BlenderGIS prepared locally; global Blender preferences unchanged.')
