from pathlib import Path
import json,base64,struct,math

p=Path('index.html'); s=p.read_text(); marker='QUATERNIUS_ARMOR_ONLY_V3'
if marker in s:
    print('Quaternius armor-only V3 ya aplicado'); raise SystemExit(0)
ROOT=Path('assets/quaternius')
FILES={'warrior':ROOT/'Warrior.gltf','wizard':ROOT/'Wizard.gltf','ranger':ROOT/'Ranger.gltf'}
for fp in FILES.values():
    if not fp.exists(): raise SystemExit(f'Falta modelo fuente Quaternius: {fp}')

COMPS={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
FMT={5126:'f',5125:'I',5123:'H',5121:'B',5122:'h',5120:'b'}

def mm(a,b):
    # matrices row-major internas
    return [[sum(a[r][k]*b[k][c] for k in range(4)) for c in range(4)] for r in range(4)]
def mv(a,v): return [sum(a[r][k]*v[k] for k in range(4)) for r in range(4)]
def ident(): return [[1.0 if r==c else 0.0 for c in range(4)] for r in range(4)]
def inv4(m):
    a=[row[:] + [1.0 if i==j else 0.0 for j in range(4)] for i,row in enumerate(m)]
    for i in range(4):
        q=max(range(i,4),key=lambda r:abs(a[r][i])); a[i],a[q]=a[q],a[i]
        d=a[i][i]
        if abs(d)<1e-12: raise ValueError('Matriz singular')
        a[i]=[x/d for x in a[i]]
        for r in range(4):
            if r==i: continue
            f=a[r][i]
            a[r]=[a[r][c]-f*a[i][c] for c in range(8)]
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

class Gltf:
    def __init__(self,path):
        self.d=json.loads(path.read_text())
        uri=self.d['buffers'][0]['uri']; self.buf=base64.b64decode(uri.split(',',1)[1])
        self.parents={}
        for i,n in enumerate(self.d['nodes']):
            for c in n.get('children',[]): self.parents[c]=i
        self._world={}
        self.node_by_name={n.get('name'):i for i,n in enumerate(self.d['nodes']) if n.get('name')}
    def acc(self,i):
        a=self.d['accessors'][i]; bv=self.d['bufferViews'][a['bufferView']]; off=bv.get('byteOffset',0)+a.get('byteOffset',0)
        comps=COMPS[a['type']]; f=FMT[a['componentType']]; size=struct.calcsize('<'+f); stride=bv.get('byteStride',comps*size)
        vals=[struct.unpack_from('<'+f*comps,self.buf,off+k*stride) for k in range(a['count'])]
        if a.get('normalized'):
            ct=a['componentType']
            if ct==5121: vals=[tuple(x/255 for x in v) for v in vals]
            elif ct==5123: vals=[tuple(x/65535 for x in v) for v in vals]
        return vals
    def world(self,i):
        if i in self._world:return self._world[i]
        M=trs(self.d['nodes'][i])
        if i in self.parents:M=mm(self.world(self.parents[i]),M)
        self._world[i]=M; return M
    def node_mesh(self,name):
        ni=self.node_by_name[name]; n=self.d['nodes'][ni]; pr=self.d['meshes'][n['mesh']]['primitives'][0]
        P=[list(x) for x in self.acc(pr['attributes']['POSITION'])]
        if 'indices' in pr:
            ids=[x[0] for x in self.acc(pr['indices'])]; faces=[ids[i:i+3] for i in range(0,len(ids),3)]
        else: faces=[list(range(i,i+3)) for i in range(0,len(P),3)]
        if 'skin' in n:
            J=self.acc(pr['attributes']['JOINTS_0']); W=self.acc(pr['attributes']['WEIGHTS_0']); sk=self.d['skins'][n['skin']]
            raw=self.acc(sk['inverseBindMatrices']); IB=[]
            for z in raw: IB.append([[z[c*4+r] for c in range(4)] for r in range(4)])
            joints=sk['joints']; mesh_inv=inv4(self.world(ni)); out=[]
            mats=[mm(mesh_inv,mm(self.world(joints[j]),IB[j])) for j in range(len(joints))]
            for pos,jj,ww in zip(P,J,W):
                v=[pos[0],pos[1],pos[2],1]; q=[0,0,0,0]
                for j,wgt in zip(jj,ww):
                    if wgt:
                        z=mv(mats[int(j)],v)
                        for k in range(4): q[k]+=wgt*z[k]
                out.append(q[:3])
            P=out
        else:
            M=self.world(ni); P=[mv(M,[q[0],q[1],q[2],1])[:3] for q in P]
        return P,faces

def piece(P,F,pred=None):
    tris=[]
    for f in F:
        c=[sum(P[i][j] for i in f)/3 for j in range(3)]
        if pred is None or pred(*c): tris.append(f)
    ids={i for f in tris for i in f}; pts=[P[i] for i in ids]
    if not pts: raise SystemExit('Pieza Quaternius vacia')
    mn=[min(q[j] for q in pts) for j in range(3)]; mx=[max(q[j] for q in pts) for j in range(3)]
    ctr=[(mn[j]+mx[j])/2 for j in range(3)]; size=[mx[j]-mn[j] for j in range(3)]
    pos=[]
    for f in tris:
        for i in f:
            q=P[i]; pos.extend(round(q[j]-ctr[j],5) for j in range(3))
    return {'p':pos,'s':[round(x,5) for x in size]}

Q={}
g=Gltf(FILES['warrior']); P,F=g.node_mesh('Warrior_Body')
Q.update({'wChest':piece(P,F,lambda x,y,z:1.25<y<2.05),'wHips':piece(P,F,lambda x,y,z:.8<y<1.3),'wArmL':piece(P,F,lambda x,y,z:x>.25 and 1<y<1.8),'wArmR':piece(P,F,lambda x,y,z:x<-.25 and 1<y<1.8),'wLegL':piece(P,F,lambda x,y,z:x>.08 and .15<y<1),'wLegR':piece(P,F,lambda x,y,z:x<-.08 and .15<y<1),'wFootL':piece(P,F,lambda x,y,z:x>.05 and y<.35),'wFootR':piece(P,F,lambda x,y,z:x<-.05 and y<.35)})
for key,node in [('wShL','ShoulderPad.L'),('wShR','ShoulderPad.R')]: P,F=g.node_mesh(node);Q[key]=piece(P,F)
g=Gltf(FILES['wizard']); P,F=g.node_mesh('Wizard.001')
Q.update({'mChest':piece(P,F,lambda x,y,z:1.25<y<2.05),'mArmL':piece(P,F,lambda x,y,z:x>.25 and 1<y<1.8),'mArmR':piece(P,F,lambda x,y,z:x<-.25 and 1<y<1.8),'mLegL':piece(P,F,lambda x,y,z:x>.08 and .15<y<1),'mLegR':piece(P,F,lambda x,y,z:x<-.08 and .15<y<1),'mFootL':piece(P,F,lambda x,y,z:x>.05 and y<.35),'mFootR':piece(P,F,lambda x,y,z:x<-.05 and y<.35)})
for key,node in [('mShL','ShoulderPad.L'),('mShR','ShoulderPad.R')]: P,F=g.node_mesh(node);Q[key]=piece(P,F)
g=Gltf(FILES['ranger']); P,F=g.node_mesh('Ranger')
Q.update({'eChest':piece(P,F,lambda x,y,z:1.2<y<2),'eLegL':piece(P,F,lambda x,y,z:x>.08 and .15<y<1),'eLegR':piece(P,F,lambda x,y,z:x<-.08 and .15<y<1),'eFootL':piece(P,F,lambda x,y,z:x>.05 and y<.35),'eFootR':piece(P,F,lambda x,y,z:x<-.05 and y<.35)})
for key,node in [('eArmL','ArmGuard.L'),('eArmR','ArmGuard.R'),('eCloak','Cloak')]: P,F=g.node_mesh(node);Q[key]=piece(P,F)

helpers='''/* QUATERNIUS_ARMOR_ONLY_V3 - solo armaduras reales, personaje/animaciones originales */\nconst QKA='''+json.dumps(Q,separators=(',',':'))+''';
function qkGeom(d){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(d.p,3));g.computeVertexNormals();return g;}
function qkGroup(parent){if(!parent)return null;const g=new THREE.Group();parent.add(g);playerRig.armorVisuals.push(g);return g;}
function qkPiece(parent,d,mat,target,pos=[0,0,0]){if(!parent||!d)return null;const g=qkGroup(parent),me=new THREE.Mesh(qkGeom(d),mat);me.scale.set(target[0]/d.s[0],target[1]/d.s[1],target[2]/d.s[2]);me.position.set(pos[0],pos[1],pos[2]);me.castShadow=true;g.add(me);return me;}
function qkIsT5(it){return !!(it&&armorTier(it)>=4);}
function qkWarriorArmor(){if(P.cls!=='guerrero')return;const a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;if(qkIsT5(a)){const m=warriorMat(a,false),t=warriorMat(a,true);qkPiece(playerRig.chest,QKA.wChest,m,[.66,.50,.32],[0,.02,.10]);qkPiece(playerRig.hips,QKA.wHips,m,[.52,.30,.30],[0,-.10,.05]);qkPiece(playerRig.uaL,QKA.wShL,t,[.28,.20,.28],[-.02,.05,.02]);qkPiece(playerRig.uaR,QKA.wShR,t,[.28,.20,.28],[.02,.05,.02]);}if(qkIsT5(g)){const m=warriorMat(g,false);qkPiece(playerRig.laL,QKA.wArmL,m,[.18,.30,.20],[0,.08,.02]);qkPiece(playerRig.laR,QKA.wArmR,m,[.18,.30,.20],[0,.08,.02]);}if(qkIsT5(b)){const m=warriorMat(b,false),t=warriorMat(b,true);qkPiece(playerRig.llL,QKA.wLegL,m,[.20,.34,.22],[0,.10,.01]);qkPiece(playerRig.llR,QKA.wLegR,m,[.20,.34,.22],[0,.10,.01]);qkPiece(playerRig.footL,QKA.wFootL,t,[.21,.14,.30],[0,.03,.08]);qkPiece(playerRig.footR,QKA.wFootR,t,[.21,.14,.30],[0,.03,.08]);}}
function qkMageArmor(){if(P.cls!=='mago')return;const a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;if(qkIsT5(a)){const m=mageMat(a,false),t=mageMat(a,true);qkPiece(playerRig.chest,QKA.mChest,m,[.56,.46,.28],[0,.02,.09]);qkPiece(playerRig.uaL,QKA.mShL,t,[.22,.15,.22],[-.02,.06,.01]);qkPiece(playerRig.uaR,QKA.mShR,t,[.22,.15,.22],[.02,.06,.01]);}if(qkIsT5(g)){const m=mageMat(g,false);qkPiece(playerRig.laL,QKA.mArmL,m,[.15,.28,.17],[0,.09,.02]);qkPiece(playerRig.laR,QKA.mArmR,m,[.15,.28,.17],[0,.09,.02]);}if(qkIsT5(b)){const m=mageMat(b,false),t=mageMat(b,true);qkPiece(playerRig.llL,QKA.mLegL,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.llR,QKA.mLegR,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.footL,QKA.mFootL,t,[.18,.13,.27],[0,.03,.07]);qkPiece(playerRig.footR,QKA.mFootR,t,[.18,.13,.27],[0,.03,.07]);}}
function qkElfArmor(){if(P.cls!=='elfa')return;const a=P.eq.armadura,g=P.eq.guantes,b=P.eq.botas;if(qkIsT5(a)){const m=elfMat(a,false),t=elfMat(a,true);qkPiece(playerRig.chest,QKA.eChest,m,[.52,.43,.26],[0,.02,.09]);qkPiece(playerRig.chest,QKA.eCloak,t,[.46,.55,.12],[0,.02,-.09]);}if(qkIsT5(g)){const m=elfMat(g,true);qkPiece(playerRig.laL,QKA.eArmL,m,[.15,.27,.16],[0,.09,.02]);qkPiece(playerRig.laR,QKA.eArmR,m,[.15,.27,.16],[0,.09,.02]);}if(qkIsT5(b)){const m=elfMat(b,false),t=elfMat(b,true);qkPiece(playerRig.llL,QKA.eLegL,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.llR,QKA.eLegR,m,[.17,.31,.18],[0,.10,.01]);qkPiece(playerRig.footL,QKA.eFootL,t,[.18,.13,.27],[0,.03,.07]);qkPiece(playerRig.footR,QKA.eFootR,t,[.18,.13,.27],[0,.03,.07]);}}
function qkArmorOnly(){qkWarriorArmor();qkMageArmor();qkElfArmor();}
'''
anchor='function gearVisuals(){'
if anchor not in s: raise SystemExit('No se encontro gearVisuals')
s=s.replace(anchor,helpers+'\n'+anchor,1)
old='}return;}\n  const w=P.eq.arma,a=P.eq.armadura'; new='}qkArmorOnly();return;}\n  const w=P.eq.arma,a=P.eq.armadura'
if old not in s: raise SystemExit('No se encontro cierre de rama GLB en gearVisuals')
s=s.replace(old,new,1); p.write_text(s)
print('Quaternius V3: solo armaduras T5 sobre el personaje original')
