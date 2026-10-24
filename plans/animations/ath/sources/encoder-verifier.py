"""Encode the HUD frames, preserving the exact AAC stream of v9."""
import subprocess,re,json,hashlib
from pathlib import Path
ff='C:/Windows/system32/ffmpeg.exe';out=Path('outputs/ath-v10');work=Path('work/ath-v10');source=Path('outputs/son-v9/chasse-galerie-1-vol-sonorise.mp4');dest=out/'chasse-galerie-1-ath.mp4'
assert len(list((work/'frames').glob('ath-*.jpg')))==1217
def run(args):return subprocess.run([ff,'-hide_banner','-nostdin',*args],capture_output=True,text=True,check=True)
run(['-v','error','-y','-framerate','30','-i',str(work/'frames/ath-%04d.jpg'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-frames:v','1217','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dest)])
decoded=run(['-v','error','-i',str(dest),'-f','null','-','-progress','pipe:1']);frames=int(re.findall(r'frame=(\d+)',decoded.stdout)[-1]);assert frames==1217 and not decoded.stderr
def ahash(p):return run(['-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip()
assert ahash(source)==ahash(dest)
report={'frames':frames,'fps':30,'duration_s':frames/30,'decode_errors':decoded.stderr,'audio_bitstream_unchanged':True,'audio_hash':ahash(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'resolution':[1920,1080]}
(out/'verification-video.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report),flush=True)
run(['-v','error','-y','-ss','6.633333','-i',str(dest),'-frames:v','1','-update','1',str(out/'apercu-video.jpg')])
