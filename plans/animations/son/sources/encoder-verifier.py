import subprocess,json,re,wave,hashlib
from pathlib import Path
out=Path('outputs/son-v9');work=Path('work/son-v9');src=Path('outputs/cinematographie-v8/chasse-galerie-1-vol-complet.mp4');ff='C:/Windows/system32/ffmpeg.exe'
def run(args):return subprocess.run([ff,'-hide_banner','-nostdin',*args],capture_output=True,text=True,check=True)
norm=run(['-y','-i',str(out/'audio/mixage.wav'),'-af','loudnorm=I=-18:TP=-2:LRA=9:print_format=json','-ar','48000',str(out/'audio/bande-son.wav')]);stats=json.loads(norm.stderr[norm.stderr.rindex('{'):])
correction='loudnorm=I=-18:TP=-2:LRA=9:measured_I='+stats['input_i']+':measured_TP='+stats['input_tp']+':measured_LRA='+stats['input_lra']+':measured_thresh='+stats['input_thresh']+':offset='+stats['target_offset']+':linear=false:print_format=json'
norm=run(['-y','-i',str(out/'audio/mixage.wav'),'-af',correction,'-ar','48000',str(out/'audio/bande-son.wav')]);stats=json.loads(norm.stderr[norm.stderr.rindex('{'):])
dest=out/'chasse-galerie-1-vol-sonorise.mp4'
run(['-v','error','-y','-i',str(src),'-i',str(out/'audio/bande-son.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','40.566666667','-movflags','+faststart',str(dest)])
decode=run(['-v','error','-i',str(dest),'-f','null','-','-progress','pipe:1']);frames=int(re.findall(r'frame=(\d+)',decode.stdout)[-1]);assert frames==1217 and not decode.stderr
def video_hash(p):return run(['-v','error','-i',str(p),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip()
original=video_hash(src);new=video_hash(dest);assert original==new
meter=run(['-i',str(dest),'-vn','-af','loudnorm=I=-18:TP=-2:LRA=9:print_format=json','-f','null','-']);encoded=json.loads(meter.stderr[meter.stderr.rindex('{'):]);assert float(encoded['input_tp']) < -1
with wave.open(str(out/'audio/bande-son.wav')) as w:assert w.getnframes()==1947200 and w.getnchannels()==2 and w.getframerate()==48000
report={'frames':frames,'duration_s':1217/30,'sample_rate':48000,'channels':2,'decode_errors':decode.stderr,'video_bitstream_unchanged':original==new,'video_hash':new,'normalization':stats,'aac_measurement':encoded,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(out/'verification-audiovisuelle.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report),flush=True)
