from pathlib import Path

p=Path('index.html')
s=p.read_text()

marker='MU_DETAIL_ACTION_FIX_V1'
if marker not in s:
    css=r'''
/* MU_DETAIL_ACTION_FIX_V1 */
@media (min-width:640px){
  .sheet.compactInv .detail{
    max-height:calc(100vh - 82px);
    overflow:auto;
    overscroll-behavior:contain;
  }
  .sheet.compactInv .detail .setbox{
    margin:4px 0 3px;
    padding:4px 5px;
    border-radius:3px;
  }
  .sheet.compactInv .detail .setbox .st{
    font-size:11px;
    line-height:1.1;
    margin-bottom:1px;
  }
  .sheet.compactInv .detail .setbox .pc{
    font-size:9px;
    line-height:1.1;
    margin-bottom:2px;
  }
  .sheet.compactInv .detail .setbox .bn{
    font-size:9px;
    line-height:1.08;
    margin:1px 0;
  }
  .sheet.compactInv .detail .primaryActions{
    margin:4px 0 5px;
    padding-bottom:4px;
    border-bottom:1px solid #3b2d29;
  }
  .sheet.compactInv .detail .primaryActions .btn{
    padding:5px 8px;
    font-size:11px;
  }
}
@media (min-width:640px) and (max-height:430px){
  .sheet.compactInv .detail{max-height:calc(100vh - 70px)}
}
'''
    if '</style>' not in s:
        raise SystemExit('No se encontro </style>')
    s=s.replace('</style>',css+'\n</style>',1)

start=s.find('function detailHTML(){')
end=s.find('function doMuReset(){',start)
if start<0 or end<0:
    raise SystemExit('No se encontro detailHTML')
fn=s[start:end]

anchor="  statLines(it).forEach(l=>{h+='<div class=\"ln\"><span>'+l[0]+'</span><span>'+l[1]+'</span></div>';});\n"
action="""  if(sel.src==='inv'){const dlt=Math.round(score(it)-score(cur));
    if(!cur)h+='<div class=\"cmp up\">Ranura libre: mejora segura</div>';
    else h+='<div class=\"cmp '+(dlt>=0?'up':'dn')+'\">'+(dlt>=0?'▲ Mejor que lo equipado (+'+dlt+')':'▼ Peor que lo equipado ('+dlt+')')+'</div>';
    h+='<div class=\"btns primaryActions\"><button class=\"btn\" data-a=\"equip\">Equipar</button><button class=\"btn alt\" data-a=\"sell\">Vender por '+price(it)+'</button></div>';}
  else h+='<div class=\"btns primaryActions\"><button class=\"btn alt\" data-a=\"unequip\">Quitar</button></div>';
"""
old_tail="""  h+=upgradeHTML(it);
  if(sel.src==='inv'){const dlt=Math.round(score(it)-score(cur));
    if(!cur)h+='<div class=\"cmp up\">Ranura libre: mejora segura</div>';
    else h+='<div class=\"cmp '+(dlt>=0?'up':'dn')+'\">'+(dlt>=0?'▲ Mejor que lo equipado (+'+dlt+')':'▼ Peor que lo equipado ('+dlt+')')+'</div>';
    h+='<div class=\"btns\"><button class=\"btn\" data-a=\"equip\">Equipar</button><button class=\"btn alt\" data-a=\"sell\">Vender por '+price(it)+'</button></div>';}
  else h+='<div class=\"btns\"><button class=\"btn alt\" data-a=\"unequip\">Quitar</button></div>';
  return h+'</div>';
"""
new_tail="""  h+=upgradeHTML(it);
  return h+'</div>';
"""

if 'primaryActions' not in fn:
    if anchor not in fn:
        raise SystemExit('No se encontro ancla de estadisticas')
    if old_tail not in fn:
        raise SystemExit('No se encontro bloque de acciones')
    fn=fn.replace(anchor,anchor+action,1)
    fn=fn.replace(old_tail,new_tail,1)
    s=s[:start]+fn+s[end:]

p.write_text(s)
print('Detalle compacto: Equipar/Vender visibles y set reducido')
