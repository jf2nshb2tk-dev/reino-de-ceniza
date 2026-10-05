from pathlib import Path
p=Path('index.html')
s=p.read_text()

# Nivel máximo 100.
old="function gainExp(n){\n  P.exp+=n;"
new="function gainExp(n){\n  if(P.lvl>=100){P.lvl=100;P.exp=0;return;}\n  P.exp+=n;"
if old not in s: raise SystemExit('gainExp start no encontrado')
s=s.replace(old,new,1)
s=s.replace("while(P.exp>=expNeed(P.lvl)){","while(P.lvl<100&&P.exp>=expNeed(P.lvl)){",1)
old="toast('¡Subiste al nivel '+P.lvl+'! +5 puntos de estadística (Personaje)','#f0d08a');saveGame();}"
new="toast('¡Subiste al nivel '+P.lvl+'! +5 puntos de estadística (Personaje)','#f0d08a');if(P.lvl===100){P.exp=0;toast('¡Nivel 100! Reset disponible en Personaje.','#ffe08a');}saveGame();}"
if old not in s: raise SystemExit('level toast no encontrado')
s=s.replace(old,new,1)

# Boss nivel 100: 20% de un item nivel 100, rareza máxima, +15.
old="if(e.boss){for(let i=0;i<3;i++){s=sp();mkDrop('item',s.x,s.z,{item:genItem(e.lvl,i===0?3:2)});}for(let i=0;i<12;i++){s=sp();mkDrop('jewel',s.x,s.z,{});}}"
new="if(e.boss){for(let i=0;i<3;i++){s=sp();mkDrop('item',s.x,s.z,{item:genItem(e.lvl,i===0?3:2)});}if(e.lvl>=100&&Math.random()<.20){const top=genItem(100,3);top.lv=15;s=sp();mkDrop('item',s.x,s.z,{item:top});}for(let i=0;i<12;i++){s=sp();mkDrop('jewel',s.x,s.z,{});}}"
if old not in s: raise SystemExit('boss drop no encontrado')
s=s.replace(old,new,1)

# Contador de resets en jugador/guardado.
s=s.replace("lvl:1,exp:0,gold:30,mpCd:0,pts:0","lvl:1,exp:0,gold:30,resets:0,mpCd:0,pts:0",1)
old="p.id=c.id;p.name=c.name;p.lvl=c.lvl||1;p.exp=c.exp||0;p.gold=c.gold||0;p.st=c.st||{str:0,agi:0,vit:0,ene:0};"
new="p.id=c.id;p.name=c.name;p.lvl=Math.min(100,c.lvl||1);p.exp=p.lvl>=100?0:(c.exp||0);p.gold=c.gold||0;p.resets=c.resets||0;p.st=c.st||{str:0,agi:0,vit:0,ene:0};"
if old not in s: raise SystemExit('fromChar no encontrado')
s=s.replace(old,new,1)
old="c.lvl=P.lvl;c.exp=P.exp;c.gold=P.gold;c.pm=1;"
new="c.lvl=P.lvl;c.exp=P.exp;c.gold=P.gold;c.resets=P.resets||0;c.pm=1;"
if old not in s: raise SystemExit('save no encontrado')
s=s.replace(old,new,1)
s=s.replace("const c={id:uid(),cls:selCls,name:nm,lvl:1,exp:0,gold:30,potions:5","const c={id:uid(),cls:selCls,name:nm,lvl:1,exp:0,gold:30,resets:0,potions:5",1)

# Reset estilo MU: nivel 1, stats a 0, 400 puntos acumulativos por reset.
marker="function ptsHTML(){const n=P.pts||0,S=[['str','Fuerza'],['agi','Agilidad'],['vit','Vitalidad'],['ene','Energía']];"
if marker not in s: raise SystemExit('ptsHTML marker no encontrado')
fn="""function doMuReset(){
  if(P.lvl<100){toast('El Reset se habilita en nivel 100.','#d9b36a');return;}
  P.resets=(P.resets||0)+1;P.lvl=1;P.exp=0;P.st={str:0,agi:0,vit:0,ene:0};P.pts=P.resets*400;
  clearTransientWorld();currentMap=0;activeTerrain=mapTerrains[0]||terrain;setMapVisibility(0);
  P.x=0;P.z=6;P.y=mapWorldH(0,0,6);P.face=Math.PI;P.vx=P.vz=0;P.dest=null;P.target=null;P.engaged=false;
  camX=P.x;camZ=P.z;camY=P.y;curBiome='';rebuildMiniBase(0);for(let i=0;i<AMB_N;i++)ambReset(i,true);zoneCheck();
  recalc();P.hp=PS.maxHp;P.mp=PS.maxMp;gearVisuals();saveGame();
  burst(P.x,P.y+1,P.z,55,[1,.82,.35],7,1.2,.35,-1);sfx('lvl');toast('¡Reset '+P.resets+' completado! '+P.pts+' puntos disponibles.','#ffe08a');
  if(panelOpen)renderPanel();
}
"""
s=s.replace(marker,fn+marker,1)

old="function ptsHTML(){const n=P.pts||0,S=[['str','Fuerza'],['agi','Agilidad'],['vit','Vitalidad'],['ene','Energía']];\n  return '<h3>Puntos: '+n+'</h3><div class=\"stat\">'+S.map(a=>'<span>'+a[1]+', '+P.st[a[0]]+'</span><span><button class=\"btn alt pt\" data-a=\"stp\" data-v=\"'+a[0]+'\"'+(n?'':' disabled')+'>+</button></span>').join('')+'</div><p class=\"note\">Ganas 5 puntos por nivel. Fuerza y Energía suben el ataque (más el atributo principal de tu clase), Agilidad sube defensa, crítico y velocidad, Vitalidad la vida y Energía el maná.</p>'; }"
if old not in s:
    old="function ptsHTML(){const n=P.pts||0,S=[['str','Fuerza'],['agi','Agilidad'],['vit','Vitalidad'],['ene','Energía']];\n  return '<h3>Puntos: '+n+'</h3><div class=\"stat\">'+S.map(a=>'<span>'+a[1]+', '+P.st[a[0]]+'</span><span><button class=\"btn alt pt\" data-a=\"stp\" data-v=\"'+a[0]+'\"'+(n?'':' disabled')+'>+</button></span>').join('')+'</div><p class=\"note\">Ganas 5 puntos por nivel. Fuerza y Energía suben el ataque (más el atributo principal de tu clase), Agilidad sube defensa, crítico y velocidad, Vitalidad la vida y Energía el maná.</p>'; }"
new="function ptsHTML(){const n=P.pts||0,S=[['str','Fuerza'],['agi','Agilidad'],['vit','Vitalidad'],['ene','Energía']],rs=P.resets||0,can=P.lvl>=100,next=(rs+1)*400;\n  return '<h3>Puntos: '+n+'</h3><div class=\"stat\">'+S.map(a=>'<span>'+a[1]+', '+P.st[a[0]]+'</span><span><button class=\"btn alt pt\" data-a=\"stp\" data-v=\"'+a[0]+'\"'+(n?'':' disabled')+'>+</button></span>').join('')+'</div><p class=\"note\">Ganas 5 puntos por nivel. Fuerza y Energía suben el ataque (más el atributo principal de tu clase), Agilidad sube defensa, crítico y velocidad, Vitalidad la vida y Energía el maná.</p><h3 style=\"margin-top:14px\">Reset MU</h3><div class=\"stat\"><span>Resets</span><span>'+rs+'</span><span>Bonus acumulado</span><span>'+rs*400+' puntos</span><span>Próximo Reset</span><span>'+next+' puntos</span></div>'+(can?'<div class=\"btns\"><button class=\"btn\" data-a=\"reset\">Hacer Reset</button></div><p class=\"note\">Vuelves a nivel 1, se reinician los atributos y conservas equipo, mochila, oro y joyas.</p>':'<p class=\"note\">Se habilita al nivel 100.</p>');}"
# El bloque exacto termina en ;} en la versión actual.
if old not in s:
    old="function ptsHTML(){const n=P.pts||0,S=[['str','Fuerza'],['agi','Agilidad'],['vit','Vitalidad'],['ene','Energía']];\n  return '<h3>Puntos: '+n+'</h3><div class=\"stat\">'+S.map(a=>'<span>'+a[1]+', '+P.st[a[0]]+'</span><span><button class=\"btn alt pt\" data-a=\"stp\" data-v=\"'+a[0]+'\"'+(n?'':' disabled')+'>+</button></span>').join('')+'</div><p class=\"note\">Ganas 5 puntos por nivel. Fuerza y Energía suben el ataque (más el atributo principal de tu clase), Agilidad sube defensa, crítico y velocidad, Vitalidad la vida y Energía el maná.</p>'; }"
# Reemplazo por límites de función para evitar depender de espacios.
a=s.find('function ptsHTML(){'); b=s.find('\nfunction shopDetailHTML',a)
if a<0 or b<0: raise SystemExit('ptsHTML no encontrado')
s=s[:a]+new+s[b:]

old="[['Experiencia',P.exp+' / '+expNeed(P.lvl)],['Vida máxima',PS.maxHp]"
new2="[['Experiencia',P.lvl>=100?'MAX (Reset disponible)':P.exp+' / '+expNeed(P.lvl)],['Resets',P.resets||0],['Vida máxima',PS.maxHp]"
if old not in s: raise SystemExit('stats no encontrado')
s=s.replace(old,new2,1)
old="if(a==='stp'){if((P.pts||0)>0&&P.st[v]!==undefined){P.pts--;P.st[v]++;recalc();saveGame();renderPanel();}return;}"
new3="if(a==='reset'){doMuReset();return;}\n  if(a==='stp'){if((P.pts||0)>0&&P.st[v]!==undefined){P.pts--;P.st[v]++;recalc();saveGame();renderPanel();}return;}"
if old not in s: raise SystemExit('stp handler no encontrado')
s=s.replace(old,new3,1)

p.write_text(s)
print('Reset MU y drop +15 aplicados')