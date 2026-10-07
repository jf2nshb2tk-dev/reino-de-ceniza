from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='MAGE_ARMOR_V1'
if marker in s:
    print('Armaduras del Mago ya aplicadas')
    raise SystemExit(0)

anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals')

helpers=r'''/* MAGE_ARMOR_V1 - cinco tiers low-poly usando la silueta original del Mage */
const MAGE_MAIN=['#344b78','#8bbfd1','#653536','#3a2f50','#2b2239'];
const MAGE_TRIM=['#aebbd0','#e8f4ff','#d8ad57','#73b78f','#d8b05c'];
const mageTier=it=>armorTier(it);
function mageColors(it){const t=mageTier(it),main=new THREE.Color(MAGE_MAIN[t]),trim=new THREE.Color(MAGE_TRIM[t]);if(it&&it.r>0){const rc=new THREE.Color(RARITY[it.r].c);main.lerp(rc,.035*it.r);trim.lerp(rc,.05*it.r);}if(it&&it.set&&SETBYN[it.set]){const sc=new THREE.Color(SETBYN[it.set].c);trim.lerp(sc,.14);}return{main,trim};}
function mageMat(it,trim){const c=mageColors(it),col=trim?c.trim:c.main,lv=lvOf(it),e=lv>=15?.55:lv>=11?.30:lv>=7?.12:0,m=new THREE.MeshPhongMaterial({color:col,flatShading:true,shininess:trim?54:22});if(e)m.emissive.copy(col).multiplyScalar(e);return m;}
function mageBaseMesh(name){return (playerMeshes||[]).find(m=>m&&m.name===name)||null;}
function magePaint(name,color,em=0){const m=mageBaseMesh(name);if(!m||!m.material)return;const mats=Array.isArray(m.material)?m.material:[m.material];m.visible=true;mats.forEach(mt=>{mt.map=null;if(mt.color)mt.color.copy(color instanceof THREE.Color?color:new THREE.Color(color));if(mt.emissive)mt.emissive.copy(color instanceof THREE.Color?color:new THREE.Color(color)).multiplyScalar(em);mt.metalness=0;mt.roughness=.82;mt.needsUpdate=true;});}
function mageHide(name){const m=mageBaseMesh(name);if(m)m.visible=false;}
function mageBaseSkin(){if(P.cls!=='mago')return;mageHide('Mage_Hat');mageHide('Mage_Cape');magePaint('Mage_Body',0x2a2c3a);magePaint('Mage_ArmLeft',0x303241);magePaint('Mage_ArmRight',0x303241);magePaint('Mage_LegLeft',0x242633);magePaint('Mage_LegRight',0x242633);const h=mageBaseMesh('Mage_Head');if(h)h.visible=true;}
function mg(parent){if(!parent)return null;const g=new THREE.Group();parent.add(g);playerRig.armorVisuals.push(g);return g;}
function mp(g,geo,m,sx,sy,sz,x=0,y=0,z=0,rx=0,ry=0,rz=0){return avPart(g,geo,m,sx,sy,sz,x,y,z,rx,ry,rz);}
function mageHelmet(it){if(!it)return;const t=mageTier(it),c=mageColors(it),lv=lvOf(it),e=lv>=15?.48:lv>=11?.26:lv>=7?.10:0;magePaint('Mage_Hat',c.main,e);const h=mageBaseMesh('Mage_Hat');if(h)h.visible=true;if(t>=2&&playerRig.head){const g=mg(playerRig.head),a=mageMat(it,true);mp(g,UOct,a,.075+.008*t,.075+.008*t,.05,0,.49,.21);if(t===4){mp(g,UCone,a,.04,.15,.04,-.16,.53,.02,0,0,.22);mp(g,UCone,a,.04,.15,.04,.16,.53,.02,0,0,-.22);}}}
function mageTorso(it){if(!it)return;const t=mageTier(it),c=mageColors(it),lv=lvOf(it),e=lv>=15?.35:lv>=11?.18:lv>=7?.07:0;magePaint('Mage_Body',c.main,e);if(t>=1){magePaint('Mage_Cape',c.trim,e*.7);const cp=mageBaseMesh('Mage_Cape');if(cp)cp.visible=true;}else mageHide('Mage_Cape');if(playerRig.chest){const g=mg(playerRig.chest),a=mageMat(it,true),m=mageMat(it,false);mp(g,UOct,a,.085+.01*t,.085+.01*t,.045,0,.02,.19);mp(g,UB,a,.24+.015*t,.035,.18,0,.15,.085);if(t>=2){mp(g,UCone,a,.035,.12+.018*t,.035,-.24,.18,.05,0,0,.20);mp(g,UCone,a,.035,.12+.018*t,.035,.24,.18,.05,0,0,-.20);}if(t===4){mp(g,UB,m,.31,.025,.16,0,-.13,.075);}}
  const sh=(bone,side)=>{if(!bone)return;const g=mg(bone),a=mageMat(it,true);mp(g,UB,a,.12+.012*t,.035,.18+.01*t,side*.025,.08,.01,0,0,side*.08);if(t>=3)mp(g,UOct,a,.045,.045,.04,side*.10,.12,.02);};sh(playerRig.uaL,-1);sh(playerRig.uaR,1);
}
function mageGloves(it){if(!it)return;const t=mageTier(it),c=mageColors(it),lv=lvOf(it),e=lv>=15?.30:lv>=11?.16:lv>=7?.06:0;magePaint('Mage_ArmLeft',c.main,e);magePaint('Mage_ArmRight',c.main,e);const one=(lower,side)=>{if(!lower)return;const g=mg(lower),a=mageMat(it,true);mp(g,UC,a,.13+.008*t,.055,.13+.008*t,0,.16,.01);if(t>=2)mp(g,UOct,a,.04+.005*t,.04+.005*t,.035,side*.08,.17,.07);};one(playerRig.laL,-1);one(playerRig.laR,1);}
function mageBoots(it){if(!it)return;const t=mageTier(it),c=mageColors(it),lv=lvOf(it),e=lv>=15?.28:lv>=11?.14:lv>=7?.05:0;magePaint('Mage_LegLeft',c.main,e);magePaint('Mage_LegRight',c.main,e);const one=(leg,foot,side)=>{if(leg){const g=mg(leg),a=mageMat(it,true);mp(g,UB,a,.12+.01*t,.15+.012*t,.13+.01*t,0,.12,.015);if(t>=3)mp(g,UOct,a,.035,.035,.03,side*.07,.20,.04);}if(foot){const f=mg(foot),m=mageMat(it,false);mp(f,UB,m,.16+.008*t,.10,.23+.012*t,0,.035,.07);}};one(playerRig.llL,playerRig.footL,-1);one(playerRig.llR,playerRig.footR,1);}
function attachMageSet(){mageHelmet(P.eq.casco);mageTorso(P.eq.armadura);mageGloves(P.eq.guantes);mageBoots(P.eq.botas);}
function mageArmorIconHTML(it,sz){const t=mageTier(it),c=mageColors(it),fill='#'+c.main.getHexString(),stroke='#'+c.trim.getHexString(),s=sz||26;let b='';if(it.slot==='casco')b='<path d="M6 20h20L18 5h-5z"/><path d="M5 21h22v4H5z"/>'+(t>=2?'<path d="M16 7l2 4-3 2"/>':'');else if(it.slot==='armadura')b='<path d="M10 6l4-2h4l4 2 4 6-4 3v13H10V15l-4-3z"/><path d="M13 10h6v14h-6z"/>'+(t>=2?'<path d="M8 10l-4 3M24 10l4 3"/>':'');else if(it.slot==='guantes')b='<path d="M9 10h14v15H9z"/><path d="M10 15h12"/>'+(t>=2?'<path d="M8 11l-3-3M24 11l3-3"/>':'');else b='<path d="M11 5h10v14l5 3v5H7v-5l4-3z"/><path d="M11 14h10"/>';const glow=lvOf(it)>=15?' style="filter:drop-shadow(0 0 4px '+stroke+')"':'';return '<svg class="gearicon" width="'+s+'" height="'+s+'" viewBox="0 0 32 32"'+glow+'><g fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.6" stroke-linejoin="round">'+b+'</g></svg>';}
function mageGroundGearVisual(g,it){const t=mageTier(it),m=mageMat(it,false),a=mageMat(it,true);if(it.slot==='casco'){mp(g,UCone,m,.34,.55,.34,0,.08,0);mp(g,UC,a,.43,.05,.43,0,-.20,0);}else if(it.slot==='armadura'){mp(g,UB,m,.50,.58,.18,0,0,0);mp(g,UOct,a,.09,.09,.05,0,.10,.20);if(t>=2){mp(g,UCone,a,.04,.15,.04,-.31,.20,0);mp(g,UCone,a,.04,.15,.04,.31,.20,0);}}else if(it.slot==='guantes'){mp(g,UC,m,.24,.20,.24,0,0,0);mp(g,UC,a,.26,.05,.26,0,.15,0);}else if(it.slot==='botas'){mp(g,UB,m,.30,.34,.42,0,0,.05);mp(g,UB,a,.31,.05,.43,0,.18,.03);}if(t===4)mp(g,UOct,a,.08,.08,.06,0,.38,.01);}
'''
s=s.replace(anchor,helpers+'\n'+anchor,1)

old="function armorIconHTML(it,sz){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return warriorArmorIconHTML(it,sz);"
new="function armorIconHTML(it,sz){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return warriorArmorIconHTML(it,sz);if(P&&P.cls==='mago'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return mageArmorIconHTML(it,sz);"
if old not in s: raise SystemExit('No se encontro armorIconHTML con rama Guerrero')
s=s.replace(old,new,1)

old="function groundGearVisual(g,it){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){warriorGroundGearVisual(g,it);return;}"
new="function groundGearVisual(g,it){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){warriorGroundGearVisual(g,it);return;}if(P&&P.cls==='mago'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){mageGroundGearVisual(g,it);return;}"
if old not in s: raise SystemExit('No se encontro groundGearVisual con rama Guerrero')
s=s.replace(old,new,1)

old="if(P.cls==='guerrero'){warriorBaseSkin();attachWarriorSet();}else{"
new="if(P.cls==='guerrero'){warriorBaseSkin();attachWarriorSet();}else if(P.cls==='mago'){mageBaseSkin();attachMageSet();}else{"
if old not in s: raise SystemExit('No se encontro rama Guerrero en gearVisuals')
s=s.replace(old,new,1)

p.write_text(s)
print('Cinco tiers visuales del Mago aplicados')
