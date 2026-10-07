from pathlib import Path
p=Path('index.html');s=p.read_text();marker='REMAINING_ARMOR_V2'
if marker in s:
    print('Armaduras restantes ya aplicadas');raise SystemExit(0)
anchor='function gearVisuals(){'
if anchor not in s: raise SystemExit('No se encontro gearVisuals')
helpers=r'''/* REMAINING_ARMOR_V2 - Barbaro, Asesino y Brujo, 5 tiers low-poly */
const REST_CFG={
 barbaro:{main:['#6b4b35','#d9d7cf','#4a2322','#252526','#211d1b'],trim:['#8f8a82','#8faab6','#a63a32','#7a3028','#b46b3d'],body:'Barbarian_Body',al:'Barbarian_ArmLeft',ar:'Barbarian_ArmRight',ll:'Barbarian_LegLeft',lr:'Barbarian_LegRight',head:'Barbarian_Head',hat:'Barbarian_BearHat',cape:null,mask:null,sc:1.22,bulk:1.28,kind:'b'},
 asesino:{main:['#24252a','#1e3140','#251d20','#17151c','#151419'],trim:['#858b95','#55b9cf','#c7443d','#8658b1','#c8a85b'],body:'Rogue_Body',al:'Rogue_ArmLeft',ar:'Rogue_ArmRight',ll:'Rogue_LegLeft',lr:'Rogue_LegRight',head:'Rogue_Head',hat:null,cape:'Rogue_Cape',mask:null,sc:1.14,bulk:.92,kind:'a'},
 brujo:{main:['#241d2d','#172736','#27191f','#151a18','#1b1424'],trim:['#76579a','#6652a1','#b23842','#5fc58a','#d7ad58'],body:'RogueHooded_Body',al:'RogueHooded_ArmLeft',ar:'RogueHooded_ArmRight',ll:'RogueHooded_LegLeft',lr:'RogueHooded_LegRight',head:'RogueHooded_Head',hat:null,cape:'RogueHooded_Cape',mask:'RogueHooded_Mask',sc:1.16,bulk:1.0,kind:'w'}
};
const restTier=it=>armorTier(it);
function restMesh(n){return (playerMeshes||[]).find(m=>m&&m.name===n)||null;}
function restHide(n){const m=n&&restMesh(n);if(m)m.visible=false;}
function restPaint(n,c,e=0){const m=n&&restMesh(n);if(!m||!m.material)return;const a=Array.isArray(m.material)?m.material:[m.material];m.visible=true;a.forEach(mt=>{mt.map=null;if(mt.color)mt.color.copy(c instanceof THREE.Color?c:new THREE.Color(c));if(mt.emissive)mt.emissive.copy(c instanceof THREE.Color?c:new THREE.Color(c)).multiplyScalar(Math.min(.12,e));mt.needsUpdate=true;});}
function restColors(it,cls){const q=REST_CFG[cls],t=restTier(it),main=new THREE.Color(q.main[t]),trim=new THREE.Color(q.trim[t]);if(it&&it.r>0)trim.lerp(new THREE.Color(RARITY[it.r].c),.03*it.r);if(it&&it.set&&SETBYN[it.set])trim.lerp(new THREE.Color(SETBYN[it.set].c),.10);return{main,trim};}
function restMat(it,cls,trim){const c=restColors(it,cls),col=trim?c.trim:c.main,lv=lvOf(it),e=lv>=15?.45:lv>=11?.24:lv>=7?.09:0,m=new THREE.MeshPhongMaterial({color:col,flatShading:true,shininess:trim?60:20});if(e)m.emissive.copy(col).multiplyScalar(e);return m;}
function rg2(parent,cls){if(!parent)return null;const g=new THREE.Group();g.scale.setScalar(REST_CFG[cls].sc);parent.add(g);playerRig.armorVisuals.push(g);return g;}
function rp2(g,geo,m,sx,sy,sz,x=0,y=0,z=0,rx=0,ry=0,rz=0){return avPart(g,geo,m,sx,sy,sz,x,y,z,rx,ry,rz);}
function restBase(cls){const q=REST_CFG[cls];if(P.cls!==cls)return;restHide(q.hat);restHide(q.mask);restHide(q.cape);restPaint(q.body,cls==='barbaro'?0x49372b:cls==='asesino'?0x202127:0x241d2b);restPaint(q.al,cls==='barbaro'?0x76553f:0x292832);restPaint(q.ar,cls==='barbaro'?0x76553f:0x292832);restPaint(q.ll,cls==='barbaro'?0x352b25:0x1d1c23);restPaint(q.lr,cls==='barbaro'?0x352b25:0x1d1c23);if(q.head){const h=restMesh(q.head);if(h)h.visible=true;}}
function restHelmet(it,cls){if(!it)return;const q=REST_CFG[cls],t=restTier(it),c=restColors(it,cls),lv=lvOf(it),e=lv>=15?.25:lv>=11?.14:lv>=7?.05:0;if(q.hat){restPaint(q.hat,c.main,e);const h=restMesh(q.hat);if(h)h.visible=true;}if(q.mask){restPaint(q.head,c.main,e*.35);restPaint(q.mask,c.trim,e);const m=restMesh(q.mask);if(m)m.visible=true;}if(!playerRig.head)return;const g=rg2(playerRig.head,cls),m=restMat(it,cls,false),a=restMat(it,cls,true);
 if(q.kind==='a'){rp2(g,USph,m,.34,.15,.33,0,.71,-.02);rp2(g,UB,a,.30,.08,.10,0,.58,.27);rp2(g,UB,m,.065,.19,.16,-.28,.57,.08,0,0,.10);rp2(g,UB,m,.065,.19,.16,.28,.57,.08,0,0,-.10);}
 if(t>=1){const x=q.kind==='b'?.25:.22;rp2(g,UCone,a,.05,.18+.02*t,.05,-x,.82,-.03,0,0,.38);rp2(g,UCone,a,.05,.18+.02*t,.05,x,.82,-.03,0,0,-.38);}
 if(t>=2)rp2(g,UOct,a,.07,.07,.045,0,.60,.30);
 if(t>=3){rp2(g,UCone,a,.06,.23,.06,-.18,.89,-.04,0,0,.24);rp2(g,UCone,a,.06,.23,.06,.18,.89,-.04,0,0,-.24);}
 if(t===4)rp2(g,UCone,a,.07,.29,.07,0,.96,-.05);
}
function restTorso(it,cls){if(!it)return;const q=REST_CFG[cls],t=restTier(it),c=restColors(it,cls),lv=lvOf(it),e=lv>=15?.14:lv>=11?.08:lv>=7?.03:0;restPaint(q.body,c.main,e);if(q.cape){if(t>=1+(q.kind==='a'?1:0)){restPaint(q.cape,t===4?c.trim:c.main,e*.4);const cp=restMesh(q.cape);if(cp)cp.visible=true;}else restHide(q.cape);}
 if(playerRig.chest){const g=rg2(playerRig.chest,cls),m=restMat(it,cls,false),a=restMat(it,cls,true),b=q.bulk;rp2(g,UB,m,.42*b+.018*t,.31*b+.015*t,.16+.009*t,0,.015,.14);rp2(g,UB,a,.34*b+.014*t,.045,.18,0,.15,.15);rp2(g,UOct,a,.08+.008*t,.08+.008*t,.05,0,.02,.25);if(t>=2){rp2(g,UB,a,.06,.22,.15,-.21*b,-.02,.15,0,0,.12);rp2(g,UB,a,.06,.22,.15,.21*b,-.02,.15,0,0,-.12);}if(t>=3){rp2(g,UCone,a,.045,.16,.045,-.21*b,.24,.07,0,0,.27);rp2(g,UCone,a,.045,.16,.045,.21*b,.24,.07,0,0,-.27);}}
 if(playerRig.hips){const h=rg2(playerRig.hips,cls),m=restMat(it,cls,false),a=restMat(it,cls,true);rp2(h,UB,a,.33*q.bulk,.065,.17,0,.08,.08);if(t>=2){rp2(h,UB,m,.13,.20,.12,-.15,-.08,.07,0,0,.08);rp2(h,UB,m,.13,.20,.12,.15,-.08,.07,0,0,-.08);}}
 const sh=(bone,side)=>{if(!bone)return;const g=rg2(bone,cls),m=restMat(it,cls,false),a=restMat(it,cls,true),w=(q.kind==='b'?.24:q.kind==='a'?.15:.18)+.012*t;rp2(g,q.kind==='b'?UOct:UB,m,w,.08+.01*t,.24+.014*t,side*.02,.09,.01,0,0,side*.10);rp2(g,UB,a,w,.03,.25+.014*t,side*.02,.15,.02,0,0,side*.12);if(t>=2)rp2(g,UCone,a,.04+(q.kind==='b'?.015:0),.15+.02*t,.04,side*(w*.75),.19,0,0,0,-side*.42);if(t===4)rp2(g,UOct,a,.055,.055,.045,side*.11,.15,.11);};sh(playerRig.uaL,-1);sh(playerRig.uaR,1);
}
function restGloves(it,cls){if(!it)return;const q=REST_CFG[cls],t=restTier(it),c=restColors(it,cls);restPaint(q.al,c.main);restPaint(q.ar,c.main);const one=(lower,hand,side)=>{if(lower){const g=rg2(lower,cls),m=restMat(it,cls,false),a=restMat(it,cls,true),b=q.bulk;rp2(g,UB,m,.15*b+.007*t,.21*b+.012*t,.14*b+.007*t,0,.11,.015);rp2(g,UB,a,.16*b+.007*t,.04,.15*b+.007*t,0,.22,.02);if(t>=2)rp2(g,q.kind==='a'?UCone:UOct,a,.035,.10+.015*t,.035,side*.09,.21,.04,0,0,-side*.28);}if(hand){const h=rg2(hand,cls),m=restMat(it,cls,false);rp2(h,USph,m,.105*q.bulk,.08,.115*q.bulk,0,.015,.025);}};one(playerRig.laL,playerRig.handL,-1);one(playerRig.laR,playerRig.handR,1);}
function restBoots(it,cls){if(!it)return;const q=REST_CFG[cls],t=restTier(it),c=restColors(it,cls);restPaint(q.ll,c.main);restPaint(q.lr,c.main);const one=(leg,foot,side)=>{if(leg){const g=rg2(leg,cls),m=restMat(it,cls,false),a=restMat(it,cls,true),b=q.bulk;rp2(g,UB,m,.15*b+.008*t,.23*b+.012*t,.14*b+.008*t,0,.13,.02);rp2(g,UB,a,.16*b+.008*t,.04,.15*b+.008*t,0,.25,.025);if(t>=3)rp2(g,UCone,a,.03,.095,.03,side*.08,.28,.02,0,0,-side*.27);}if(foot){const f=rg2(foot,cls),m=restMat(it,cls,false);rp2(f,UB,m,.17*q.bulk+.008*t,.10,.24*q.bulk+.012*t,0,.04,.075);}};one(playerRig.llL,playerRig.footL,-1);one(playerRig.llR,playerRig.footR,1);}
function attachRestSet(cls){restHelmet(P.eq.casco,cls);restTorso(P.eq.armadura,cls);restGloves(P.eq.guantes,cls);restBoots(P.eq.botas,cls);}
function restArmorIconHTML(it,sz,cls){const t=restTier(it),c=restColors(it,cls),fill='#'+c.main.getHexString(),stroke='#'+c.trim.getHexString(),s=sz||26;let b='';if(it.slot==='casco')b='<path d="M6 18q10-12 20 0v6H6z"/><path d="M9 16l-5-5 7 2M23 16l5-5-7 2"/>'+(t>=3?'<path d="M16 10V4"/>':'');else if(it.slot==='armadura')b='<path d="M8 7l6-3h4l6 3 6 6-5 4v11H7V17l-5-4z"/><path d="M12 10h8v14h-8z"/>'+(t>=2?'<path d="M7 10l-5 4M25 10l5 4"/>':'');else if(it.slot==='guantes')b='<path d="M8 9h16v16H8z"/><path d="M9 18h14"/>';else b='<path d="M10 4h12v15l5 3v6H6v-6l4-3z"/><path d="M10 14h12"/>';const glow=lvOf(it)>=15?' style="filter:drop-shadow(0 0 4px '+stroke+')"':'';return '<svg class="gearicon" width="'+s+'" height="'+s+'" viewBox="0 0 32 32"'+glow+'><g fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.65" stroke-linejoin="round">'+b+'</g></svg>';}
function restGroundGearVisual(g,it,cls){const t=restTier(it),q=REST_CFG[cls],m=restMat(it,cls,false),a=restMat(it,cls,true),b=q.bulk;if(it.slot==='casco'){rp2(g,USph,m,.44,.22,.41,0,.08,0);if(t>=2){rp2(g,UCone,a,.05,.18,.05,-.30,.23,0,0,0,.4);rp2(g,UCone,a,.05,.18,.05,.30,.23,0,0,0,-.4);}}else if(it.slot==='armadura'){rp2(g,UB,m,.58*b,.60,.21,0,0,0);rp2(g,UOct,a,.11*b,.10,.06,0,.10,.22);if(t>=3){rp2(g,UCone,a,.04,.15,.04,-.34*b,.25,0);rp2(g,UCone,a,.04,.15,.04,.34*b,.25,0);}}else if(it.slot==='guantes'){rp2(g,UB,m,.30*b,.32,.26*b,0,0,0);rp2(g,UB,a,.31*b,.05,.27*b,0,.18,0);}else{rp2(g,UB,m,.33*b,.39,.47*b,0,0,.05);rp2(g,UB,a,.34*b,.05,.48*b,0,.21,.04);}if(t===4)rp2(g,UOct,a,.09,.09,.06,0,.42,.01);}
'''
s=s.replace(anchor,helpers+'\n'+anchor,1)
needle="if(P&&P.cls==='elfa'&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return elfArmorIconHTML(it,sz);"
if needle not in s: raise SystemExit('No se encontro Elfo en armorIconHTML')
s=s.replace(needle,needle+"if(P&&['barbaro','asesino','brujo'].includes(P.cls)&&it&&['casco','armadura','guantes','botas'].includes(it.slot))return restArmorIconHTML(it,sz,P.cls);",1)
needle="if(P&&P.cls==='elfa'&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){elfGroundGearVisual(g,it);return;}"
if needle not in s: raise SystemExit('No se encontro Elfo en groundGearVisual')
s=s.replace(needle,needle+"if(P&&['barbaro','asesino','brujo'].includes(P.cls)&&it&&['casco','armadura','guantes','botas'].includes(it.slot)){restGroundGearVisual(g,it,P.cls);return;}",1)
needle="else if(P.cls==='elfa'){elfBaseSkin();attachElfSet();}else{"
if needle not in s: raise SystemExit('No se encontro Elfo en gearVisuals')
s=s.replace(needle,"else if(P.cls==='elfa'){elfBaseSkin();attachElfSet();}else if(['barbaro','asesino','brujo'].includes(P.cls)){restBase(P.cls);attachRestSet(P.cls);}else{",1)
p.write_text(s);print('Barbaro, Asesino y Brujo: 5 tiers aplicados')
