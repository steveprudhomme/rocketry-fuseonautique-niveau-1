"""Visual shadow samples from native orthophoto; project the direction to scene grid."""
import sys,json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path('work/terrain-hybride-v6/pydeps').resolve()))
from pyproj import Transformer
w=Path('work/eclairage-v7');out=Path('outputs/eclairage-v7');roi=json.loads((w/'roi.json').read_text());samples=[{'name':'maison ouest','roof':[868,633],'shadow':[848,611]},{'name':'maison sud','roof':[1066,744],'shadow':[1053,723]},{'name':'bâtiment est','roof':[1357,451],'shadow':[1340,431]}]
t=Transformer.from_crs(2950,32618,always_xy=True);angles=[];im=Image.open(w/'intersection-20cm.png');dr=ImageDraw.Draw(im)
for a in samples:
 p=a['roof'];q=a['shadow'];dx=q[0]-p[0];dy=p[1]-q[1];a['sun_azimuth_mtm_deg']=(math.degrees(math.atan2(dx,dy))+180)%360;angles.append(a['sun_azimuth_mtm_deg']);dr.line([tuple(p),tuple(q)],fill='yellow',width=3);dr.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),outline='red',width=2)
az=float(np.mean(angles));rad=math.radians(az);x,y=roi['roi_upper_left_mtm'];u,v=t.transform(x,y);u2,v2=t.transform(x+100*math.sin(rad),y+100*math.cos(rad));grid=math.degrees(math.atan2(u2-u,v2-v))%360
report={'method':'Manual visual estimate from three roof/shadow edges; approximate, no surveyed building height or capture time','samples':samples,'sun_azimuth_mtm_deg':az,'sun_azimuth_utm_deg':grid,'azimuth_uncertainty_deg':10,'sun_elevation_deg':50,'elevation_status':'Visual choice, not inferred from unknown building heights','sun_energy':2.8,'sun_angular_size_rad':.035,'shadow_correction':'Blender compositor: luminance-dependent linear-light gain up to 1.75; dark materials may also be affected; no geometry changes or invented hidden detail','roi':roi}
(out/'donnees/eclairage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');im.save(out/'mesures-ombres.png');print('SUN_GRID',grid,flush=True)
