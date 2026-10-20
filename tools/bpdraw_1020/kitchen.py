from bp import *
f=4.2
X0,Y0,X1,Y1=40,28,320,188   # kitchen/dining pavilion 66'x38'
def base(name,num='A-111'):
    s=Sheet(name,num)
    s.walls([(X0,Y0),(X1,Y0),(X1,Y1),(X0,Y1)],7)
    for gx,l in ((X0,'A'),(180,'B'),(X1,'C')): s.grid(x=gx,lab=l,a=12,b=Y0+4)
    s.dim(X0,Y1,X1,Y1,f,off=10); s.dim(X1,Y0,X1,Y1,f,off=12)
    s.door(X0,Y1-34,16,-90,0,7); s.win(X1,Y0+40,X1,Y0+90,7); s.win(230,Y1,300,Y1,7)
    return s
def kitchen(s,layout='island',stools=True,cook='island',sink='north',x=56,y=40):
    # back counter on north wall
    if layout=='island':
        s.rect(x,Y0+3.5,110,10,PAPER,1.2); s.t(x+55,Y0+11,'',6)
        ix,iy=x+20,Y0+40; s.rect(ix,iy,70,18,PAPER,1.4); s.t(ix+35,iy-4,"ISLAND 10'x4'",7,w=700)
        if stools:
            for k in range(4): s.add(f'<circle cx="{ix+11+k*16}" cy="{iy+26}" r="4.5" fill="none" stroke="{INK}" stroke-width=".9"/>')
        if cook=='island': hob(s,ix+35,iy+9)
        else: hob(s,x+80,Y0+9); s.rect(x+64,Y0+3.5,32,14,'none',.7,INK2,'3 2'); s.note(x+96,Y0+17,'HOOD ABOVE',x+130,Y0+30)
        sk(s,x+30,Y0+9) if sink=='north' else sk(s,ix+18,iy+9)
    else:
        s.rect(x,Y0+3.5,120,10,PAPER,1.2); s.rect(x,Y0+38,120,10,PAPER,1.2); s.t(x+60,Y0+30,"GALLEY 4'-0\" AISLE",7,w=700)
        hob(s,x+90,Y0+9); sk(s,x+30,Y0+43)
def hob(s,x,y):
    s.rect(x-11,y-6,22,12,PAPER,.9)
    for dx in (-6,6):
        for dy in (-3,3): s.add(f'<circle cx="{x+dx}" cy="{y+dy}" r="2.4" fill="none" stroke="{INK}" stroke-width=".7"/>')
def sk(s,x,y): s.rect(x-8,y-3.5,16,7,'none',1,rx=1.5); s.add(f'<circle cx="{x}" cy="{y}" r="1" fill="{INK}"/>')
def table(s,kind='long',x=250,y=110):
    if kind=='long':
        s.rect(x-40,y-9,80,18,PAPER,1.3)
        for k in range(5):
            for dy in (-14,14): s.rect(x-34+k*16,y+dy-3,8,6,'none',.7,INK2)
        s.t(x,y+30,"TABLE 10'x3'-6\" · SEATS 10",7,w=600,col=INK2)
    else:
        s.add(f'<circle cx="{x}" cy="{y}" r="19" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
        for k in range(8):
            a=math.radians(k*45); s.add(f'<rect x="{x+26*math.cos(a)-3:.1f}" y="{y+26*math.sin(a)-3:.1f}" width="6" height="6" fill="none" stroke="{INK2}" stroke-width=".7"/>')
        s.t(x,y+42,"ROUND 6'-0\" Ø · SEATS 8",7,w=600,col=INK2)
def common(s,dining='open',view='north'):
    s.room(110,150,'KITCHEN',"26'x22'"); s.win(70,Y0,150,Y0,7) if view=='north' else s.win(70,Y1,150,Y1,7)
    s.t(110,Y0-4 if view=='north' else Y1+16,'COURTYARD' if view=='north' else 'POOL + VIEW',7,w=700,col=INK2)
    if dining=='room':
        s.part(200,Y0,200,Y1,2.2); s.gap(200,80,200,140,6); s.add(f'<rect x="198" y="80" width="4" height="60" fill="none" stroke="{INK2}" stroke-width=".6" stroke-dasharray="2 2"/>')
        s.note(200,140,"8'-0\" OPENING",220,176)
    s.room(250,62,'DINING',"28'x22'")
def draw(i,side,o):
    a=side=='A'
    N=['KITCHEN PLAN · LAYOUT','KITCHEN PLAN · ISLAND SEATING','PLAN · DINING','KITCHEN PLAN · SINK VIEW','PLAN · PANTRY','PLAN · MUDROOM LINK','PLAN · ENGAWA GRILL','KITCHEN PLAN · COOKTOP','DINING PLAN · TABLE','KITCHEN + DINING PLAN'][i]
    if i in (4,5): return service(N,i,a).svg()
    if i==6: return grill(N,a).svg()
    s=base(N)
    if i==0: kitchen(s,'island' if a else 'galley'); common(s); table(s)
    elif i==1: kitchen(s,stools=a); common(s); table(s)
    elif i==2: kitchen(s); common(s,'open' if a else 'room'); table(s)
    elif i==3: kitchen(s,sink='north' if a else 'south'); common(s,view='north' if a else 'south')
    elif i==7: kitchen(s,cook='island' if a else 'wall'); common(s); table(s)
    elif i==8: kitchen(s); common(s); table(s,'long' if a else 'round')
    else:
        if a: kitchen(s,cook='island'); common(s,'open','north'); table(s)
        else: kitchen(s,cook='wall',stools=False); common(s,'room','south'); table(s,'long')
        if not a: s.note(X0+4,Y1-20,'SCULLERY BEYOND',X0+12,Y1-30)
    if i==3: s.note(86,Y0+9 if a else Y0+49,'SINK',140 if a else 140,Y0+24 if a else Y0+70)
    return s.svg()
def service(N,i,a):
    s=Sheet(N,'A-112'); f2=9; kx0,ky0=40,40
    s.walls([(30,30),(330,30),(330,184),(30,184)],7); s.part(150,30,150,184,2); s.part(30,110,150,110,2)
    s.room(250,110,'KITCHEN',None,9); s.rect(170,33.5,140,10,PAPER,1.2)
    s.door(30,150,18,-90,0); s.t(18,166,'GARAGE',7,w=700,rot=-90)
    if i==4:
        if a:
            s.room(90,64,'WALK-IN PANTRY',"10'-0\" x 8'-0\"",8)
            for yy in (33.5,): s.rect(36,yy,108,10,'url(#bpTile)',1)
            s.rect(34,40,10,64,'url(#bpTile)',1); s.rect(136,40,10,64,'url(#bpTile)',1); s.note(40,72,'SHELVES 12" D',60,94)
            s.door(150,72,20,90,180)
        else:
            s.room(90,82,'SCULLERY',"13'-0\" x 8'-0\"",8); s.rect(36,33.5,108,12,PAPER,1.2); sk(s,70,39.5); sk(s,96,39.5); hob(s,124,39.5)
            s.note(70,39.5,'2ND SINK + PREP',60,60); s.door(150,72,20,90,180)
        s.room(90,148,'MUDROOM',"13'x8'",8)
    else:
        s.room(90,64,'PANTRY',None,8); s.room(90,148,'MUDROOM',"13'x8'",8)
        s.door(150,72,20,90,180)
        if a: s.door(150,150,18,90,180); s.arrow('M36 150H230'); s.head(236,150,0); s.t(196,144,'GROCERIES IN',7,w=600,col='#B5562F')
        else: s.door(110,110,16,180,90); s.arrow('M36 150H100V80H200'); s.head(206,80,0); s.t(70,124,'',7)
    s.dim(30,184,150,184,f2/2.4,off=10); return s
def grill(N,a):
    s=Sheet(N,'A-113'); s.walls([(30,30),(330,30),(330,100),(30,100)],7); s.room(180,62,'KITCHEN + DINING',None,8.5)
    s.door(240,100,18,0,-90); s.win(60,100,200,100,7)
    s.rect(30,104,300,36,'url(#bpDeck)',1); s.t(46,124,'ENGAWA',7.5,'start',700)
    s.line(30,150,330,150,.9,INK2,'8 3'); s.t(320,158,'EAVE LINE ABOVE',7,'end',600,INK2)
    s.rect(30,160,300,30,'url(#bpGravel)',0); s.t(180,180,'COURTYARD',8,w=700)
    s.dim(30,104,30,150,4,off=-12)
    if a: s.rect(110,112,52,18,PAPER,1.4); s.path('M116 116h40M116 121h40M116 126h40',sw=.6,col=INK2); s.note(162,121,"GRILL + 6'-0\" COUNTER",220,128)
    else: s.note(140,122,"CLEAR 11'-0\" GALLERY",210,128)
    return s
