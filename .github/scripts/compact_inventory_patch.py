from pathlib import Path

p=Path('index.html')
s=p.read_text()

marker='MU_COMPACT_INVENTORY_V1'
if marker not in s:
    css=r'''
/* MU_COMPACT_INVENTORY_V1 */
@media (min-width:640px){
  .sheet.compactInv{
    width:min(720px,94vw);
    max-height:calc(100vh - 18px);
    overflow:hidden;
    border-width:1px;
    border-radius:4px;
  }
  .sheet.compactInv .tabs button{
    padding:4px 4px;
    font-size:13px;
    border-bottom-width:2px;
  }
  .sheet.compactInv .tabs .x{width:34px;font-size:17px}
  .sheet.compactInv .pb{padding:5px 6px}
  .sheet.compactInv .bagl{
    grid-template-columns:118px minmax(0,1fr) 194px;
    gap:6px;
    align-items:start;
  }
  .sheet.compactInv h3{font-size:12px;margin:0 0 3px}
  .sheet.compactInv .bagl .eq{gap:3px}
  .sheet.compactInv .grid{grid-template-columns:repeat(8,1fr);gap:3px}
  .sheet.compactInv .cell{border-radius:2px}
  .sheet.compactInv .cell svg{width:23px!important;height:23px!important}
  .sheet.compactInv .cell b{right:2px;bottom:0;font-size:8px}
  .sheet.compactInv .cell i.up{left:2px;top:0;font-size:8px}
  .sheet.compactInv .cell i.sp{right:2px;top:1px;font-size:8px}
  .sheet.compactInv .cell small.pr{left:2px;top:0;font-size:8px}
  .sheet.compactInv .detail,
  .sheet.compactInv .fcard{
    margin-top:0;
    min-height:0;
    max-height:none;
    overflow:visible;
    padding:5px 6px;
    border-radius:3px;
  }
  .sheet.compactInv .detail .nm,
  .sheet.compactInv .fcard .nm{font-size:13px;margin-bottom:1px}
  .sheet.compactInv .detail .sb,
  .sheet.compactInv .fcard .sb{font-size:10px;line-height:1.15;margin-bottom:3px}
  .sheet.compactInv .ln,
  .sheet.compactInv .detail .ln,
  .sheet.compactInv .fcard .ln{font-size:10px;line-height:1.12;padding:0}
  .sheet.compactInv .cmp{font-size:10px;margin-top:3px}
  .sheet.compactInv .forge{
    margin-top:4px;
    padding:4px 5px;
    font-size:10px;
    border-radius:3px;
  }
  .sheet.compactInv .forge .ln{font-size:10px}
  .sheet.compactInv .btns{gap:4px;margin-top:4px}
  .sheet.compactInv .btns .btn{
    padding:4px 7px;
    font-size:11px;
    line-height:1.1;
  }
  .sheet.compactInv .note{
    font-size:9px;
    line-height:1.15;
    margin:2px 0 4px;
  }
  .sheet.compactInv .seg{gap:3px;margin:3px 0 5px}
  .sheet.compactInv .seg button{
    padding:4px 2px;
    font-size:9px;
    line-height:1.1;
  }
  .sheet.compactInv .fcard .big{
    font-size:13px;
    padding:3px 0 4px;
    margin-bottom:3px;
  }
  .sheet.compactInv .fcard .warn{
    margin-top:4px;
    padding:3px 4px;
    font-size:9px;
    line-height:1.15;
  }
  .sheet.compactInv .ftab{font-size:9px;margin-top:3px}
  .sheet.compactInv .ftab th,.sheet.compactInv .ftab td{padding:1px 2px}
}
@media (min-width:640px) and (max-height:430px){
  .sheet.compactInv{width:min(700px,94vw)}
  .sheet.compactInv .bagl{grid-template-columns:112px minmax(0,1fr) 184px;gap:5px}
  .sheet.compactInv .tabs button{padding:3px 3px;font-size:12px}
  .sheet.compactInv .pb{padding:4px 5px}
  .sheet.compactInv .grid,.sheet.compactInv .bagl .eq{gap:2px}
  .sheet.compactInv .cell svg{width:21px!important;height:21px!important}
}
'''
    if '</style>' not in s:
        raise SystemExit('No se encontro </style>')
    s=s.replace('</style>',css+'\n</style>',1)

old="function renderPanel(){\n  if(panelTab==='travel'){sheet.innerHTML=travelPanelHTML();return;}"
new="function renderPanel(){\n  sheet.classList.toggle('compactInv',panelTab==='bag'||panelTab==='shop');\n  if(panelTab==='travel'){sheet.innerHTML=travelPanelHTML();return;}"
if "sheet.classList.toggle('compactInv'" not in s:
    if old not in s:
        raise SystemExit('No se encontro renderPanel para activar modo compacto')
    s=s.replace(old,new,1)

p.write_text(s)
print('Inventario compacto estilo MU aplicado')
