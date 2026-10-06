"""Encode and fully decode the two final MP4s with credited French overlays."""
import subprocess,json,sys,hashlib,re
from pathlib import Path
out=Path('outputs/cinematographie-v8');w=Path('work/cinematographie-v8');ff='C:/Windows/system32/ffmpeg.exe'
assert len(list((w/'frames').glob('vol-*.jpg')))==1217
assert len(list((w/'optique-corrigee').glob('optique-*.jpg')))==150
ass=(out/'sources/titres.ass').read_text(encoding='utf-8-sig')
ass=ass.replace('Paysage, fumée et déploiement illustratifs — vent moyen : 2 m/s (7,2 km/h)','Altitude : niveau initial de simulation · raccord au relief illustratif\\NOrthophoto © Région Centre-du-Québec 2025 · CC BY 4.0 · relief SRTM NASA/NGA')
ass=ass.replace('Style: Footer,Arial,23','Style: Footer,Arial,21');(out/'sources/titres.ass').write_text(ass,encoding='utf-8-sig')
header=ass.split('[Events]')[0]+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
detail=header+'Dialogue: 0,0:00:00.00,0:00:05.00,Title,,0,0,0,,CHASSE GALERIE 1 | CONTRÔLE OPTIQUE\nDialogue: 0,0:00:00.00,0:00:05.00,Data,,0,0,0,,Vue de contrôle face au soleil\\NReflets conditionnés à la direction lumineuse\nDialogue: 0,0:00:00.00,0:00:05.00,Footer,,0,0,0,,Orthophoto © Région Centre-du-Québec 2025 · CC BY 4.0\\NRelief SRTM NASA/NGA · pas de tir et chaumes illustratifs\n'
(out/'sources/detail.ass').write_text(detail,encoding='utf-8-sig')
reports=[]
for pattern,count,subtitle,name in [('frames/vol-%04d.jpg',1217,'titres.ass','chasse-galerie-1-vol-complet.mp4'),('optique-corrigee/optique-%04d.jpg',150,'detail.ass','extrait-optique.mp4')]:
 dest=out/name;cmd=[ff,'-hide_banner','-loglevel','error','-y','-framerate','30','-start_number','1','-i',str(w/pattern),'-frames:v',str(count),'-vf','ass='+str(out/'sources'/subtitle).replace('\\','/'),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)];subprocess.run(cmd,check=True)
 check=subprocess.run([ff,'-hide_banner','-v','error','-i',str(dest),'-map','0:v:0','-f','null','-','-progress','pipe:1'],capture_output=True,text=True,check=True);frames=int(re.findall(r'frame=(\d+)',check.stdout)[-1]);assert frames==count and not check.stderr,(frames,check.stderr)
 reports.append({'file':name,'decoded_frames':frames,'fps':30,'duration_s':frames/30,'size_bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'decode_errors':check.stderr});print('ENCODED_VERIFIED',name,frames,flush=True)
(out/'verification-video.json').write_text(json.dumps(reports,indent=2),encoding='utf8')
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss','7.7','-i',str(out/'chasse-galerie-1-vol-complet.mp4'),'-frames:v','1','-update','1',str(out/'apercu-video.jpg')],check=True)
