from pathlib import Path

p=Path("index.html")
s=p.read_text()
marker="QUATERNIUS_T5_V1"
if marker in s:
    print("Quaternius T5 ya aplicado")
    raise SystemExit(0)

anchor="const _qa=new THREE.Quaternion(),_ax=new THREE.Vector3(1,0,0),_ay=new THREE.Vector3(0,1,0);"
if anchor not in s:
    raise SystemExit("No se encontro ancla despues de KK_ENEMY")

helpers=r"""/* QUATERNIUS_T5_V1 - modelos T5 reales, carga bajo demanda */
const QK={chars:{},loading:{}};
const QK_SPEC={
  guerrero:{key:'Warrior',url:'assets/quaternius/Warrior.gltf',s:.68,weapon:/Warrior_Sword/i},
  mago:{key:'Wizard',url:'assets/quaternius/Wizard.gltf',s:.68,weapon:/Wizard_Staff/i},
  elfa:{key:'Ranger',url:'assets/quaternius/Ranger.gltf',s:.70,weapon:/Ranger_Bow/i}
};
function qkArmorCount(){
  if(!P)return 0;
  let n=0;
  ['casco','armadura','guantes','botas'].forEach(sl=>{const it=P.eq&&P.eq[sl];if(it&&armorTier(it)>=4)n++;});
  return n;
}
function qkCandidate(){
  return !!(P&&QK_SPEC[P.cls]&&((P.lvl||1)>=81||qkArmorCount()>=2));
}
function qkReady(cls){
  const sp=QK_SPEC[cls];
  return !!(sp&&QK.chars[sp.key]);
}
function qkEnsure(cls){
  const sp=QK_SPEC[cls];
  if(!sp||!THREE.GLTFLoader)return Promise.resolve(false);
  if(QK.chars[sp.key])return Promise.resolve(true);
  if(QK.loading[sp.key])return QK.loading[sp.key];
  QK.loading[sp.key]=new Promise(resolve=>{
    const ld=new THREE.GLTFLoader();
    ld.load(sp.url,g=>{QK.chars[sp.key]=g;resolve(true);},undefined,()=>resolve(false));
  }).finally(()=>{delete QK.loading[sp.key];});
  return QK.loading[sp.key];
}
function qkRequestIfNeeded(){
  if(!qkCandidate()||qkReady(P.cls))return;
  const cls=P.cls;
  qkEnsure(cls).then(ok=>{
    if(ok&&P&&P.cls===cls&&qkCandidate()&&playerRig&&!playerRig.qk)buildPlayerModel();
  });
}
function qkFind(model,name){
  const nm=name.replace(/[._]/g,'').toLowerCase();let f=null;
  model.traverse(o=>{if(!f&&o.isBone&&o.name.replace(/[._]/g,'').toLowerCase()===nm)f=o;});
  return f;
}
function qkBuild(cls){
  const sp=QK_SPEC[cls],src=sp&&QK.chars[sp.key];
  if(!src)return null;
  const model=THREE.SkeletonUtils.clone(src.scene),g=new THREE.Group(),rollG=new THREE.Group(),off=new THREE.Group();
  g.add(rollG);rollG.position.y=.8;rollG.add(off);off.position.y=-.8;off.add(model);model.scale.setScalar(sp.s);
  const mats=[],meshes=[],wmats=[];
  model.traverse(m=>{
    if(!m.isMesh)return;
    const mt=m.material.clone();
    mt.skinning=!!m.isSkinnedMesh;
    if('metalness' in mt)mt.metalness=Math.min(.18,mt.metalness||0);
    if('roughness' in mt)mt.roughness=.78;
    if(mt.emissive)mt.userData.em0=mt.emissive.clone();
    m.material=mt;m.castShadow=true;meshes.push(m);mats.push(mt);
    if(sp.weapon.test(m.name||''))wmats.push(mt);
  });
  const bn={
    uaR:qkFind(model,'UpperArm.R'),uaL:qkFind(model,'UpperArm.L'),
    laR:qkFind(model,'LowerArm.R'),laL:qkFind(model,'LowerArm.L'),
    handR:qkFind(model,'Fist.R'),handL:qkFind(model,'Fist.L'),
    chest:qkFind(model,'Torso'),hips:qkFind(model,'Hips'),
    llR:qkFind(model,'LowerLeg.R'),llL:qkFind(model,'LowerLeg.L'),
    footR:qkFind(model,'Foot.R'),footL:qkFind(model,'Foot.L'),
    head:qkFind(model,'Head')
  };
  const mixer=new THREE.AnimationMixer(model),act={};
  const cmap={Idle_A:'Idle',Walking_A:'Walk',Running_A:'Run',Death_A:'Death',Hit_A:'RecieveHit',Jump_Idle:'Roll'};
  Object.keys(cmap).forEach(k=>{
    const c=(src.animations||[]).find(x=>x.name===cmap[k]);
    if(c)act[k]=mixer.clipAction(c);
  });
  const rig={type:'glb',qk:true,qkClass:cls,mixer:mixer,act:act,cur:null,rollG:rollG,tip:null,base:null,weaponMats:wmats,
    uaR:bn.uaR,uaL:bn.uaL,laR:bn.laR,laL:bn.laL,chest:bn.chest,hips:bn.hips,head:bn.head,
    handR:bn.handR,handL:bn.handL,llR:bn.llR,llL:bn.llL,footR:bn.footR,footL:bn.footL,armorVisuals:[]};
  glbPlay(rig,'Idle_A');
  if(act.Idle_A)act.Idle_A.time=Math.random()*act.Idle_A.getClip().duration;
  return {g:g,glb:true,meshes:meshes,mats:mats,rig:rig};
}
function qkT5Active(){
  return qkCandidate()&&qkReady(P.cls);
}
function qkGearVisuals(){
  if(!playerRig||!playerRig.qk)return;
  const its=['casco','armadura','guantes','botas'].map(sl=>P.eq&&P.eq[sl]).filter(Boolean);
  let best=0;
  its.forEach(it=>{best=Math.max(best,lvOf(it));});
  const accent={guerrero:0xf0b24a,mago:0x9d78d0,elfa:0x68c994}[P.cls]||0xf0b24a;
  const glow=best>=15?.18:best>=11?.09:best>=7?.035:0;
  playerMeshes.forEach(me=>{
    const ms=Array.isArray(me.material)?me.material:[me.material];
    ms.forEach(mt=>{
      if(mt.color)mt.color.setHex(0xffffff);
      if(mt.emissive)mt.emissive.setHex(accent).multiplyScalar(glow);
      mt.needsUpdate=true;
    });
  });
  const w=P.eq&&P.eq.arma;
  playerRig.weaponMats.forEach(mt=>{
    if(!mt.emissive)return;
    if(w&&w.r>=2)mt.emissive.set(RARITY[w.r].c).multiplyScalar(.28);
  });
}
"""
s=s.replace(anchor,helpers+"\n"+anchor,1)

old="""function buildPlayerModel(){
  if(playerG){scene.remove(playerG);}
  const m=(KK.ok&&KK_PLAYER[P.cls])?kkBuild(KK_PLAYER[P.cls]):humanoid(MODEL_OPT[P.cls]);playerG=m.g;playerRig=m.rig;scene.add(playerG);
  if(trail){trail.dispose();trail=null;}
  if(playerRig.tip)trail=new Trail(22,[1,.85,.55]);
  playerMeshes=m.glb?m.meshes:collect(playerG);
  if(!m.glb)playerMeshes.forEach(me=>{me.userData.mat=me.material=me.material.clone();});
  gearVisuals();
}"""
new="""function buildPlayerModel(){
  if(playerG){scene.remove(playerG);}
  const qm=qkT5Active()?qkBuild(P.cls):null;
  const m=qm||((KK.ok&&KK_PLAYER[P.cls])?kkBuild(KK_PLAYER[P.cls]):humanoid(MODEL_OPT[P.cls]));playerG=m.g;playerRig=m.rig;scene.add(playerG);
  if(trail){trail.dispose();trail=null;}
  if(playerRig.tip)trail=new Trail(22,[1,.85,.55]);
  playerMeshes=m.glb?m.meshes:collect(playerG);
  if(!m.glb)playerMeshes.forEach(me=>{me.userData.mat=me.material=me.material.clone();});
  gearVisuals();
  qkRequestIfNeeded();
}"""
if old not in s:
    raise SystemExit("No se encontro buildPlayerModel esperado")
s=s.replace(old,new,1)

old2="""function gearVisuals(){
  if(!playerRig)return;
  if(playerRig.type==='glb'){const w=P.eq.arma;"""
new2="""function gearVisuals(){
  if(!playerRig)return;
  const wantQ=qkT5Active();
  if(!!playerRig.qk!==wantQ){buildPlayerModel();return;}
  if(playerRig.qk){qkGearVisuals();return;}
  if(qkCandidate()&&!qkReady(P.cls))qkRequestIfNeeded();
  if(playerRig.type==='glb'){const w=P.eq.arma;"""
if old2 not in s:
    raise SystemExit("No se encontro gearVisuals esperado")
s=s.replace(old2,new2,1)

p.write_text(s)
print("Quaternius T5 aplicado para Guerrero, Mago y Elfo con carga bajo demanda")
