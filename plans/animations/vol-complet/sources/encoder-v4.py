from pathlib import Path
import subprocess,time,json
b=Path.cwd();w=b/'work/atmosphere-v4';out=b/'outputs/vol-complet-v4';ff='C:/Windows/system32/ffmpeg.exe'
while not all('Blender quit' in (w/name).read_text(encoding='utf8',errors='replace') for name in ['rendu.log','dilution.log']):time.sleep(5)
assert len(list((w/'frames').glob('vol-*.png')))==1217
def run(args):subprocess.run([ff,'-hide_banner','-loglevel','error','-y']+args,check=True)
if not (out/'chasse-galerie-1-vol-complet.mp4').exists():run(['-framerate','30','-start_number','1','-i',str(w/'frames/vol-%04d.png'),'-frames:v','1217','-vf','ass=outputs/vol-complet-v4/sources/titres.ass','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'chasse-galerie-1-vol-complet.mp4')])
ass=(out/'sources/titres.ass').read_text(encoding='utf-8-sig').split('Dialogue:')[0]
ass+='Dialogue: 0,0:00:00.00,0:00:08.04,Title,,0,0,0,,FUMÉE VOLUMÉTRIQUE | VUE FIXE\nDialogue: 0,0:00:00.00,0:00:08.04,Footer,,0,0,0,,Vent moyen : 2 m/s (7,2 km/h)\\NDispersion et turbulences procédurales — illustration\n'
(w/'detail.ass').write_text(ass,encoding='utf-8-sig')
run(['-framerate','30','-start_number','61','-i',str(w/'detail/fumee-%04d.png'),'-frames:v','241','-vf','ass=work/atmosphere-v4/detail.ass','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'extrait-atmosphere.mp4')])
for name,start,count in [('extrait-atterrissage.mp4',29.5,332),('extrait-recuperation.mp4',10,180)]:
 run(['-ss',str(start),'-i',str(out/'chasse-galerie-1-vol-complet.mp4'),'-frames:v',str(count),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/name)])
run(['-ss','2.8','-i',str(out/'chasse-galerie-1-vol-complet.mp4'),'-frames:v','1',str(out/'apercu-video.jpg')])
reports={}
for name in ['chasse-galerie-1-vol-complet.mp4','extrait-atmosphere.mp4','extrait-atterrissage.mp4','extrait-recuperation.mp4']:
 log=w/(name+'.verification.txt');run(['-i',str(out/name),'-f','null','-','-progress',str(log)]);reports[name]=log.read_text()
(out/'verification-videos.json').write_text(json.dumps(reports,indent=2),encoding='utf8')
print('VIDEOS_ENCODED_AND_DECODED',flush=True)
