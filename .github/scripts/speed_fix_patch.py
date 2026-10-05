from pathlib import Path

p=Path('index.html')
s=p.read_text()

# La Agilidad no debe aumentar la velocidad de movimiento.
old="PS={atk:atk,def:(g.def+P.lvl*1.2+st.agi*.4)*(1+g.defP/100),maxHp:Math.round(mhp),maxMp:Math.round(mmp),crit:5+g.crit+st.agi*.1,ls:g.ls,refl:g.refl,spd:g.spd+st.agi*.05,setN:setN,dbl:g.dbl,dr:Math.min(50,g.dr),cdm:g.cdm,setFull:full?full.n:null};"
new="PS={atk:atk,def:(g.def+P.lvl*1.2+st.agi*.4)*(1+g.defP/100),maxHp:Math.round(mhp),maxMp:Math.round(mmp),crit:5+g.crit+st.agi*.1,ls:g.ls,refl:g.refl,spd:Math.min(20,g.spd),setN:setN,dbl:g.dbl,dr:Math.min(50,g.dr),cdm:g.cdm,setFull:full?full.n:null};"
if old not in s:
    raise SystemExit('No se encontro formula de velocidad del personaje')
s=s.replace(old,new,1)

# Aclarar el texto de puntos de estadistica.
s=s.replace('Agilidad sube defensa, crítico y velocidad, Vitalidad la vida y Energía el maná.','Agilidad sube defensa y crítico; los puntos de Agilidad ya no aumentan la velocidad de movimiento. Vitalidad sube la vida y Energía el maná.',1)

# Evitar que los nuevos objetos de nivel alto generen bonos absurdos de movimiento.
old_aff="{k:'spd',v:()=>r1(3+ilvl*.4)}"
new_aff="{k:'spd',v:()=>r1(3+Math.min(ilvl,35)*.2)}"
if old_aff in s:
    s=s.replace(old_aff,new_aff,1)

p.write_text(s)
print('Velocidad corregida: Agilidad sin movimiento y bonus de equipo limitado a +20%')
