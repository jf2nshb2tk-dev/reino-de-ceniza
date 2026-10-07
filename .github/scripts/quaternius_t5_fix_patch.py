from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='QUATERNIUS_T5_FIX_V2'
if marker in s:
    print('Correccion Quaternius V2 ya aplicada')
    raise SystemExit(0)

# 1) Usar poses/ataques nativos del mismo esqueleto Quaternius.
old="""  const mixer=new THREE.AnimationMixer(model),act={};
  const cmap={Idle_A:'Idle',Walking_A:'Walk',Running_A:'Run',Death_A:'Death',Hit_A:'RecieveHit',Jump_Idle:'Roll'};
  Object.keys(cmap).forEach(k=>{
    const c=(src.animations||[]).find(x=>x.name===cmap[k]);
    if(c)act[k]=mixer.clipAction(c);
  });"""
new="""  const mixer=new THREE.AnimationMixer(model),act={};
  const cmap={Idle_A:'Idle_Weapon',Walking_A:'Walk',Running_A:'Run_Weapon',Death_A:'Death',Hit_A:'RecieveHit',Jump_Idle:'Roll'};
  if(cls==='guerrero'){cmap.QK_Attack0='Sword_Attack';cmap.QK_Attack1='Sword_Attack2';cmap.QK_Attack2='Sword_Attack2';}
  else if(cls==='mago'){cmap.QK_Attack0='Staff_Attack';cmap.QK_Attack1='Spell1';cmap.QK_Attack2='Spell2';}
  else if(cls==='elfa'){cmap.Running_A='Run_Holding';cmap.QK_Attack0='Bow_Shoot';cmap.QK_Attack1='Bow_Shoot';cmap.QK_Attack2='Bow_Shoot';}
  Object.keys(cmap).forEach(k=>{
    let c=(src.animations||[]).find(x=>x.name===cmap[k]);
    // Algunos clips no tienen variante con arma; mantenemos un fallback seguro.
    if(!c&&k==='Idle_A')c=(src.animations||[]).find(x=>x.name==='Idle');
    if(!c&&k==='Running_A')c=(src.animations||[]).find(x=>x.name==='Run');
    if(c)act[k]=mixer.clipAction(c);
  });"""
if old not in s:
    raise SystemExit('No se encontro mapa de animaciones Quaternius')
s=s.replace(old,new,1)

# 2) Mantener las texturas originales legibles/brillantes. Los modelos son KHR_unlit;
#    evitamos que el postprocesado oscurezca la ropa hasta casi negro en iPhone.
old="""    const mt=m.material.clone();
    mt.skinning=!!m.isSkinnedMesh;
    if('metalness' in mt)mt.metalness=Math.min(.18,mt.metalness||0);
    if('roughness' in mt)mt.roughness=.78;
    if(mt.emissive)mt.userData.em0=mt.emissive.clone();
    m.material=mt;m.castShadow=true;meshes.push(m);mats.push(mt);"""
new="""    const mt=m.material.clone();
    mt.skinning=!!m.isSkinnedMesh;
    if(mt.map){mt.map.encoding=THREE.sRGBEncoding;mt.map.needsUpdate=true;}
    // Face casi neutra; ropa/armadura algo mas clara para no perder detalle en pantalla chica.
    const qb=/Face/i.test(m.name||'')?1.05:(sp.weapon.test(m.name||'')?1.14:1.28);
    if(mt.color)mt.color.setRGB(qb,qb,qb);
    mt.toneMapped=false;
    if('metalness' in mt)mt.metalness=0;
    if('roughness' in mt)mt.roughness=.82;
    if(mt.emissive)mt.userData.em0=mt.emissive.clone();
    m.material=mt;m.castShadow=true;meshes.push(m);mats.push(mt);"""
if old not in s:
    raise SystemExit('No se encontro bloque de materiales Quaternius')
s=s.replace(old,new,1)

old="""  playerMeshes.forEach(me=>{
    const ms=Array.isArray(me.material)?me.material:[me.material];
    ms.forEach(mt=>{
      if(mt.color)mt.color.setHex(0xffffff);
      if(mt.emissive)mt.emissive.setHex(accent).multiplyScalar(glow);
      mt.needsUpdate=true;
    });
  });"""
new="""  playerMeshes.forEach(me=>{
    const ms=Array.isArray(me.material)?me.material:[me.material];
    const qb=/Face/i.test(me.name||'')?1.05:(QK_SPEC[P.cls]&&QK_SPEC[P.cls].weapon.test(me.name||'')?1.14:1.28);
    ms.forEach(mt=>{
      if(mt.color)mt.color.setRGB(qb,qb,qb);
      if(mt.map){mt.map.encoding=THREE.sRGBEncoding;mt.map.needsUpdate=true;}
      mt.toneMapped=false;
      if(mt.emissive)mt.emissive.setHex(accent).multiplyScalar(glow);
      mt.needsUpdate=true;
    });
  });"""
if old not in s:
    raise SystemExit('No se encontro qkGearVisuals para aclarar materiales')
s=s.replace(old,new,1)

# 3) Las rotaciones manuales de KayKit usan ejes locales distintos y doblaban el torso
#    Quaternius. Para esos rigs reproducimos clips del propio modelo y NO tocamos huesos.
anchor="""function animGLB(e,dt){
  const r=e.rig,isP=(e===P),dead=isP?P.dead:e.state==='dead',atk=e.swing>0;"""
if anchor not in s:
    raise SystemExit('No se encontro animGLB esperado')
helper=r'''/* QUATERNIUS_T5_FIX_V2 - animacion nativa, sin torsion de huesos */
function qkAnimNative(e,dt){
  const r=e.rig,isP=(e===P),dead=isP?P.dead:e.state==='dead',atk=e.swing>0;
  let name='Idle_A',o={};
  if(dead){name='Death_A';o={once:true,ts:1.2};}
  else if(isP&&(P.jump||P.roll)){name='Jump_Idle';o={ts:1.0};}
  else if(atk){
    const ty=e.swingType||0;
    name=ty===1?'QK_Attack1':ty>=2?'QK_Attack2':'QK_Attack0';
    const a=r.act[name];
    if(a){
      const dur=Math.max(.16,e.swingDur||.35),clipDur=Math.max(.1,a.getClip().duration||dur);
      o={once:true,ts:clamp(clipDur/dur,.72,3.1)};
    }else name='Idle_A';
  }
  else if(e.hitT>0){name='Hit_A';o={once:true,ts:1.6};}
  else if(e.moving){
    const spd=isP?pSpeed():e.spd*(e.slowT>0?.45:1);
    if(spd>4.3){name='Running_A';o={ts:clamp(spd/5.6,.65,1.55)};}
    else{name='Walking_A';o={ts:clamp(spd/2.6,.65,1.45)};}
  }
  if(r.cur!==name)glbPlay(r,name,o);
  else if(o.ts&&r.act[name])r.act[name].timeScale=o.ts;
  if(e.hitT>0)e.hitT=Math.max(0,e.hitT-dt);
  r.mixer.update(dt);
  if(e.swing>0)e.swing=Math.max(0,e.swing-dt);
}
'''
newanchor=helper+"\nfunction animGLB(e,dt){\n  if(e.rig&&e.rig.qk){qkAnimNative(e,dt);return;}\n  const r=e.rig,isP=(e===P),dead=isP?P.dead:e.state==='dead',atk=e.swing>0;"
s=s.replace(anchor,newanchor,1)

# 4) El tercer golpe basico ya tiene Sword_Attack2 nativo: no sumar un giro 360 del grupo.
old="""    if(fin){P.spin=.3;lungeP(dx,dz,2.6,.2);}else lungeP(dx,dz,1.1,.14);"""
new="""    if(fin){if(!(playerRig&&playerRig.qk))P.spin=.3;lungeP(dx,dz,2.6,.2);}else lungeP(dx,dz,1.1,.14);"""
if old not in s:
    raise SystemExit('No se encontro giro del combo basico')
s=s.replace(old,new,1)

p.write_text(s)
print('Quaternius V2: texturas aclaradas y ataques nativos sin torsion')
