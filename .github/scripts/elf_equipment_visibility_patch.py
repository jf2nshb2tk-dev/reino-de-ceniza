from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='ELF_EQUIPMENT_VISIBILITY_V1'
if marker in s:
    print('Contraste visual del Elfo ya aplicado')
    raise SystemExit(0)

# El problema visible era doble: la ropa base del Ranger parecia una armadura completa
# aun sin equipo, y las piezas Quaternius estaban demasiado cerca/dentro del cuerpo.
# Dejamos una ropa base neutra y sacamos las mallas equipadas mas afuera para que el
# cambio sin equipo -> T1..T5 sea obvio desde la camara del iPhone.
repls={
"elfPaint('Ranger_Body',0x26332c);elfPaint('Ranger_ArmLeft',0x37443b);elfPaint('Ranger_ArmRight',0x37443b);":"elfPaint('Ranger_Body',0x4b4439);elfPaint('Ranger_ArmLeft',0x6a5946);elfPaint('Ranger_ArmRight',0x6a5946);",
"elfPaint('Ranger_LegLeft',0x29342e);elfPaint('Ranger_LegRight',0x29342e);":"elfPaint('Ranger_LegLeft',0x383633);elfPaint('Ranger_LegRight',0x383633);",
"const QLOW_SCALE=[.72,.82,.92,1.03];":"const QLOW_SCALE=[.84,.98,1.13,1.30];",
"qkPiece(playerRig.chest,QKA.eChest,m,[.52,.43,.26],[0,.02,.09]);":"qkPiece(playerRig.chest,QKA.eChest,m,[.82,.70,.42],[0,.04,.15]);",
"qkPiece(playerRig.chest,QKA.eCloak,t,[.46,.55,.12],[0,.02,-.09]);":"qkPiece(playerRig.chest,QKA.eCloak,t,[.64,.78,.17],[0,.02,-.16]);",
"qkPiece(playerRig.laL,QKA.eArmL,m,[.15,.27,.16],[0,.09,.02]);":"qkPiece(playerRig.laL,QKA.eArmL,m,[.23,.38,.24],[0,.10,.035]);",
"qkPiece(playerRig.laR,QKA.eArmR,m,[.15,.27,.16],[0,.09,.02]);":"qkPiece(playerRig.laR,QKA.eArmR,m,[.23,.38,.24],[0,.10,.035]);",
"qkPiece(playerRig.llL,QKA.eLegL,m,[.17,.31,.18],[0,.10,.01]);":"qkPiece(playerRig.llL,QKA.eLegL,m,[.25,.44,.27],[0,.12,.025]);",
"qkPiece(playerRig.llR,QKA.eLegR,m,[.17,.31,.18],[0,.10,.01]);":"qkPiece(playerRig.llR,QKA.eLegR,m,[.25,.44,.27],[0,.12,.025]);",
"qkPiece(playerRig.footL,QKA.eFootL,t,[.18,.13,.27],[0,.03,.07]);":"qkPiece(playerRig.footL,QKA.eFootL,t,[.26,.19,.36],[0,.05,.11]);",
"qkPiece(playerRig.footR,QKA.eFootR,t,[.18,.13,.27],[0,.03,.07]);":"qkPiece(playerRig.footR,QKA.eFootR,t,[.26,.19,.36],[0,.05,.11]);",
"qkfPiece(playerRig.head,QKF.helm,m,[.48,.50,.42],[0,.61,.01]);":"qkfPiece(playerRig.head,QKF.helm,m,[.55,.58,.49],[0,.63,.02]);",
"qkfPiece(playerRig.uaL,QKF.shL,t,[.34,.24,.30],[-.03,.10,.03],[0,0,.14]);":"qkfPiece(playerRig.uaL,QKF.shL,t,[.52,.36,.44],[-.04,.12,.05],[0,0,.16]);",
"qkfPiece(playerRig.uaR,QKF.shR,t,[.34,.24,.30],[.03,.10,.03],[0,0,-.14]);":"qkfPiece(playerRig.uaR,QKF.shR,t,[.52,.36,.44],[.04,.12,.05],[0,0,-.16]);",
"qkfPiece(playerRig.hips,QKF.hip,m,[.56,.30,.30],[0,-.10,.05]);":"qkfPiece(playerRig.hips,QKF.hip,m,[.72,.42,.42],[0,-.08,.08]);",
"qkfPiece(playerRig.hips,QKF.pouch,t,[.18,.20,.12],[-.22,-.04,.10],[0,.20,0]);":"qkfPiece(playerRig.hips,QKF.pouch,t,[.22,.25,.15],[-.28,-.03,.14],[0,.20,0]);",
"qkfPiece(playerRig.hips,QKF.pouch,t,[.18,.20,.12],[.22,-.04,.10],[0,-.20,0]);":"qkfPiece(playerRig.hips,QKF.pouch,t,[.22,.25,.15],[.28,-.03,.14],[0,-.20,0]);",
"qkfPiece(playerRig.chest,QKA.eCloak,t,[.22,.62,.12],[-.20,.02,-.14],[0,.16,.16]);":"qkfPiece(playerRig.chest,QKA.eCloak,t,[.30,.78,.16],[-.26,.02,-.20],[0,.18,.18]);",
"qkfPiece(playerRig.chest,QKA.eCloak,t,[.22,.62,.12],[.20,.02,-.14],[0,-.16,-.16]);":"qkfPiece(playerRig.chest,QKA.eCloak,t,[.30,.78,.16],[.26,.02,-.20],[0,-.18,-.18]);",
"const opacity=lv>=15?.34:lv>=11?.24:.17;":"const opacity=lv>=15?.62:lv>=11?.48:.34;",
"const em=lv>=15?.95:lv>=11?.72:.50;":"const em=lv>=15?1.20:lv>=11?1.02:.88;",
"shell.position.copy(me.position);shell.quaternion.copy(me.quaternion);shell.scale.copy(me.scale).multiplyScalar(lv>=15?1.035:lv>=11?1.028:1.020);":"shell.position.copy(me.position);shell.quaternion.copy(me.quaternion);shell.scale.copy(me.scale).multiplyScalar(lv>=15?1.060:lv>=11?1.050:1.042);",
}

for old,new in repls.items():
    if old not in s:
        raise SystemExit('No se encontro patron para contraste del Elfo: '+old[:90])
    s=s.replace(old,new,1)

# Marcador y una placa frontal real usando la misma malla del Ranger. No cambia el rig.
# La placa se agrega solo si hay pechera equipada y queda por delante del cuerpo base.
js=r'''/* ELF_EQUIPMENT_VISIBILITY_V1 */
function qkElfChestAccent(){
  if(P.cls!=='elfa'||!P.eq||!P.eq.armadura||!playerRig||!playerRig.chest)return;
  const it=P.eq.armadura,t=armorTier(it),trim=elfMat(it,true),main=elfMat(it,false);
  const size=t>=4?[.76,.60,.37]:[.62+.035*t,.50+.03*t,.33+.018*t];
  const me=qkPiece(playerRig.chest,QKA.eChest,main,size,[0,.045,.18]);
  if(me&&lvOf(it)>=7){
    const shell=new THREE.Mesh(me.geometry,new THREE.MeshBasicMaterial({color:elfColors(it).trim,transparent:true,opacity:lvOf(it)>=15?.58:lvOf(it)>=11?.44:.32,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.FrontSide}));
    shell.position.copy(me.position);shell.quaternion.copy(me.quaternion);shell.scale.copy(me.scale).multiplyScalar(1.045);shell.renderOrder=4;me.parent.add(shell);
  }
}
'''
anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals para contraste Elfo')
s=s.replace(anchor,js+'\n'+anchor,1)
old='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();qkUpgradeSurfaceGlow();}'
new='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();qkElfChestAccent();qkUpgradeSurfaceGlow();}'
if old not in s:
    raise SystemExit('No se encontro qkArmorOnly final para contraste Elfo')
s=s.replace(old,new,1)

p.write_text(s)
print('Elfo: ropa base neutra, armaduras separadas del cuerpo y +9 visible sobre el pecho')
