from pathlib import Path

p=Path('index.html')
s=p.read_text()

# +20% de vida, ataque y defensa para todos los monstruos y bosses.
old="maxHp:Math.round(d.hp*(1+.4*(lv-1))),atk:d.atk*(1+.22*(lv-1)),def:2+lv*2,"
new="maxHp:Math.round(d.hp*(1+.4*(lv-1))*1.20),atk:d.atk*(1+.22*(lv-1))*1.20,def:(2+lv*2)*1.20,"
if old not in s:
    raise SystemExit('No se encontro formula base de monstruos')
s=s.replace(old,new,1)

# EXP: conservar +20% base, pero premiar de verdad matar enemigos muy por encima del nivel.
# Ejemplo calibrado: un PJ lvl 37 matando un mob lvl 80 recibe ~36k EXP,
# equivalente aproximadamente a 3 niveles con la curva actual de expNeed().
old="const diff=e.lvl-P.lvl,f=clamp(1+diff*.08,.35,1.75),baseXp=e.boss?Math.round(800+e.lvl*140):Math.round(40+e.lvl*18);gainExp(Math.round(baseXp*f));"
new="const diff=e.lvl-P.lvl,gap=Math.max(0,diff),low=diff<0?clamp(1+diff*.08,.35,1):1,baseXp=e.boss?Math.round(800+e.lvl*140):Math.round(40+e.lvl*18);let xp=baseXp*low*1.20;if(gap>0)xp+=expNeed(P.lvl)*(gap/14.4);gainExp(Math.round(xp));"
if old not in s:
    raise SystemExit('No se encontro formula completa de EXP')
s=s.replace(old,new,1)

p.write_text(s)
print('Balance aplicado: +20% combate y EXP con bonus fuerte por diferencia de nivel')
