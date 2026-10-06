from pathlib import Path

p=Path('index.html')
s=p.read_text()

old="const bn={};['upperarm.r','upperarm.l','chest','head','handslot.r','handslot.l'].forEach(n=>{bn[n]=kkFind(model,n);});"
new="const bn={};['upperarm.r','upperarm.l','lowerarm.r','lowerarm.l','hand.r','hand.l','chest','head','hips','foot.r','foot.l','lowerleg.r','lowerleg.l','handslot.r','handslot.l'].forEach(n=>{bn[n]=kkFind(model,n);});"
if old not in s: raise SystemExit('No se encontró lista de huesos KayKit')
s=s.replace(old,new,1)

old="const rig={type:'glb',mixer:mixer,act:act,cur:null,rollG:rollG,tip:tip,base:base,weaponMats:wmats,uaR:bn['upperarm.r'],uaL:bn['upperarm.l'],chest:bn.chest};"
new="const rig={type:'glb',mixer:mixer,act:act,cur:null,rollG:rollG,tip:tip,base:base,weaponMats:wmats,uaR:bn['upperarm.r'],uaL:bn['upperarm.l'],chest:bn.chest,head:bn.head,handR:bn['hand.r'],handL:bn['hand.l'],footR:bn['foot.r'],footL:bn['foot.l'],armorVisuals:[]};"
if old not in s: raise SystemExit('No se encontró rig KayKit')
s=s.replace(old,new,1)

marker="function gearVisuals(){"
if marker not in s: raise SystemExit('No se encontró gearVisuals')
helpers=r'''const ARMOR_TIER_HEX=['#6b4a32','#7b8086','#46515d','#292634','#51351f'];
const ARMOR_TIER_TRIM=['#9b7652','#b7bdc3','#95a3b3','#8a63ad','#f0b24a'];
const armorTier=it=>Math.max(0,Math.min(4,Math.floor((((it&&it.ilvl)||1)-1)/20)));
function armorUIColor(it){if(it&&it.set&&SETBYN[it.set])return SETBYN[it.set].c;return ARMOR_TIER_HEX[armorTier(it)];}
function armorThreeColors(it){const t=armorTier(it),main=new THREE.Color(ARMOR_TIER_HEX[t]),trim=new THREE.Color(ARMOR_TIER_TRIM[t]),rc=new THREE.Color(RARITY[(it&&it.r)||0].c);if(it&&it.set&&SETBYN[it.set]){const sc=new THREE.Color(SETBYN[it.set].c);main.lerp(sc,.40);trim.lerp(sc,.55);}else if(it&&it.r>0){main.lerp(rc,.12+.07*it.r);trim.lerp(rc,.22+.08*it.r);}return{main,trim};}
function armorMat(it,trim){const c=armorThreeColors(it),lv=lvOf(it),em=lv>=15?.58:lv>=11?.34:lv>=7?.16:0,col=trim?c.trim:c.main,m=new THREE.MeshPhongMaterial({color:col,flatShading:true,shininess:trim?55:24});if(em>0)m.emissive.copy(col).multiplyScalar(em);return m;}
function clearArmorVisuals(){if(!playerRig||!playerRig.armorVisuals)return;playerRig.armorVisuals.forEach(g=>{if(g.parent)g.parent.remove(g);g.traverse(o=>{if(o.isMesh&&o.material&&o.material.dispose)o.material.dispose();});});playerRig.armorVisuals.length=0;}
function avPart(g,geo,m,sx,sy,sz,x,y,z,rx,ry,rz){return part(g,geo,m,sx,sy,sz,x||0,y||0,z||0,rx||0,ry||0,rz||0);}
function attachArmorVisual(it,slot,parent,side){if(!it||!parent)return;const t=armorTier(it),g=new THREE.Group(),mm=armorMat(it,false),tm=armorMat(it,true),k=1+t*.055;parent.add(g);playerRig.armorVisuals.push(g);
  if(slot==='casco'){avPart(g,USph,mm,.32*k,.19+.025*t,.31*k,0,.08,.015);avPart(g,UC,tm,.34*k,.045,.34*k,0,.075,.01);if(t>=1)avPart(g,UB,tm,.055,.20+.03*t,.27,0,.21,.015);if(t>=2){avPart(g,UCone,tm,.075,.18+.04*t,.075,-.25,.20,0,0,0,.42);avPart(g,UCone,tm,.075,.18+.04*t,.075,.25,.20,0,0,0,-.42);}if(t>=4)avPart(g,UCone,tm,.08,.28,.08,0,.31,-.02);}
  else if(slot==='armadura'){avPart(g,UB,mm,.58*k,.48+.035*t,.20+.018*t,0,.02,.09);avPart(g,UB,tm,.48*k,.055,.225,0,.17,.10);if(t>=1){avPart(g,USph,mm,.22+.025*t,.15+.018*t,.24,-.34,.16,.045,0,0,.18);avPart(g,USph,mm,.22+.025*t,.15+.018*t,.24,.34,.16,.045,0,0,-.18);}if(t>=2){avPart(g,UB,tm,.08,.30,.23,-.27,-.02,.10,0,0,.12);avPart(g,UB,tm,.08,.30,.23,.27,-.02,.10,0,0,-.12);}if(t>=3){avPart(g,UCone,tm,.06,.20+.035*t,.06,-.38,.30,.03,0,0,.25);avPart(g,UCone,tm,.06,.20+.035*t,.06,.38,.30,.03,0,0,-.25);}}
  else if(slot==='guantes'){avPart(g,USph,mm,.17+.015*t,.15+.01*t,.19+.015*t,0,.01,.035);avPart(g,UC,tm,.19+.012*t,.065,.19+.012*t,0,-.11,.02);if(t>=3)avPart(g,UCone,tm,.045,.14,.045,(side||1)*.08,.06,.02,0,0,(side||1)*.3);}
  else if(slot==='botas'){avPart(g,UB,mm,.20+.014*t,.16+.014*t,.31+.018*t,0,.05,.10);avPart(g,UB,tm,.215+.014*t,.055,.32+.018*t,0,.14,.09);if(t>=2)avPart(g,UB,tm,.08,.20+.02*t,.18,(side||1)*.08,.18,.02,0,0,(side||1)*.08);if(t>=4)avPart(g,UCone,tm,.045,.13,.045,(side||1)*.10,.27,.01,0,0,(side||1)*.25);}}
function armorIconHTML(it,sz){if(!it||!['casco','armadura','guantes','botas'].includes(it.slot))return icon(it?it.slot:'armadura',sz||26);const t=armorTier(it),fill=armorUIColor(it),stroke=it.set&&SETBYN[it.set]?SETBYN[it.set].c:RARITY[it.r].c,s=sz||26;let body='';if(it.slot==='casco')body='<path d="M6 13Q8 4 16 4t10 9v7H6z"/><path d="M10 13h12v8H10z"/>'+(t>=2?'<path d="M7 8L3 4l6 2M25 8l4-4-6 2"/>':'')+(t>=4?'<path d="M16 4V1"/>':'');else if(it.slot==='armadura')body='<path d="M8 7l5-3h6l5 3 5 7-5 3v11H8V17l-5-3z"/>'+(t>=1?'<path d="M8 8L3 11M24 8l5 3"/>':'')+(t>=3?'<path d="M11 12h10M12 17h8"/>':'');else if(it.slot==='guantes')body='<path d="M8 14V7h3v6-8h3v8-9h3v9-7h3v9l3-2 2 3-5 9H11l-5-6z"/>'+(t>=3?'<path d="M9 20h12"/>':'');else body='<path d="M10 4h9v13l7 3v7H7v-6l3-4z"/>'+(t>=2?'<path d="M10 12h9"/>':'')+(t>=4?'<path d="M20 18l5-5"/>':'');const glow=lvOf(it)>=15?' style="filter:drop-shadow(0 0 4px '+stroke+')"':'';return '<svg class="gearicon" width="'+s+'" height="'+s+'" viewBox="0 0 32 32"'+glow+'><g fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.8" stroke-linejoin="round">'+body+'</g></svg>';}
const UGearRing=new THREE.TorusGeometry(.38,.085,5,10);
function groundGearVisual(g,it){const t=armorTier(it),mm=armorMat(it,false),tm=armorMat(it,true),k=.86+t*.07;if(it.slot==='casco'){avPart(g,USph,mm,.46*k,.28,.42*k,0,.02,0);avPart(g,UC,tm,.49*k,.07,.49*k,0,-.08,0);if(t>=2){avPart(g,UCone,tm,.10,.25,.10,-.32,.18,0,0,0,.45);avPart(g,UCone,tm,.10,.25,.10,.32,.18,0,0,0,-.45);}}else if(it.slot==='armadura'){avPart(g,UB,mm,.72*k,.58,.24,0,0,0);avPart(g,USph,mm,.27,.18,.28,-.43,.14,0);avPart(g,USph,mm,.27,.18,.28,.43,.14,0);if(t>=3){avPart(g,UCone,tm,.08,.28,.08,-.48,.32,0);avPart(g,UCone,tm,.08,.28,.08,.48,.32,0);}}else if(it.slot==='guantes'){avPart(g,USph,mm,.34,.28,.38,0,0,0);avPart(g,UC,tm,.36,.12,.36,0,-.22,0);}else if(it.slot==='botas'){avPart(g,UB,mm,.42,.30,.62,0,0,.08);avPart(g,UB,tm,.44,.09,.64,0,.17,.05);}else if(it.slot==='anillo'){const q=new THREE.Mesh(UGearRing,tm);q.rotation.x=Math.PI/2;q.castShadow=true;g.add(q);}else{avPart(g,UB,mm,.10,1.0,.06,0,.18,0,.25,0,0);avPart(g,UB,tm,.42,.08,.12,0,-.28,0,.25,0,0);}if(t>=4&&it.slot!=='anillo')avPart(g,UOct,tm,.13,.13,.13,0,.42,0);}
'''
s=s.replace(marker,helpers+marker,1)

old="""function gearVisuals(){
  if(!playerRig)return;
  if(playerRig.type==='glb'){const w=P.eq.arma;playerRig.weaponMats.forEach(mt=>{if(w&&w.r>=2)mt.emissive.set(RARITY[w.r].c).multiplyScalar(.45);else mt.emissive.setHex(0);mt.userData.em0=mt.emissive.clone();});return;}const w=P.eq.arma,a=P.eq.armadura;
  const rc=it=>new THREE.Color(RARITY[it.r].c);
  if(playerRig.glow){const gm=playerRig.glow.material;
    if(w&&w.r>=2){gm.emissive.copy(rc(w)).multiplyScalar(.55);}
    else gm.emissive.setHex(P.cls==='mago'?0x6bb6ff:0x000000);}
  if(playerRig.torso){const tm=playerRig.torso.material,base=new THREE.Color(MODEL_OPT[P.cls].armor);
    if(a&&a.r>=1){tm.color.copy(base).lerp(rc(a),.28+.1*a.r);tm.emissive.copy(rc(a)).multiplyScalar(a.r>=2?.18:0);}
    else{tm.color.copy(base);tm.emissive.setHex(0);}}
}"""
new="""function gearVisuals(){
  if(!playerRig)return;
  if(playerRig.type==='glb'){const w=P.eq.arma;playerRig.weaponMats.forEach(mt=>{if(w&&w.r>=2)mt.emissive.set(RARITY[w.r].c).multiplyScalar(.45);else mt.emissive.setHex(0);mt.userData.em0=mt.emissive.clone();});clearArmorVisuals();attachArmorVisual(P.eq.casco,'casco',playerRig.head,1);attachArmorVisual(P.eq.armadura,'armadura',playerRig.chest,1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handL,-1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handR,1);attachArmorVisual(P.eq.botas,'botas',playerRig.footL,-1);attachArmorVisual(P.eq.botas,'botas',playerRig.footR,1);return;}
  const w=P.eq.arma,a=P.eq.armadura,rc=it=>new THREE.Color(RARITY[it.r].c);if(playerRig.glow){const gm=playerRig.glow.material;if(w&&w.r>=2)gm.emissive.copy(rc(w)).multiplyScalar(.55);else gm.emissive.setHex(P.cls==='mago'?0x6bb6ff:0x000000);}if(playerRig.torso){const tm=playerRig.torso.material,base=new THREE.Color(MODEL_OPT[P.cls].armor);if(a&&a.r>=1){tm.color.copy(base).lerp(rc(a),.28+.1*a.r);tm.emissive.copy(rc(a)).multiplyScalar(a.r>=2?.18:0);}else{tm.color.copy(base);tm.emissive.setHex(0);}}
}"""
if old not in s: raise SystemExit('No se encontró gearVisuals esperado')
s=s.replace(old,new,1)

old="""  else{const c=new THREE.Color(RARITY[data.item.r].c);part(g,UOct,new THREE.MeshBasicMaterial({color:c}),.5,.7,.5,0,0,0);
    if(data.item.r>=1){beam=new THREE.Mesh(BEAM,new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:.28+.08*data.item.r,depthWrite:false,blending:THREE.AdditiveBlending}));beam.position.y=-.55;g.add(beam);}}"""
new="""  else{const c=new THREE.Color(RARITY[data.item.r].c);groundGearVisual(g,data.item);
    if(data.item.r>=1){beam=new THREE.Mesh(BEAM,new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:.28+.08*data.item.r,depthWrite:false,blending:THREE.AdditiveBlending}));beam.position.y=-.55;g.add(beam);}}"""
if old not in s: raise SystemExit('No se encontró visual genérico de drop')
s=s.replace(old,new,1)

old="return '<button class=\"cell has'+(sel&&sel.id===it.id?' sel':'')+'\" '+attr+' style=\"--rc:'+RARITY[it.r].c+'\">'+icon(it.slot,26)+(lvOf(it)?'<i class=\"up\">+'+lvOf(it)+'</i>':'')+(it.set&&SETBYN[it.set]?'<i class=\"sp\" style=\"color:'+SETBYN[it.set].c+'\">◆</i>':'')+'<b>'+it.ilvl+'</b></button>';"
new="return '<button class=\"cell has'+(sel&&sel.id===it.id?' sel':'')+'\" '+attr+' style=\"--rc:'+RARITY[it.r].c+'\">'+armorIconHTML(it,26)+(lvOf(it)?'<i class=\"up\">+'+lvOf(it)+'</i>':'')+(it.set&&SETBYN[it.set]?'<i class=\"sp\" style=\"color:'+SETBYN[it.set].c+'\">◆</i>':'')+'<b>'+it.ilvl+'</b></button>';"
if old not in s: raise SystemExit('No se encontró cellHTML de equipo')
s=s.replace(old,new,1)

p.write_text(s)
print('Sistema visual de armaduras aplicado: 5 tiers, equipo, inventario y suelo')
