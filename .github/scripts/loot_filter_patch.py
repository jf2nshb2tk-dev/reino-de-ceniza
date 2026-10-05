from pathlib import Path
p=Path('index.html')
s=p.read_text()

old="let autoPick=true;"
new="let autoPick=true,pickRarity=[true,true,true,true],sellRarity=[false,false,false,false];"
if old not in s: raise SystemExit('autoPick no encontrado')
s=s.replace(old,new,1)

old="""      +'<h3>Sonido</h3><div class=\"seg\"><button data-a=\"snd\" data-v=\"1\" class=\"'+(soundOn?'on':'')+'\">Activado</button><button data-a=\"snd\" data-v=\"0\" class=\"'+(!soundOn?'on':'')+'\">Silencio</button></div><h3>Objetos</h3><div class=\"seg\"><button data-a=\"ap\" data-v=\"1\" class=\"'+(autoPick?'on':'')+'\">Recoger solo</button><button data-a=\"ap\" data-v=\"0\" class=\"'+(!autoPick?'on':'')+'\">Recoger al tocar</button></div>'
"""
new="""      +'<h3>Sonido</h3><div class=\"seg\"><button data-a=\"snd\" data-v=\"1\" class=\"'+(soundOn?'on':'')+'\">Activado</button><button data-a=\"snd\" data-v=\"0\" class=\"'+(!soundOn?'on':'')+'\">Silencio</button></div><h3>Recoger objetos</h3><div class=\"seg\"><button data-a=\"ap\" data-v=\"1\" class=\"'+(autoPick?'on':'')+'\">Recoger solo</button><button data-a=\"ap\" data-v=\"0\" class=\"'+(!autoPick?'on':'')+'\">Recoger al tocar</button></div>'
      +'<p class=\"note\">Con Recoger solo activado, marca los colores de equipo que quieres levantar automáticamente. Oro, joyas y pociones se siguen recogiendo normalmente.</p>'
      +'<div class=\"seg\">'+RARITY.map((R,i)=>'<button data-a=\"apr\" data-v=\"'+i+'\" class=\"'+(pickRarity[i]?'on':'')+'\"><span style=\"color:'+R.c+'\">●</span> '+(pickRarity[i]?'✓ ':'')+R.n+'</button>').join('')+'</div>'
"""
if old not in s: raise SystemExit('bloque de ajustes Objetos no encontrado')
s=s.replace(old,new,1)

old="""    const cm=P.inv.filter(i=>!i.kind&&i.r===0);h+='<div class=\"btns\"><button class=\"btn alt\" data-a=\"sellcommon\">Vender comunes ('+cm.length+') por '+cm.reduce((a,b)=>a+price(b),0)+'</button></div></div>';
"""
new="""    const sellItems=P.inv.filter(i=>!i.kind&&sellRarity[i.r]),sellGold=sellItems.reduce((a,b)=>a+price(b),0);
    h+='<h3 style=\"margin-top:12px\">Vender por color</h3><p class=\"note\">Marca uno o varios colores y vende todo ese equipo de la mochila de una sola vez.</p>'
      +'<div class=\"seg\">'+RARITY.map((R,i)=>'<button data-a=\"sellr\" data-v=\"'+i+'\" class=\"'+(sellRarity[i]?'on':'')+'\"><span style=\"color:'+R.c+'\">●</span> '+(sellRarity[i]?'✓ ':'')+R.n+'</button>').join('')+'</div>'
      +'<div class=\"btns\"><button class=\"btn alt\" data-a=\"sellrar\"'+(sellItems.length?'':' disabled')+'>Vender seleccionados ('+sellItems.length+') por '+sellGold+'</button></div></div>';
"""
if old not in s: raise SystemExit('venta de comunes no encontrada')
s=s.replace(old,new,1)

old="""  if(a==='sellcommon'){let g=0;P.inv=P.inv.filter(i=>{if(!i.kind&&i.r===0){g+=price(i);return false;}return true;});P.gold+=g;sel=null;renderPanel();return;}
  if(a==='q'){qUser=true;applyQuality(+v);saveGame();renderPanel();return;}
  if(a==='ap'){autoPick=v==='1';renderPanel();return;}
"""
new="""  if(a==='sellcommon'){let g=0;P.inv=P.inv.filter(i=>{if(!i.kind&&i.r===0){g+=price(i);return false;}return true;});P.gold+=g;sel=null;saveGame();renderPanel();return;}
  if(a==='sellr'){const r=+v;if(r>=0&&r<RARITY.length){sellRarity[r]=!sellRarity[r];saveGame();renderPanel();}return;}
  if(a==='sellrar'){
    let g=0,n=0;P.inv=P.inv.filter(i=>{if(!i.kind&&sellRarity[i.r]){g+=price(i);n++;return false;}return true;});
    if(!n){toast('No hay objetos de los colores seleccionados','#d9b36a');renderPanel();return;}
    P.gold+=g;sel=null;sfx('loot');float('+'+g+' oro',P.x,P.y+2.9,P.z,'gold');toast('Vendiste '+n+' objeto'+(n===1?'':'s')+' por '+g+' de oro','#f0d08a');saveGame();renderPanel();return;
  }
  if(a==='q'){qUser=true;applyQuality(+v);saveGame();renderPanel();return;}
  if(a==='apr'){const r=+v;if(r>=0&&r<RARITY.length){pickRarity[r]=!pickRarity[r];saveGame();renderPanel();}return;}
  if(a==='ap'){autoPick=v==='1';saveGame();renderPanel();return;}
"""
if old not in s: raise SystemExit('handlers sellcommon/ap no encontrados')
s=s.replace(old,new,1)

old="function applySettings(){autoPick=DB.st.ap!==false;soundOn=DB.st.sn!==false;if(DB.st.qu&&typeof DB.st.q==='number'){qUser=true;applyQuality(DB.st.q);}}"
new="function applySettings(){autoPick=DB.st.ap!==false;soundOn=DB.st.sn!==false;if(Array.isArray(DB.st.pr))pickRarity=RARITY.map((_,i)=>DB.st.pr[i]!==false);if(Array.isArray(DB.st.sr))sellRarity=RARITY.map((_,i)=>!!DB.st.sr[i]);if(DB.st.qu&&typeof DB.st.q==='number'){qUser=true;applyQuality(DB.st.q);}}"
if old not in s: raise SystemExit('applySettings no encontrado')
s=s.replace(old,new,1)
old="DB.active=P.id;DB.st={q:Q,ap:autoPick,qu:qUser,sn:soundOn};dbSave();"
new="DB.active=P.id;DB.st={q:Q,ap:autoPick,pr:pickRarity.slice(),sr:sellRarity.slice(),qu:qUser,sn:soundOn};dbSave();"
if old not in s: raise SystemExit('DB.st save no encontrado')
s=s.replace(old,new,1)

old="""    if(playing&&autoPick&&Math.hypot(d.x-P.x,d.z-P.z)<2.5){if(pickup(d))drops.splice(i,1);}
    else if(playing&&!autoPick&&P.dest&&Math.hypot(d.x-P.dest.x,d.z-P.dest.z)<2&&Math.hypot(d.x-P.x,d.z-P.z)<2){if(pickup(d)){drops.splice(i,1);}}}
"""
new="""    const autoThis=autoPick&&(d.kind!=='item'||pickRarity[d.item.r]!==false);
    if(playing&&autoThis&&Math.hypot(d.x-P.x,d.z-P.z)<2.5){if(pickup(d))drops.splice(i,1);}
    else if(playing&&P.dest&&Math.hypot(d.x-P.dest.x,d.z-P.dest.z)<2&&Math.hypot(d.x-P.x,d.z-P.z)<2){if(pickup(d)){drops.splice(i,1);}}}
"""
if old not in s: raise SystemExit('loop de pickup no encontrado')
s=s.replace(old,new,1)

p.write_text(s)
print('Filtros de recogida y venta por color aplicados')
