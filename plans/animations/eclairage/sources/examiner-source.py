"""Read a native-resolution ROI for shadow direction measurement only."""
from pathlib import Path
import urllib.request,struct,json,sys
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path('work/terrain-hybride-v6/pydeps').resolve()))
from pyproj import Transformer
w=Path('work/eclairage-v7');p=json.loads(Path('work/terrain-hybride-v6/orthos/MOS_25_364-5096_20CM_F08.json').read_text(encoding='utf8'));u=p['url']
def get(r):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'Range':'bytes='+r}),timeout=60) as f:
  assert f.status==206;return f.read(),f.headers
head,h=get('0-7');n=int(h['Content-Range'].split('/')[-1]);start=n-90000;tail,_=get(f'{start}-{n-1}');ifd=struct.unpack('<I',head[4:])[0]-start;entries={}
for i in range(struct.unpack('<H',tail[ifd:ifd+2])[0]):
 tag,typ,cnt,val=struct.unpack('<HHII',tail[ifd+2+i*12:ifd+14+i*12]);entries[tag]=(typ,cnt,val)
offs=np.frombuffer(tail,dtype='<u4',count=10000,offset=entries[273][2]-start)
tx=Transformer.from_crs(4326,2950,always_xy=True);x,y=tx.transform(-72.7232675,46.004782);cx=round((x-p['tiepoint'][3])/.2);cy=round((p['tiepoint'][4]-y)/.2)
# 300 m square around intersection, for roof/vegetation shadows.
x0=cx-750;y0=cy-750;assert x0>=0 and y0>=0;raw,_=get(f'{offs[y0]}-{offs[y0+1499]+39999}');a=np.frombuffer(raw,dtype=np.uint8).reshape(1500,10000,4)[:,x0:x0+1500,:3]
Image.fromarray(a).save(w/'intersection-20cm.png');(w/'roi.json').write_text(json.dumps({'x0':x0,'y0':y0,'pixel_size_m':.2,'roi_upper_left_mtm':[p['tiepoint'][3]+x0*.2,p['tiepoint'][4]-y0*.2],'tile':p['file'],'url':u},indent=2),encoding='utf8');print('ROI_READY',cx,cy,flush=True)
