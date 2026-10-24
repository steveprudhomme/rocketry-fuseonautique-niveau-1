"""Frame-accurate glass HUD, qualitative force vectors and post-flight report."""
import json,math,argparse
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
out=Path('outputs/ath-v10');work=Path('work/ath-v10');src=Path('outputs/cinematographie-v8');tele=json.loads((src/'donnees/telemetrie.json').read_text(encoding='utf8'));proj=json.loads((out/'donnees/projections.json').read_text(encoding='utf8'));phys=np.genfromtxt(src/'donnees/vol-h143.csv',delimiter=',',names=True)
W,H=1920,1080;cyan=(102,225,240,255);white=(235,244,249,255);muted=(161,184,197,255);amber=(255,194,105,255);blue=(132,166,255,255)
fonts={}
def font(size,mono=False):
 key=(size,mono)
 if key not in fonts:fonts[key]=ImageFont.truetype('C:/Windows/Fonts/consola.ttf' if mono else 'C:/Windows/Fonts/bahnschrift.ttf',size)
 return fonts[key]
def text(draw,xy,s,size=23,color=white,mono=False,anchor=None):draw.text(xy,s,font=font(size,mono),fill=color,anchor=anchor)
def glass(im,box):
 x0,y0,x1,y1=box;crop=im.crop(box).filter(ImageFilter.GaussianBlur(9)).convert('RGBA');crop=Image.alpha_composite(crop,Image.new('RGBA',crop.size,(4,18,29,210)));mask=Image.new('L',crop.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,crop.width-1,crop.height-1),12,fill=255);im.paste(crop,(x0,y0),mask);d=ImageDraw.Draw(im);d.rounded_rectangle(box,12,outline=(81,137,158,255),width=1);d.line((x0+18,y0,x0+72,y0),fill=cyan,width=2)
def gauge(d,c,value,limit,label,unit):
 x,y=c;r=82;box=(x-r,y-r,x+r,y+r);d.arc(box,140,400,fill=(37,62,79),width=9);d.arc(box,140,140+260*min(max(value/limit,0),1),fill=cyan,width=9)
 for i in range(11):
  th=math.radians(140+i*26);d.line((x+(r+12)*math.cos(th),y+(r+12)*math.sin(th),x+(r+18)*math.cos(th),y+(r+18)*math.sin(th)),fill=muted,width=1)
 text(d,(x,y-10),f'{value:05.1f}',36,mono=True,anchor='mm');text(d,(x,y+29),unit,20,muted,anchor='mm');text(d,(x,y-120),label,20,cyan,anchor='mm');text(d,(x,y+105),f'0 — {limit} {unit}',17,muted,anchor='mm')
phases=['ATTENTE','ALLUMAGE','INERTIE','APOGÉE','DESCENTE','FIN DE VOL']
def phase(f):return 0 if f<61 else 1 if f<113 else 2 if f<366 else 3 if f<384 else 4 if f<977 else 5
ap=int(np.argmax(phys['altitude_m']));mx=float(phys['speed_m_s'].max());landing=tele[976];drift=math.hypot(landing['x'],landing['y'])
report={'apogee_m':float(phys['altitude_m'][ap]),'apogee_time_s':float(phys['time_s'][ap]),'speed_max_m_s':mx,'contact_time_s':landing['time'],'contact_speed_m_s':landing['speed'],'horizontal_range_m':drift,'wind_mean_m_s':2,'reference':'Altitude relative to initial simulation level, not AGL over terrain. Contact speed is the last simulated speed, before visual cushioning.'}
(out/'donnees/bilan.json').write_text(json.dumps(report,indent=2),encoding='utf8')
def wire(d,rotation):
 # Schematic 3D body with nose and three fins, using the evaluated body attitude.
 vertices=[];edges=[];N=10
 for z,r in ((-.65,.065),(.45,.065),(.72,0)):
  for i in range(N):vertices.append([r*math.cos(i*2*math.pi/N),r*math.sin(i*2*math.pi/N),z])
 for j in range(2):
  for i in range(N):edges.extend([(j*N+i,j*N+(i+1)%N),(j*N+i,(j+1)*N+i)])
 for ang in (0,2*math.pi/3,4*math.pi/3):
  k=len(vertices);vertices.extend([[.065*math.cos(ang),.065*math.sin(ang),-.3],[.25*math.cos(ang),.25*math.sin(ang),-.65],[.065*math.cos(ang),.065*math.sin(ang),-.65]]);edges.extend([(k,k+1),(k+1,k+2),(k+2,k)])
 v=np.array(vertices)@np.array(rotation).T;view=np.array([[.83,-.55,0],[.25,.37,-.89]]);q=v@view.T*115+np.array([180,768])
 for i,j in edges:d.line((*q[i],*q[j]),fill=(102,198,215),width=1)
 text(d,(180,667),'ATTITUDE · VUE 3D',18,cyan,anchor='mm');text(d,(180,877),'Schéma du corps',17,muted,anchor='mm')
def draw_report(d):
 text(d,(60,145),'BILAN DU VOL SIMULÉ',27,cyan)
 rows=[('APOGÉE',f"{report['apogee_m']:.1f} m"),('VITESSE MAX.',f'{mx:.1f} m/s'),('DURÉE DU VOL',f"{landing['time']:.2f} s"),('DÉRIVE HORIZ.',f'{drift:.1f} m'),('VITESSE AU CONTACT',f"{landing['speed']:.2f} m/s")]
 for i,(label,value) in enumerate(rows):text(d,(60,203+i*49),label,19,muted);text(d,(540,203+i*49),value,24,white,True,anchor='ra')
 x0,y0,x1,y1=70,490,532,670;d.line((x0,y0,x0,y1,x1,y1),fill=muted,width=1)
 pts=[(x0+float(t)/landing['time']*(x1-x0),y1-float(h)/650*(y1-y0)) for t,h in zip(phys['time_s'],phys['altitude_m']) if t<=landing['time']];d.line(pts,fill=cyan,width=2)
 text(d,(70,465),'ALTITUDE / TEMPS PHYSIQUE',17,cyan);text(d,(70,680),'0 s',17,muted);text(d,(532,680),'106,7 s',17,muted,anchor='ra')
 for i,line in enumerate(['Altitude relative au départ simulé.','Vitesse avant amortissement visuel.','Vent moyen du scénario : 2 m/s.','Modèle provisoire · aucune mesure réelle.']):text(d,(60,730+i*30),line,18,muted)
def arrows(im,d,r,p):
 f=r['frame'];keys=['poussee','trainee','gravite'] if 76<=f<=106 else ['trainee','gravite'] if 165<=f<=230 else []
 if not keys:return
 anchor=np.array(p['anchor']);colors={'poussee':cyan,'trainee':amber,'gravite':blue}
 for i,key in enumerate(keys):
  vec=p['vectors'][key]
  if vec is None:continue
  v=np.array(vec);perp=np.array([-v[1],v[0]]);start=anchor+perp*(i-1)*18;end=start+v*(100 if key=='poussee' else 75)
  d.line((*start,*end),fill=colors[key],width=4);d.polygon([tuple(end),tuple(end-v*15+perp*7),tuple(end-v*15-perp*7)],fill=colors[key])
 # Fixed key avoids overlapping names when gravity and drag project together.
 glass(im,(620,840,1375,920));d=ImageDraw.Draw(im)
 text(d,(645,855),'POUSSÉE' if 'poussee' in keys else 'POUSSÉE NULLE',17,cyan if 'poussee' in keys else muted);text(d,(830,855),'TRAÎNÉE',19,amber);text(d,(1010,855),'GRAVITÉ',19,blue)
 text(d,(645,886),'Directions qualitatives · longueurs non comparables',19,white)
def render(f):
 r=tele[f-1];p=proj[f-1];im=Image.open(Path('work/cinematographie-v8/frames')/f'vol-{f:04d}.jpg').convert('RGBA');glass(im,(32,24,1888,92));glass(im,(1580,118,1888,700));glass(im,(1580,722,1888,923));glass(im,(32,950,1888,1054));glass(im,(32,118,570 if f>=977 else 328,923));d=ImageDraw.Draw(im)
 text(d,(56,43),'CHASSE GALERIE 1',30);text(d,(530,49),'TÉLÉMÉTRIE DE SIMULATION / H143',21,muted);text(d,(1855,49),'ATH · 10',21,cyan,True,anchor='ra')
 if f<977:gauge(d,(180,265),r['altitude'],650,'ALTITUDE','m');gauge(d,(180,515),r['speed'],150,'VITESSE','m/s');wire(d,p['body_rotation'])
 else:draw_report(d)
 text(d,(1604,143),'SÉQUENCE DE VOL',23,cyan);active=phase(f);d.line((1622,220,1622,610),fill=(60,89,105),width=2)
 for i,label in enumerate(phases):
  y=220+i*78
  if i==active:
   glow=Image.new('RGBA',im.size);gd=ImageDraw.Draw(glow);rad=14+int(3*math.sin(f/5));gd.ellipse((1622-rad,y-rad,1622+rad,y+rad),fill=(70,230,255,160));im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(7)));d=ImageDraw.Draw(im)
  d.ellipse((1617,y-5,1627,y+5),fill=cyan if i<=active else (57,80,96));text(d,(1646,y-12),label,23,cyan if i==active else muted)
 text(d,(1605,657),'Repères pédagogiques',17,muted)
 text(d,(1604,746),'TEMPS PHYSIQUE',18,cyan);text(d,(1604,776),f"t + {r['time']:06.2f} s",29,white,True)
 rate=r['rate'];text(d,(1604,833),'APRÈS CONTACT' if f>=977 else 'LECTURE',17,muted);text(d,(1604,861),f"+ {r.get('post_contact_s',0):.1f} s visuelles" if f>=977 else rate.replace('TEMPS RÉEL','Temps réel').replace('ATTENTE','Attente'),20)
 arrows(im,d,r,p);d=ImageDraw.Draw(im)
 text(d,(55,965),'OPENROCKET · MODÈLE PROVISOIRE  |  Altitude relative au départ simulé · raccord au relief illustratif',20)
 text(d,(55,1000),'Orthophoto © Région Centre-du-Québec 2025 · CC BY 4.0  |  Relief SRTM NASA/NGA  |  Musique originale : Sept sillages',18,muted)
 path=work/'frames'/f'ath-{f:04d}.jpg';im.convert('RGB').save(path,quality=95)
 if f in (1,85,200,369,650,977,1100,1217):im.convert('RGB').save(out/f'apercu-{f}.jpg',quality=95)
frames=(1,85,200,369,650,977,1100,1217) if a.preview else range(1,1218)
for f in frames:
 render(f)
 if f%100==0:print('FRAME',f,flush=True)
(out/'donnees/ath.json').write_text(json.dumps({'frames':1217,'fps':30,'font':'Bahnschrift + Consolas (system fonts, not redistributed)','glass_blur_px':9,'phases':phases,'phase_frame_boundaries':[1,61,113,366,384,977],'apogee_highlight':'Visual event window around the simulated apogee, not an additional physical state.','force_windows_frames':[[76,106],[165,230]],'force_note':'Qualitative projected directions only. Drag opposes velocity relative to mean westward 2 m/s wind, ignoring wind fluctuations. No force magnitudes or force balance inferred.','wireframe_note':'Schematic rocket body using evaluated Blender body orientation; not a manufacturing model.','postflight_report_frame':977},ensure_ascii=False,indent=2),encoding='utf8')
print('HUD_RENDERED',len(frames),flush=True)
