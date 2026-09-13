"""Plan pédagogique A3, mm. Dépendances : Python, reportlab, Pillow, OpenSCAD.
Les contours SVG viennent du modèle; les lignes de jonction et cotes sont ajoutées.
Les repères de perspective sont des annotations manuelles à contrôler après modification.
Usage : python plans/outils/generer-plan-ensemble.py [--render] [--openscad CHEMIN]
"""
import argparse, hashlib, re, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageChops
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'ensemble'
SOURCE = ROOT / 'loc-iv-4po.scad'
parser = argparse.ArgumentParser()
parser.add_argument('--render', action='store_true', help='Régénérer les vues depuis OpenSCAD')
parser.add_argument('--openscad', default='C:/Program Files/OpenSCAD/openscad.com')
args = parser.parse_args()
OUT.mkdir(exist_ok=True)
if args.render:
    # Garder les variables au niveau global pour que -D view s'applique.
    source_text = SOURCE.read_text(encoding='utf-8-sig')
    dispatch = 'if(part == "assembly") assembly();'
    assert source_text.count(dispatch) == 1
    temporary = OUT/'_projection.scad'
    try:
        for name, transform in [('face','rotate([-90,0,0])'), ('profil','rotate([-90,0,0]) rotate([0,0,-90])'), ('dessus','')]:
            temporary.write_text(source_text.replace(dispatch, 'projection(cut=false) '+transform+' '+dispatch), encoding='utf-8')
            subprocess.run([args.openscad, '-o', str(OUT/f'{name}.svg'), '-D', 'view="assembled"', str(temporary)], check=True)
    finally:
        temporary.unlink(missing_ok=True)
    subprocess.run([args.openscad, '-o', str(OUT/'ecorche.png'), '--imgsize=1800,2400', '--projection=o', '--viewall', '--autocenter', '--camera=0,0,0,65,0,30,500', '--colorscheme=Tomorrow', str(SOURCE)], check=True)

src = SOURCE.read_text(encoding='utf-8-sig')
def val(name):
    return float(re.search(r'^'+name+r'\s*=\s*([\d.]+)\s*;', src, re.M)[1])
body, booster, payload, total = map(val, ['body_d','booster_l','payload_l','total_l'])
nose = total-booster-payload
aft = val('fin_aft_extent')-val('fin_root')
stamp = hashlib.sha256(SOURCE.read_bytes()).hexdigest()[:12]
c = canvas.Canvas(str(OUT/'loc-iv-plan-ensemble.pdf'), pagesize=(297*mm,420*mm))
c.setTitle("Chasse Galerie 1 - LOC-IV 4 po - Plan d'ensemble avec vue écorchée")
c.setAuthor("Projet de Steve Prud'Homme")

def text(x,y,s,size=9,bold=False):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    c.drawString(x*mm,y*mm,s)
def line(x,y,a,b): c.line(x*mm,y*mm,a*mm,b*mm)
def header(page,title,scale):
    c.setStrokeColorRGB(.17,.23,.28); c.setFillColorRGB(.12,.18,.23); c.setLineWidth(.25*mm)
    c.rect(10*mm,10*mm,277*mm,400*mm)
    text(16,401,'Chasse Galerie 1',19,True); text(16,395,'Base : LOC-IV / 4 po',9); text(170,401,title,12,True)
    text(170,395,'PLAN TECHNIQUE PÉDAGOGIQUE - RÉVISION B',8)
    line(10,390,287,390)
    line(10,36,287,36)
    text(15,28,'LOC-IV-ENS-001  |  2026-09-12  |  Feuille '+str(page)+'/2',10,True)
    text(15,21,'A3 portrait  |  Unités : mm  |  '+scale,9)
    text(15,15,'Source : loc-iv-4po.scad v1.1  |  SHA-256 : '+stamp,8)
    text(188,28,'BROUILLON - KIT NON MESURÉ',9,True)
    text(188,21,'Aucune conformité industrielle déclarée.',8)
    text(188,15,'Ne constitue pas un plan de fabrication.',8)

def svg(name,x,y,s=.2):
    # OpenSCAD : SVG Y vers le bas; PDF Y vers le haut. Aucun ajustement automatique.
    root = ET.parse(OUT/f'{name}.svg').getroot()
    c.saveState(); c.translate(x*mm,y*mm); c.scale(s*mm,-s*mm)
    c.setLineWidth(.23/s); c.setFillColorRGB(.94,.95,.96)
    for el in root.findall('{http://www.w3.org/2000/svg}path'):
        tokens = re.findall(r'[MLzZ]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',el.attrib['d'])
        p=c.beginPath(); i=0
        while i<len(tokens):
            cmd=tokens[i]; i+=1
            if cmd in 'zZ': p.close(); continue
            if cmd not in ['M','L']: raise ValueError('Commande SVG non prise en charge : '+cmd)
            a,b=map(float,tokens[i:i+2]); i+=2
            (p.moveTo if cmd=='M' else p.lineTo)(a,b)
        c.drawPath(p,stroke=1,fill=1,fillMode=0)
    c.restoreState()

def dim(x,y1,y2,ref,label):
    c.setLineWidth(.15*mm)
    line(ref,y1,x,y1); line(ref,y2,x,y2); line(x,y1,x,y2)
    for y in [y1,y2]: line(x-1,y-1.2,x+1,y+1.2)
    c.saveState(); c.translate((x-1.6)*mm,((y1+y2)/2)*mm); c.rotate(90)
    c.setFont('Helvetica',8); c.drawCentredString(0,0,label); c.restoreState()

header(1,'VUES ORTHOGONALES','Échelle 1:5 à impression 100 %')
# Même origine axiale et même facteur pour les deux élévations.
baseline=99
for name,x in [('face',80),('profil',218)]:
    svg(name,x,baseline)
    for z in [0,booster,booster+payload]: line(x-body*.1,baseline+z*.2,x+body*.1,baseline+z*.2)
    c.saveState(); c.setDash([6,2,1,2]); c.setLineWidth(.12*mm)
    line(x,87,x,baseline+total*.2+3); c.restoreState()
    text(x-12,80,name.upper(),10,True)
svg('dessus',80,360)
text(105,374,'DESSUS (+Z)',9,True)
text(105,368,'3 ailerons à 120° [N]',8)
text(105,362,'X vers la droite; Y vers le haut',8)
text(198,360,'PROFIL : depuis +X',8)
text(198,354,'Y vers la droite; Z vers le haut',8)
dim(34,baseline-aft*.2,baseline+total*.2,64,f'{total+aft:.3f} [D] hors tout')
dim(47,baseline,baseline+total*.2,69,f'{total:g} [N] corps-pointe')
for z1,z2,label in [(0,booster,f'{booster:g} [N]'),(booster,booster+payload,f'{payload:g} [N]'),(booster+payload,total,f'{nose:g} [D/A]')]:
    dim(125,baseline+z1*.2,baseline+z2*.2,91,label)
text(58,74,'FACE : depuis -Y; X à droite, Z en haut',8)
text(179,74,'Ø 101,6 nominal [N] - extérieur à mesurer',8)
text(16,65,'Projection orthographique : dessus au-dessus de la face, profil à droite. Contours visibles uniquement.',9)
text(16,59,'[N] source nominale documentée   [F] fichier LOC   [D] calcul   [A] approximation à valider sur le kit',9)
text(16,53,'Ailerons [F] : racine 171,45; portée 107,95; épaisseur 3,175 [N]. Dépassement arrière : 34,925 [D].',9)
text(16,47,'Ogive : longueur exposée déduite; profil ellipsoïdal [A]. Les silhouettes utilisent la discrétisation OpenSCAD.',9)
text(16,41,'Cotes prioritaires sur le dessin. Aucune tolérance de fabrication définie; ne pas relever de cotes à la règle.',9)
c.showPage()

header(2,'PERSPECTIVE ÉCORCHÉE','Perspective sans échelle')
# Recadrage du fond seulement; aucune modification de la géométrie rendue.
im=Image.open(OUT/'ecorche.png').convert('RGB')
bg=Image.new('RGB',im.size,im.getpixel((0,0)))
box=ImageChops.difference(im,bg).getbbox()
im=im.crop(box)
h=290; w=h*im.width/im.height; ix=84-w/2; iy=85
c.drawImage(ImageReader(im),ix*mm,iy*mm,w*mm,h*mm)
def call(n,u,v,xx,yy):
    # Coordonnées normalisées du rendu recadré (origine en haut à gauche).
    ax=ix+u*w; ay=iy+(1-v)*h
    c.setLineWidth(.18*mm); line(ax,ay,xx,yy)
    c.setFillColorRGB(1,1,1); c.circle(xx*mm,yy*mm,3.3*mm,fill=1,stroke=1)
    c.setFillColorRGB(.12,.18,.23); c.setFont('Helvetica-Bold',8)
    c.drawCentredString(xx*mm,(yy-1)*mm,str(n))

# Contrôler visuellement ces points si caméra, pièces ou proportions changent.
for item in [(1,.46,.15,37,346),(2,.48,.38,130,278),(3,.49,.50,37,242),
             (4,.50,.535,130,222),(5,.59,.69,130,175),(6,.46,.593,37,211),
             (7,.49,.66,37,186),(8,.42,.60,37,198),(9,.39,.79,37,157),
             (10,.49,.88,130,120),(11,.49,.713,130,158),(12,.83,.93,130,94)]:
    call(*item)
text(153,376,'NOMENCLATURE',12,True)
text(153,369,'Rep. / Qté / Composant et statut',9)
items=[('01','1','Ogive et épaulement','Profil et parois [A]'),
('02','1','Tube payload','Longueur 279,4 [N]'),('03','1','Coupleur','Longueur 140 [A]'),
('04','1','Cloison du coupleur','Épaisseur 6,35 [A]'),('05','1','Corps booster','Longueur 584,2 [N]'),
('06','1','Parachute 36 po','Tissu Ø 914,4 [N]; paquet [A]'),('07','1','Protecteur','Carré 304,8 proposé [A]'),
('08','1','Sangle de récupération','4572 × 9,525 [N]; tracé [A]'),('09','1','Support moteur 38 mm','Longueur 300; alésage 38,5 [A]'),
('10','1','Moteur Pro38 2G','Enveloppe Ø 38 × 186 [N]'),('11','3','Anneaux de centrage','Épaisseur 6,35 [N]; positions [A]'),
('12','3','Ailerons avec languettes','Profil [F]; épaisseur 3,175 [N]'),('13*','1 jeu','Rétention LOC MR-1','Deux clips; forme simplifiée [A]'),
('14*','2','Boutons de rail 1010','Dimensions et positions [A]'),('15*','2','Points d’attache','Symboles; montage à valider [A]')]
y=358
for num,q,name,note in items:
    text(153,y,num,9,True); text(166,y,q,8); text(181,y,name,9,True)
    text(181,y-4.5,note,8); line(153,y-7,280,y-7); y-=14
text(153,140,'* Petites pièces masquées ou peu lisibles :',8)
text(153,135,'voir les rendus individuels dans plans/images.',8)
text(153,126,'11 : un repère pour les trois anneaux.',8)
text(153,121,'13 : à l’arrière; 14 : sur le corps à 60°.',8)
text(153,116,'15 : anneau avant et cloison du coupleur.',8)
text(153,107,'H143 représenté; H152 : même enveloppe.',8)
text(153,102,'ProDAT-38 : outil au sol, hors ensemble.',8)
text(16,75,'Coupe graphique longitudinale : matières retirées pour la lecture; ce ne sont pas des ouvertures à fabriquer.',9)
text(16,69,'Récupération rangée schématique : pliage, cheminement et attaches ne définissent pas une procédure de montage.',9)
text(16,63,'Sources : notes/loc-iv-configuration-budget-niveau-1.md; notice LOC PK-48; catalogue Cesaroni Pro38.',9)
text(16,57,'Profil d’aileron : PK-48 Loc-IV.rkt publié par LOC. Provenance et écarts : notes/loc-iv-comparaison-modeles.md.',9)
text(16,51,'Cotes [A], masse et centre de gravité : à confirmer dans notes/loc-iv-mesures-kit.md.',9)
text(16,45,'Le PDF décrit la révision 1.1 du modèle; il ne remplace ni la notice du kit ni la validation de la configuration de vol.',9)
c.save()
print(OUT/'loc-iv-plan-ensemble.pdf')

