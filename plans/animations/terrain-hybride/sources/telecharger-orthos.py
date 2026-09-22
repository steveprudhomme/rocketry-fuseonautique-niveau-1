"""Read one native row in ten using HTTP multiranges; keep RGB, discard NIR.
Source images are 0.2 m uncompressed TIFFs. Output is a 2 m visual texture,
not a substitute for the original orthophotography for measurement.
"""
import urllib.request,struct,json,re,concurrent.futures,hashlib,time
from pathlib import Path
import numpy as np
from PIL import Image
w=Path('work/terrain-hybride-v6');out=Path('outputs/terrain-hybride-v6/donnees');(w/'orthos').mkdir(exist_ok=True)
fs=json.loads((w/'index-site.json').read_text(encoding='utf8'))['features'];fs=[f for f in fs if re.fullmatch(r'MOS_25_\d+-\d+_20CM_F08',f['properties']['NOM_FICHIER'])]
def get(url,ranges):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':'bytes='+ranges,'User-Agent':'ChasseGalerieTerrain/1.0'}),timeout=50) as r:
    assert r.status==206,('Server must honor byte ranges',url,ranges,r.status);return r.read(),r.headers
  except Exception:
   if attempt==2:raise
   time.sleep(1+attempt)
fs.sort(key=lambda f: f['properties']['NOM_FICHIER'] != 'MOS_25_364-5096_20CM_F08')
records=[]
for f in fs:
 p=f['properties'];name=p['NOM_FICHIER'];dest=w/'orthos'/f'{name}.png';meta=w/'orthos'/f'{name}.json'
 if dest.exists() and meta.exists():records.append(json.loads(meta.read_text(encoding='utf8')));continue
 u=p['TELECHARGEMENT_FICHIER'];head,hd=get(u,'0-7');total=int(hd['Content-Range'].split('/')[-1]);start=total-90000;tail,_=get(u,f'{start}-{total-1}');ifd=struct.unpack('<I',head[4:8])[0]-start;n=struct.unpack('<H',tail[ifd:ifd+2])[0];entries={}
 for i in range(n):
  tag,typ,count,value=struct.unpack('<HHII',tail[ifd+2+i*12:ifd+14+i*12]);entries[tag]=(typ,count,value)
 def vals(tag):
  typ,count,v=entries[tag];fmt={3:'H',4:'I',12:'d'}[typ];size=struct.calcsize(fmt)*count;raw=struct.pack('<I',v) if size<=4 else tail[v-start:v-start+size];return struct.unpack('<'+fmt*count,raw[:size])
 assert vals(256)==(10000,) and vals(257)==(10000,) and vals(259)==(1,) and vals(277)==(4,) and vals(278)==(1,) and vals(284)==(1,)
 offsets=vals(273);sizes=vals(279);tie=vals(33922);scale=vals(33550);pixels=np.zeros((1000,1000,3),dtype=np.uint8)
 groups=[list(range(k,min(k+2,1000))) for k in range(0,1000,2)]
 def batch(js):
  requests=[(offsets[j*10+5],sizes[j*10+5],j) for j in js];data,h=get(u,','.join(f'{a}-{a+n-1}' for a,n,j in requests));lookup={a:j for a,n,j in requests}
  boundary=h['Content-Type'].split('boundary=')[-1].strip('"').encode();seen=0
  for part in data.split(b'--'+boundary):
   if b'Content-Range:' not in part:continue
   header,raw=part.split(b'\r\n\r\n',1);match=re.search(rb'Content-Range: bytes (\d+)-(\d+)/',header);a,z=map(int,match.groups());raw=raw[:z-a+1];arr=np.frombuffer(raw,dtype=np.uint8).reshape(10000,4)[:,:3];pixels[lookup[a]]=arr.reshape(1000,10,3).mean(axis=1).astype(np.uint8);seen+=1
  assert seen==len(js),(seen,len(js))
  if js[0]%100==0: print(name,js[0],flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(batch,groups))
 Image.fromarray(pixels).save(dest)
 record={'file':name,'url':u,'original_resolution_m':.2,'output_resolution_m':2,'processing':'one native row in ten, horizontal mean of ten RGB pixels; NIR discarded','tiepoint':tie,'pixel_scale':scale,'licence':p['LICENCE'],'copyright':'© Région Centre-du-Québec','acquisition':p['DATE_ACQUISITION'],'season':'Printemps','sha256_texture':hashlib.sha256(dest.read_bytes()).hexdigest()};meta.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8');records.append(record);print('ORTHO_READY',name,flush=True)
(out/'provenance-orthophotos.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print('ALL_ORTHOS_READY',len(records),flush=True)
