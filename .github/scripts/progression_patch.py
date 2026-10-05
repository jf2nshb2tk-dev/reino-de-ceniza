from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Progresión de niveles: cada mapa secundario sube 20 niveles.
# Nieve 20, Dragones 40, Muertos 60, Ruinas 80.
repls = [
    ("const R=rngMap(7000+mi),jobs=[];", "const R=rngMap(7000+mi),jobs=[],baseLv=mi*20;"),
    ("add(t,x,z,undefined,mi);c++;", "add(t,x,z,baseLv,mi);c++;"),
    ("add('yeti_glacial',-28,-72,12,mi);add('yeti_alfa',28,-72,14,mi);", "add('yeti_glacial',-28,-72,30,mi);add('yeti_alfa',28,-72,40,mi);"),
    ("add('dragon_ancient',-30,-72,16,mi);add('dragon_evolved',30,-72,18,mi);", "add('dragon_ancient',-30,-72,50,mi);add('dragon_evolved',30,-72,60,mi);"),
    ("add('ghost_skull_lord',-28,-72,20,mi);add('skull_warlord',28,-72,22,mi);", "add('ghost_skull_lord',-28,-72,70,mi);add('skull_warlord',28,-72,80,mi);"),
    ("add('golem_evolved_boss',-30,-72,24,mi);add('blue_demon_boss',30,-72,26,mi);", "add('golem_evolved_boss',-30,-72,90,mi);add('blue_demon_boss',30,-72,100,mi);"),
]
for old, new in repls:
    if old not in s:
        raise SystemExit('No se encontró patrón de progresión: ' + old[:70])
    s = s.replace(old, new, 1)

# EXP acorde al nivel real del enemigo, sin que los bosses altos salten demasiados niveles.
old = "const diff=e.lvl-P.lvl,f=clamp(1+diff*.15,.25,1.6);gainExp(Math.round(e.d.xp*(1+.3*(e.lvl-1))*f));"
new = "const diff=e.lvl-P.lvl,f=clamp(1+diff*.08,.35,1.75),baseXp=e.boss?Math.round(800+e.lvl*140):Math.round(40+e.lvl*18);gainExp(Math.round(baseXp*f));"
if old not in s:
    raise SystemExit('No se encontró fórmula de EXP')
s = s.replace(old, new, 1)

# Los objetos caen con el mismo nivel del enemigo. Los mobs normales ya usan e.lvl;
# hacemos lo mismo con los bosses.
old = "genItem(e.lvl+1,i===0?3:2)"
if old not in s:
    raise SystemExit('No se encontró el nivel de objeto de boss')
s = s.replace(old, "genItem(e.lvl,i===0?3:2)", 1)

# A niveles altos, mantener una probabilidad razonable de joyas y equipamiento.
s = s.replace("Math.random()<.2+e.lvl*.015", "Math.random()<Math.min(.55,.2+e.lvl*.015)", 1)
s = s.replace("Math.random()<.22+e.lvl*.012", "Math.random()<Math.min(.65,.22+e.lvl*.012)", 1)

p.write_text(s)
print('Progresión aplicada: mobs 20/40/60/80, bosses 30-100, EXP e items escalados')
