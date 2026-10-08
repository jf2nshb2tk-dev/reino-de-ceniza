from pathlib import Path
import json,base64,struct
p=Path('index.html');s=p.read_text();M='REMAINING_T5_FINAL_V1'
if M in s: print('T5 restantes ya aplicados');raise SystemExit
R=Path('assets/quaternius')
SRC={'w':('Warrior.gltf','Warrior_Body'),'m':('Wizard.gltf','Wizard.001'),'b':('Monk.gltf','Monk'),'a':('Rogue.gltf','Rogue'),'r':('Cleric.gltf','Cleric')}
FMT={5126:'f',5125:'I',5123:'H',5121:'B'}; NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
def load(fn,node):
 d=json.loads((R/fn).read_text());buf=base64.b64decode(d['buffers'][0]['uri'].split(',',1)[1]);n=next(x for x in d['nodes'] if x.get('name')==node);pr=d['meshes'][n['mesh']]['primitives'][0]
 def acc(i):
  a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];c=NC[a['type']];f=FMT[a['componentType']];z=struct.calcsize('<'+f);o=v.get('byteOffset',0)+a.get('byteOffset',0);st=v.get('byteStride',c*z);return [struct.unpack_from('<'+f*c,buf,o+k*st) for k in range(a['count'])]
 P=acc(pr['attributes']['POSITION']);I=[x[0] for x in acc(pr['indices'])] if 'indices'in pr else list(range(len(P)));F=[I[i:i+3] for i in range(0,len(I),3)];return P,F
def cut(P,F,pred):
 T=[f for f in F if pred(*[sum(P[i][j] for i in f)/3 for j in range(3)])];ids={i for f in T for i in f};pts=[P[i] for i in ids]
 if not pts: raise SystemExit('pieza vacia')
 mn=[min(q[j] for q in pts) for j in range(3)];mx=[max(q[j] for q in pts) for j in range(3)];ct=[(mn[j]+mx[j])/2 for j in range(3)];pos=[]
 for f in T:
  for i in f: pos += [round(P[i][j]-ct[j],5) for j in range(3)]
 return {'p':pos,'s':[round(max(mx[j]-mn[j],1e-5),5) for j in range(3)]}
Q={}
for k,(fn,node) in SRC.items():
 P,F=load(fn,node);Q[k+'C']=cut(P,F,lambda x,y,z:1.25<y<2.02);Q[k+'H']=cut(P,F,lambda x,y,z:.78<y<1.28);Q[k+'SL']=cut(P,F,lambda x,y,z:x>.22 and 1.56<y<2.08);Q[k+'SR']=cut(P,F,lambda x,y,z:x<-.22 and 1.56<y<2.08);Q[k+'AL']=cut(P,F,lambda x,y,z:x>.24 and 1.02<y<1.62);Q[k+'AR']=cut(P,F,lambda x,y,z:x<-.24 and 1.02<y<1.62);Q[k+'LL']=cut(P,F,lambda x,y,z:x>.07 and .18<y<1);Q[k+'LR']=cut(P,F,lambda x,y,z:x<-.07 and .18<y<1);Q[k+'FL']=cut(P,F,lambda x,y,z:x>.05 and y<.36);Q[k+'FR']=cut(P,F,lambda x,y,z:x<-.05 and y<.36)
J='''/* REMAINING_T5_FINAL_V1 */\nconst QKR='''+json.dumps(Q,separators=(',',':'))+''';
function qr(p,d,m,z,o=[0,0,0],r=[0,0,0]){if(!p||!d)return;const g=qkGroup(p),x=new THREE.Mesh(qkGeom(d),m);x.scale.set(z[0]/d.s[0],z[1]/d.s[1],z[2]/d.s[2]);x.position.set(...o);x.rotation.set(...r);x.castShadow=true;g.add(x);}
function qFinalCore(cls,k,mat,cfg){const h=P.eq.casco,a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;
 if(qkIsT5(a)){const m=mat(a,false),t=mat(a,true);qr(playerRig.chest,QKR[k+'C'],m,cfg.c,[0,.02,.10]);qr(playerRig.hips,QKR[k+'H'],m,cfg.h,[0,-.10,.05]);qr(playerRig.uaL,QKR[k+'SL'],t,cfg.s,[-.03,.10,.02],[0,0,.14]);qr(playerRig.uaR,QKR[k+'SR'],t,cfg.s,[.03,.10,.02],[0,0,-.14]);}
 if(qkIsT5(g)){const m=mat(g,false);qr(playerRig.laL,QKR[k+'AL'],m,cfg.a,[0,.08,.02]);qr(playerRig.laR,QKR[k+'AR'],m,cfg.a,[0,.08,.02]);}
 if(qkIsT5(b)){const m=mat(b,false),t=mat(b,true);qr(playerRig.llL,QKR[k+'LL'],m,cfg.l,[0,.10,.01]);qr(playerRig.llR,QKR[k+'LR'],m,cfg.l,[0,.10,.01]);qr(playerRig.footL,QKR[k+'FL'],t,cfg.f,[0,.03,.08]);qr(playerRig.footR,QKR[k+'FR'],t,cfg.f,[0,.03,.08]);}}
function qkWarriorFinal(){if(P.cls!=='guerrero')return;qFinalCore('guerrero','w',(i,t)=>warriorMat(i,t),{c:[.70,.54,.35],h:[.60,.34,.33],s:[.38,.25,.34],a:[.21,.35,.22],l:[.23,.38,.24],f:[.24,.16,.33]});if(qkIsT5(P.eq.armadura)){const t=warriorMat(P.eq.armadura,true),g=qkGroup(playerRig.chest);wp(g,UOct,t,.11,.11,.06,0,.05,.27);}}
function qkMageFinal(){if(P.cls!=='mago')return;qFinalCore('mago','m',(i,t)=>mageMat(i,t),{c:[.60,.50,.30],h:[.52,.34,.28],s:[.30,.21,.29],a:[.18,.31,.19],l:[.20,.35,.21],f:[.20,.14,.30]});if(qkIsT5(P.eq.casco)){const t=mageMat(P.eq.casco,true),g=qkGroup(playerRig.head);mp(g,UOct,t,.09,.09,.055,0,.52,.24);}}
function qkRestFinalOne(cls,k,cfg){if(P.cls!==cls)return;qFinalCore(cls,k,(i,t)=>restMat(i,cls,t),cfg);const h=P.eq.casco,a=P.eq.armadura;if(qkIsT5(h)){const t=restMat(h,cls,true),g=qkGroup(playerRig.head);if(cls==='barbaro'){rp2(g,UCone,t,.075,.30,.075,-.23,.82,.01,0,0,.38);rp2(g,UCone,t,.075,.30,.075,.23,.82,.01,0,0,-.38);}else if(cls==='asesino'){rp2(g,UB,t,.31,.07,.10,0,.58,.28);}else{rp2(g,UOct,t,.11,.11,.06,0,.58,.28);rp2(g,UCone,t,.05,.24,.05,0,.82,-.02);}}if(cls==='brujo'&&qkIsT5(a)){const q=REST_CFG[cls],c=restColors(a,cls);if(q.cape){restPaint(q.cape,c.main,.04);const cp=restMesh(q.cape);if(cp)cp.visible=true;}}}
function qkRestFinal(){qkRestFinalOne('barbaro','b',{c:[.72,.55,.36],h:[.62,.35,.34],s:[.40,.26,.35],a:[.22,.36,.23],l:[.24,.39,.25],f:[.25,.17,.34]});qkRestFinalOne('asesino','a',{c:[.54,.46,.27],h:[.46,.28,.25],s:[.25,.18,.24],a:[.16,.30,.17],l:[.18,.33,.18],f:[.19,.13,.28]});qkRestFinalOne('brujo','r',{c:[.61,.50,.31],h:[.53,.32,.29],s:[.31,.21,.29],a:[.18,.31,.19],l:[.20,.35,.21],f:[.20,.14,.30]});}
'''
s=s.replace('function gearVisuals(){',J+'\nfunction gearVisuals(){',1)
s=s.replace('function qkArmorOnly(){qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();}','function qkArmorOnly(){qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();qkWarriorFinal();qkMageFinal();qkRestFinal();}',1)
old="""}else if(['barbaro','asesino','brujo'].includes(P.cls)){
    restBase(P.cls);attachRestSet(P.cls);
  }else{""";new="""}else if(['barbaro','asesino','brujo'].includes(P.cls)){
    restBase(P.cls);if(!qkIsT5(P.eq.casco))restHelmet(P.eq.casco,P.cls);if(!qkIsT5(P.eq.armadura))restTorso(P.eq.armadura,P.cls);if(!qkIsT5(P.eq.guantes))restGloves(P.eq.guantes,P.cls);if(!qkIsT5(P.eq.botas))restBoots(P.eq.botas,P.cls);
  }else{"""
if old not in s:raise SystemExit('rama restante no encontrada')
s=s.replace(old,new,1);p.write_text(s);print('T5 finales restantes aplicados')
