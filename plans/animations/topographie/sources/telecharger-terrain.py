import urllib.request,concurrent.futures
from pathlib import Path
urls={'N46W073.tif':'https://opentopography.s3.sdsc.edu/raster/SRTM_GL1/SRTM_GL1_srtm/N46W073.tif','BlenderGIS.zip':'https://codeload.github.com/domlysz/BlenderGIS/zip/refs/heads/master'}
def fetch(pair):
 name,url=pair
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RocketryTerrainProject/1.0'}),timeout=60);data=r.read();Path('work/topographie-v5',name).write_bytes(data);return name,len(data)
 except Exception as e:return name,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for result in ex.map(fetch,urls.items()):print(result,flush=True)
