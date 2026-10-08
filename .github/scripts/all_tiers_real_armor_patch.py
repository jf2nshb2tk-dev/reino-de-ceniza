from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='ALL_TIERS_REAL_ARMOR_V1'
if marker in s:
    print('T1-T4 reales ya aplicados')
    raise SystemExit(0)

# Este parche reutiliza las geometrías Quaternius ya embebidas por los parches anteriores.
# No cambia personaje, rig ni animaciones: solo reemplaza torso/guantes/botas procedurales T1-T4.
js=r'''/* ALL_TIERS_REAL_ARMOR_V1 - T1/T2/T3/T4 con geometria Quaternius real */
const QLOW_SCALE=[.72,.82,.92,1.03];
function qlow(it){return !!(it&&armorTier(it)<4);}
function qlv(it){return Math.max(0,Math.min(3,armorTier(it)));}
function qscale(v,t){return v.map(x=>+(x*QLOW_SCALE[t]).toFixed(4));}
function qmatFor(cls,it,trim){
  if(cls==='guerrero')return warriorMat(it,trim);
  if(cls==='mago')return mageMat(it,trim);
  if(cls==='elfa')return elfMat(it,trim);
  return restMat(it,cls,trim);
}
function qkeyFor(cls){return cls==='guerrero'?'w':cls==='mago'?'m':cls==='barbaro'?'b':cls==='asesino'?'a':cls==='brujo'?'r':null;}
function qcfgFor(cls){
  if(cls==='guerrero')return{c:[.66,.50,.33],h:[.54,.30,.30],s:[.32,.22,.30],a:[.19,.32,.20],l:[.21,.35,.22],f:[.22,.15,.31]};
  if(cls==='mago')return{c:[.56,.46,.28],h:[.48,.29,.27],s:[.26,.18,.25],a:[.17,.29,.18],l:[.19,.33,.20],f:[.19,.14,.29]};
  if(cls==='barbaro')return{c:[.68,.51,.34],h:[.58,.32,.32],s:[.36,.24,.33],a:[.21,.34,.22],l:[.23,.37,.24],f:[.24,.16,.33]};
  if(cls==='asesino')return{c:[.52,.44,.27],h:[.44,.27,.25],s:[.23,.17,.23],a:[.16,.28,.17],l:[.18,.32,.18],f:[.18,.13,.27]};
  return{c:[.58,.47,.30],h:[.50,.30,.28],s:[.28,.20,.27],a:[.17,.29,.18],l:[.19,.33,.20],f:[.19,.14,.29]};
}
function qlowerCore(cls){
  if(P.cls!==cls)return;
  const k=qkeyFor(cls),cfg=qcfgFor(cls),arm=P.eq.armadura,gl=P.eq.guantes,bo=P.eq.botas;
  if(!k)return;
  if(qlow(arm)){
    const t=qlv(arm),m=qmatFor(cls,arm,false),a=qmatFor(cls,arm,true);
    qr(playerRig.chest,QKR[k+'C'],m,qscale(cfg.c,t),[0,.02,.10]);
    if(t>=1)qr(playerRig.hips,QKR[k+'H'],m,qscale(cfg.h,t),[0,-.10,.05]);
    if(t>=2){
      qr(playerRig.uaL,QKR[k+'SL'],a,qscale(cfg.s,t),[-.025,.09,.02],[0,0,.11+.02*t]);
      qr(playerRig.uaR,QKR[k+'SR'],a,qscale(cfg.s,t),[.025,.09,.02],[0,0,-(.11+.02*t)]);
    }
    if(t===3){
      const g=qkGroup(playerRig.chest);
      const deco=qmatFor(cls,arm,true);
      avPart(g,UOct,deco,.075,.075,.045,0,.04,.25);
    }
  }
  if(qlow(gl)){
    const t=qlv(gl),m=qmatFor(cls,gl,t>=2);
    qr(playerRig.laL,QKR[k+'AL'],m,qscale(cfg.a,t),[0,.08,.02]);
    qr(playerRig.laR,QKR[k+'AR'],m,qscale(cfg.a,t),[0,.08,.02]);
  }
  if(qlow(bo)){
    const t=qlv(bo),m=qmatFor(cls,bo,false),a=qmatFor(cls,bo,t>=2);
    qr(playerRig.llL,QKR[k+'LL'],m,qscale(cfg.l,t),[0,.10,.01]);
    qr(playerRig.llR,QKR[k+'LR'],m,qscale(cfg.l,t),[0,.10,.01]);
    qr(playerRig.footL,QKR[k+'FL'],a,qscale(cfg.f,t),[0,.03,.08]);
    qr(playerRig.footR,QKR[k+'FR'],a,qscale(cfg.f,t),[0,.03,.08]);
  }
}
function qlowerElf(){
  if(P.cls!=='elfa')return;
  const arm=P.eq.armadura,gl=P.eq.guantes,bo=P.eq.botas;
  if(qlow(arm)){
    const t=qlv(arm),m=elfMat(arm,false),a=elfMat(arm,true);
    qkPiece(playerRig.chest,QKA.eChest,m,qscale([.56,.46,.29],t),[0,.02,.10]);
    if(t>=1)qkPiece(playerRig.chest,QKA.eCloak,t>=2?a:m,qscale([.46,.58,.13],t),[0,.01,-.10]);
    if(t>=2){
      qkfPiece(playerRig.uaL,QKF.shL,a,qscale([.27,.19,.26],t),[-.02,.09,.02],[0,0,.12]);
      qkfPiece(playerRig.uaR,QKF.shR,a,qscale([.27,.19,.26],t),[.02,.09,.02],[0,0,-.12]);
    }
    if(t===3)qkfPiece(playerRig.hips,QKF.hip,m,[.50,.27,.27],[0,-.09,.05]);
  }
  if(qlow(gl)){
    const t=qlv(gl),m=elfMat(gl,t>=2);
    qkPiece(playerRig.laL,QKA.eArmL,m,qscale([.16,.29,.17],t),[0,.08,.02]);
    qkPiece(playerRig.laR,QKA.eArmR,m,qscale([.16,.29,.17],t),[0,.08,.02]);
  }
  if(qlow(bo)){
    const t=qlv(bo),m=elfMat(bo,false),a=elfMat(bo,t>=2);
    qkPiece(playerRig.llL,QKA.eLegL,m,qscale([.18,.33,.19],t),[0,.10,.01]);
    qkPiece(playerRig.llR,QKA.eLegR,m,qscale([.18,.33,.19],t),[0,.10,.01]);
    qkPiece(playerRig.footL,QKA.eFootL,a,qscale([.19,.14,.29],t),[0,.03,.08]);
    qkPiece(playerRig.footR,QKA.eFootR,a,qscale([.19,.14,.29],t),[0,.03,.08]);
  }
}
function qkLowerTiers(){
  qlowerCore('guerrero');qlowerCore('mago');qlowerElf();
  qlowerCore('barbaro');qlowerCore('asesino');qlowerCore('brujo');
}
'''

anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals')
s=s.replace(anchor,js+'\n'+anchor,1)

old='function qkArmorOnly(){qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();}'
new='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();}'
if old not in s:
    raise SystemExit('No se encontro qkArmorOnly final')
s=s.replace(old,new,1)

# Mantener casco por clase (varios ya usan malla nativa que calza bien),
# pero quitar cuerpo/guantes/botas procedurales para que T1-T4 sean las mallas reales.
repls={
"if(!qkIsT5(P.eq.armadura))warriorTorso(P.eq.armadura);":"",
"if(!qkIsT5(P.eq.guantes))warriorGloves(P.eq.guantes);":"",
"if(!qkIsT5(P.eq.botas))warriorBoots(P.eq.botas);":"",
"if(!qkIsT5(P.eq.armadura))mageTorso(P.eq.armadura);":"",
"if(!qkIsT5(P.eq.guantes))mageGloves(P.eq.guantes);":"",
"if(!qkIsT5(P.eq.botas))mageBoots(P.eq.botas);":"",
"if(!qkIsT5(P.eq.armadura))elfTorso(P.eq.armadura);":"",
"if(!qkIsT5(P.eq.guantes))elfGloves(P.eq.guantes);":"",
"if(!qkIsT5(P.eq.botas))elfBoots(P.eq.botas);":"",
"if(!qkIsT5(P.eq.armadura))restTorso(P.eq.armadura,P.cls);":"",
"if(!qkIsT5(P.eq.guantes))restGloves(P.eq.guantes,P.cls);":"",
"if(!qkIsT5(P.eq.botas))restBoots(P.eq.botas,P.cls);":"",
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit('No se encontro llamada procedural: '+a)
    s=s.replace(a,b,1)

p.write_text(s)
print('T1-T4 de las 6 clases reemplazados por geometria Quaternius real')
