from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Ajuste visual de Montaña Helada + Herrero solo en Mapa 1.
visual = [
    (
        "  if(mi===1){\n    const ice=ss(.38,.78,n2);r=lerp(.72,.92,ice);g=lerp(.78,.95,ice);b=lerp(.82,1,ice);\n    if(n<.28){r*=.72;g*=.78;b*=.82;}\n  }else if(mi===2){",
        "  if(mi===1){\n    const ice=ss(.38,.78,n2);r=lerp(.44,.70,ice);g=lerp(.52,.78,ice);b=lerp(.60,.86,ice);\n    if(n<.30){r*=.68;g*=.73;b*=.79;}\n    if(h>4){const cap=clamp((h-4)/12,0,.08);r+=cap;g+=cap;b+=cap;}\n  }else if(mi===2){",
    ),
    (
        "1:{fog:new THREE.Color(0x9aabb7),hemi:new THREE.Color(0xd9edff),top:new THREE.Color(0x334b68),near:38,far:132,star:.15},",
        "1:{fog:new THREE.Color(0x617487),hemi:new THREE.Color(0xa9bfd2),top:new THREE.Color(0x1d3147),near:42,far:128,star:.06},",
    ),
    (
        "fg.color.lerp(A.fog,k);scene.background.copy(fg.color);fg.near+=(A.near-fg.near)*k;fg.far+=(A.far-fg.far)*k;hemi.color.lerp(A.hemi,k);",
        "fg.color.lerp(A.fog,k);scene.background.copy(fg.color);fg.near+=(A.near-fg.near)*k;fg.far+=(A.far-fg.far)*k;hemi.color.lerp(A.hemi,k);if(currentMap===1){hemi.intensity+=(.58-hemi.intensity)*k;if(bloom){bloom.strength=.22;bloom.threshold=.9;bloom.radius=.32;}}",
    ),
    (
        "const nm=Math.hypot(P.x-MERCH.x,P.z-MERCH.z)<7;els.shop.hidden=!(nm&&!panelOpen&&!P.dead);",
        "const nm=currentMap===0&&Math.hypot(P.x-MERCH.x,P.z-MERCH.z)<7;els.shop.hidden=!(nm&&!panelOpen&&!P.dead);",
    ),
]
for old, new in visual:
    if old in s:
        s = s.replace(old, new, 1)

# Los mapas 1 (nieve) y 3 (muertos) deben poder mostrarse antes de cargar sus GLTF.
old = "function putEnv(mi,g,path,x,z,s,ry,tint,col){const o=cloneEnv(path,tint);o.position.set(x,mapLocalH(mi,x,z),z);o.rotation.y=ry||0;o.scale.setScalar(s||1);g.add(o);if(col)addMapCol(mi,x,z,col*(s||1));return o;}"
new = """let heavyEnvQueue=null;
const heavyHydration={};
function putEnvNow(mi,g,path,x,z,s,ry,tint,col){const o=cloneEnv(path,tint);o.position.set(x,mapLocalH(mi,x,z),z);o.rotation.y=ry||0;o.scale.setScalar(s||1);g.add(o);if(col)addMapCol(mi,x,z,col*(s||1));return o;}
function putEnv(mi,g,path,x,z,s,ry,tint,col){if(heavyEnvQueue&&(mi===1||mi===3)){heavyEnvQueue.push([mi,g,path,x,z,s,ry,tint,col]);return null;}return putEnvNow(mi,g,path,x,z,s,ry,tint,col);}
const mapYield=()=>new Promise(r=>requestAnimationFrame(()=>r()));"""
if old not in s:
    raise SystemExit('No se encontró putEnv original')
s = s.replace(old, new, 1)

# Terreno más liviano solo en móvil para los dos mapas problemáticos.
old = "const seg=isTouch?96:126,geo=new THREE.PlaneGeometry(WORLD,WORLD,seg,seg);"
new = "const seg=isTouch?((mi===1||mi===3)?56:88):126,geo=new THREE.PlaneGeometry(WORLD,WORLD,seg,seg);"
if old in s:
    s = s.replace(old, new, 1)

# Convertir el spawn en trabajos para poder distribuirlo entre frames.
a = s.index('function spawnMapPopulation(mi)')
b = s.index('async function ensureMap(mi)', a)
new_pop = """function makeMapPopulationJobs(mi){
  const R=rngMap(7000+mi),jobs=[];
  const add=(...args)=>jobs.push(args);
  function wave(t,n,test){let c=0,k=0;while(c<n&&k<n*80){k++;const x=(R()*2-1)*(LIMIT-7),z=(R()*2-1)*(LIMIT-7);if(Math.hypot(x,z-6)<22||z<-56||!test(x,z))continue;if(mi===2&&MAP_LAVA[2].some(p=>Math.hypot(x-p.x,z-p.z)<p.r+4))continue;add(t,x,z,undefined,mi);c++;}}
  if(mi===1){wave('frost_orc',12,()=>true);wave('frost_tribal',10,(x,z)=>x<35);wave('yeti',7,(x,z)=>Math.abs(x)>24||z<0);add('yeti_glacial',-28,-72,12,mi);add('yeti_alfa',28,-72,14,mi);}
  else if(mi===2){wave('dino_fire',11,()=>true);wave('armabee_fire',11,()=>true);wave('goleling_fire',8,(x,z)=>Math.abs(x)>20);add('dragon_ancient',-30,-72,16,mi);add('dragon_evolved',30,-72,18,mi);}
  else if(mi===3){wave('ghost_mob',14,()=>true);wave('orc_skull',13,(x,z)=>z<30);add('ghost_skull_lord',-28,-72,20,mi);add('skull_warlord',28,-72,22,mi);}
  else{wave('ruin_orc',12,()=>true);wave('mushroom_corrupt',10,(x,z)=>x<35);wave('golem_guard',9,(x,z)=>Math.abs(x)>18);add('golem_evolved_boss',-30,-72,24,mi);add('blue_demon_boss',30,-72,26,mi);}
  return jobs;
}
function spawnMapPopulation(mi){for(const j of makeMapPopulationJobs(mi))spawnEnemy(...j);}
async function streamMapPopulation(mi){
  const jobs=makeMapPopulationJobs(mi);
  for(let i=0;i<jobs.length;i++){
    spawnEnemy(...jobs[i]);
    const e=enemies[enemies.length-1];
    if(e&&e.map===mi)e.group.visible=(currentMap===mi);
    await mapYield();
  }
}"""
s = s[:a] + new_pop + '\n' + s[b:]

# Crear terreno primero. Para móvil, el resto se hidrata después de entrar al mapa.
old = "async function ensureMap(mi){if(mapBuilt[mi])return;await prepareMapAssets(mi);const g=new THREE.Group();g.position.y=MAP_Y[mi];g.visible=false;scene.add(g);const terr=makeTerrain(mi);g.add(terr);mapGroups[mi]=g;mapTerrains[mi]=terr;buildScenery(mi,g);spawnMapPopulation(mi);mapBuilt[mi]=true;}"
new = """async function ensureMap(mi){
  if(mapBuilt[mi])return;
  const heavy=isTouch&&(mi===1||mi===3);
  if(!heavy)await prepareMapAssets(mi);
  await mapYield();
  const g=new THREE.Group();
  g.position.y=MAP_Y[mi];g.visible=false;scene.add(g);
  const terr=makeTerrain(mi);g.add(terr);mapGroups[mi]=g;mapTerrains[mi]=terr;
  mapBuilt[mi]=true;
  if(heavy)return;
  buildScenery(mi,g);spawnMapPopulation(mi);
}
async function hydrateHeavyMap(mi){
  if(!(isTouch&&(mi===1||mi===3)))return;
  if(heavyHydration[mi])return heavyHydration[mi];
  heavyHydration[mi]=(async()=>{
    const q=MAP_REQ[mi],g=mapGroups[mi];
    for(const name of q.mon){await needMonster(name);await mapYield();}
    for(const path of q.env){await needEnv(path);await mapYield();}
    heavyEnvQueue=[];
    buildScenery(mi,g);
    const jobs=heavyEnvQueue;heavyEnvQueue=null;
    for(let i=0;i<jobs.length;i++){putEnvNow(...jobs[i]);await mapYield();}
    await streamMapPopulation(mi);
    setMapVisibility(currentMap);
    if(currentMap===mi)toast(GAME_MAPS[mi].name+' listo','#8bd7a2');
    return true;
  })().catch(err=>{
    console.error(err);delete heavyHydration[mi];
    if(currentMap===mi)toast('No se pudieron terminar de cargar los detalles del mapa.','#e5655a');
    throw err;
  });
  return heavyHydration[mi];
}"""
if old not in s:
    raise SystemExit('No se encontró ensureMap original')
s = s.replace(old, new, 1)

# CRÍTICO: cambiar al nuevo mapa antes de descargar y construir su decoración pesada.
old = "async function travelTo(mi){if(mi===currentMap||state!=='play'||P.dead)return;mapLoad(true,mi);try{await ensureMap(mi);clearTransientWorld();currentMap=mi;activeTerrain=mapTerrains[mi]||terrain;setMapVisibility(mi);P.x=0;P.z=6;P.y=mapWorldH(mi,0,6);P.face=Math.PI;P.vx=P.vz=0;camX=P.x;camZ=P.z;camY=P.y;curBiome='';rebuildMiniBase(mi);for(let i=0;i<AMB_N;i++)ambReset(i,true);zoneCheck();toast('Llegaste a '+GAME_MAPS[mi].name,'#d9b36a');}catch(err){console.error(err);toast('No se pudo cargar ese mapa. Revisa que la carpeta assets esté junto a index.html.','#e5655a');}finally{mapLoad(false,mi);}}"
new = """async function travelTo(mi){
  if(mi===currentMap||state!=='play'||P.dead)return;
  mapLoad(true,mi);
  try{
    await ensureMap(mi);
    clearTransientWorld();
    currentMap=mi;activeTerrain=mapTerrains[mi]||terrain;setMapVisibility(mi);
    P.x=0;P.z=6;P.y=mapWorldH(mi,0,6);P.face=Math.PI;P.vx=P.vz=0;
    camX=P.x;camZ=P.z;camY=P.y;curBiome='';
    rebuildMiniBase(mi);for(let i=0;i<AMB_N;i++)ambReset(i,true);zoneCheck();
    mapLoad(false,mi);
    if(isTouch&&(mi===1||mi===3)){
      toast('Entraste a '+GAME_MAPS[mi].name+' · cargando detalles…','#d9b36a');
      hydrateHeavyMap(mi);
    }else{
      toast('Llegaste a '+GAME_MAPS[mi].name,'#d9b36a');
    }
  }catch(err){
    console.error(err);
    toast('No se pudo cargar ese mapa. Revisa que la carpeta assets esté junto a index.html.','#e5655a');
  }finally{
    mapLoad(false,mi);
  }
}"""
if old not in s:
    raise SystemExit('No se encontró travelTo original')
s = s.replace(old, new, 1)

p.write_text(s)
print('Parche móvil aplicado correctamente')
