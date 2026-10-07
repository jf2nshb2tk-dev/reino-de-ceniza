from pathlib import Path
p=Path('index.html')
s=p.read_text()

marker='WARRIOR_ARMOR_V1'
if marker in s:
    print('Guerrero low-poly ya aplicado')
    raise SystemExit(0)

old="const rig={type:'glb',mixer:mixer,act:act,cur:null,rollG:rollG,tip:tip,base:base,weaponMats:wmats,uaR:bn['upperarm.r'],uaL:bn['upperarm.l'],chest:bn.chest,head:bn.head,handR:bn['hand.r'],handL:bn['hand.l'],footR:bn['foot.r'],footL:bn['foot.l'],armorVisuals:[]};"
new="const rig={type:'glb',mixer:mixer,act:act,cur:null,rollG:rollG,tip:tip,base:base,weaponMats:wmats,uaR:bn['upperarm.r'],uaL:bn['upperarm.l'],laR:bn['lowerarm.r'],laL:bn['lowerarm.l'],chest:bn.chest,hips:bn.hips,head:bn.head,handR:bn['hand.r'],handL:bn['hand.l'],llR:bn['lowerleg.r'],llL:bn['lowerleg.l'],footR:bn['foot.r'],footL:bn['foot.l'],armorVisuals:[]};"
if old not in s:
    raise SystemExit('No se encontro rig GLB esperado para ampliar huesos')
s=s.replace(old,new,1)

anchor='function armorIconHTML(it,sz){'
if anchor not in s:
    raise SystemExit('No se encontro armorIconHTML')

helpers=r'''/* WARRIOR_ARMOR_V1 - cinco tiers low-poly articulados */
const WARRIOR_MAIN=['#858a90','#c9d0d6','#44474c','#30343a','#2b2b2d'];
const WARRIOR_TRIM=['#795437','#54a6df','#dc3d35','#78cf58','#f0b24a'];
const warriorTier=it=>{const n=(it&&it.ilvl)||1;return n<20?0:n<40?1:n<60?2:n<80?3:4;};
function warriorColors(it){const t=warriorTier(it),main=new THREE.Color(WARRIOR_MAIN[t]),trim=new THREE.Color(WARRIOR_TRIM[t]);if(it&&it.r>0){const rc=new THREE.Color(RARITY[it.r].c);main.lerp(rc,.025*it.r);trim.lerp(rc,.04*it.r);}if(it&&it.set&&SETBYN[it.set]){const sc=new THREE.Color(SETBYN[it.set].c);trim.lerp(sc,.12);}return{main,trim};}
function warriorMat(it,trim){const c=warriorColors(it),col=trim?c.trim:c.main,lv=lvOf(it),e=lv>=15?.60:lv>=11?.34:lv>=7?.15:0,m=new THREE.MeshPhongMaterial({color:col,flatShading:true,shininess:trim?68:30});if(e){m.emissive.copy(col).multiplyScalar(e);}return m;}
function wg(parent){if(!parent)return null;const g=new THREE.Group();parent.add(g);playerRig.armorVisuals.push(g);return g;}
function wp(g,geo,m,sx,sy,sz,x=0,y=0,z=0,rx=0,ry=0,rz=0){return avPart(g,geo,m,sx,sy,sz,x,y,z,rx,ry,rz);}
function warriorHelmet(it){const p=playerRig.head;if(!it||!p)return;const t=warriorTier(it),g=wg(p),m=warriorMat(it,false),a=warriorMat(it,true);
  if(t===0){wp(g,USph,m,.30,.20,.30,0,.07,.015);wp(g,UB,a,.22,.09,.31,0,.00,.19);wp(g,UB,a,.035,.17,.30,-.22,.04,.01,0,0,.18);wp(g,UB,a,.035,.17,.30,.22,.04,.01,0,0,-.18);}
  if(t===1){wp(g,USph,m,.31,.22,.31,0,.08,.01);wp(g,UB,a,.24,.10,.32,0,.02,.20);wp(g,UCone,a,.055,.16,.055,0,.27,.015);wp(g,UB,a,.05,.17,.28,-.24,.09,.02,0,0,.22);wp(g,UB,a,.05,.17,.28,.24,.09,.02,0,0,-.22);}
  if(t===2){wp(g,USph,m,.32,.23,.32,0,.075,.01);wp(g,UB,a,.25,.11,.33,0,.01,.20);wp(g,UCone,a,.07,.24,.07,-.23,.26,.00,0,0,.34);wp(g,UCone,a,.07,.24,.07,.23,.26,.00,0,0,-.34);wp(g,UB,a,.035,.19,.34,0,.18,.08);}
  if(t===3){wp(g,USph,m,.33,.24,.33,0,.08,.005);wp(g,UB,a,.25,.115,.34,0,.01,.205);wp(g,UCone,a,.075,.25,.075,-.24,.27,-.01,0,0,.32);wp(g,UCone,a,.075,.25,.075,.24,.27,-.01,0,0,-.32);wp(g,UB,a,.06,.20,.34,0,.18,.09);wp(g,UOct,a,.075,.075,.05,0,.05,.235);}
  if(t===4){wp(g,USph,m,.34,.25,.34,0,.08,0);wp(g,UB,a,.26,.12,.35,0,.005,.21);wp(g,UCone,a,.08,.30,.08,-.25,.29,-.01,0,0,.28);wp(g,UCone,a,.08,.30,.08,.25,.29,-.01,0,0,-.28);wp(g,UCone,a,.065,.29,.065,0,.34,-.02);wp(g,UB,a,.065,.22,.35,0,.17,.09);wp(g,UOct,a,.085,.085,.055,0,.05,.24);}
}
function warriorTorso(it){if(!it)return;const t=warriorTier(it),m=warriorMat(it,false),a=warriorMat(it,true);
  if(playerRig.chest){const g=wg(playerRig.chest);wp(g,UB,m,.52+.025*t,.42+.02*t,.18+.008*t,0,.015,.105);wp(g,UB,a,.39+.02*t,.055,.205,0,.16,.112);wp(g,UB,a,.08,.29+.02*t,.205,-.27,-.035,.11,0,0,.08);wp(g,UB,a,.08,.29+.02*t,.205,.27,-.035,.11,0,0,-.08);if(t>=2){wp(g,UOct,a,.09,.09,.05,0,.02,.225);wp(g,UB,a,.23,.035,.23,0,-.16,.115);}if(t>=3){wp(g,UCone,a,.05,.16+.02*t,.05,-.25,.26,.08,0,0,.20);wp(g,UCone,a,.05,.16+.02*t,.05,.25,.26,.08,0,0,-.20);}if(t===4){wp(g,UB,a,.30,.035,.225,0,.075,.12,0,0,.0);}}
  const shoulder=(bone,side)=>{if(!bone)return;const g=wg(bone);const sc=.19+.018*t;wp(g,USph,m,sc,.13+.015*t,.23+.012*t,side*.03,.03,.02,0,0,side*.08);wp(g,UB,a,.19+.018*t,.045,.24+.012*t,side*.03,.08,.02,0,0,side*.10);if(t>=2)wp(g,UCone,a,.045+.006*t,.13+.025*t,.045+.006*t,side*(.17+.008*t),.13,.01,0,0,-side*.40);if(t===4){wp(g,UCone,a,.055,.20,.055,side*.14,.19,.0,0,0,-side*.28);}};
  shoulder(playerRig.uaL,-1);shoulder(playerRig.uaR,1);
  if(playerRig.hips){const g=wg(playerRig.hips);wp(g,UC,a,.36+.015*t,.055,.36+.015*t,0,.04,0);wp(g,UB,m,.16+.012*t,.22+.018*t,.10,-.18,-.14,.08,0,0,.06);wp(g,UB,m,.16+.012*t,.22+.018*t,.10,.18,-.14,.08,0,0,-.06);if(t>=2)wp(g,UB,a,.10,.25+.02*t,.09,0,-.16,.16);}
}
function warriorGloves(it){if(!it)return;const t=warriorTier(it),m=warriorMat(it,false),a=warriorMat(it,true);const one=(lower,hand,side)=>{if(lower){const g=wg(lower);wp(g,UB,m,.15+.01*t,.22+.015*t,.17+.01*t,0,.08,.02);wp(g,UB,a,.16+.01*t,.045,.18+.01*t,0,.19,.02);if(t>=2)wp(g,UCone,a,.035,.12+.015*t,.035,side*.09,.20,.02,0,0,-side*.25);}if(hand){const h=wg(hand);wp(h,USph,m,.145+.008*t,.11+.008*t,.16+.008*t,0,.0,.03);wp(h,UB,a,.12+.008*t,.035,.16+.008*t,0,.075,.035);}};one(playerRig.laL,playerRig.handL,-1);one(playerRig.laR,playerRig.handR,1);}
function warriorBoots(it){if(!it)return;const t=warriorTier(it),m=warriorMat(it,false),a=warriorMat(it,true);const one=(leg,foot,side)=>{if(leg){const g=wg(leg);wp(g,UB,m,.17+.012*t,.25+.018*t,.18+.012*t,0,.11,.01);wp(g,UB,a,.18+.012*t,.05,.19+.012*t,0,.26,.01);if(t>=2)wp(g,UCone,a,.038,.12+.015*t,.038,side*.09,.25,.015,0,0,-side*.22);}if(foot){const f=wg(foot);wp(f,UB,m,.20+.012*t,.14+.008*t,.29+.018*t,0,.04,.095);wp(f,UB,a,.205+.012*t,.04,.30+.018*t,0,.13,.09);if(t===4)wp(f,UCone,a,.04,.11,.04,side*.10,.15,.07,0,0,-side*.20);}};one(playerRig.llL,playerRig.footL,-1);one(playerRig.llR,playerRig.footR,1);}
function attachWarriorSet(){warriorHelmet(P.eq.casco);warriorTorso(P.eq.armadura);warriorGloves(P.eq.guantes);warriorBoots(P.eq.botas);}
function warriorArmorIconHTML(it,sz){const t=warriorTier(it),c=warriorColors(it),fill='#'+c.main.getHexString(),stroke='#'+c.trim.getHexString(),s=sz||26;let b='';if(it.slot==='casco'){b='<path d="M8 13L11 5h10l3 8-2 12H10z"/><path d="M11 14h10v5H11z"/>'+(t>=2?'<path d="M10 7L6 3l5 2M22 7l4-4-5 2"/>':'')+(t===4?'<path d="M16 5V1"/>':'');}else if(it.slot==='armadura'){b='<path d="M9 7l4-3h6l4 3 5 5-4 4v12H8V16l-4-4z"/><path d="M11 10h10v12H11z"/>'+(t>=1?'<path d="M8 8L3 11l4 5M24 8l5 3-4 5"/>':'')+(t>=3?'<path d="M12 15h8M13 20h6"/>':'');}else if(it.slot==='guantes'){b='<path d="M8 13l3-7h10l3 7-3 13H11z"/><path d="M10 18h12"/>'+(t>=2?'<path d="M9 10L5 7M23 10l4-3"/>':'');}else{b='<path d="M10 4h10v13l6 4v6H7v-6l3-4z"/><path d="M10 13h10"/>'+(t>=2?'<path d="M8 22h17"/>':'')+(t===4?'<path d="M20 18l5-5"/>':'');}const glow=lvOf(it)>=15?' style="filter:drop-shadow(0 0 4px '+stroke+')"':'';return '<svg class="gearicon" width="'+s+'" height="'+s+'" viewBox="0 0 32 32"'+glow+'><g fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.7" stroke-linejoin="round">'+b+'</g></svg>';}
function warriorGroundGearVisual(g,it){const t=warriorTier(it),m=warriorMat(it,false),a=warriorMat(it,true);if(it.slot==='casco'){wp(g,USph,m,.43,.28,.41,0,.0,0);wp(g,UB,a,.28,.10,.43,0,-.04,.20);if(t>=2){wp(g,UCone,a,.08,.22,.08,-.31,.17,0,0,0,.38);wp(g,UCone,a,.08,.22,.08,.31,.17,0,0,0,-.38);}}else if(it.slot==='armadura'){wp(g,UB,m,.66,.53,.23,0,0,0);wp(g,USph,m,.24,.15,.26,-.40,.13,0);wp(g,USph,m,.24,.15,.26,.40,.13,0);wp(g,UB,a,.44,.055,.245,0,.18,.01);if(t>=3){wp(g,UCone,a,.06,.22,.06,-.43,.29,0);wp(g,UCone,a,.06,.22,.06,.43,.29,0);}}else if(it.slot==='guantes'){wp(g,UB,m,.31,.33,.28,0,0,0);wp(g,UB,a,.33,.07,.30,0,.19,0);}else if(it.slot==='botas'){wp(g,UB,m,.38,.40,.55,0,0,.07);wp(g,UB,a,.40,.08,.57,0,.22,.04);}if(t===4)wp(g,UOct,a,.11,.11,.08,0,.38,.02);}
'''
s=s.replace(anchor,helpers+'\n'+anchor,1)

old="function armorIconHTML(it,sz){if(!it||!['casco','armadura','guantes','botas'].includes(it.slot))return icon(it?it.slot:'armadura',sz||26);"
new="function armorIconHTML(it,sz){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return warriorArmorIconHTML(it,sz);if(!it||!['casco','armadura','guantes','botas'].includes(it.slot))return icon(it?it.slot:'armadura',sz||26);"
if old not in s:
    raise SystemExit('No se encontro inicio de armorIconHTML')
s=s.replace(old,new,1)

old="function groundGearVisual(g,it){const t=armorTier(it),mm=armorMat(it,false),tm=armorMat(it,true),k=.86+t*.07;"
new="function groundGearVisual(g,it){if(P&&P.cls==='guerrero'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){warriorGroundGearVisual(g,it);return;}const t=armorTier(it),mm=armorMat(it,false),tm=armorMat(it,true),k=.86+t*.07;"
if old not in s:
    raise SystemExit('No se encontro groundGearVisual')
s=s.replace(old,new,1)

old="clearArmorVisuals();attachArmorVisual(P.eq.casco,'casco',playerRig.head,1);attachArmorVisual(P.eq.armadura,'armadura',playerRig.chest,1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handL,-1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handR,1);attachArmorVisual(P.eq.botas,'botas',playerRig.footL,-1);attachArmorVisual(P.eq.botas,'botas',playerRig.footR,1);return;"
new="clearArmorVisuals();if(P.cls==='guerrero')attachWarriorSet();else{attachArmorVisual(P.eq.casco,'casco',playerRig.head,1);attachArmorVisual(P.eq.armadura,'armadura',playerRig.chest,1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handL,-1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handR,1);attachArmorVisual(P.eq.botas,'botas',playerRig.footL,-1);attachArmorVisual(P.eq.botas,'botas',playerRig.footR,1);}return;"
if old not in s:
    raise SystemExit('No se encontro bloque de gearVisuals GLB')
s=s.replace(old,new,1)

p.write_text(s)
print('Cinco tiers low-poly de Guerrero aplicados')
