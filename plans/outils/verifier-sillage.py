"""Contrôles du livrable : physique OR intacte, images embarquées, raccord, échelle."""
from pathlib import Path
import copy,json,math,zipfile,xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
P=Path(__file__).resolve().parents[1];D=P/'decalques/sillage'
def semantic(node):
    return (node.tag,tuple(sorted(node.attrib.items())),(node.text or '').strip(),
            tuple(semantic(n) for n in node if n.tag not in ('appearance','insideappearance')))
base=ET.parse(P/'loc-iv-4po.xml').getroot()
new=ET.parse(D/'chasse-galerie-1-sillage.xml').getroot()
assert semantic(base)==semantic(new),'Un paramètre hors apparence a changé'
with zipfile.ZipFile(D/'chasse-galerie-1-sillage.ork') as z:
    # Git peut convertir le XML en CRLF sur Windows; comparer le contenu XML.
    assert semantic(ET.fromstring(z.read('rocket.ork')))==semantic(new)
    assert ET.canonicalize(z.read('rocket.ork').decode('utf-8'))==ET.canonicalize((D/'chasse-galerie-1-sillage.xml').read_text(encoding='utf-8'))
    for decal in new.iter('decal'):
        name=decal.attrib['name'];assert z.read(name)==(D/name).read_bytes()
        assert decal.find('scale').attrib=={'x':'1.0','y':'1.0'}
for name in ('payload','booster','corps'):
    im=Image.open(D/f'texture-{name}.png').convert('RGB')
    for y in range(im.height):
        assert im.getpixel((0,y))==im.getpixel((im.width-1,y)),f'Raccord ouvert : {name}/{y}'
m=json.loads((D/'dimensions-generees.json').read_text(encoding='utf-8'))
assert math.isclose(m['circonference_mm'],math.pi*m['diametre_mm'])
pdf=PdfReader(D/'epreuve-gabarits-provisoires.pdf');assert len(pdf.pages)==2
for page,length in zip(pdf.pages,(m['payload_mm'],m['booster_mm'])):
    width=m['circonference_mm']+m['chevauchement_mm']+2*m['fond_perdu_mm']+24
    height=length-2*m['retrait_mm']+2*m['fond_perdu_mm']+48
    assert abs(float(page.mediabox.width)/72*25.4-width)<1e-4
    assert abs(float(page.mediabox.height)/72*25.4-height)<1e-4
    assert 'PROVISOIRE' in page.extract_text()
print('OK : géométrie, masses, moteurs et simulations OR identiques; archive autonome; bords périodiques; deux pages à échelle exacte.')
