"""Mosaic open orthophotos in their native MTM8 CRS and compute terrain UVs."""
from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path('work/terrain-hybride-v6/pydeps').resolve()))
from pyproj import Transformer
w=Path('work/terrain-hybride-v6');out=Path('outputs/terrain-hybride-v6');d=np.load('outputs/topographie-v5/donnees/terrain-srtm.npz');m=json.load(open('outputs/topographie-v5/donnees/georeferencement.json',encoding='utf8'))
records=json.load(open(out/'donnees/provenance-orthophotos.json',encoding='utf8'))
left=min(r['tiepoint'][3] for r in records);top=max(r['tiepoint'][4] for r in records);right=max(r['tiepoint'][3]+2000 for r in records);bottom=min(r['tiepoint'][4]-2000 for r in records)
canvas=Image.new('RGB',(round((right-left)/2),round((top-bottom)/2)))
for r in records:
 im=Image.open(w/'orthos'/str(r['file']+'.png'));canvas.paste(im,(round((r['tiepoint'][3]-left)/2),round((top-r['tiepoint'][4])/2)))
canvas.save(out/'donnees/orthophoto-2025-2m.jpg',quality=95,subsampling=0)
t=Transformer.from_crs(32618,2950,always_xy=True);tll=Transformer.from_crs(32618,4326,always_xy=True)
v=d['vertices'];x,y=t.transform(v[:,0]+m['origin_easting_m'],v[:,1]+m['origin_northing_m']);uv=np.stack(((x-left)/(right-left),(y-bottom)/(top-bottom)),axis=1)
assert np.all((uv>=0)&(uv<=1))
# Bilinear elevations precomputed on a 2 m render grid. This adds no measured detail.
gx=np.arange(-3300,3301,2);gy=np.arange(-3300,3301,2)
# Three render subdivisions of each native sample interval; reference mesh stays intact.
lo,la=np.meshgrid(np.linspace(d['lons'][0],d['lons'][-1],(len(d['lons'])-1)*3+1),np.linspace(d['lats'][0],d['lats'][-1],(len(d['lats'])-1)*3+1));back=Transformer.from_crs(4326,32618,always_xy=True);px,py=back.transform(lo,la);px-=m['origin_easting_m'];py-=m['origin_northing_m'];u=(lo-d['lons'][0])*3600;vv=(d['lats'][0]-la)*3600;i=np.clip(u.astype(int),0,len(d['lons'])-2);j=np.clip(vv.astype(int),0,len(d['lats'])-2);a=u-i;b=vv-j;h=d['heights'];z=(h[j,i]*(1-a)+h[j,i+1]*a)*(1-b)+(h[j+1,i]*(1-a)+h[j+1,i+1]*a)*b-m['origin_elevation_egm96_m']
pad=np.array([-80.,0.]);landing=pad+[-163.75930786132812,-.01506391353905201]
def height(p):
 lo,la=tll.transform(p[0]+m['origin_easting_m'],p[1]+m['origin_northing_m']);uu=(lo-d['lons'][0])*3600;v0=(d['lats'][0]-la)*3600;ii=int(uu);jj=int(v0);aa=uu-ii;bb=v0-jj
 return float((h[jj,ii]*(1-aa)+h[jj,ii+1]*aa)*(1-bb)+(h[jj+1,ii]*(1-aa)+h[jj+1,ii+1]*aa)*bb-m['origin_elevation_egm96_m'])
# Small render support discs avoid claiming SRTM resolves centimetric contact physics.
zoriginal=z.copy();levels=[]
for p in (pad,landing):
 level=height(p);levels.append(level);r=np.hypot(px-p[0],py-p[1]);f=np.clip((r-16)/16,0,1);f=f*f*(3-2*f);z=level*(1-f)+z*f
xx,yy=t.transform(px+m['origin_easting_m'],py+m['origin_northing_m']);patchuv=np.stack(((xx-left)/(right-left),(yy-bottom)/(top-bottom)),axis=-1)
np.savez_compressed(out/'donnees/hybride.npz',uv=uv,patch_xyz=np.stack((px,py,z),axis=-1),patch_uv=patchuv,pad=np.r_[pad,levels[0]],landing=np.r_[landing,levels[1]])
spec={'crs_imagery':'EPSG:2950','crs_scene':'EPSG:32618','imagery_bounds_m':[left,bottom,right,top],'texture_resolution_m':2,'texture_size':canvas.size,'pad_local_m':[*pad,levels[0]],'landing_local_m':[*landing,levels[1]],'pad_wgs84':list(tll.transform(pad[0]+m['origin_easting_m'],pad[1]+m['origin_northing_m'])),'pad_status':'Provisional illustrative placement 80 m west of intersection, not surveyed','detail_radius_m':30,'blend_start_m':24,'blend_end_m':36,'support_flat_radius_m':16,'support_blend_end_m':32,'render_support_max_height_change_m':float(abs(z-zoriginal).max()),'elevation_note':'Native SRTM unchanged in reference scene; render mesh bilinearly interpolated, with two level support discs for existing landing animation. No new measured elevation accuracy.'}
(out/'donnees/terrain-hybride.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf8')
# A geospatially faithful plan-view preview around the site for placement review.
cx,cy=t.transform(m['origin_easting_m'],m['origin_northing_m']);ix=int((cx-left)/2);iy=int((top-cy)/2);canvas.crop((ix-200,iy-150,ix+200,iy+150)).resize((1200,900)).save(w/'site-orthophoto.png')
print('MOSAIC_UV_READY',spec,flush=True)
