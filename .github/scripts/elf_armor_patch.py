from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='ELF_ARMOR_V2'
if marker in s:
    print('Armaduras del Elfo V2 ya aplicadas')
    raise SystemExit(0)

# Solo cambia el texto visible; la clave interna sigue siendo `elfa` para no romper guardados ni balance.
s=s.replace("elfa:{name:'Elfa',desc:'Arquera veloz. Dispara desde lejos, envenena y se cura sola.'", "elfa:{name:'Elfo',desc:'Arquero veloz. Dispara desde lejos, envenena y se cura solo.'", 1)

anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals')

helpers=r'''/* ELF_ARMOR_V2 - silueta más marcada para que el equipo se lea en cámara móvil */
const ELF_MAIN=['#3d563e','#d4ded8','#304238','#202a27','#0d5f45'];
const ELF_TRIM=['#9b7549','#92beb4','#bd5147','#69d38c','#e2bb57'];
const elfTier=it=>armorTier(it);
function elfColors(it){
  const t=elfTier(it),main=new THREE.Color(ELF_MAIN[t]),trim=new THREE.Color(ELF_TRIM[t]);
  if(it&&it.r>0){const rc=new THREE.Color(RARITY[it.r].c);main.lerp(rc,.018*it.r);trim.lerp(rc,.025*it.r);}
  if(it&&it.set&&SETBYN[it.set]){const sc=new THREE.Color(SETBYN[it.set].c);trim.lerp(sc,.10);}
  return{main,trim};
}
function elfMat(it,trim){const c=elfColors(it),col=trim?c.trim:c.main,lv=lvOf(it),e=lv>=15?.38:lv>=11?.20:lv>=7?.08:0,m=new THREE.MeshPhongMaterial({color:col,flatShading:true,shininess:trim?50:20});if(e)m.emissive.copy(col).multiplyScalar(e);return m;}
function elfBaseMesh(name){return (playerMeshes||[]).find(m=>m&&m.name===name)||null;}
function elfPaint(name,color,em=0){const m=elfBaseMesh(name);if(!m||!m.material)return;const mats=Array.isArray(m.material)?m.material:[m.material];m.visible=true;mats.forEach(mt=>{mt.map=null;if(mt.color)mt.color.copy(color instanceof THREE.Color?color:new THREE.Color(color));if(mt.emissive)mt.emissive.copy(color instanceof THREE.Color?color:new THREE.Color(color)).multiplyScalar(Math.min(.10,em));mt.metalness=0;mt.roughness=.88;mt.needsUpdate=true;});}
function elfHide(name){const m=elfBaseMesh(name);if(m)m.visible=false;}
function elfBaseSkin(){
  if(P.cls!=='elfa')return;
  elfHide('Ranger_Cape');
  elfPaint('Ranger_Body',0x26332c);elfPaint('Ranger_ArmLeft',0x37443b);elfPaint('Ranger_ArmRight',0x37443b);
  elfPaint('Ranger_LegLeft',0x29342e);elfPaint('Ranger_LegRight',0x29342e);elfPaint('Ranger_Quiver',0x533d2b);
  const h=elfBaseMesh('Ranger_Head');if(h)h.visible=true;
}
function eg(parent){if(!parent)return null;const g=new THREE.Group();g.scale.setScalar(1.16);parent.add(g);playerRig.armorVisuals.push(g);return g;}
function ep(g,geo,m,sx,sy,sz,x=0,y=0,z=0,rx=0,ry=0,rz=0){return avPart(g,geo,m,sx,sy,sz,x,y,z,rx,ry,rz);}
function elfHelmet(it){
  if(!it||!playerRig.head)return;
  const t=elfTier(it),g=eg(playerRig.head),m=elfMat(it,false),a=elfMat(it,true);
  // Casquete facetado + frontal ancho: se distingue incluso con la cámara alejada del móvil.
  ep(g,USph,m,.36,.13,.33,0,.71,-.015);
  ep(g,UB,a,.31,.055,.12,0,.61,.245);
  ep(g,UB,m,.075,.18,.17,-.30,.57,.08,0,0,.10);
  ep(g,UB,m,.075,.18,.17,.30,.57,.08,0,0,-.10);
  if(t>=1){
    ep(g,UCone,a,.055,.18,.055,-.28,.77,-.02,0,0,.42);
    ep(g,UCone,a,.055,.18,.055,.28,.77,-.02,0,0,-.42);
  }
  if(t>=2){ep(g,UOct,a,.075,.075,.045,0,.60,.30);}
  if(t>=3){
    ep(g,UCone,a,.06,.22,.06,-.22,.84,-.03,0,0,.28);
    ep(g,UCone,a,.06,.22,.06,.22,.84,-.03,0,0,-.28);
  }
  if(t===4){
    ep(g,UCone,a,.07,.27,.07,0,.91,-.04);
    ep(g,UB,a,.23,.04,.14,0,.76,.18);
  }
}
function elfTorso(it){
  if(!it)return;
  const t=elfTier(it),c=elfColors(it),lv=lvOf(it),e=lv>=15?.16:lv>=11?.09:lv>=7?.04:0;
  elfPaint('Ranger_Body',c.main,e);
  if(t>=1){elfPaint('Ranger_Cape',t===1?c.main:c.trim,e*.5);const cp=elfBaseMesh('Ranger_Cape');if(cp)cp.visible=true;}else elfHide('Ranger_Cape');
  if(playerRig.chest){
    const g=eg(playerRig.chest),m=elfMat(it,false),a=elfMat(it,true);
    ep(g,UB,m,.42+.018*t,.31+.015*t,.16+.008*t,0,.015,.14);
    ep(g,UB,a,.34+.012*t,.045,.175,0,.145,.155);
    ep(g,UOct,a,.09+.008*t,.09+.008*t,.05,0,.025,.245);
    if(t>=2){ep(g,UB,a,.07,.24,.16,-.22,-.02,.155,0,0,.10);ep(g,UB,a,.07,.24,.16,.22,-.02,.155,0,0,-.10);}
    if(t>=3){ep(g,UCone,a,.045,.16,.045,-.19,.24,.08,0,0,.28);ep(g,UCone,a,.045,.16,.045,.19,.24,.08,0,0,-.28);}
    if(t===4){ep(g,UB,a,.26,.035,.18,0,-.15,.155);}
  }
  if(playerRig.hips){
    const h=eg(playerRig.hips),m=elfMat(it,false),a=elfMat(it,true);
    ep(h,UB,a,.33,.07,.17,0,.08,.08);
    if(t>=2){ep(h,UB,m,.12,.18,.12,-.14,-.07,.07,0,0,.08);ep(h,UB,m,.12,.18,.12,.14,-.07,.07,0,0,-.08);}
  }
  const shoulder=(bone,side)=>{if(!bone)return;const g=eg(bone),m=elfMat(it,false),a=elfMat(it,true);
    ep(g,UB,m,.18+.012*t,.075,.25+.012*t,side*.025,.075,.015,0,0,side*.10);
    ep(g,UB,a,.18+.012*t,.035,.26+.012*t,side*.025,.125,.02,0,0,side*.12);
    if(t>=2)ep(g,UCone,a,.045,.15+.018*t,.045,side*(.14+.005*t),.17,.0,0,0,-side*.42);
    if(t>=3)ep(g,UCone,a,.04,.18+.018*t,.04,side*.05,.21,-.11,.45,0,-side*.15);
    if(t===4)ep(g,UOct,a,.055,.055,.045,side*.12,.15,.12);
  };
  shoulder(playerRig.uaL,-1);shoulder(playerRig.uaR,1);
}
function elfGloves(it){
  if(!it)return;const t=elfTier(it),c=elfColors(it),lv=lvOf(it),e=lv>=15?.12:lv>=11?.07:lv>=7?.03:0;
  elfPaint('Ranger_ArmLeft',c.main,e);elfPaint('Ranger_ArmRight',c.main,e);
  const one=(lower,hand,side)=>{if(lower){const g=eg(lower),m=elfMat(it,false),a=elfMat(it,true);ep(g,UB,m,.15+.008*t,.19+.01*t,.14+.008*t,0,.11,.015);ep(g,UB,a,.16+.008*t,.04,.15+.008*t,0,.22,.02);if(t>=2)ep(g,UCone,a,.032,.10+.012*t,.032,side*.09,.23,.025,0,0,-side*.32);}if(hand){const h=eg(hand),m=elfMat(it,false);ep(h,USph,m,.105+.004*t,.08,.115+.004*t,0,.015,.025);}};
  one(playerRig.laL,playerRig.handL,-1);one(playerRig.laR,playerRig.handR,1);
}
function elfBoots(it){
  if(!it)return;const t=elfTier(it),c=elfColors(it),lv=lvOf(it),e=lv>=15?.12:lv>=11?.07:lv>=7?.03:0;
  elfPaint('Ranger_LegLeft',c.main,e);elfPaint('Ranger_LegRight',c.main,e);
  const one=(leg,foot,side)=>{if(leg){const g=eg(leg),m=elfMat(it,false),a=elfMat(it,true);ep(g,UB,m,.15+.009*t,.23+.012*t,.14+.008*t,0,.13,.02);ep(g,UB,a,.16+.009*t,.045,.15+.008*t,0,.25,.025);if(t>=3)ep(g,UCone,a,.03,.095,.03,side*.09,.28,.02,0,0,-side*.28);}if(foot){const f=eg(foot),m=elfMat(it,false),a=elfMat(it,true);ep(f,UB,m,.17+.008*t,.10,.24+.012*t,0,.04,.075);if(t===4)ep(f,UB,a,.13,.035,.20,0,.10,.09);}};
  one(playerRig.llL,playerRig.footL,-1);one(playerRig.llR,playerRig.footR,1);
}
function attachElfSet(){elfHelmet(P.eq.casco);elfTorso(P.eq.armadura);elfGloves(P.eq.guantes);elfBoots(P.eq.botas);}
function elfArmorIconHTML(it,sz){const t=elfTier(it),c=elfColors(it),fill='#'+c.main.getHexString(),stroke='#'+c.trim.getHexString(),s=sz||26;let b='';if(it.slot==='casco')b='<path d="M6 18q10-11 20 0v5H6z"/><path d="M9 14l-5-5 7 2M23 14l5-5-7 2"/>'+(t>=3?'<path d="M16 10V4"/>':'');else if(it.slot==='armadura')b='<path d="M9 7l5-3h4l5 3 6 5-5 4v12H8V16l-5-4z"/><path d="M12 10h8v14h-8z"/><path d="M8 9l-5 4M24 9l5 4"/>'+(t>=3?'<path d="M16 11l3 5-3 3-3-3z"/>':'');else if(it.slot==='guantes')b='<path d="M8 9h16v16H8z"/><path d="M9 18h14"/>'+(t>=2?'<path d="M7 10l-4-3M25 10l4-3"/>':'');else b='<path d="M10 4h12v15l5 3v6H6v-6l4-3z"/><path d="M10 14h12"/>'+(t>=3?'<path d="M7 24h19"/>':'');const glow=lvOf(it)>=15?' style="filter:drop-shadow(0 0 4px '+stroke+')"':'';return '<svg class="gearicon" width="'+s+'" height="'+s+'" viewBox="0 0 32 32"'+glow+'><g fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.65" stroke-linejoin="round">'+b+'</g></svg>';}
function elfGroundGearVisual(g,it){const t=elfTier(it),m=elfMat(it,false),a=elfMat(it,true);if(it.slot==='casco'){ep(g,USph,m,.43,.18,.39,0,.08,0);ep(g,UB,a,.36,.06,.14,0,.04,.35);if(t>=2){ep(g,UCone,a,.055,.18,.055,-.30,.22,0,0,0,.4);ep(g,UCone,a,.055,.18,.055,.30,.22,0,0,0,-.4);}}else if(it.slot==='armadura'){ep(g,UB,m,.58,.60,.20,0,0,0);ep(g,UOct,a,.10,.10,.055,0,.10,.22);ep(g,UB,a,.42,.045,.21,0,.20,.01);if(t>=3){ep(g,UCone,a,.045,.16,.045,-.36,.26,0);ep(g,UCone,a,.045,.16,.045,.36,.26,0);}}else if(it.slot==='guantes'){ep(g,UB,m,.30,.32,.26,0,0,0);ep(g,UB,a,.31,.055,.27,0,.18,0);}else if(it.slot==='botas'){ep(g,UB,m,.34,.40,.48,0,0,.05);ep(g,UB,a,.35,.055,.49,0,.22,.04);}if(t===4)ep(g,UOct,a,.09,.09,.06,0,.42,.01);}
'''
s=s.replace(anchor,helpers+'\n'+anchor,1)

old="function armorIconHTML(it,sz){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return warriorArmorIconHTML(it,sz);if(P&&P.cls==='mago'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return mageArmorIconHTML(it,sz);"
new="function armorIconHTML(it,sz){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return warriorArmorIconHTML(it,sz);if(P&&P.cls==='mago'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return mageArmorIconHTML(it,sz);if(P&&P.cls==='elfa'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return elfArmorIconHTML(it,sz);"
if old not in s: raise SystemExit('No se encontro armorIconHTML con ramas Guerrero/Mago')
s=s.replace(old,new,1)

old="function groundGearVisual(g,it){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){warriorGroundGearVisual(g,it);return;}if(P&&P.cls==='mago'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){mageGroundGearVisual(g,it);return;}"
new="function groundGearVisual(g,it){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){warriorGroundGearVisual(g,it);return;}if(P&&P.cls==='mago'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){mageGroundGearVisual(g,it);return;}if(P&&P.cls==='elfa'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){elfGroundGearVisual(g,it);return;}"
if old not in s: raise SystemExit('No se encontro groundGearVisual con ramas Guerrero/Mago')
s=s.replace(old,new,1)

old="if(P.cls==='guerrero'){warriorBaseSkin();attachWarriorSet();}else if(P.cls==='mago'){mageBaseSkin();attachMageSet();}else{"
new="if(P.cls==='guerrero'){warriorBaseSkin();attachWarriorSet();}else if(P.cls==='mago'){mageBaseSkin();attachMageSet();}else if(P.cls==='elfa'){elfBaseSkin();attachElfSet();}else{"
if old not in s: raise SystemExit('No se encontro rama Guerrero/Mago en gearVisuals')
s=s.replace(old,new,1)

p.write_text(s)
print('ELF_ARMOR_V2 aplicada: piezas más grandes y silueta T4/T5 reforzada')
