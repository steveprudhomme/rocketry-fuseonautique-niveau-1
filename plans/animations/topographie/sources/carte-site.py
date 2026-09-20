"""Static elevation map from the native SRTM raster; north-up, geographic grid."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
out=Path('outputs/topographie-v5');a=np.load(out/'donnees/terrain-srtm.npz');z=a['heights'].astype(float);m=json.loads((out/'donnees/georeferencement.json').read_text(encoding='utf8'));features=json.loads((out/'donnees/site.geojson').read_text(encoding='utf8'))['features']
dy,dx=np.gradient(z,30.9,21.5);shade=np.clip(.75+dx*.75+dy*.9,.3,1.1)
stops=np.array([[22,64,78],[39,91,86],[91,124,99],[174,176,130],[231,218,174]])
t=np.clip((z-10)/49,0,1)*4;ii=np.minimum(3,t.astype(int));f=t-ii;rgb=(stops[ii]*(1-f[:,:,None])+stops[ii+1]*f[:,:,None])*shade[:,:,None];rgb=np.clip(rgb,0,255).astype('uint8')
W=1600;canvas=Image.new('RGB',(W,1840),'#101e28');draw=ImageDraw.Draw(canvas)
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),n)
draw.text((80,55),'CHASSE GALERIE 1',font=font(26,True),fill='#f1b783');draw.text((80,101),'Le site en relief',font=font(62,True),fill='white');draw.text((80,181),'Rang Letendre × 10e Rang · Saint-Pie-de-Guire',font=font(30),fill='#c8d9de')
box=(110,300,1490,1680);size=1380;canvas.paste(Image.fromarray(rgb).resize((size,size),Image.Resampling.BILINEAR),(110,300));draw=ImageDraw.Draw(canvas)
west,south,east,north=m['bounds_wgs84']
def xy(lon,lat):return (110+(lon-west)/(east-west)*size,300+(north-lat)/(north-south)*size)
for lo in np.arange(math.ceil(west*100)/100,east,.01):
 x,y=xy(lo,north);draw.line((x,300,x,1680),fill='#6b8583',width=1);draw.text((x-25,272),f'{lo:.2f}°',font=font(17),fill='#b9cccf')
for la in np.arange(math.ceil(south*100)/100,north,.01):
 x,y=xy(west,la);draw.line((110,y,1490,y),fill='#6b8583',width=1);draw.text((16,y-8),f'{la:.2f}°',font=font(17),fill='#b9cccf')
for feature in features:
 if feature['geometry']['type']!='LineString':continue
 pts=[xy(*c) for c in feature['geometry']['coordinates']];draw.line(pts,fill='#102832',width=10);draw.line(pts,fill='#fff1d4',width=5)
x,y=xy(m['longitude'],m['latitude']);draw.ellipse((x-14,y-14,x+14,y+14),fill='#f37759',outline='white',width=3)
draw.rounded_rectangle((x+30,y-100,x+530,y-3),radius=12,fill='#142934');draw.text((x+48,y-86),'INTERSECTION · REPÈRE',font=font(23,True),fill='white');draw.text((x+48,y-49),'46,004782° N  ·  72,7232675° O',font=font(22),fill='#d1dedf');draw.line((x+12,y-12,x+30,y-20),fill='white',width=2)
draw.text((x-390,y+115),'Rang Letendre',font=font(25,True),fill='white');draw.text((x-95,y-210),'10e Rang',font=font(25,True),fill='white')
draw.polygon([(1410,345),(1396,388),(1410,380),(1424,388)],fill='white');draw.text((1400,400),'N',font=font(25,True),fill='white')
scale=1000/((east-west)*111319.49*math.cos(math.radians(m['latitude'])))*size;draw.line((165,1600,165+scale,1600),fill='white',width=5);draw.text((165,1560),'1 km',font=font(23),fill='white')
for i in range(440):
 t=i/439*4;j=min(3,int(t));f=t-j;c=tuple((stops[j]*(1-f)+stops[j+1]*f).astype(int));draw.line((1000+i,1588,1000+i,1607),fill=c)
draw.text((1000,1550),'Altitude EGM96',font=font(23),fill='white');draw.text((1000,1618),'10 m',font=font(21),fill='white');draw.text((1385,1618),'59 m',font=font(21),fill='white')
draw.text((110,1710),'SRTM GL1 · 1 seconde d’arc (~30 m) · 57 200 sommets · relief sans exagération',font=font(23),fill='#e3eded');draw.text((110,1747),'NASA / NGA · OpenTopography · © contributeurs OpenStreetMap (ODbL)',font=font(21),fill='#a4bcc4');draw.text((110,1784),'Repère cartographique : emplacement exact du pas de tir à confirmer sur le terrain.',font=font(21),fill='#a4bcc4');canvas.save(out/'carte-topographique.png')
