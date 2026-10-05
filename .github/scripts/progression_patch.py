from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Progresión de niveles: cada mapa secundario sube 20 niveles.
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

# La EXP ya escala con e.lvl en el juego. Los objetos normales ya usan e.lvl;
# hacemos que los bosses también tiren objetos exactamente de su nivel.
old = "genItem(e.lvl+1,i===0?3:2)"
if old not in s:
    raise SystemExit('No se encontró el nivel de objeto de boss')
s = s.replace(old, "genItem(e.lvl,i===0?3:2)", 1)

# Evitar que a niveles altos la probabilidad de joya llegue a 100% y bloquee
# por completo el drop de equipamiento normal.
s = s.replace("Math.random()<.2+e.lvl*.015", "Math.random()<Math.min(.55,.2+e.lvl*.015)", 1)
s = s.replace("Math.random()<.22+e.lvl*.012", "Math.random()<Math.min(.65,.22+e.lvl*.012)", 1)

p.write_text(s)
print('Progresión por mapas aplicada: 20/40/60/80; bosses hasta 100')
