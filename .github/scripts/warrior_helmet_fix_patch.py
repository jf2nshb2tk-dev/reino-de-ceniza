from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='WARRIOR_HELMET_FIX_V4'
if marker in s:
    print('Casco del Guerrero V4 ya corregido')
    raise SystemExit(0)

start=s.find('function warriorHelmet(it){')
end=s.find('function warriorTorso(it){', start)
if start<0 or end<0:
    raise SystemExit('No se encontro warriorHelmet/warriorTorso para corregir casco')

new=r'''/* WARRIOR_HELMET_FIX_V4 - reutiliza el casco del Knight, que ya calza exactamente en la cabeza */
function warriorHelmet(it){
  if(!it)return;
  const t=warriorTier(it),cols=warriorColors(it);
  const helmet=warriorBaseMesh('Knight_Helmet');
  const visor=warriorBaseMesh('Knight_HelmetVisor');
  const paint=(mesh,col,em)=>{
    if(!mesh)return;
    mesh.visible=true;
    const mats=Array.isArray(mesh.material)?mesh.material:[mesh.material];
    mats.forEach(mt=>{
      if(mt.color)mt.color.copy(col);
      if(mt.emissive)mt.emissive.copy(col).multiplyScalar(em||0);
      if('metalness' in mt)mt.metalness=.18+.10*t;
      if('roughness' in mt)mt.roughness=.72-.08*t;
      mt.needsUpdate=true;
    });
  };
  const lv=lvOf(it),glow=lv>=15?.26:lv>=11?.14:lv>=7?.06:0;
  paint(helmet,cols.main,glow);
  paint(visor,cols.trim,glow*1.25);
  // Solo los tiers altos agregan un detalle pequeño; sin barras laterales ni franja en la frente.
  if(t>=3&&playerRig.head){
    const g=wg(playerRig.head),a=warriorMat(it,true);
    g.scale.setScalar(.95);
    if(t===3)wp(g,UCone,a,.045,.16,.045,0,1.00,-.03);
    if(t===4){
      wp(g,UCone,a,.05,.20,.05,-.18,.99,-.03,0,0,.18);
      wp(g,UCone,a,.05,.20,.05,.18,.99,-.03,0,0,-.18);
    }
  }
}
'''

s=s[:start]+new+s[end:]
p.write_text(s)
print('Casco del Guerrero reemplazado por el casco Knight bien ajustado')
