from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='QUATERNIUS_T5_REPLACE_V1'
if marker in s:
    print('Reemplazo T5 Quaternius ya aplicado')
    raise SystemExit(0)

old="""if(P.cls==='guerrero'){warriorBaseSkin();attachWarriorSet();}else if(P.cls==='mago'){mageBaseSkin();attachMageSet();}else if(P.cls==='elfa'){elfBaseSkin();attachElfSet();}else if(['barbaro','asesino','brujo'].includes(P.cls)){restBase(P.cls);attachRestSet(P.cls);}else{attachArmorVisual(P.eq.casco,'casco',playerRig.head,1);attachArmorVisual(P.eq.armadura,'armadura',playerRig.chest,1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handL,-1);attachArmorVisual(P.eq.guantes,'guantes',playerRig.handR,1);attachArmorVisual(P.eq.botas,'botas',playerRig.footL,-1);attachArmorVisual(P.eq.botas,'botas',playerRig.footR,1);}qkArmorOnly();return;}"""
new="""if(P.cls==='guerrero'){
    warriorBaseSkin();
    // El casco original del Knight se conserva porque ya quedo bien; el resto T5 usa geometria Quaternius real.
    warriorHelmet(P.eq.casco);
    if(!qkIsT5(P.eq.armadura))warriorTorso(P.eq.armadura);
    if(!qkIsT5(P.eq.guantes))warriorGloves(P.eq.guantes);
    if(!qkIsT5(P.eq.botas))warriorBoots(P.eq.botas);
  }else if(P.cls==='mago'){
    mageBaseSkin();
    mageHelmet(P.eq.casco);
    if(!qkIsT5(P.eq.armadura))mageTorso(P.eq.armadura);
    if(!qkIsT5(P.eq.guantes))mageGloves(P.eq.guantes);
    if(!qkIsT5(P.eq.botas))mageBoots(P.eq.botas);
  }else if(P.cls==='elfa'){
    elfBaseSkin();
    elfHelmet(P.eq.casco);
    if(!qkIsT5(P.eq.armadura))elfTorso(P.eq.armadura);
    if(!qkIsT5(P.eq.guantes))elfGloves(P.eq.guantes);
    if(!qkIsT5(P.eq.botas))elfBoots(P.eq.botas);
  }else if(['barbaro','asesino','brujo'].includes(P.cls)){
    restBase(P.cls);attachRestSet(P.cls);
  }else{
    attachArmorVisual(P.eq.casco,'casco',playerRig.head,1);
    attachArmorVisual(P.eq.armadura,'armadura',playerRig.chest,1);
    attachArmorVisual(P.eq.guantes,'guantes',playerRig.handL,-1);
    attachArmorVisual(P.eq.guantes,'guantes',playerRig.handR,1);
    attachArmorVisual(P.eq.botas,'botas',playerRig.footL,-1);
    attachArmorVisual(P.eq.botas,'botas',playerRig.footR,1);
  }
  qkArmorOnly();return;}"""
if old not in s:
    raise SystemExit('No se encontro la rama de armaduras GLB esperada')
s=s.replace(old,new,1)

# Hacer que la silueta real Quaternius del Elfo T5 se lea claramente en la camara del juego.
repls={
"qkPiece(playerRig.chest,QKA.eChest,m,[.52,.43,.26],[0,.02,.09])":"qkPiece(playerRig.chest,QKA.eChest,m,[.62,.50,.33],[0,.02,.12])",
"qkPiece(playerRig.chest,QKA.eCloak,t,[.46,.55,.12],[0,.02,-.09])":"qkPiece(playerRig.chest,QKA.eCloak,t,[.54,.70,.16],[0,.00,-.12])",
"qkPiece(playerRig.laL,QKA.eArmL,m,[.15,.27,.16],[0,.09,.02])":"qkPiece(playerRig.laL,QKA.eArmL,m,[.18,.32,.19],[0,.08,.03])",
"qkPiece(playerRig.laR,QKA.eArmR,m,[.15,.27,.16],[0,.09,.02])":"qkPiece(playerRig.laR,QKA.eArmR,m,[.18,.32,.19],[0,.08,.03])",
"qkPiece(playerRig.llL,QKA.eLegL,m,[.17,.31,.18],[0,.10,.01])":"qkPiece(playerRig.llL,QKA.eLegL,m,[.20,.36,.21],[0,.10,.02])",
"qkPiece(playerRig.llR,QKA.eLegR,m,[.17,.31,.18],[0,.10,.01])":"qkPiece(playerRig.llR,QKA.eLegR,m,[.20,.36,.21],[0,.10,.02])",
"qkPiece(playerRig.footL,QKA.eFootL,t,[.18,.13,.27],[0,.03,.07])":"qkPiece(playerRig.footL,QKA.eFootL,t,[.21,.15,.31],[0,.03,.09])",
"qkPiece(playerRig.footR,QKA.eFootR,t,[.18,.13,.27],[0,.03,.07])":"qkPiece(playerRig.footR,QKA.eFootR,t,[.21,.15,.31],[0,.03,.09])",
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit('No se encontro pieza Quaternius esperada: '+a[:70])
    s=s.replace(a,b,1)

# Marcador dentro del HTML para hacer el parche idempotente.
s=s.replace('/* QUATERNIUS_ARMOR_ONLY_V3 - solo armaduras reales, personaje/animaciones originales */',
            '/* QUATERNIUS_ARMOR_ONLY_V3 - solo armaduras reales, personaje/animaciones originales */\n/* QUATERNIUS_T5_REPLACE_V1 - T5 reemplaza lo procedural por geometria real */',1)

p.write_text(s)
print('T5 Quaternius reemplaza la armadura procedural; Elfo reforzado visualmente')
