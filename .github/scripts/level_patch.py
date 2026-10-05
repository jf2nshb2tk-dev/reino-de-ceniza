from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Progresión fija por mapa:
# 1 Nieve: mobs 20, bosses 30/40
# 2 Dragones: mobs 40, bosses 50/60
# 3 Muertos: mobs 60, bosses 70/80
# 4 Ruinas: mobs 80, bosses 90/100
start=s.find('function makeMapPopulationJobs(mi){')
end=s.find('\nfunction spawnMapPopulation(mi)', start)
if start<0 or end<0:
    raise SystemExit('No se encontró makeMapPopulationJobs')

new_pop="""function makeMapPopulationJobs(mi){
  const R=rngMap(7000+mi),jobs=[];
  const add=(...args)=>jobs.push(args);
  function wave(t,n,test,lvl){let c=0,k=0;while(c<n&&k<n*80){k++;const x=(R()*2-1)*(LIMIT-7),z=(R()*2-1)*(LIMIT-7);if(Math.hypot(x,z-6)<22||z<-56||!test(x,z))continue;if(mi===2&&MAP_LAVA[2].some(p=>Math.hypot(x-p.x,z-p.z)<p.r+4))continue;add(t,x,z,lvl,mi);c++;}}
  if(mi===1){wave('frost_orc',12,()=>true,20);wave('frost_tribal',10,(x,z)=>x<35,20);wave('yeti',7,(x,z)=>Math.abs(x)>24||z<0,20);add('yeti_glacial',-28,-72,30,mi);add('yeti_alfa',28,-72,40,mi);}
  else if(mi===2){wave('dino_fire',11,()=>true,40);wave('armabee_fire',11,()=>true,40);wave('goleling_fire',8,(x,z)=>Math.abs(x)>20,40);add('dragon_ancient',-30,-72,50,mi);add('dragon_evolved',30,-72,60,mi);}
  else if(mi===3){wave('ghost_mob',14,()=>true,60);wave('orc_skull',13,(x,z)=>z<30,60);add('ghost_skull_lord',-28,-72,70,mi);add('skull_warlord',28,-72,80,mi);}
  else{wave('ruin_orc',12,()=>true,80);wave('mushroom_corrupt',10,(x,z)=>x<35,80);wave('golem_guard',9,(x,z)=>Math.abs(x)>18,80);add('golem_evolved_boss',-30,-72,90,mi);add('blue_demon_boss',30,-72,100,mi);}
  return jobs;
}"""
s=s[:start]+new_pop+s[end:]

# EXP basada directamente en el nivel real del enemigo, con ajuste por diferencia de nivel.
old="const diff=e.lvl-P.lvl,f=clamp(1+diff*.15,.25,1.6);gainExp(Math.round(e.d.xp*(1+.3*(e.lvl-1))*f));"
new="const diff=e.lvl-P.lvl,f=clamp(1+diff*.08,.35,1.75),baseXp=e.boss?Math.round(800+e.lvl*140):Math.round(40+e.lvl*18);gainExp(Math.round(baseXp*f));"
if old not in s:
    raise SystemExit('No se encontró fórmula de EXP')
s=s.replace(old,new,1)

# El nivel de objeto coincide con el nivel del enemigo que lo tira.
# Los mobs normales ya usan genItem(e.lvl); hacemos lo mismo con los bosses.
s=s.replace("genItem(e.lvl+1,i===0?3:2)","genItem(e.lvl,i===0?3:2)",1)

p.write_text(s)
print('Progresión de niveles aplicada correctamente')
