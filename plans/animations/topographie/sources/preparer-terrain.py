"""Crop native SRTM GL1 point samples; project with BlenderGIS's UTM implementation."""
from pathlib import Path
import json,math,hashlib,importlib.util,shutil
import numpy as np
from PIL import Image,TiffImagePlugin
w=Path('work/topographie-v5');out=Path('outputs/topographie-v5');(out/'donnees').mkdir(parents=True,exist_ok=True);(out/'sources').mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('utm',w/'addons/BlenderGIS-master/core/proj/utm.py');utm=importlib.util.module_from_spec(spec);spec.loader.exec_module(utm);proj=utm.UTM(18,True)
a=json.loads((w/'letendre-osm.json').read_text(encoding='utf8'));b=json.loads((w/'rang10-osm.json').read_text(encoding='utf8'));ways=[next(x for x in d['elements'] if x['type']=='way') for d in [a,b]];common=set(ways[0]['nodes'])&set(ways[1]['nodes']);assert common=={540514913};node=next(x for x in a['elements'] if x['id'] in common);lon0,lat0=node['lon'],node['lat'];ex,ny=proj.lonlat_to_utm(lon0,lat0)
tiles={lat:np.array(Image.open(w/f'N{lat}W073.tif')) for lat in [45,46]}
assert np.array_equal(tiles[46][-1],tiles[45][0]),'Tile seam mismatch'
def sample(lon,lat):
 degree=math.floor(lat);arr=tiles[degree];x=(lon+73)*3600;y=(degree+1-lat)*3600;i,j=int(x),int(y);fx,fy=x-i,y-j
 return float((arr[j,i]*(1-fx)+arr[j,i+1]*fx)*(1-fy)+(arr[j+1,i]*(1-fx)+arr[j+1,i+1]*fx)*fy)
h0=sample(lon0,lat0)
# Native geographic grid covering approximately 6.1 km by 6.1 km.
west=math.floor((lon0-.0395)*3600);east=math.ceil((lon0+.0395)*3600);south=math.floor((lat0-.0275)*3600);north=math.ceil((lat0+.0275)*3600)
lons=np.arange(west,east+1)/3600;lats=np.arange(north,south-1,-1)/3600;vertices=[];heights=[];errors=[]
for lat in lats:
 line=[]
 for lon in lons:
  degree=math.floor(lat);i=round((lon+73)*3600);j=round((degree+1-lat)*3600);h=int(tiles[degree][j,i]);assert h!=-32768
  x,y=proj.lonlat_to_utm(float(lon),float(lat));vertices.append((x-ex,y-ny,h-h0));line.append(h)
  if len(vertices)%997==0:
   lo,la=proj.utm_to_lonlat(x,y);errors.append(max(abs(lo-lon),abs(la-lat)))
 heights.append(line)
vertices=np.array(vertices,dtype=np.float64);heights=np.array(heights,dtype=np.int16);np.savez_compressed(out/'donnees/terrain-srtm.npz',vertices=vertices,heights=heights,lons=lons,lats=lats)
tags=TiffImagePlugin.ImageFileDirectory_v2();tags[33550]=(1/3600,1/3600,0);tags[33922]=(0.,0.,0.,float(lons[0]),float(lats[0]),0.);tags[34735]=(1,1,0,3,1024,0,1,2,1025,0,1,2,2048,0,1,4326);tags[42113]='-32768'
tags.tagtype[33550]=12;tags.tagtype[33922]=12;tags.tagtype[34735]=3;tags.tagtype[42113]=2
Image.fromarray(heights.astype(np.int32)).save(out/'donnees/srtm-site-wgs84.tif',tiffinfo=tags,compression='tiff_deflate')
roads=[];features=[]
for data,way in zip([a,b],ways):
 nodes={n['id']:n for n in data['elements'] if n['type']=='node'};coords=[[nodes[n]['lon'],nodes[n]['lat']] for n in way['nodes']];xyz=[]
 for lon,lat in coords:
  x,y=proj.lonlat_to_utm(lon,lat);xyz.append([x-ex,y-ny,sample(lon,lat)-h0])
 roads.append({'osm_way_id':way['id'],'name':way['tags']['name'],'vertices':xyz})
 features.append({'type':'Feature','properties':{'name':way['tags']['name'],'osm_way_id':way['id']},'geometry':{'type':'LineString','coordinates':coords}})
features.append({'type':'Feature','properties':{'name':'Intersection — origine de la scène','osm_node_id':540514913},'geometry':{'type':'Point','coordinates':[lon0,lat0]}})
(out/'donnees/site.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False,indent=2),encoding='utf8')
(out/'donnees/routes-locales.json').write_text(json.dumps(roads,ensure_ascii=False),encoding='utf8')
meta={'name':'Intersection du rang Letendre et du 10e Rang, Saint-Pie-de-Guire','latitude':lat0,'longitude':lon0,'osm_node_id':540514913,'osm_way_ids':[w['id'] for w in ways],'crs':'EPSG:32618','origin_easting_m':ex,'origin_northing_m':ny,'origin_elevation_egm96_m':h0,'vertical_datum':'EGM96 EPSG:5773','dem':'NASA/NGA SRTM GL1 v3, hosted by OpenTopography','acquisition':'2000-02-11/2000-02-22','native_spacing_arcsec':1,'approx_spacing_east_m':21.5,'approx_spacing_north_m':30.9,'rows':len(lats),'cols':len(lons),'vertices':len(vertices),'faces':(len(lats)-1)*(len(lons)-1),'elevation_range_m':[int(heights.min()),int(heights.max())],'bounds_wgs84':[float(lons[0]),float(lats[-1]),float(lons[-1]),float(lats[0])],'vertical_exaggeration':1,'void_samples':0,'tile_seam_equal':True,'utm_roundtrip_max_degrees':max(errors),'retrieved':'2026-09-17','source_tiles':[{'name':f'N{lat}W073.tif','url':f'https://opentopography.s3.sdsc.edu/raster/SRTM_GL1/SRTM_GL1_srtm/N{lat}W073.tif','sha256':hashlib.sha256((w/f'N{lat}W073.tif').read_bytes()).hexdigest()} for lat in [45,46]],'scope':'Intersection is a geographic reference, not a surveyed launch-pad position. SRTM is a radar surface model, not centimetre-accurate bare-earth lidar.'}
(out/'donnees/georeferencement.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
for name in ['letendre-osm.json','rang10-osm.json']:shutil.copy2(w/name,out/'donnees'/name)
shutil.copy2(w/'BlenderGIS.zip',out/'sources/BlenderGIS-original.zip')
print(json.dumps(meta,ensure_ascii=False,indent=2))
