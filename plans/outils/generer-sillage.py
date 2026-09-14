"""Gabarits provisoires, textures OR et mosaïque SCAD depuis une source commune.
Python + Pillow + reportlab + pypdfium2. Aucun prix ni cote physique inventée.
Usage : python plans/outils/generer-sillage.py
Les PNG sont des rendus de documents, l'illustration-source reste intacte.
"""
import base64, copy, hashlib, io, json, math, re, tempfile, zipfile
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

PLANS = Path(__file__).resolve().parents[1]
OUT = PLANS / 'decalques/sillage'
CFG = json.loads((OUT/'configuration.json').read_text(encoding='utf-8'))
SCAD = (PLANS/'loc-iv-4po.scad').read_text(encoding='utf-8')
def val(key):
    return float(re.search(r'^'+key+r'\s*=\s*([\d.]+)\s*;', SCAD, re.M)[1])
D = val('body_d')
C = CFG['circonference_mesuree_mm'] or math.pi*D
P = CFG['longueur_payload_mesuree_mm'] or val('payload_l')
B = CFG['longueur_booster_mesuree_mm'] or val('booster_l')
H = P+B
R = C/(2*math.pi)
O, F, I = [CFG[k] for k in ('chevauchement_mm','fond_perdu_mm','retrait_extremites_mm')]
S, FADE = CFG['bande_raccord_unie_mm'], CFG['fondu_raccord_mm']
assert 0 < O <= S and S+FADE < C/4 and 0 <= I < min(P,B)/2
assert abs(C-math.pi*D)<1e-6 and P==val('payload_l') and B==val('booster_l'), 'Mettre à jour les deux modèles SCAD/ORK avant une régénération avec de nouvelles mesures.'
base_root=ET.parse(PLANS/'loc-iv-4po.xml').getroot()
base_tubes=base_root.findall('rocket/subcomponents/stage/subcomponents/bodytube')
assert len(base_tubes)==2 and all(abs(float(n.findtext('radius'))*2000-D)<1e-6 for n in base_tubes)
assert abs(float(base_tubes[0].findtext('length'))*1000-P)<1e-6 and abs(float(base_tubes[1].findtext('length'))*1000-B)<1e-6
ART = OUT/'illustration-source.png'
NAVY = (8/255,42/255,85/255)
sections = [('payload', I, P-2*I, P), ('booster', P+I, B-2*I, B)]

def artwork(c):
    """Document à fond bleu, coordonnées mm depuis le bas de l'art global."""
    c.setFillColorRGB(*NAVY); c.rect(0,0,C,H,fill=1,stroke=0)
    c.drawImage(str(ART),0,0,width=C,height=H)
    for side in (0,1):
        c.setFillAlpha(1)
        c.rect(0 if side==0 else C-S,0,S,H,fill=1,stroke=0)
        # Fondu de document, indépendant de la résolution de l'illustration.
        for n in range(80):
            c.setFillAlpha(1-(n+.5)/80)
            x=S+n*FADE/80 if side==0 else C-S-(n+1)*FADE/80
            c.rect(x,0,FADE/80+.002,H,fill=1,stroke=0)
    c.setFillAlpha(1)

def region(c,x,y,start,length,bleed=0,overlap=0):
    c.saveState()
    p=c.beginPath();p.rect(x-bleed,y-bleed,C+overlap+2*bleed,length+2*bleed)
    c.clipPath(p,stroke=0)
    c.setFillColorRGB(*NAVY);c.rect(x-bleed,y-bleed,C+overlap+2*bleed,length+2*bleed,fill=1,stroke=0)
    for cycle in (-1,0,1):
        c.saveState(); c.translate(x+cycle*C,y-(H-start-length)); artwork(c); c.restoreState()
    c.restoreState()

def render_region(name,start,length):
    # PDF technique temporaire; pas de manipulation du bitmap d'illustration.
    buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(C*mm,length*mm));c.scale(mm,mm)
    region(c,0,0,start,length)
    if name in ('texture-payload','texture-booster'):
        c.setFillColorRGB(*NAVY)
        c.rect(0,0,C,I,fill=1,stroke=0);c.rect(0,length-I,C,I,fill=1,stroke=0)
    c.showPage();c.save()
    doc=pdfium.PdfDocument(buf.getvalue())
    image=doc[0].render(scale=CFG['texture_pixels_par_mm']/mm).to_pil()
    image.save(OUT/(name+'.png'));doc.close()
    return image.convert('RGB')

image64=base64.b64encode(ART.read_bytes()).decode('ascii')
defs=f'''<defs><linearGradient id="fade"><stop offset="0" stop-color="#082a55"/><stop offset="1" stop-color="#082a55" stop-opacity="0"/></linearGradient>
<g id="art"><image width="{C}" height="{H}" href="data:image/png;base64,{image64}"/>
<path d="M0 0H{S}V{H}H0Z M{C-S} 0H{C}V{H}H{C-S}Z" fill="#082a55"/>
<rect x="{S}" width="{FADE}" height="{H}" fill="url(#fade)"/>
<rect width="{FADE}" height="{H}" fill="url(#fade)" transform="translate({C-S},0) scale(-1,1)"/></g></defs>'''
for name,start,length,full in sections:
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{C+O+2*F}mm" height="{length+2*F}mm" viewBox="{-F} {start-F} {C+O+2*F} {length+2*F}">
<title>PROVISOIRE - {name}, fond perdu {F} mm; coupe C+{O} mm par {length} mm</title>{defs}
<rect x="{-F}" y="{start-F}" width="{C+O+2*F}" height="{length+2*F}" fill="#082a55"/>
<use href="#art" x="{-C}"/><use href="#art"/><use href="#art" x="{C}"/></svg>'''
    (OUT/f'panneau-{name}.svg').write_text(svg,encoding='utf-8')

# Une épreuve grand format par section, à imprimer 100 % ou en mosaïque.
c=canvas.Canvas(str(OUT/'epreuve-gabarits-provisoires.pdf'))
c.setTitle('Chasse Galerie 1 - Sillage fleurdelise - EPREUVE PROVISOIRE 1:1')
for n,(name,start,length,full) in enumerate(sections,1):
    W=C+O+2*F+24;PH=length+2*F+48
    c.setPageSize((W*mm,PH*mm)); c.saveState();c.scale(mm,mm)
    x,y=12+F,20+F
    region(c,x,y,start,length,F,O)
    c.setFillColorRGB(.04,.12,.2);c.setFont('Helvetica-Bold',4)
    c.drawString(12,PH-9,f'CHASSE GALERIE 1 / {name.upper()} / EPREUVE PROVISOIRE')
    c.setFont('Helvetica',2.7)
    c.drawString(12,PH-14,f'Coupe : {C+O:.3f} x {length:.3f} mm | tour : {C:.3f} mm | recouvrement : {O:g} mm')
    c.drawString(12,PH-18,f'Cotes du plan, non mesurees. Fond perdu {F:g} mm; retrait {I:g} mm a chaque extremite.')
    # Repères externes, trait pointillé de coupe, limite de recouvrement.
    c.setStrokeColorRGB(.85,.05,.5);c.setLineWidth(.15);c.setDash(2,1)
    c.rect(x,y,C+O,length,fill=0,stroke=1);c.line(x+C,y,x+C,y+length)
    c.setDash()
    for xx in (x,x+C+O):
        for yy in (y,y+length):
            c.line(xx-3,yy,xx+3,yy);c.line(xx,yy-3,xx,yy+3)
    # Axes d'obstacles [A] : repères de contrôle papier, pas trous de coupe.
    if name=='booster':
        for theta in (0,120,240):
            u=((theta-CFG['angle_raccord_scad_deg'])%360)/360*C
            c.setStrokeColorRGB(1,.5,0);c.setDash(2,1)
            c.line(x+u,y-I,x+u,y+val('fin_root')-I)
        c.setDash()
        rails=re.search(r'^rail_z\s*=\s*\[([^]]+)\]',SCAD,re.M)[1]
        for z in map(float,rails.split(',')):
            c.circle(x,y+z-I,6,stroke=1,fill=0)
    c.setStrokeColorRGB(.04,.12,.2);c.setFillColorRGB(.04,.12,.2)
    c.line(12,11,112,11);c.line(12,9,12,13);c.line(112,9,112,13)
    c.setFont('Helvetica',2.5);c.drawString(12,6,'Controle 100 mm - imprimer a 100 %, sans ajuster a la page')
    c.drawRightString(W-12,11,f'Page {n}/2 - guides exclus des SVG et textures')
    c.drawRightString(W-12,6,'Essai papier uniquement; image source env. 61 ppp au format final')
    c.restoreState();c.showPage()
c.save()

# Textures plein tube : marge de peinture de I mm aux extrémités, même repère global.
textures={}
for name,start,length,full in sections:
    im=render_region('texture-'+name,start-I,full)
    textures[name]=im

# OpenRocket : seules les apparences changent, paramètres physiques intacts.
tree=ET.parse(PLANS/'loc-iv-4po.xml');root=tree.getroot()
stage=root.find('rocket/subcomponents/stage/subcomponents')
for node in stage:
    if node.tag not in ('bodytube','nosecone'): continue
    old=node.find('appearance')
    if old is not None: node.remove(old)
    app=ET.SubElement(node,'appearance')
    ET.SubElement(app,'paint',red='8',green='42',blue='85',alpha='255')
    ET.SubElement(app,'shine').text='0.15'
    if node.tag=='bodytube':
        name='payload' if 'payload' in node.findtext('name').lower() else 'booster'
        decal=ET.SubElement(app,'decal',name=f'decals/texture-{name}.png',rotation='0.0',edgemode='REPEAT')
        ET.SubElement(decal,'center',x='0.0',y='0.0')
        ET.SubElement(decal,'offset',x=str(CFG['angle_raccord_scad_deg']/360),y='0.0')
        # RocketFigure3d inverse déjà U pour sa convention main gauche.
        ET.SubElement(decal,'scale',x='1.0',y='1.0')
for node in root.iter('freeformfinset'):
    old=node.find('appearance')
    if old is not None:node.remove(old)
    app=ET.SubElement(node,'appearance');ET.SubElement(app,'paint',red='8',green='42',blue='85',alpha='255');ET.SubElement(app,'shine').text='0.15'
ET.indent(root,space='  ')
xml=ET.tostring(root,encoding='utf-8',xml_declaration=True)
(OUT/'chasse-galerie-1-sillage.xml').write_bytes(xml)
(OUT/'decals').mkdir(exist_ok=True)
with zipfile.ZipFile(OUT/'chasse-galerie-1-sillage.ork','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('rocket.ork',xml)
    for name in textures:
        data=(OUT/f'texture-{name}.png').read_bytes()
        (OUT/f'decals/texture-{name}.png').write_bytes(data)
        z.writestr(f'decals/texture-{name}.png',data)

# SCAD 2021.01 ne plaque pas d'image : tesselles colorées, F5 seulement.
# La conversion échantillonne le document rendu; ne retouche pas l'illustration.
fullimage=render_region('texture-corps',0,H)
cols,rows=CFG['scad_colonnes'],CFG['scad_lignes']
groups=defaultdict(lambda:[[],[]])
for j in range(rows):
    source_y=(j+.5)/rows*H
    if source_y<I or abs(source_y-P)<I or source_y>H-I:continue
    ztop=H-j/rows*H;zbot=H-(j+1)/rows*H
    # Ne pas relier les sections avec une tesselle.
    if source_y<P: zbot=max(ztop-H/rows,B+I)
    else:ztop=min(ztop,B-I)
    for i in range(cols):
        rgb=fullimage.getpixel((min(fullimage.width-1,int((i+.5)/cols*fullimage.width)),min(fullimage.height-1,int((j+.5)/rows*fullimage.height))))
        rgb=tuple(round(v/32)*32/256 for v in rgb)
        pts,faces=groups[rgb];base=len(pts)
        a=math.radians(CFG['angle_raccord_scad_deg']+i*360/cols)
        b=math.radians(CFG['angle_raccord_scad_deg']+(i+1)*360/cols)
        # Coques de tesselles fermées, épaisseur purement graphique 0.10 mm.
        for rr in (R+.05,R+.15):
            for zz,ang in ((zbot,a),(zbot,b),(ztop,b),(ztop,a)):
                pts.append([round(rr*math.cos(ang),5),round(rr*math.sin(ang),5),round(zz,5)])
        for face in ([0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]):
            faces.append([base+k for k in face])
parts=['// GENERE : mosaïque graphique F5; ni texture UV ni pièce de vol.\nmodule sillage_mosaique() {']
for rgb,(pts,faces) in groups.items():
    parts.append(f'color({list(rgb)}) polyhedron(points={json.dumps(pts,separators=(",",":"))},faces={json.dumps(faces,separators=(",",":"))},convexity=4);')
parts.append('}')
(OUT/'mosaique-generee.scad').write_text('\n'.join(parts),encoding='utf-8')
# Source du plan incluse, son dispatch est supprimé dans une copie dérivée.
# Les modules exacts du kit sont réutilisés, jamais le mockup généré.
dispatch='if(part == "assembly") assembly();'
base=SCAD.split(dispatch)[0].replace('view = "cutaway"','view = "assembled"')
base=base.replace('body_d = 101.6;',f'body_d = {2*R};').replace('booster_l = 584.2;',f'booster_l = {B};').replace('payload_l = 279.4;',f'payload_l = {P};')
(OUT/'chasse-galerie-1-sillage.scad').write_text('// GENERE par plans/outils/generer-sillage.py; changer la configuration, puis regenerer.\n// F5 : aperçu coloré. F6/STL ne préservent pas le décor.\n'+base+'''
include <mosaique-generee.scad>
color([0.031,0.165,0.333]) { booster(); translate([0,0,payload_z]) payload();
 translate([0,0,nose_z]) nose();
 for(a=[0:360/fin_count:359]) rotate([0,0,a]) translate([body_d/2-fin_embed,0,fin_z]) fin(); }
if(show_rail_buttons) color("Black") for(z=rail_z) rotate([0,0,60])
 translate([body_d/2,0,z]) rotate([0,90,0]) rail_button();
color("Silver") translate([0,0,aft_ring_z]) retainer();
sillage_mosaique();
''',encoding='utf-8')
metrics={'date':'2026-09-14','statut':CFG['statut'],'circonference_mm':C,'diametre_mm':2*R,'payload_mm':P,'booster_mm':B,'chevauchement_mm':O,'fond_perdu_mm':F,'retrait_mm':I,'image_source_pixels':list(Image.open(ART).size),'resolution_source_ppp':Image.open(ART).width/(C/25.4),'source_scad_sha256':hashlib.sha256(SCAD.encode()).hexdigest(),'tesselles_scad':sum(len(f)//6 for p,f in groups.values()),'couleurs_scad':len(groups)}
(OUT/'dimensions-generees.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(metrics,indent=2,ensure_ascii=False))
