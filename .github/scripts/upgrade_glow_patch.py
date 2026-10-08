from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='UPGRADE_GLOW_V1'
if marker in s:
    print('Brillo por mejora ya aplicado')
    raise SystemExit(0)

# Reforzar el emissive de las armaduras reales. +7/+10 debe notarse incluso con la cámara móvil.
repls={
"lv>=15?.60:lv>=11?.34:lv>=7?.15:0":"lv>=15?1.00:lv>=11?.70:lv>=7?.38:0",
"lv>=15?.55:lv>=11?.30:lv>=7?.12:0":"lv>=15?1.00:lv>=11?.68:lv>=7?.36:0",
"lv>=15?.38:lv>=11?.20:lv>=7?.08:0":"lv>=15?.95:lv>=11?.64:lv>=7?.34:0",
"lv>=15?.45:lv>=11?.24:lv>=7?.09:0":"lv>=15?.98:lv>=11?.66:lv>=7?.35:0",
"Math.min(.10,em)":"Math.min(.85,em)",
"Math.min(.12,e)":"Math.min(.85,e)",
}
for a,b in repls.items():
    if a in s:
        s=s.replace(a,b)

# También reforzar cascos/mallas base que usan sus propios valores de emissive.
s=s.replace("lv>=15?.48:lv>=11?.26:lv>=7?.10:0","lv>=15?.95:lv>=11?.62:lv>=7?.34:0")
s=s.replace("lv>=15?.25:lv>=11?.14:lv>=7?.05:0","lv>=15?.90:lv>=11?.58:lv>=7?.32:0")

js=r'''/* UPGRADE_GLOW_V1 - brillo MU visible para +7, +11 y +15 */
function qkUpgradeColor(it){
  if(P.cls==='guerrero')return warriorColors(it).trim.clone();
  if(P.cls==='mago')return mageColors(it).trim.clone();
  if(P.cls==='elfa')return elfColors(it).trim.clone();
  if(['barbaro','asesino','brujo'].includes(P.cls))return restColors(it,P.cls).trim.clone();
  return new THREE.Color(0xffcc66);
}
function qkUpgradeAura(){
  if(!playerRig)return;
  const items=[P.eq&&P.eq.casco,P.eq&&P.eq.armadura,P.eq&&P.eq.guantes,P.eq&&P.eq.botas].filter(Boolean);
  if(!items.length)return;
  let best=items[0],lv=lvOf(best);
  for(const it of items){const n=lvOf(it);if(n>lv){lv=n;best=it;}}
  if(lv<7)return;
  const col=qkUpgradeColor(best),parent=playerRig.chest||playerRig.hips||playerRig.head;
  if(!parent)return;
  const g=qkGroup(parent);if(!g)return;
  const intensity=lv>=15?1.30:lv>=11?.95:.62;
  const distance=lv>=15?3.0:lv>=11?2.7:2.35;
  const light=new THREE.PointLight(col.getHex(),intensity,distance,2);
  light.position.set(0,.10,.18);g.add(light);
  // Halo muy liviano, sin partículas: ayuda a que +7/+10 se lea en iPhone.
  const hm=new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:lv>=15?.105:lv>=11?.075:.05,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.BackSide});
  const halo=new THREE.Mesh(USph,hm);halo.scale.set(lv>=15?.72:.62,lv>=15?.88:.76,lv>=15?.58:.50);halo.position.set(0,.05,.02);g.add(halo);
}
'''
anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals para brillo')
s=s.replace(anchor,js+'\n'+anchor,1)

old='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();}'
new='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();qkUpgradeAura();}'
if old not in s:
    raise SystemExit('No se encontro qkArmorOnly para agregar aura')
s=s.replace(old,new,1)

# En inventario, desde +7 también se marca la mejora (antes solo +15).
s=s.replace("const glow=lvOf(it)>=15?' style=\"filter:drop-shadow(0 0 4px '+stroke+')\"':'';",
            "const _ul=lvOf(it),glow=_ul>=7?' style=\"filter:drop-shadow(0 0 '+(_ul>=15?6:_ul>=11?4:2)+'px '+stroke+')\"':'';")

p.write_text(s)
print('Brillo +7/+11/+15 reforzado en armaduras y aura equipada')
