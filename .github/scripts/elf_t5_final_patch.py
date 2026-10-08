from pathlib import Path
import json,base64,struct

p=Path('index.html')
s=p.read_text()
marker='ELF_T5_FINAL_V1'
if marker in s:
    print('Elfo T5 final ya aplicado')
    raise SystemExit(0)

src=Path('assets/quaternius/Ranger.gltf')
if not src.exists():
    raise SystemExit('Falta assets/quaternius/Ranger.gltf para construir Elfo T5')

d=json.loads(src.read_text())
uri=d['buffers'][0]['uri']
if not uri.startswith('data:'):
    raise SystemExit('Ranger.gltf no tiene buffer embebido')
buf=base64.b64decode(uri.split(',',1)[1])
COMPS={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
FMT={5126:'f',5125:'I',5123:'H',5121:'B',5122:'h',5120:'b'}

def acc(i):
    a=d['accessors'][i]; bv=d['bufferViews'][a['bufferView']]
    off=bv.get('byteOffset',0)+a.get('byteOffset',0)
    comps=COMPS[a['type']]; f=FMT[a['componentType']]; size=struct.calcsize('<'+f)
    stride=bv.get('byteStride',comps*size)
    vals=[struct.unpack_from('<'+f*comps,buf,off+k*stride) for k in range(a['count'])]
    if a.get('normalized'):
        ct=a['componentType']
        if ct==5121: vals=[tuple(x/255 for x in v) for v in vals]
        elif ct==5123: vals=[tuple(x/65535 for x in v) for v in vals]
    return vals

def ident(): return [[1.0 if r==c else 0.0 for c in range(4)] for r in range(4)]
def mm(a,b): return [[sum(a[r][k]*b[k][c] for k in range(4)) for c in range(4)] for r in range(4)]
def mv(a,v): return [sum(a[r][k]*v[k] for k in range(4)) for r in range(4)]
def inv4(m):
    a=[row[:] + [1.0 if i==j else 0.0 for j in range(4)] for i,row in enumerate(m)]
    for i in range(4):
        q=max(range(i,4),key=lambda r:abs(a[r][i])); a[i],a[q]=a[q],a[i]
        z=a[i][i]
        if abs(z)<1e-12: raise SystemExit('Matriz singular en Ranger')
        a[i]=[x/z for x in a[i]]
        for r in range(4):
            if r==i: continue
            f=a[r][i]; a[r]=[a[r][c]-f*a[i][c] for c in range(8)]
    return [row[4:] for row in a]
def trs(n):
    if 'matrix' in n:
        z=n['matrix']; return [[z[c*4+r] for c in range(4)] for r in range(4)]
    t=n.get('translation',[0,0,0]); x,y,z,w=n.get('rotation',[0,0,0,1]); sc=n.get('scale',[1,1,1])
    R=[[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w,0],
       [2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w,0],
       [2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y,0],[0,0,0,1]]
    S=[[sc[0],0,0,0],[0,sc[1],0,0],[0,0,sc[2],0],[0,0,0,1]]
    T=ident(); T[0][3],T[1][3],T[2][3]=t
    return mm(T,mm(R,S))

parents={}
for i,n in enumerate(d['nodes']):
    for c in n.get('children',[]): parents[c]=i
world_cache={}
def world(i):
    if i in world_cache:return world_cache[i]
    M=trs(d['nodes'][i])
    if i in parents:M=mm(world(parents[i]),M)
    world_cache[i]=M;return M
names={n.get('name'):i for i,n in enumerate(d['nodes']) if n.get('name')}

def node_mesh(name):
    ni=names[name]; n=d['nodes'][ni]; pr=d['meshes'][n['mesh']]['primitives'][0]
    P=[list(x) for x in acc(pr['attributes']['POSITION'])]
    if 'indices' in pr:
        ids=[x[0] for x in acc(pr['indices'])]; F=[ids[i:i+3] for i in range(0,len(ids),3)]
    else:F=[list(range(i,i+3)) for i in range(0,len(P),3)]
    if 'skin' in n:
        J=acc(pr['attributes']['JOINTS_0']); W=acc(pr['attributes']['WEIGHTS_0']); sk=d['skins'][n['skin']]
        raw=acc(sk['inverseBindMatrices']); IB=[[[z[c*4+r] for c in range(4)] for r in range(4)] for z in raw]
        joints=sk['joints']; mesh_inv=inv4(world(ni)); mats=[mm(mesh_inv,mm(world(joints[j]),IB[j])) for j in range(len(joints))]
        out=[]
        for pos,jj,ww in zip(P,J,W):
            v=[pos[0],pos[1],pos[2],1]; q=[0,0,0,0]
            for j,wgt in zip(jj,ww):
                if wgt:
                    z=mv(mats[int(j)],v)
                    for k in range(4):q[k]+=wgt*z[k]
            out.append(q[:3])
        P=out
    else:
        M=world(ni); P=[mv(M,[q[0],q[1],q[2],1])[:3] for q in P]
    return P,F

def piece(P,F,pred=None):
    tris=[]
    for f in F:
        c=[sum(P[i][j] for i in f)/3 for j in range(3)]
        if pred is None or pred(*c):tris.append(f)
    ids={i for f in tris for i in f}; pts=[P[i] for i in ids]
    if not pts:raise SystemExit('Pieza T5 de Elfo vacia')
    mn=[min(q[j] for q in pts) for j in range(3)];mx=[max(q[j] for q in pts) for j in range(3)]
    ctr=[(mn[j]+mx[j])/2 for j in range(3)];size=[mx[j]-mn[j] for j in range(3)]
    pos=[]
    for f in tris:
        for i in f:
            q=P[i];pos.extend(round(q[j]-ctr[j],5) for j in range(3))
    return {'p':pos,'s':[round(x,5) for x in size]}

P,F=node_mesh('Ranger')
final={
    'helm':piece(P,F,lambda x,y,z:y>2.20),
    'shL':piece(P,F,lambda x,y,z:x>.22 and 1.58<y<2.08),
    'shR':piece(P,F,lambda x,y,z:x<-.22 and 1.58<y<2.08),
    'hip':piece(P,F,lambda x,y,z:.78<y<1.28),
}
P,F=node_mesh('Pouch');final['pouch']=piece(P,F)

js='''/* ELF_T5_FINAL_V1 - set final lvl 81-100 claramente distinto */\nconst QKF='''+json.dumps(final,separators=(',',':'))+''';
function qkfPiece(parent,d,mat,target,pos=[0,0,0],rot=[0,0,0]){
  if(!parent||!d)return null;
  const g=qkGroup(parent),me=new THREE.Mesh(qkGeom(d),mat);
  me.scale.set(target[0]/d.s[0],target[1]/d.s[1],target[2]/d.s[2]);
  me.position.set(pos[0],pos[1],pos[2]);me.rotation.set(rot[0],rot[1],rot[2]);me.castShadow=true;g.add(me);return me;
}
function qkElfFinal(){
  if(P.cls!=='elfa')return;
  const h=P.eq.casco,a=P.eq.armadura;
  if(qkIsT5(h)&&playerRig.head){
    const m=elfMat(h,false),t=elfMat(h,true);
    qkfPiece(playerRig.head,QKF.helm,m,[.48,.50,.42],[0,.61,.01]);
    const g=qkGroup(playerRig.head);
    ep(g,UOct,t,.10,.10,.055,0,.69,.30);
    ep(g,UCone,t,.055,.22,.055,-.20,.83,.02,0,0,.30);
    ep(g,UCone,t,.055,.22,.055,.20,.83,.02,0,0,-.30);
  }
  if(qkIsT5(a)){
    const m=elfMat(a,false),t=elfMat(a,true);
    qkfPiece(playerRig.uaL,QKF.shL,t,[.34,.24,.30],[-.03,.10,.03],[0,0,.14]);
    qkfPiece(playerRig.uaR,QKF.shR,t,[.34,.24,.30],[.03,.10,.03],[0,0,-.14]);
    qkfPiece(playerRig.hips,QKF.hip,m,[.56,.30,.30],[0,-.10,.05]);
    qkfPiece(playerRig.hips,QKF.pouch,t,[.18,.20,.12],[-.22,-.04,.10],[0,.20,0]);
    qkfPiece(playerRig.hips,QKF.pouch,t,[.18,.20,.12],[.22,-.04,.10],[0,-.20,0]);
    qkfPiece(playerRig.chest,QKA.eCloak,t,[.22,.62,.12],[-.20,.02,-.14],[0,.16,.16]);
    qkfPiece(playerRig.chest,QKA.eCloak,t,[.22,.62,.12],[.20,.02,-.14],[0,-.16,-.16]);
  }
}
'''
anchor='function gearVisuals(){'
if anchor not in s:raise SystemExit('No se encontro gearVisuals para Elfo T5 final')
s=s.replace(anchor,js+'\n'+anchor,1)
old='function qkArmorOnly(){qkWarriorArmor();qkMageArmor();qkElfArmor();}'
new='function qkArmorOnly(){qkWarriorArmor();qkMageArmor();qkElfArmor();qkElfFinal();}'
if old not in s:raise SystemExit('No se encontro qkArmorOnly')
s=s.replace(old,new,1)
old2="""}else if(P.cls==='elfa'){
    elfBaseSkin();
    elfHelmet(P.eq.casco);"""
new2="""}else if(P.cls==='elfa'){
    elfBaseSkin();
    if(!qkIsT5(P.eq.casco))elfHelmet(P.eq.casco);"""
if old2 not in s:raise SystemExit('No se encontro casco del Elfo en rama T5')
s=s.replace(old2,new2,1)
p.write_text(s)
print('Elfo T5 final: casco, hombreras, cinturon y alas diferenciadas')
