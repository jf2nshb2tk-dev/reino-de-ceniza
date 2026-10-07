from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='WARRIOR_HELMET_FIX_V3'
if marker in s:
    print('Casco del Guerrero ya corregido')
    raise SystemExit(0)

start=s.find('function warriorHelmet(it){')
end=s.find('function warriorTorso(it){', start)
if start<0 or end<0:
    raise SystemExit('No se encontro warriorHelmet/warriorTorso para corregir casco')

new=r'''/* WARRIOR_HELMET_FIX_V3 - el hueso head nace en la base del cuello; subimos el casco a la cabeza real */
function warriorHelmet(it){
  const p=playerRig.head;if(!it||!p)return;
  const t=warriorTier(it),g=wg(p),m=warriorMat(it,false),a=warriorMat(it,true);
  // La cabeza del Knight ocupa aprox. y=0..1 desde el hueso head. El casco anterior quedaba en y~0.07 (cuello).
  wp(g,USph,m,.48,.34,.48,0,.70,.02);
  wp(g,UB,a,.40,.075,.49,0,.55,.18);
  wp(g,UB,m,.075,.27,.42,-.42,.46,.03,0,0,.08);
  wp(g,UB,m,.075,.27,.42,.42,.46,.03,0,0,-.08);
  if(t===0){
    wp(g,UB,a,.24,.055,.46,0,.78,.08);
  }else if(t===1){
    wp(g,UCone,a,.055,.20,.055,0,1.02,.00);
    wp(g,UB,a,.29,.06,.47,0,.80,.08);
  }else if(t===2){
    wp(g,UCone,a,.07,.25,.07,-.36,.93,-.01,0,0,.38);
    wp(g,UCone,a,.07,.25,.07,.36,.93,-.01,0,0,-.38);
    wp(g,UB,a,.055,.27,.48,0,.82,.10);
  }else if(t===3){
    wp(g,UCone,a,.075,.28,.075,-.37,.96,-.01,0,0,.34);
    wp(g,UCone,a,.075,.28,.075,.37,.96,-.01,0,0,-.34);
    wp(g,UB,a,.065,.29,.49,0,.83,.11);
    wp(g,UOct,a,.085,.085,.055,0,.54,.50);
  }else{
    wp(g,UCone,a,.085,.34,.085,-.39,.98,-.02,0,0,.30);
    wp(g,UCone,a,.085,.34,.085,.39,.98,-.02,0,0,-.30);
    wp(g,UCone,a,.07,.34,.07,0,1.08,-.02);
    wp(g,UB,a,.07,.31,.50,0,.84,.12);
    wp(g,UOct,a,.10,.10,.06,0,.54,.51);
    wp(g,UB,a,.30,.055,.50,0,.40,.27);
  }
}
'''

s=s[:start]+new+s[end:]
p.write_text(s)
print('Casco del Guerrero reposicionado sobre la cabeza real')
