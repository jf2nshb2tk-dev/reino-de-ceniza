from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='WARRIOR_BASE_SKIN_V2'
if marker in s:
    print('Base visual del Guerrero ya aplicada')
    raise SystemExit(0)

# Hacer un poco más grandes las piezas procedurales para que queden por encima del traje base.
old="function wg(parent){if(!parent)return null;const g=new THREE.Group();parent.add(g);playerRig.armorVisuals.push(g);return g;}"
new="function wg(parent){if(!parent)return null;const g=new THREE.Group();g.scale.setScalar(1.18);parent.add(g);playerRig.armorVisuals.push(g);return g;}"
if old not in s:
    raise SystemExit('No se encontro helper wg del Guerrero')
s=s.replace(old,new,1)

anchor='function gearVisuals(){'
if anchor not in s:
    raise SystemExit('No se encontro gearVisuals')

helpers=r'''/* WARRIOR_BASE_SKIN_V2 - el Knight queda como cuerpo base neutro */
function warriorBaseMesh(name){return (playerMeshes||[]).find(m=>m&&m.name===name)||null;}
function warriorBasePaint(name,color){
  const m=warriorBaseMesh(name);if(!m||!m.material)return;
  m.visible=true;
  const mats=Array.isArray(m.material)?m.material:[m.material];
  mats.forEach(mt=>{if(!mt.userData)mt.userData={};if(!mt.userData.wbSaved){mt.userData.wbSaved=true;mt.userData.wbMap=mt.map||null;mt.userData.wbColor=mt.color?mt.color.clone():null;}
    mt.map=null;if(mt.color)mt.color.setHex(color);if(mt.emissive)mt.emissive.setHex(0);mt.metalness=0;mt.roughness=.95;mt.needsUpdate=true;});
}
function warriorBaseHide(name){const m=warriorBaseMesh(name);if(m)m.visible=false;}
function warriorBaseSkin(){
  if(P.cls!=='guerrero')return;
  // El casco y la capa originales tapaban casi por completo las nuevas piezas.
  warriorBaseHide('Knight_Helmet');
  warriorBaseHide('Knight_HelmetVisor');
  warriorBaseHide('Knight_Cape');
  // Conservamos cabeza/cuerpo animado, pero convertido en una ropa interior neutra.
  const torso=P.eq.armadura?0x25292e:0x554239;
  const arms=P.eq.guantes?0x24282d:0x4c3b34;
  const legs=P.eq.botas?0x23272c:0x403630;
  warriorBasePaint('Knight_Body',torso);
  warriorBasePaint('Knight_ArmLeft',arms);
  warriorBasePaint('Knight_ArmRight',arms);
  warriorBasePaint('Knight_LegLeft',legs);
  warriorBasePaint('Knight_LegRight',legs);
  const h=warriorBaseMesh('Knight_Head');if(h)h.visible=true;
}
'''
s=s.replace(anchor,helpers+'\n'+anchor,1)

old="clearArmorVisuals();if(P.cls==='guerrero')attachWarriorSet();else{"
new="clearArmorVisuals();if(P.cls==='guerrero'){warriorBaseSkin();attachWarriorSet();}else{"
if old not in s:
    raise SystemExit('No se encontro rama Guerrero en gearVisuals')
s=s.replace(old,new,1)

p.write_text(s)
print('Traje base del Guerrero neutralizado; armaduras visibles por encima')
