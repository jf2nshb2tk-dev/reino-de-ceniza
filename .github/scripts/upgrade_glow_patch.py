from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='UPGRADE_GLOW_V2'
if marker in s:
    print('Brillo por mejora V2 ya aplicado')
    raise SystemExit(0)

# Refuerzo base de emissive. La V2 deja de usar una esfera/halo externo y hace brillar
# la propia superficie de cada pieza equipada.
repls={
"lv>=15?.60:lv>=11?.34:lv>=7?.15:0":"lv>=15?1.00:lv>=11?.78:lv>=7?.48:0",
"lv>=15?.55:lv>=11?.30:lv>=7?.12:0":"lv>=15?1.00:lv>=11?.76:lv>=7?.46:0",
"lv>=15?.38:lv>=11?.20:lv>=7?.08:0":"lv>=15?.98:lv>=11?.72:lv>=7?.44:0",
"lv>=15?.45:lv>=11?.24:lv>=7?.09:0":"lv>=15?.98:lv>=11?.74:lv>=7?.45:0",
"Math.min(.10,em)":"Math.min(.90,em)",
"Math.min(.12,e)":"Math.min(.90,e)",
}
for a,b in repls.items():
    if a in s:
        s=s.replace(a,b)

s=s.replace("lv>=15?.48:lv>=11?.26:lv>=7?.10:0","lv>=15?.98:lv>=11?.72:lv>=7?.44:0")
s=s.replace("lv>=15?.25:lv>=11?.14:lv>=7?.05:0","lv>=15?.95:lv>=11?.68:lv>=7?.42:0")

js=r'''/* UPGRADE_GLOW_V2 - brillo aplicado directamente sobre las piezas equipadas */
function qkUpgradeColor(it){
  if(P.cls==='guerrero')return warriorColors(it).trim.clone();
  if(P.cls==='mago')return mageColors(it).trim.clone();
  if(P.cls==='elfa')return elfColors(it).trim.clone();
  if(['barbaro','asesino','brujo'].includes(P.cls))return restColors(it,P.cls).trim.clone();
  return new THREE.Color(0xffcc66);
}
function qkGlowItemForGroup(g){
  const p=g&&g.parent;if(!p||!P.eq)return null;
  if(p===playerRig.head)return P.eq.casco||null;
  if(p===playerRig.chest||p===playerRig.hips||p===playerRig.uaL||p===playerRig.uaR)return P.eq.armadura||null;
  if(p===playerRig.laL||p===playerRig.laR||p===playerRig.handL||p===playerRig.handR)return P.eq.guantes||null;
  if(p===playerRig.llL||p===playerRig.llR||p===playerRig.footL||p===playerRig.footR)return P.eq.botas||null;
  return null;
}
function qkUpgradeSurfaceGlow(){
  if(!playerRig||!playerRig.armorVisuals)return;
  const groups=[...playerRig.armorVisuals];
  for(const g of groups){
    const it=qkGlowItemForGroup(g);if(!it)continue;
    const lv=lvOf(it);if(lv<7)continue;
    const col=qkUpgradeColor(it);
    const opacity=lv>=15?.34:lv>=11?.24:.17;
    const em=lv>=15?.95:lv>=11?.72:.50;
    const meshes=[];
    g.traverse(o=>{if(o&&o.isMesh)meshes.push(o);});
    for(const me of meshes){
      const mats=Array.isArray(me.material)?me.material:[me.material];
      mats.forEach(mt=>{
        if(mt&&mt.emissive){mt.emissive.copy(col).multiplyScalar(em);mt.needsUpdate=true;}
      });
      if(!me.geometry)continue;
      const shell=new THREE.Mesh(me.geometry,new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:opacity,blending:THREE.AdditiveBlending,depthWrite:false,depthTest:true,side:THREE.FrontSide}));
      shell.position.copy(me.position);shell.quaternion.copy(me.quaternion);shell.scale.copy(me.scale).multiplyScalar(lv>=15?1.035:lv>=11?1.028:1.020);
      shell.renderOrder=(me.renderOrder||0)+1;
      me.parent.add(shell);
    }
  }
}
'''
anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals para brillo V2')
s=s.replace(anchor,js+'\n'+anchor,1)

old='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();}'
new='function qkArmorOnly(){qkLowerTiers();qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();qkUpgradeSurfaceGlow();}'
if old not in s:
    raise SystemExit('No se encontro qkArmorOnly para brillo V2')
s=s.replace(old,new,1)

# Inventario: indicar visualmente desde +7.
s=s.replace("const glow=lvOf(it)>=15?' style=\"filter:drop-shadow(0 0 4px '+stroke+')\"':'';",
            "const _ul=lvOf(it),glow=_ul>=7?' style=\"filter:drop-shadow(0 0 '+(_ul>=15?6:_ul>=11?4:2)+'px '+stroke+')\"':'';")

p.write_text(s)
print('Brillo +7/+11/+15 aplicado sobre la superficie de casco/pecho/guantes/botas; halo externo eliminado')
