from pathlib import Path
import json

p=Path('index.html')
s=p.read_text()
marker='QUATERNIUS_ARMOR_ONLY_V2'
if marker in s:
    print('Quaternius armor-only V2 ya aplicado')
    raise SystemExit(0)

ROOT=Path('assets/quaternius')
SRC={
    'warrior':(ROOT/'Warrior.obj','Warrior_Body__ncl1_29.005'),
    'wizard':(ROOT/'Wizard.obj','Wizard.001__ncl1_29.006'),
    'ranger':(ROOT/'Ranger.obj','Ranger_Cube.003'),
}
for fp,_ in SRC.values():
    if not fp.exists(): raise SystemExit(f'Falta pieza Quaternius: {fp}')

def parse_obj(path):
    vs=[]; objs={}; cur=None
    for line in path.read_text().splitlines():
        if line.startswith('v '):
            vs.append(tuple(map(float,line.split()[1:4])))
        elif line.startswith('o '):
            cur=line[2:].strip(); objs[cur]=[]
        elif line.startswith('f ') and cur:
            ids=[int(x.split('/')[0])-1 for x in line.split()[1:]]
            if len(ids)==3: objs[cur].append(ids)
            else:
                for i in range(1,len(ids)-1): objs[cur].append([ids[0],ids[i],ids[i+1]])
    return vs,objs

def piece(vs,faces,pred=None):
    tris=[]
    for f in faces:
        c=[sum(vs[i][j] for i in f)/3 for j in range(3)]
        if pred is None or pred(*c): tris.append(f)
    ids={i for f in tris for i in f}; pts=[vs[i] for i in ids]
    if not pts: raise SystemExit('Pieza Quaternius vacia')
    mn=[min(q[j] for q in pts) for j in range(3)]; mx=[max(q[j] for q in pts) for j in range(3)]
    ctr=[(mn[j]+mx[j])/2 for j in range(3)]; size=[mx[j]-mn[j] for j in range(3)]
    pos=[]
    for f in tris:
        for i in f:
            q=vs[i]; pos.extend(round(q[j]-ctr[j],5) for j in range(3))
    return {'p':pos,'s':[round(x,5) for x in size]}

Q={}
vs,o=parse_obj(SRC['warrior'][0]); b=o[SRC['warrior'][1]]
Q.update({
'wChest':piece(vs,b,lambda x,y,z:1.25<y<2.05),'wHips':piece(vs,b,lambda x,y,z:.8<y<1.3),
'wArmL':piece(vs,b,lambda x,y,z:x>.25 and 1<y<1.8),'wArmR':piece(vs,b,lambda x,y,z:x<-.25 and 1<y<1.8),
'wLegL':piece(vs,b,lambda x,y,z:x>.08 and .15<y<1),'wLegR':piece(vs,b,lambda x,y,z:x<-.08 and .15<y<1),
'wFootL':piece(vs,b,lambda x,y,z:x>.05 and y<.35),'wFootR':piece(vs,b,lambda x,y,z:x<-.05 and y<.35),
'wShL':piece(vs,o['ShoulderPad.L__ncl1_29.000']),'wShR':piece(vs,o['ShoulderPad.R__ncl1_29.001'])})
vs,o=parse_obj(SRC['wizard'][0]); b=o[SRC['wizard'][1]]
Q.update({
'mChest':piece(vs,b,lambda x,y,z:1.25<y<2.05),'mArmL':piece(vs,b,lambda x,y,z:x>.25 and 1<y<1.8),'mArmR':piece(vs,b,lambda x,y,z:x<-.25 and 1<y<1.8),
'mLegL':piece(vs,b,lambda x,y,z:x>.08 and .15<y<1),'mLegR':piece(vs,b,lambda x,y,z:x<-.08 and .15<y<1),
'mFootL':piece(vs,b,lambda x,y,z:x>.05 and y<.35),'mFootR':piece(vs,b,lambda x,y,z:x<-.05 and y<.35),
'mShL':piece(vs,o['ShoulderPad.L__ncl1_29.002']),'mShR':piece(vs,o['ShoulderPad.R__ncl1_29.004'])})
vs,o=parse_obj(SRC['ranger'][0]); b=o[SRC['ranger'][1]]
Q.update({
'eChest':piece(vs,b,lambda x,y,z:1.2<y<2),'eLegL':piece(vs,b,lambda x,y,z:x>.08 and .15<y<1),'eLegR':piece(vs,b,lambda x,y,z:x<-.08 and .15<y<1),
'eFootL':piece(vs,b,lambda x,y,z:x>.05 and y<.35),'eFootR':piece(vs,b,lambda x,y,z:x<-.05 and y<.35),
'eArmL':piece(vs,o['ArmGuard.L_Cube.002']),'eArmR':piece(vs,o['ArmGuard.R_Cube.004']),'eCloak':piece(vs,o['Cloak_Cube.000'])})

helpers=f'''/* QUATERNIUS_ARMOR_ONLY_V2 - piezas reales sobre el personaje original */
const QKA={json.dumps(Q,separators=(',',':'))};
function qkGeom(d){{const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(d.p,3));g.computeVertexNormals();return g;}}
function qkGroup(parent){{if(!parent)return null;const g=new THREE.Group();parent.add(g);playerRig.armorVisuals.push(g);return g;}}
function qkPiece(parent,d,mat,target,pos=[0,0,0]){{if(!parent||!d)return null;const g=qkGroup(parent),me=new THREE.Mesh(qkGeom(d),mat);me.scale.set(target[0]/d.s[0],target[1]/d.s[1],target[2]/d.s[2]);me.position.set(pos[0],pos[1],pos[2]);me.castShadow=true;g.add(me);return me;}}
function qkIsT5(it){{return !!(it&&armorTier(it)>=4);}}
function qkWarriorArmor(){{if(P.cls!=='guerrero')return;const a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;if(qkIsT5(a)){{const m=warriorMat(a,false),t=warriorMat(a,true);qkPiece(playerRig.chest,QKA.wChest,m,[.66,.50,.32],[0,.02,.10]);qkPiece(playerRig.hips,QKA.wHips,m,[.52,.30,.30],[0,-.10,.05]);qkPiece(playerRig.uaL,QKA.wShL,t,[.28,.20,.28],[-.02,.05,.02]);qkPiece(playerRig.uaR,QKA.wShR,t,[.28,.20,.28],[.02,.05,.02]);}}if(qkIsT5(g)){{const m=warriorMat(g,false);qkPiece(playerRig.laL,QKA.wArmL,m,[.18,.30,.20],[0,.08,.02]);qkPiece(playerRig.laR,QKA.wArmR,m,[.18,.30,.20],[0,.08,.02]);}}if(qkIsT5(b)){{const m=warriorMat(b,false),t=warriorMat(b,true);qkPiece(playerRig.llL,QKA.wLegL,m,[.20,.34,.22],[0,.10,.01]);qkPiece(playerRig.llR,QKA.wLegR,m,[.20,.34,.22],[0,.10,.01]);qkPiece(playerRig.footL,QKA.wFootL,t,[.21,.14,.30],[0,.03,.08]);qkPiece(playerRig.footR,QKA.wFootR,t,[.21,.14,.30],[0,.03,.08]);}}}}
function qkMageArmor(){{if(P.cls!=='mago')return;const a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;if(qkIsT5(a)){{const m=mageMat(a,false),t=mageMat(a,true);qkPiece(playerRig.chest,QKA.mChest,m,[.56,.46,.28],[0,.02,.09]);qkPiece(playerRig.uaL,QKA.mShL,t,[.22,.15,.22],[-.02,.06,.01]);qkPiece(playerRig.uaR,QKA.mShR,t,[.22,.15,.22],[.02,.06,.01]);}}if(qkIsT5(g)){{const m=mageMat(g,false);qkPiece(playerRig.laL,QKA.mArmL,m,[.15,.28,.17],[0,.09,.02]);qkPiece(playerRig.laR,QKA.mArmR,m,[.15,.28,.17],[0,.09,.02]);}}if(qkIsT5(b)){{const m=mageMat(b,false),t=mageMat(b,true);qkPiece(playerRig.llL,QKA.mLegL,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.llR,QKA.mLegR,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.footL,QKA.mFootL,t,[.18,.13,.27],[0,.03,.07]);qkPiece(playerRig.footR,QKA.mFootR,t,[.18,.13,.27],[0,.03,.07]);}}}}
function qkElfArmor(){{if(P.cls!=='elfa')return;const a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;if(qkIsT5(a)){{const m=elfMat(a,false),t=elfMat(a,true);qkPiece(playerRig.chest,QKA.eChest,m,[.52,.43,.26],[0,.02,.09]);qkPiece(playerRig.chest,QKA.eCloak,t,[.46,.55,.12],[0,.02,-.09]);}}if(qkIsT5(g)){{const m=elfMat(g,true);qkPiece(playerRig.laL,QKA.eArmL,m,[.15,.27,.16],[0,.09,.02]);qkPiece(playerRig.laR,QKA.eArmR,m,[.15,.27,.16],[0,.09,.02]);}}if(qkIsT5(b)){{const m=elfMat(b,false),t=elfMat(b,true);qkPiece(playerRig.llL,QKA.eLegL,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.llR,QKA.eLegR,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.footL,QKA.eFootL,t,[.18,.13,.27],[0,.03,.07]);qkPiece(playerRig.footR,QKA.eFootR,t,[.18,.13,.27],[0,.03,.07]);}}}}
function qkArmorOnly(){{qkWarriorArmor();qkMageArmor();qkElfArmor();}}
'''
anchor='function gearVisuals(){'
if anchor not in s: raise SystemExit('No se encontro gearVisuals')
s=s.replace(anchor,helpers+'\n'+anchor,1)
old='}return;}\n  const w=P.eq.arma,a=P.eq.armadura'
new='}qkArmorOnly();return;}\n  const w=P.eq.arma,a=P.eq.armadura'
if old not in s: raise SystemExit('No se encontro cierre de rama GLB')
s=s.replace(old,new,1)
p.write_text(s)
print('Quaternius T5: armaduras reales, personaje original sin reemplazo')
