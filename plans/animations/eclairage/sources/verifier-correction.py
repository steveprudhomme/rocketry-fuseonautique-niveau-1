"""Pixel-layout and tone-change QA; comparison panels are inspection artifacts."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
w=Path('work/eclairage-v7');out=Path('outputs/eclairage-v7');old=Image.open('outputs/terrain-hybride-v6/donnees/orthophoto-2025-2m.jpg').convert('RGB');new=Image.open(out/'donnees/orthophoto-ombres-attenuees.png').convert('RGB');assert old.size==new.size==(5000,4000)
a=np.asarray(old).astype(np.float32)/255;b=np.asarray(new).astype(np.float32)/255
lin=lambda x:np.where(x<=.04045,x/12.92,((x+.055)/1.055)**2.4)
al=lin(a);bl=lin(b);lum=al@np.array([.2126,.7152,.0722],dtype=np.float32);gain=1+.75*np.clip((.085-lum)/(.085-.008),0,1);expected=al*gain[:,:,None];err=np.abs(bl-expected);dark=(lum>.01)&(lum<.045);bright=lum>.12
# Blender's RGB-to-luminance coefficients can vary slightly with color management.
assert np.percentile(err,99)<.008,float(np.percentile(err,99));assert np.percentile(np.abs(b-a)[bright],99)<=2/255
report={'size':old.size,'no_warp_or_resampling':True,'linear_model_error_p99':float(np.percentile(err,99)),'dark_linear_luminance_gain_median':float(np.median((bl@np.array([.2126,.7152,.0722]))[dark]/lum[dark])),'bright_srgb_change_p99':float(np.percentile(np.abs(b-a)[bright],99)),'source_sha256':hashlib.sha256(Path('outputs/terrain-hybride-v6/donnees/orthophoto-2025-2m.jpg').read_bytes()).hexdigest(),'result_sha256':hashlib.sha256((out/'donnees/orthophoto-ombres-attenuees.png').read_bytes()).hexdigest()}
(out/'verification-correction.json').write_text(json.dumps(report,indent=2),encoding='utf8')
# Central ROI in the same MTM grid, annotated before/after without changing delivered texture.
roi=json.loads((w/'roi.json').read_text());cx=int((roi['roi_upper_left_mtm'][0]+150-360000)/2);cy=int((5100000-roi['roi_upper_left_mtm'][1]+150)/2);box=(cx-160,cy-130,cx+160,cy+130)
panel=Image.new('RGB',(1600,700),'#172735');dr=ImageDraw.Draw(panel);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
for i,(im,title) in enumerate([(old,'AVANT — orthophoto v6'),(new,'APRÈS — ombres atténuées')]):panel.paste(im.crop(box).resize((800,650)),(800*i,45));dr.text((20+800*i,15),title,fill='white',font=font)
panel.save(out/'comparaison-orthophoto.jpg',quality=95);print('PIXELS_VERIFIED',report,flush=True)
