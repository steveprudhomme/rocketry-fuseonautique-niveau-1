import urllib.request
from pathlib import Path
urls={'N45W073.tif':'https://opentopography.s3.sdsc.edu/raster/SRTM_GL1/SRTM_GL1_srtm/N45W073.tif','rang10-osm.json':'https://api.openstreetmap.org/api/0.6/way/349408868/full.json'}
for name,url in urls.items():
 data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RocketryTerrainProject/1.0'}),timeout=45).read();Path('work/topographie-v5',name).write_bytes(data);print(name,len(data))
