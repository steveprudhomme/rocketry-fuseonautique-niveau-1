"""Original deterministic progressive instrumental and flight sound design (NumPy only)."""
import argparse,json,wave,math
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--source',default='outputs/cinematographie-v8');p.add_argument('--output',default='outputs/son-v9');a=p.parse_args()
src=Path(a.source);out=Path(a.output);(out/'audio').mkdir(parents=True,exist_ok=True);(out/'donnees').mkdir(exist_ok=True)
sr=48000;tele=json.loads((src/'donnees/telemetrie.json').read_text());n=round(len(tele)/30*sr);t=np.arange(n)/sr;rng=np.random.default_rng(14309)
music=np.zeros((n,2));fx=np.zeros((n,2));events=[]
def noise(length,lo,hi):
 x=rng.normal(size=length);f=np.fft.rfftfreq(length,1/sr);z=np.fft.rfft(x);mask=(1-np.exp(-(f/max(lo,1))**4))*np.exp(-(f/hi)**4);x=np.fft.irfft(z*mask,n=length);return x/(np.std(x)+1e-9)
def put(track,sound,start,gain=1,pan=0):
 i=round(start*sr);j=min(n,i+len(sound));
 if i>=n or j<=0:return
 sound=sound[max(0,-i):j-i];i=max(0,i);angle=(pan+1)*np.pi/4;track[i:j,0]+=gain*sound*np.cos(angle);track[i:j,1]+=gain*sound*np.sin(angle)
def note(freq,duration,kind='guitar'):
 u=np.arange(round(duration*sr))/sr
 if kind=='guitar':
  x=sum(np.sin(2*np.pi*freq*k*u+.13*k)/(k**1.1) for k in range(1,19));x=np.tanh(2*x)*np.exp(-u*6/max(duration,.2));x*=np.minimum(u/.004,1);x*=np.minimum((duration-u)/.025,1);return x*.4
 if kind=='bass':return (np.sin(2*np.pi*freq*u)+.2*np.sin(4*np.pi*freq*u))*np.minimum(u/.005,1)*np.exp(-u*4/max(duration,.1))
 return (np.sin(2*np.pi*freq*u)+.25*np.sin(4*np.pi*freq*u))*np.minimum(u/.012,1)*np.exp(-u*5/duration)
def drum(kind):
 dur={'kick':.35,'snare':.23,'hat':.09,'crash':1.4}[kind];u=np.arange(round(dur*sr))/sr
 if kind=='kick':return np.sin(2*np.pi*(48*u+65*.025*(1-np.exp(-u/.025))))*np.exp(-u*16)+.04*noise(len(u),2000,7000)*np.exp(-u*180)
 if kind=='snare':return .5*noise(len(u),700,9000)*np.exp(-u*23)+.25*np.sin(2*np.pi*185*u)*np.exp(-u*35)
 return noise(len(u),5000,15000)*np.exp(-u*(65 if kind=='hat' else 4))*.15
drums={k:drum(k) for k in ('kick','snare','hat','crash')}
# Short tension build during the existing two seconds of waiting.
put(music,note(73.416,2,'bass'),0,.12)
for st in (0,.5,1,1.5):put(fx,note(880,.065,'bell'),st,.045)
# 120 BPM; 7/8 bars grouped 2+2+3. Double-tracked synthetic power chords.
roots=[73.416,73.416,87.307,65.406,73.416,98,87.307,65.406]
for bar,start in enumerate(np.arange(2,30,1.75)):
 root=roots[bar%len(roots)];energy=1 if start<12.2 else .45
 for step in range(7):
  st=start+step*.25;accent=step in (0,2,4);gain=(.14 if accent else .065)*energy
  for pan,detune in ((-.7,.997),(.7,1.003)):
   chord=note(root*detune,.22)+.7*note(root*1.5*detune,.22)+.3*note(root*2*detune,.22)
   put(music,chord,st+(0 if pan<0 else .008),gain,pan)
  put(music,note(root/2,.24,'bass'),st,.14*energy)
  put(music,drums['kick'],st,.22*energy if accent else .04)
  if step in (2,6):put(music,drums['snare'],st,.17*energy,.12)
 # Three cymbal beats per second against two quarter-note beats: 3:2 overlay.
for st in np.arange(2,30,1/3):put(music,drums['hat'],st,.12,-.25)
for st in (2,5.5,9,12.5):put(music,drums['crash'],st,.16,.35)
for i,st in enumerate(np.arange(12.5,36,.25)):
 freq=[293.665,349.228,440,587.33,523.251,440,349.228][i%7];put(music,note(freq,.7,'bell'),st,.04,math.sin(i*.7)*.6)
put(music,note(73.416,4,'bass'),36,.15)
for freq in (293.665,349.228,440):put(music,note(freq,4,'bell'),36,.055)
ft=np.arange(len(tele))/30;physical=np.interp(t,ft,[r['time'] for r in tele]);speed=np.interp(t,ft,[r['speed'] for r in tele]);phys=np.genfromtxt(src/'donnees/vol-h143.csv',delimiter=',',names=True);thrust=np.interp(physical,phys['time_s'],phys['thrust_N']);engine=(t>=2)&(physical<1.73)
env=np.sqrt(np.maximum(thrust,0)/(thrust.max()+1e-9))*engine;env*=np.minimum(np.maximum((t-2)/.025,0),1)
roar=noise(n,25,2200)*.19+np.sin(2*np.pi*56*t)*.07;fx[:,0]+=roar*env;fx[:,1]+=(.94*roar+.025*noise(n,100,3000))*env
coast=(t>3.73)&(physical<10.1954595315);air=np.clip(speed/max(speed),0,1)**1.5*coast;air=np.convolve(air,np.ones(2400)/2400,mode='same')
for ch in (0,1):fx[:,ch]+=.032*noise(n,500,6500)*air
deployment=next((r['frame']-1)/30 for r in tele if r['time']>=10.1954595315)
contact=next((r['frame']-1)/30 for r in tele if r.get('post_contact_s')==0)
u=np.arange(round(.22*sr))/sr;put(fx,(noise(len(u),60,5000)*.30+np.sin(2*np.pi*130*u)*.12)*np.exp(-u*35),deployment,.9)
u=np.arange(round(1.5*sr))/sr;put(fx,noise(len(u),500,6000)*np.sin(np.pi*u/1.5)**2,deployment,.015,.2)
put(fx,drums['kick'],contact,.12);put(fx,noise(sr,200,4000)*np.exp(-np.arange(sr)/sr*5),contact,.018,-.25)
ambient=.0025*noise(n,100,1600)
fx[:,0]+=ambient;fx[:,1]+=np.roll(ambient,233)
fade=np.minimum(t/.025,1)*np.minimum(np.maximum((n/sr-t)/1.2,0),1);music*=fade[:,None];fx*=fade[:,None]
# Duck the score during thrust and ejection; retain stems at their mixed gain.
duck=1-.50*env-.45*np.exp(-np.maximum(t-deployment,0)*5)*(t>=deployment);music*=np.clip(duck,.3,1)[:,None]
mix=music+fx;gain=min(1,.80/(np.max(np.abs(mix))+1e-12));music*=gain;fx*=gain;mix*=gain
def save(name,x):
 assert np.isfinite(x).all() and np.max(np.abs(x))<1
 with wave.open(str(out/'audio'/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.round(x*32767).astype('<i2').tobytes())
save('musique-originale.wav',music);save('bruitages.wav',fx);save('mixage.wav',mix)
events=[{'event':'allumage','video_s':2,'physical_s':0},{'event':'extinction','video_s':3.73,'physical_s':1.73},{'event':'ejection','video_s':deployment,'physical_s':10.1954595315},{'event':'contact','video_s':contact,'physical_s':106.68214059725395}]
report={'sample_rate':sr,'channels':2,'samples':n,'duration_s':n/sr,'seed':14309,'events':events,'composition':{'title':'Sept sillages','tempo_bpm':120,'meter':'7/8, accents 2+2+3','polyrhythm':'3:2 cymbal overlay against quarter-note pulse','instruments':'synthetic distorted power chords, bass, drums, bell arpeggio','original':True},'audio_sources':'Procedural synthesis only; no recordings or third-party music. Illustrative sound design, not measured motor acoustics.','peak_dbfs':float(20*np.log10(np.max(np.abs(mix))))}
(out/'donnees/son.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False),flush=True)
