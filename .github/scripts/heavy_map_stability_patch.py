from pathlib import Path

p=Path('index.html')
s=p.read_text()

# Dar todavía más margen al iPhone en los dos mapas pesados.
s=s.replace("const seg=isTouch?((mi===1||mi===3)?56:88):126,geo=new THREE.PlaneGeometry(WORLD,WORLD,seg,seg);",
            "const seg=isTouch?((mi===1||mi===3)?40:88):126,geo=new THREE.PlaneGeometry(WORLD,WORLD,seg,seg);",1)

# Forzar al navegador a pintar el nuevo mapa ANTES de empezar a hidratar GLTF pesados.
old="""    rebuildMiniBase(mi);for(let i=0;i<AMB_N;i++)ambReset(i,true);zoneCheck();
    mapLoad(false,mi);
    if(isTouch&&(mi===1||mi===3)){
      toast('Entraste a '+GAME_MAPS[mi].name+' · cargando detalles…','#d9b36a');
      hydrateHeavyMap(mi);
    }else{
"""
new="""    rebuildMiniBase(mi);for(let i=0;i<AMB_N;i++)ambReset(i,true);zoneCheck();
    mapLoad(false,mi);
    await mapYield();await mapYield();
    if(isTouch&&(mi===1||mi===3)){
      toast('Entraste a '+GAME_MAPS[mi].name+' · cargando detalles…','#d9b36a');
      setTimeout(()=>hydrateHeavyMap(mi),350);
    }else{
"""
if old not in s:
    raise SystemExit('No se encontró bloque travelTo pesado')
s=s.replace(old,new,1)

# La hidratación pesada espera un momento extra y cede siempre el hilo entre recursos.
old="""  heavyHydration[mi]=(async()=>{
    const q=MAP_REQ[mi],g=mapGroups[mi];
    for(const name of q.mon){await needMonster(name);await mapYield();}
"""
new="""  heavyHydration[mi]=(async()=>{
    await new Promise(r=>setTimeout(r,250));
    await mapYield();
    const q=MAP_REQ[mi],g=mapGroups[mi];
    for(const name of q.mon){await needMonster(name);await mapYield();}
"""
if old not in s:
    raise SystemExit('No se encontró inicio hydrateHeavyMap')
s=s.replace(old,new,1)

p.write_text(s)
print('Estabilidad extra aplicada a Montaña Helada y Reino de los Muertos')
