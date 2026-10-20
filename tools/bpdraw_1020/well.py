from bp import *
f=4.0; X0,Y0,D=24,44,25*4.0
def tatami(s,b): s.rect(b[0]+4,b[1]+4,b[2]-b[0]-8,b[3]-b[1]-8,'url(#bpTatami)',0)
def planks(s,b): s.rect(b[0]+4,b[1]+4,b[2]-b[0]-8,b[3]-b[1]-8,'url(#bpPlank)',0)
def tile(s,b): s.rect(b[0]+4,b[1]+4,b[2]-b[0]-8,b[3]-b[1]-8,'url(#bpTile)',0)
def bench(s,b,n=2):
    for k in range(n): s.rect(b[0]+4,b[1]+4+k*10,b[2]-b[0]-8,9,'url(#bpPlank)',1)
def gymeq(s,b):
    for k in range(2): s.rect(b[0]+12+k*30,b[1]+16,18,40,'none',.9,INK2,rx=2)
    s.rect(b[2]-30,b[1]+20,18,18,'none',.9,INK2); s.t(b[2]-21,b[1]+31,'RACK',5.5,w=600,col=INK2)
def plunge(s,x,y,r=11,lab='COLD PLUNGE'):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#bpWater)" stroke="{INK}" stroke-width="1.4"/><circle cx="{x}" cy="{y}" r="{r-3}" fill="none" stroke="{INK}" stroke-width=".6"/>')
    s.note(x+r*.7,y+r*.7,lab,x+r+14,y+r+8)
def shower(s,x,y):
    s.add(f'<circle cx="{x}" cy="{y}" r="4" fill="none" stroke="{INK}" stroke-width=".9"/><circle cx="{x}" cy="{y}" r="1" fill="{INK}"/>')
def bifold(s,x1,x2,y):
    s.gap(x1,y,x2,y,7); n=6; w=(x2-x1)/n; d='M%.1f %.1f'%(x1,y)
    for k in range(n): d+='L%.1f %.1f'%(x1+w*(k+.5),y+(6 if k%2==0 else -0)+0) + 'L%.1f %.1f'%(x1+w*(k+1),y)
    s.path(d,sw=1.3); s.line(x1,y,x2,y,.4,INK2,'2 2')
def slider(s,x1,x2,y):
    s.gap(x1,y,x2,y,7); m=(x1+x2)/2; s.rect(x1,y-3,m-x1+4,2.6,PAPER,1); s.rect(m-4,y+.4,x2-m+4,2.6,PAPER,1)
def plan(name,rooms,num='A-121',south=None,east_win=False,sky=None,roofs=None):
    s=Sheet(name,num); x=X0; boxes={}
    tot=sum(r[1] for r in rooms)*f; X1=X0+tot; Y1=Y0+D
    s.walls([(X0,Y0),(X1,Y0),(X1,Y1),(X0,Y1)],7)
    for k,(nm,w,*fx) in enumerate(rooms):
        b=(x,Y0,x+w*f,Y1); boxes[nm]=b
        if k: s.part(x,Y0,x,Y1,1.8)
        x+=w*f
    for gx,l in ((X0+tot/2,'2'),(X1,'3')): s.grid(x=gx,lab=l,a=Y0-14,b=Y1+6)
    s.dim(X0,Y0,X1,Y0,f,off=-7) if False else None
    s.dim(X0,Y0,X0,Y1,f,off=-10)
    s.rect(X0,Y1+4,tot,36,'url(#bpGrass)',0); s.t(X0+6,Y1+34,'GARDEN / POOL SIDE (S)',6.8,'start',700,INK2)
    for nm,b in boxes.items():
        lab=nm.split('|')[0]; sz=f"{round((b[2]-b[0])/f)}'x25'"
        boxes[nm]=b
    s._boxes=boxes; s._labels=[(nm.split('|')[0],b) for nm,b in boxes.items()]; s.X1=X1; s.Y1=Y1
    return s
def labels(s,dy=0):
    for lab,b in s._labels:
        sz=f"{round((b[2]-b[0])/f)}'x25'"; s.room((b[0]+b[2])/2,b[3]-22+dy*0,lab,sz,7.2 if b[2]-b[0]<56 else 8)
def door(s,b,side='n',r=10):
    x=b[0]+6
    if side=='w': s.door(b[0],b[1]+8,r,90,0,wall=True)
    else: s.door(b[0]+4,b[3],r,0,-90,7)
# ---------- deck W1 (details) ----------
def W1(i,a):
    N=['WELLNESS PLAN · GYM','WELLNESS PLAN · SAUNA','WELLNESS PLAN · COLD PLUNGE','WELLNESS PLAN · SHOWERS','PLAN · STRETCH ROOM FLOOR','WELLNESS PLAN · HEAT ROOMS','SECTION · SOUTH WALKWAY','WELLNESS PLAN · CHANGING','WELLNESS PLAN · MORNING LIGHT','WELLNESS WING PLAN'][i]
    if i==6: return walkway(N,a)
    st=a if i==9 else None
    R=[('GYM',22),('STRETCH',14),('CHANGE',12),('SAUNA',10),('STEAM',8)]
    if i==1 and not a or (i==9 and a): R=[('GYM',24),('STRETCH',16),('CHANGE',14),('SHOWERS',12)]
    if i==5 and not a: R=[('GYM',22),('STRETCH',14),('CHANGE',12),('SAUNA',14)]
    if i==9 and not a: R=[('GYM',22),('STRETCH',14),('CHANGE',12),('SAUNA',10),('STEAM',8)]
    if i==7 and a: R=[('GYM',22),('STRETCH',14),('HALL',8),('SAUNA',10),('STEAM',8)]
    if i==2 and not a: R=[('GYM',20),('STRETCH',12),('CHANGE',10),('SAUNA',10),('PLUNGE',10)]
    if i==9 and not a: R=[('GYM',20),('STRETCH',12),('CHANGE',10),('SAUNA',10),('STEAM',8),('PLUNGE',8)]
    s=plan(N,R); B=s._boxes
    g=B['GYM']; gymeq(s,g)
    if i==0 and a or i==9 and a: bifold(s,g[0]+10,g[2]-10,g[3]); s.note(g[0]+40,g[3]+3,'FOLDING GLASS 16\'-0"',g[0]+40,g[3]+30)
    else: door(s,g)
    if i==0 and not a: s.note(g[0]+30,g[1],'ACOUSTIC WALLS, STC 55',g[0]+20,g[1]-6) if False else s.t((g[0]+g[2])/2,g[3]-8,'ACOUSTIC WALLS',6.5,w=600,col=INK2)
    tatami(s,B['STRETCH']) if (i==4 and a) or i==9 else planks(s,B['STRETCH']) if i==4 else None
    if 'SAUNA' in B: bench(s,B['SAUNA']); door(s,B['SAUNA'])
    if 'STEAM' in B: tile(s,B['STEAM']); door(s,B['STEAM'])
    if 'CHANGE' in B:
        c=B['CHANGE']; door(s,c)
        for k in range(4): s.rect(c[0]+4,c[1]+4+k*9,8,9,'none',.6,INK2)
        if i in (3,) and not a or i==9 and not a:
            for k in range(2): shower(s,c[2]-10,c[1]+16+k*20)
    if 'SHOWERS' in B: door(s,B['SHOWERS'])
    if 'PLUNGE' in B: p=B['PLUNGE']; s.rect(p[0]+6,p[1]+20,p[2]-p[0]-12,40,'url(#bpWater)',1.4); s.t((p[0]+p[2])/2,p[1]+74,'INDOOR',6.5,w=600,col=INK2)
    if 'HALL' in B: h=B['HALL']; s.arrow(f'M{(h[0]+h[2])/2} {h[3]-10}V{h[1]-8}'); s.head((h[0]+h[2])/2,h[1]-12,-90); s.t((h[0]+h[2])/2+6,h[1]-16,'TO PRIMARY BATH',6.8,'start',700,'#B5562F')
    if i==7 and not a: s.note(B['CHANGE'][0]+8,B['CHANGE'][1]+20,'LOCKERS + OWN DOOR',B['CHANGE'][0]+10,B['CHANGE'][1]-6)
    # outside features
    Y1=s.Y1; X1=s.X1
    if i==1 and not a or i==9 and a:
        cx=X1-60; s.walls([(cx,Y1+14),(cx+36,Y1+14),(cx+36,Y1+38),(cx,Y1+38)],4); bench(s,(cx,Y1+14,cx+36,Y1+38),1); s.note(cx+36,Y1+26,"SAUNA CABIN 9'x6'",cx+44,Y1+52)
    if i==2 and a or i==9 and a: plunge(s,X1-80 if i==9 else B['SAUNA'][0]+20,Y1+26,10,'OUTDOOR PLUNGE')
    if i==3 and a or i==9 and a:
        sx=B['CHANGE'][0]; s.wall(sx,Y1,sx,Y1+38,4); s.wall(sx,Y1+38,sx+44,Y1+38,4); shower(s,sx+16,Y1+20); s.note(sx+16,Y1+20,'RAIN SHOWER, WALLED',sx-10,Y1+52,'end') ; s.door(sx+44,Y1,12,180,90) if False else None
    if i==8:
        if a: s.win(X1,Y0+20,X1,Y0+80,7); [s.arrow(f'M{X1+40} {Y0+30+k*20}H{X1+10}') for k in range(3)]; s.head(X1+8,Y0+50,180); s.t(X1+10,Y0+16,'SUNRISE',6.8,'start',700,'#B5562F')
        else:
            for b in B.values(): s.rect(b[0]+8,b[1]+12,b[2]-b[0]-16,14,'none',.9,INK,'5 3')
            s.note(B['GYM'][0]+20,B['GYM'][1]+12,'SKYLIGHTS ABOVE',B['GYM'][0]+30,B['GYM'][1]-8)
    labels(s,dy=12 if i==8 and not a else 0); return s.svg()
def walkway(N,a):
    s=Sheet(N,'A-321',scale='SCALE: 1/4" = 1\'-0"',north=False); gy=178
    s.ground(14,346,gy,12); s.rect(24,40,10,gy-40,'url(#bpConc)',1.4); s.rect(326,40,10,gy-40,'url(#bpConc)',1.4)
    s.t(29,34,'MAIN',6.5,w=700); s.t(331,34,'WELL.',6.5,w=700)
    for x in (110,250): s.rect(x-3,70,6,gy-70,'url(#bpPlankV)',1.2)
    s.rect(34,gy-4,292,4,'url(#bpPaver)',.8); s.t(180,gy-8,"STONE WALK 9'-0\" CLEAR",7,w=600,col=INK2)
    if a:
        s.path('M14 64L180 52L346 64',sw=2); s.path('M14 70L180 58L346 70',sw=1); s.add('<path d="M14 64L180 52L346 64L346 70L180 58L14 70Z" fill="url(#bpMetal)"/>')
        s.note(220,56,'SOLID ROOF, STANDING SEAM',230,30)
    else:
        s.rect(20,62,320,8,'url(#bpH)',1.2)
        for k in range(26): s.rect(24+k*12.2,54,4,8,'url(#bpPlankV)',.8)
        s.note(200,58,'2x4 SLATS @ 12" O.C., VINES',210,30)
        for k in range(8): s.line(60+k*32,70,48+k*32,gy-10,.5,'#B5562F','2 3')
    s.level(40,70,"T.O. BEAM 8'-6\""); s.dim(34,gy,326,gy,8,off=12) if False else None
    return s.svg()
# ---------- deck J5 (wellness wing) ----------
def J5(i,a):
    N=['BATH HOUSE PLAN','PLAN · HEAT ROOM','PLAN · GYM','PLAN · YOGA','PLAN · REST','PLAN · SHOWERS','PLAN · TREATMENT','REFLECTED CEILING · LIGHT','PLAN · POOL LINK','WELLNESS WING PLAN'][i]
    R=[('GYM',20),('BATH',18),('HEAT',12),('REST',14)]
    if i==3 and a: R=[('GYM',18),('YOGA',10),('BATH',14),('HEAT',10),('REST',12)]
    if i==6 and a: R=[('GYM',18),('BATH',16),('HEAT',10),('REST',12),('MASSAGE',8)]
    if i==4 and a: R=[('GYM',22),('BATH',20),('HEAT',14),('LOUNGE',8)]
    if i==9: R=[('GYM',14),('BATH',24),('HEAT',12),('REST',14)] if a else [('GYM',26),('YOGA',12),('BATH',10),('HEAT',8),('REST',8)]
    num='A-131' if i!=7 else 'A-141'
    s=plan(N,R,num); B=s._boxes; X1,Y1=s.X1,s.Y1
    gymeq(s,B['GYM'])
    b=B['BATH']; bx=(b[0]+b[2])/2
    if (i==0 and not a):
        s.rect(b[0]+8,b[1]+20,(b[2]-b[0])/2-12,40,'url(#bpWater)',1.4); s.rect(bx+4,b[1]+20,(b[2]-b[0])/2-12,40,'url(#bpWater)',1.4)
        s.t(b[0]+20,b[1]+16,'HOT 104°',6.5,w=700); s.t(b[2]-18,b[1]+16,'COLD 50°',6.5,w=700)
    else:
        s.rect(b[0]+10,b[1]+22,b[2]-b[0]-20,36,'url(#bpWater)',1.4); s.rect(b[0]+14,b[1]+26,b[2]-b[0]-28,28,'none',.7)
        s.note(b[2]-12,b[1]+40,'SUNK STONE TUB, 2 STEPS',b[2]-6,b[1]-6) if i==0 else None
        if i==0: s.win(b[0]+10,b[1],b[2]-10,b[1],7); s.t(bx,b[1]-16,'',6)
    h=B['HEAT']
    if i==1 and not a: tile(s,h); s.rect(h[0]+4,h[1]+4,h[2]-h[0]-8,9,'url(#bpTile)',1); s.note(h[0]+12,h[1]+40,'TILED STEAM, BENCH',h[0]-4,h[3]+20,'end')
    else: bench(s,h); s.note(h[0]+12,h[1]+9,'CEDAR BENCHES',h[0],h[1]-6,'end') if i==1 else None
    if i==1 and a: s.win(h[0]+8,h[1],h[2]-8,h[1],7)
    s.door(h[0],h[3]-8,10,-90,0,wall=False) if i==8 and a else door(s,h,'n')
    g=B['GYM']
    if i==2 and a or i==9 and not a: slider(s,g[0]+8,g[2]-8,g[3]); s.note(g[0]+20,g[3],'GLASS SLIDES AWAY',g[0]+40,g[3]+30)
    elif i==2: s.win(g[0]+10,g[1],g[2]-10,g[1],7); s.note(g[0]+20,g[1],'HIGH WINDOW, SILL 7\'-0"',g[0]+30,g[1]-8); door(s,g)
    else: door(s,g)
    if 'YOGA' in B: tatami(s,B['YOGA']); door(s,B['YOGA'])
    if i==3 and not a: s.rect(g[2]-28,g[1]+56,24,40,'url(#bpTatami)',1); s.note(g[2]-16,g[1]+76,'MAT CORNER',g[2]+4,g[3]+20)
    if 'REST' in B:
        r=B['REST']
        for k in range(2): s.rect(r[0]+8,r[1]+10+k*26,(r[2]-r[0])-16,16,'none',.9,INK2,rx=3)
        if i==6 and not a: s.rect(r[0]+10,r[1]+64,r[2]-r[0]-20,14,'none',1,INK,'4 2'); s.note(r[0]+14,r[1]+71,'FOLD-OUT TABLE',r[0]+10,r[3]+20)
    if 'MASSAGE' in B: m=B['MASSAGE']; s.rect(m[0]+8,m[1]+14,m[2]-m[0]-16,52,'none',1.2,rx=3); door(s,m)
    if i==4 and a: s.rect(X1-80,Y1+4,80,34,'none',1,INK,'6 3'); [s.rect(X1-74+k*24,Y1+12,16,22,'none',.9,INK2,rx=3) for k in range(3)]; s.note(X1-40,Y1+38,'COVERED PORCH, LOUNGERS',X1-40,Y1+52,'end')
    if i==5:
        if a: s.wall(b[2],Y1,b[2],Y1+38,4); s.wall(b[2]-40,Y1+38,b[2],Y1+38,4); shower(s,b[2]-16,Y1+20); s.note(b[2]-16,Y1+20,'OUTDOOR RAIN SHOWER',b[2]+10,Y1+50)
        else: s.rect(b[2]-30,b[1]+66,26,28,'url(#bpTile)',1); shower(s,b[2]-17,b[1]+80); s.note(b[2]-17,b[1]+80,'WALK-IN SHOWER + BENCH',b[2]+10,Y1+50)
    if i==7:
        if a:
            for bb in B.values():
                for k in range(2): x=bb[0]+8+k*(bb[2]-bb[0]-16); s.add(f'<circle cx="{x}" cy="{bb[3]-10}" r="3.5" fill="none" stroke="{INK}" stroke-width=".8"/><path d="M{x-2.5} {bb[3]-12.5}l5 5m0-5l-5 5" stroke="{INK}" stroke-width=".6"/>')
            s.note(B['BATH'][0]+8,B['BATH'][3]-10,'LOW WARM LIGHT 18" A.F.F., 2700K',B['BATH'][0]+30,Y1+30)
        else:
            for bb in B.values(): s.rect(bb[0]+10,bb[1]+8,bb[2]-bb[0]-20,12,'none',.9,INK,'5 3')
            s.note(B['BATH'][0]+30,B['BATH'][1]+14,'LINEAR SKYLIGHTS ABOVE',B['BATH'][0]+40,Y1+30)
    if i==8:
        s.rect(h[0]-30,Y1+16,110,22,'url(#bpWater)',1.4); s.t(h[0]+25,Y1+30,'POOL',7,w=700)
        if not a:
            for k in range(4): s.add(f'<ellipse cx="{h[0]+6+k*1}" cy="{Y1+1+k*4}" rx="5" ry="2.5" fill="none" stroke="{INK}" stroke-width=".8"/>')
            s.rect(h[0]-30,Y1+16,110,22,'url(#bpWater)',1.4); s.note(h[0]+6,Y1+6,'STEPPING STONES',h[0]-36,Y1+14,'end')
        else: s.rect(h[0]-30,Y1+4,110,12,'url(#bpPaver)',1); s.note(h[0]+4,Y1+10,'DOOR ONTO POOL EDGE',h[0]-36,Y1+12,'end')
    labels(s); return s.svg()
def draw(i,side,o): return (W1 if MODE=='W1' else J5)(i,side=='A')
MODE='W1'
