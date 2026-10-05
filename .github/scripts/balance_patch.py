from pathlib import Path

p=Path('index.html')
s=p.read_text()

# +20% de vida, ataque y defensa para todos los monstruos y bosses.
old="maxHp:Math.round(d.hp*(1+.4*(lv-1))),atk:d.atk*(1+.22*(lv-1)),def:2+lv*2,"
new="maxHp:Math.round(d.hp*(1+.4*(lv-1))*1.20),atk:d.atk*(1+.22*(lv-1))*1.20,def:(2+lv*2)*1.20,"
if old not in s:
    raise SystemExit('No se encontro formula base de monstruos')
s=s.replace(old,new,1)

# +20% de EXP manteniendo el ajuste por diferencia de nivel.
old="gainExp(Math.round(baseXp*f));"
new="gainExp(Math.round(baseXp*f*1.20));"
if old not in s:
    raise SystemExit('No se encontro formula de EXP')
s=s.replace(old,new,1)

p.write_text(s)
print('Balance aplicado: +20% vida/defensa/ataque y +20% EXP')
