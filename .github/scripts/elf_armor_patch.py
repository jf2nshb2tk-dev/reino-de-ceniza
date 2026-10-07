from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='ELF_ARMOR_V1'
if marker in s:
    print('Armaduras del Elfo ya aplicadas')
    raise SystemExit(0)

# Solo cambia el texto visible; la clave interna sigue siendo `elfa` para no romper guardados ni balance.
s=s.replace("elfa:{name:'Elfa',desc:'Arquera veloz. Dispara desde lejos, envenena y se cura sola.'", "elfa:{name:'Elfo',desc:'Arquero veloz. Dispara desde lejos, envenena y se cura solo.'", 1)

anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals')

helpers=r'''/* ELF_ARMOR_V1 - cinco tiers low-poly ligeros para el Ranger; clave interna: elfa */
const ELF_MAIN=['#35543d','#d7e7df','#263a30','#505956','#1f6048'];
const ELF_TRIM=['#8b6a45','#8fc6b7','#b94a40','#62bd7d','#d8b45c'];
const elfTier=it=>armorTier(it);
function elfColors(it){const t=elfTier(it),main=new THREE.Color(ELF_MAIN[t]),trim=new THREE.Color(ELF_TRIM[t]);if(it&&it.r>0){const rc=new THREE.Color(RARITY[it.r].c);main.lerp(rc,.03*it.r);trim.lerp(rc,.045*it.r);}if(it&&it.set&&SETBYN[it.set]){const sc=new THREE.Color(SETBYN[it.set].c);trim.lerp(sc,.13);}return{main,trim};}
function elfMat(it,trim){const c=elfColors(it),col=trim?c.trim:c.main,lv=lvOf(it),e=lv>=15?.52:lv>=11?.28:lv>=7?.11:0,m=new THREE.MeshPhongMaterial({color:col,flatShading:true,shininess:trim?48:18});if(e)m.emissive.copy(col).multiplyScalar(e);return m;}
function elfBaseMesh(name){return (playerMeshes||[]).find(m=>m&&m.name===name)||null;}
function elfPaint(name,color,em=0){const m=elfBaseMesh(name);if(!m||!m.material)return;const mats=Array.isArray(m.material)?m.material:[m.material];m.visible=true;mats.forEach(mt=>{mt.map=null;if(mt.color)mt.color.copy(color instanceof THREE.Color?color:new THREE.Color(color));if(mt.emissive)mt.emissive.copy(color instanceof THREE.Color?color:new THREE.Color(color)).multiplyScalar(em);mt.metalness=0;mt.roughness=.88;mt.needsUpdate=true;});}
function elfHide(name){const m=elfBaseMesh(name);if(m)m.visible=false;}
function elfBaseSkin(){if(P.cls!=='elfa')return;elfHide('Ranger_Cape');elfPaint('Ranger_Body',0x37423b);elfPaint('Ranger_ArmLeft',0x4a4037);elfPaint('Ranger_ArmRight',0x4a4037);elfPaint('Ranger_LegLeft',0x343a35);elfPaint('Ranger_LegRight',0x343a35);elfPaint('Ranger_Quiver',0x5a4230);const h=elfBaseMesh('Ranger_Head');if(h)h.visible=true;}
function eg(parent){if(!parent)return null;const g=new THREE.Group();parent.add(g);playerRig.armorVisuals.push(g);return g;}
function ep(g,geo,m,sx,sy,sz,x=0,y=0,z=0,rx=0,ry=0,rz=0){return avPart(g,geo,m,sx,sy,sz,x,y,z,rx,ry,rz);}
function elfHelmet(it){if(!it||!playerRig.head)return;const t=elfTier(it),g=eg(playerRig.head),m=elfMat(it,false),a=elfMat(it,true);ep(g,UC,m,.34+.012*t,.038,.34+.012*t,0,.62,.005);ep(g,UOct,a,.055+.007*t,.055+.007*t,.035,0,.55,.205);if(t>=1){ep(g,UCone,a,.025,.10+.012*t,.025,-.23,.69,.02,0,0,.38);ep(g,UCone,a,.025,.10+.012*t,.025,.23,.69,.02,0,0,-.38);}if(t>=3){ep(g,UOct,a,.035,.035,.025,-.16,.60,.19);ep(g,UOct,a,.035,.035,.025,.16,.60,.19);}if(t===4)ep(g,UCone,a,.035,.14,.035,0,.76,.01);}
function elfTorso(it){if(!it)return;const t=elfTier(it),c=elfColors(it),lv=lvOf(it),e=lv>=15?.32:lv>=11?.17:lv>=7?.06:0;elfPaint('Ranger_Body',c.main,e);if(t>=1){elfPaint('Ranger_Cape',t===1?c.main:c.trim,e*.55);const cp=elfBaseMesh('Ranger_Cape');if(cp)cp.visible=true;}else elfHide('Ranger_Cape');if(playerRig.chest){const g=eg(playerRig.chest),a=elfMat(it,true),m=elfMat(it,false);ep(g,UOct,a,.075+.008*t,.075+.008*t,.035,0,.015,.175);ep(g,UB,a,.24+.012*t,.03,.16,0,.14,.075);if(t>=2)ep(g,UB,m,.15,.025,.15,0,-.12,.065);if(t===4){ep(g,UCone,a,.03,.13,.03,-.19,.18,.04,0,0,.30);ep(g,UCone,a,.03,.13,.03,.19,.18,.04,0,0,-.30);}}const shoulder=(bone,side)=>{if(!bone)return;const g=eg(bone),m=elfMat(it,false),a=elfMat(it,true);ep(g,UB,m,.105+.008*t,.032,.17+.008*t,side*.02,.075,.01,0,0,side*.06);ep(g,UB,a,.10+.008*t,.02,.18+.008*t,side*.02,.105,.01,0,0,side*.08);if(t>=3)ep(g,UCone,a,.026,.09+.01*t,.026,side*.10,.13,.01,0,0,-side*.38);};shoulder(playerRig.uaL,-1);shoulder(playerRig.uaR,1);}
function elfGloves(it){if(!it)return;const t=elfTier(it),c=elfColors(it),lv=lvOf(it),e=lv>=15?.28:lv>=11?.14:lv>=7?.05:0;elfPaint('Ranger_ArmLeft',c.main,e);elfPaint('Ranger_ArmRight',c.main,e);const one=(lower,hand,side)=>{if(lower){const g=eg(lower),a=elfMat(it,true);ep(g,UC,a,.115+.006*t,.045,.115+.006*t,0,.15,.01);if(t>=2)ep(g,UCone,a,.024,.08+.01*t,.024,side*.07,.17,.025,0,0,-side*.28);}if(hand&&t>=3){const h=eg(hand),m=elfMat(it,false);ep(h,USph,m,.10,.075,.11,0,.01,.025);}};one(playerRig.laL,playerRig.handL,-1);one(playerRig.laR,playerRig.handR,1);}
function elfBoots(it){if(!it)return;const t=elfTier(it),c=elfColors(it),lv=lvOf(it),e=lv>=15?.25:lv>=11?.13:lv>=7?.045:0;elfPaint('Ranger_LegLeft',c.main,e);elfPaint('Ranger_LegRight',c.main,e);const one=(leg,foot,side)=>{if(leg){const g=eg(leg),a=elfMat(it,true);ep(g,UB,a,.105+.007*t,.14+.01*t,.115+.008*t,0,.12,.01);if(t>=3)ep(g,UCone,a,.022,.075,.022,side*.065,.20,.02,0,0,-side*.25);}if(foot){const f=eg(foot),m=elfMat(it,false);ep(f,UB,m,.145+.007*t,.085,.21+.01*t,0,.03,.065);}};one(playerRig.llL,playerRig.footL,-1);one(playerRig.llR,playerRig.footR,1);}
function attachElfSet(){elfHelmet(P.eq.casco);elfTorso(P.eq.armadura);elfGloves(P.eq.guantes);elfBoots(P.eq.botas);}
function elfArmorIconHTML(it,sz){const t=elfTier(it),c=elfColors(it),fill='#'+c.main.getHexString(),stroke='#'+c.trim.getHexString(),s=sz||26;let b='';if(it.slot==='casco')b='<path d="M7 17q9-9 18 0v5H7z"/><path d="M9 16l-3-5 6 3M23 16l3-5-6 3"/>'+(t>=3?'<path d="M16 10v-4"/>':'');else if(it.slot==='armadura')b='<path d="M10 7l4-3h4l4 3 5 5-4 3v13H9V15l-4-3z"/><path d="M12 10h8v14h-8z"/>'+(t>=2?'<path d="M9 9l-5 4M23 9l5 4"/>':'');else if(it.slot==='guantes')b='<path d="M9 10h14v15H9z"/><path d="M10 18h12"/>'+(t>=2?'<path d="M8 11l-3-2M24 11l3-2"/>':'');else b='<path d="M11 5h10v14l5 3v5H7v-5l4-3z"/><path d="M11 14h10"/>'+(t>=3?'<path d="M8 24h17"/>':'');const glow=lvOf(it)>=15?' style="filter:drop-shadow(0 0 4px '+stroke+')"':'';return '<svg class="gearicon" width="'+s+'" height="'+s+'" viewBox="0 0 32 32"'+glow+'><g fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.55" stroke-linejoin="round">'+b+'</g></svg>';}
function elfGroundGearVisual(g,it){const t=elfTier(it),m=elfMat(it,false),a=elfMat(it,true);if(it.slot==='casco'){ep(g,UC,m,.40,.055,.40,0,.04,0);ep(g,UOct,a,.08,.08,.05,0,.10,.39);if(t>=2){ep(g,UCone,a,.04,.15,.04,-.28,.17,0,0,0,.4);ep(g,UCone,a,.04,.15,.04,.28,.17,0,0,0,-.4);}}else if(it.slot==='armadura'){ep(g,UB,m,.48,.52,.17,0,0,0);ep(g,UOct,a,.08,.08,.04,0,.10,.18);ep(g,UB,a,.34,.035,.18,0,.18,.01);if(t>=3){ep(g,UCone,a,.035,.13,.035,-.30,.22,0);ep(g,UCone,a,.035,.13,.035,.30,.22,0);}}else if(it.slot==='guantes'){ep(g,UC,m,.22,.18,.22,0,0,0);ep(g,UC,a,.24,.045,.24,0,.13,0);}else if(it.slot==='botas'){ep(g,UB,m,.28,.31,.40,0,0,.04);ep(g,UB,a,.29,.045,.41,0,.17,.03);}if(t===4)ep(g,UOct,a,.07,.07,.05,0,.34,.01);}
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
print('Cinco tiers visuales del Elfo aplicados; clave interna elfa conservada')
