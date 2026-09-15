"""Generate a French ASS telemetry overlay from rendered-frame flight samples."""
import json, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent/'vol-complet'
rows=json.loads((root/'telemetrie.json').read_text())
def ts(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Arial,44,&H00FFFFFF,&H00FFFFFF,&H00201810,&H80201810,-1,0,0,0,100,100,1,0,1,2,1,7,65,65,45,1
Style: Data,Arial,30,&H00FFFFFF,&H00FFFFFF,&H00201810,&H80201810,0,0,0,0,100,100,0,0,3,9,0,7,65,65,110,1
Style: Footer,Arial,23,&H00FFFFFF,&H00FFFFFF,&H00201810,&H80201810,0,0,0,0,100,100,0,0,3,7,0,1,65,65,45,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
duration=len(rows)/30
lines=[header,f'Dialogue: 0,0:00:00.00,{ts(duration)},Title,,0,0,0,,CHASSE GALERIE 1  |  VOL COMPLET\n',f'Dialogue: 0,0:00:00.00,{ts(duration)},Footer,,0,0,0,,OpenRocket · H143 · apogée idéale · modèle provisoire\\NPaysage, fumée et déploiement illustratifs — vent nul\n']
for i in range(0,len(rows),3):
 r=dict(rows[i]);r['rate']='ARRÊT SUR IMAGE' if r['phase']=='RETOUR AU SOL' else r['rate'];r['phase']=r['phase'].replace('RETOUR AU SOL','CONTACT AU SOL — FIN DU CALCUL').replace('MONTEE','MONTÉE');r['rate']=r['rate'].replace('REEL','RÉEL').replace('ACCELEREE x6','ACCÉLÉRÉE ×6');text=f"{r['phase']}   ·   {r['rate']}\\Nt + {r['time']:05.1f} s    |    {r['altitude']:05.1f} m    |    {r['speed']:05.1f} m/s"
 lines.append(f'Dialogue: 0,{ts(i/30)},{ts(min(i+3,len(rows))/30)},Data,,0,0,0,,{text}\n')
(root/'titres.ass').write_text(''.join(lines),encoding='utf-8-sig')
