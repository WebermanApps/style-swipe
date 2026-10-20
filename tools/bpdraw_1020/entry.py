from bp import *
import math
F=3.2
def site(name,path='straight',car=None,gate=None,glass=None,calm=None):
    s=Sheet(name,'A-101',scale='SCALE: 1/16" = 1\'-0"')
    x0,x1,y0,y1=70,290,26,86; dx=180
    for gx,l in ((x0,'A'),(150,'B'),(210,'C'),(x1,'D')): s.grid(x=gx,lab=l,a=12,b=96)
    s.walls([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],6); s.part(150,y0,150,y1); s.part(210,y0,210,y1)
    s.door(dx-8,y1,14,0,-90); s.room(dx,52,'GENKAN',None,7.5); s.room(110,58,'KIDS WING',None,7.5); s.room(250,58,'GUEST',None,7.5)
    s.win(95,y1,125,y1); s.win(235,y1,265,y1)
    if glass: s.win(158,y0,202,y0); s.t(dx,22,'GLASS TO COURTYARD',6.8,w=600,col=INK2)
    if calm: s.part(160,40,200,40,2.4); s.t(dx,37,'CALM WALL',6.8,w=600,col=INK2)
    s.line(14,176,346,176,.9,INK,'14 3 3 3'); s.t(330,172,'P.L.',7,'end',600,INK2)
    s.line(14,186,346,186,1.4); s.line(14,190,346,190,.6,INK2); s.t(60,200,'STREET',7.5,w=700)
    if path=='straight':
        s.rect(dx-8,y1+3,16,176-y1-3,'url(#bpPaver)',1)
    else:
        d=f'M{dx-8} {y1+3}C{dx-8} 120 {dx+60} 110 {dx+52} 150S{dx+16} 170 {dx+20} 176'
        s.path(d,sw=1); s.path(f'M{dx+8} {y1+3}C{dx+8} 112 {dx+76} 110 {dx+68} 150S{dx+32} 168 {dx+36} 176',sw=1)
        for (x,y) in ((dx,100),(dx+18,111),(dx+40,122),(dx+58,138),(dx+56,156),(dx+34,168)): s.add(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="4" fill="none" stroke="{INK2}" stroke-width=".8"/>')
        s.tree(dx-40,130,16); s.tree(dx+100,128,12)
    if car=='carport':
        s.rect(214,96,62,74,'none',1,INK,'6 3');
        for (x,y) in ((216,98),(274,98),(216,168),(274,168)): s.rect(x-2.5,y-2.5,5,5,INK,0)
        s.rect(230,106,30,56,'none',.8,INK2,rx=6); s.t(245,138,'CAR',7,w=600,col=INK2); s.t(245,92+0,'CARPORT 20\'x24\'',7,w=700)
    if car=='garage':
        g=(26,104,92,160); s.walls([(26,104),(92,104),(92,160),(26,160)],6); s.gap(34,160,84,160,7); s.line(34,160,84,160,.9,INK,'4 2')
        s.rect(43,114,30,40,'none',.8,INK2,rx=6); s.room(59,138,'GARAGE',"20'x18'",7); s.door(92,112,10,90,0)
        s.path(f'M98 112C130 112 140 96 {dx-10} 92',sw=.9,col=INK2,dash='3 2'); s.t(132,104,'GARDEN PATH',6.5,w=600,col=INK2)
    if gate=='wall':
        s.wall(20,170,dx-12,170,6); s.wall(dx+12,170,340,170,6)
        s.door(dx-12,170,12,0,-60,wall=False); s.door(dx+12,170,12,180,240,wall=False); s.t(dx+26,163,'GATE',7,'start',700)
    if gate=='open':
        for x in (40,80,120,250,290,320): s.tree(x,160,10)
        s.t(80,140,'OPEN GARDEN',7,w=700,col=INK2)
    s.dim(310,y1,310,176,F,off=12)
    return s
def genkan(name,w=8,d=10,bench=False,plant=False,shoes=None,view=None):
    f=12; cx=170; x0=cx-w*f/2; x1=cx+w*f/2; y1=182; y0=y1-d*f
    s=Sheet(name,'A-201',scale='SCALE: 1/4" = 1\'-0"')
    if view=='glass': s.rect(x0-20,y0-30,w*f+40,24,'url(#bpGravel)',0); s.t(cx,y0-14,'COURTYARD',7.5,w=700)
    s.walls([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],8)
    s.door(cx-18,y1,36,0,-90,8)
    s.line(x0+4,y1-40,x1-4,y1-40,1.2,INK,'5 2'); s.rect(x0+4,y1-39,w*f-8,35,'url(#bpPaver)',0)
    s.note(x1-10,y1-40,'STEP UP 7"',x1+24,y1-48); s.note(x0+10,y1-12,'STONE FLOOR',x0-16,y1-20,'end')
    s.room(cx+(20 if shoes=='closet' else 26 if view else 0),(y0+y1-40)/2+(14 if view else 2),'GENKAN',f"{w}'-0\" x {d}'-0\"",9)
    s.dim(x0,y0,x1,y0,f,off=-10); s.dim(x1,y0,x1,y1,f,off=12)
    if bench: s.rect(x0+4,y0+30,16,48,'url(#bpPlankV)',1); s.note(x0+12,y0+54,'BENCH',x0-16,y0+50,'end')
    if plant: s.tree(x1-18,y0+18,10); s.note(x1-18,y0+18,'PLANT',x1+24,y0+14)
    if shoes=='cubby':
        h=d*f-50; s.rect(x0+4,y0+4,16,h,PAPER,1)
        for k in range(1,7): s.line(x0+4,y0+4+k*h/7,x0+20,y0+4+k*h/7,.6)
        s.note(x0+12,y0+20,'CUBBIES 14" DEEP',x0-16,y0+16,'end'); s.rect(x1-20,y0+24,16,40,'url(#bpPlankV)',1); s.note(x1-12,y0+44,'BENCH',x1+24,y0+40)
    if shoes=='closet':
        cw=40; s.wall(x0+cw,y0,x0+cw,y0+34,4); s.line(x0+8,y0+6,x0+8,y0+30,.6,INK2,'3 2'); s.line(x0+16,y0+6,x0+16,y0+30,.6,INK2,'3 2')
        s.part(x0+4,y0+34,x0+6,y0+34); s.door(x0+cw,y0+34,cw-4,180,120,wall=False)
        s.note(x0+12,y0+18,'SHOE CLOSET, SHELVES',x0-16,y0+14,'end')
    if view=='glass':
        s.win(x0+10,y0,x1-10,y0,8); s.arrow(f'M{cx} {y1-50}V{y0+12}'); s.head(cx,y0+8,-90); s.note(x1-14,y0,'FULL GLASS',x1+24,y0+10)
    if view=='calm':
        s.wall(x0+26,y0+34,x1,y0+34,4); s.win(x0,y0+6,x0,y0+28,8); s.rect(x0-30,y0+4,24,26,'url(#bpGravel)',0)
        s.note(x1-20,y0+34,'CALM WALL',x1+24,y0+44)
        s.arrow(f'M{cx} {y1-50}V{y0+48}Q{cx} {y0+18} {x0+18} {y0+18}H{x0-8}'); s.head(x0-12,y0+18,180); s.t(x0-12,y0-2,'COURTYARD',7,'end',700)
    return s
def door(name,kind):
    s=Sheet(name,'A-501',scale='SCALE: 1/2" = 1\'-0"'); f=14; y=120; xa,xb=110,110+4*f
    s.wall(30,y,xa,y,10); s.wall(xb,y,330,y,10); s.t(60,y+20,'EXTERIOR',7,w=600,col=INK2); s.t(60,y-14,'GENKAN',7,w=600,col=INK2)
    s.dim(xa,y,xb,y,f,off=34,txt="4'-0\" CLEAR")
    if kind=='pivot':
        px=xa+0.75*f; s.add(f'<circle cx="{px}" cy="{y}" r="2.6" fill="{INK}"/>')
        s.rect(xa,y-3,4*f,6,'url(#bpPlank)',1.4,col=INK).add(f'<g/>')
        s.line(px,y,px+(4*f-.75*f)*math.cos(math.radians(-80)),y+(4*f-.75*f)*math.sin(math.radians(-80)),2.4)
        s.path(f'M{xb} {y}A{3.25*f} {3.25*f} 0 0 0 {px+3.25*f*math.cos(math.radians(-80)):.1f} {y+3.25*f*math.sin(math.radians(-80)):.1f}',sw=.7,col=INK2)
        s.path(f'M{xa} {y}A{.75*f} {.75*f} 0 0 1 {px+.75*f*math.cos(math.radians(100)):.1f} {y+.75*f*math.sin(math.radians(100)):.1f}',sw=.7,col=INK2)
        s.note(px,y,'PIVOT 9" FROM JAMB',200,40); s.t(200,60,"SOLID WOOD LEAF 2-1/4\"",7,'start',500,INK2)
    else:
        s.rect(xa,y-12,4*f,4,PAPER,1.6); s.rect(xb,y-12,4*f+4,4,'none',.6,INK2,'3 2')
        s.line(xa,y-14,xb+4*f,y-14,.5,INK2); s.arrow(f'M{xa+8} {y-22}H{xb+40}'); s.head(xb+44,y-22,0)
        s.note(xb+20,y-3,'POCKET IN WALL',200,40); s.t(200,60,'WOOD SCREEN ON TOP TRACK',7,'start',500,INK2)
    return s
def engawa(name,turn):
    s=Sheet(name,'A-102'); f=3.2
    s.walls([(40,30),(320,30),(320,70),(40,70)],6); s.room(180,52,'LIVING WING',None,7.5)
    s.walls([(40,70),(80,70),(80,180),(40,180)],6); s.room(60,128,'ENTRY',None,7.5); s.door(40,154,14,-90,0)
    s.t(26,165,'GENKAN',6.5,w=700,rot=-90)
    s.walls([(280,70),(320,70),(320,180),(280,180)],6); s.room(300,128,'PRIMARY',None,7)
    s.rect(80,180-30,200,30,'none',.9,INK2,'5 3'); s.t(180,170,'WELLNESS (SOUTH)',7,w=700,col=INK2)
    s.rect(86,76,188,14,'url(#bpDeck)',.9); s.t(180,86,'ENGAWA',6.8,w=700)
    s.rect(98,96,164,48,'url(#bpGravel)',0); s.t(180,124,'COURTYARD',8,w=700)
    s.gap(80,96,80,118,7); s.dim(86,96,86,144,f,off=-0.1) if False else None
    if turn=='straight':
        s.arrow('M50 160V108H88V84H160'); s.head(166,84,0)
    else:
        s.arrow('M50 160V108H88V150H180'); s.head(186,150,0); s.rect(84,140,190,14,'url(#bpDeck)',.9)
    s.dim(80,30,280,30,f,off=-8); return s
def canopy(name,depth):
    s=Sheet(name,'A-301',scale='SCALE: 1/4" = 1\'-0"',north=False); f=8.5; gy=176; wx=230
    s.ground(20,340,gy,14); s.rect(wx,40,12,gy-40,'url(#bpConc)',1.4); s.t(wx+30,110,'POURED WALL',7,'start',600,INK2)
    s.rect(wx+12,60,90,8,'url(#bpH)',1.2); s.t(wx+20,56,'INTERIOR',6.8,'start',600,INK2)
    s.gap(wx+6,gy-58,wx+6,gy-2,14); s.rect(wx+3,gy-58,6,56,PAPER,1.2); s.t(wx+20,gy-28,'DOOR',7,'start',600)
    L=depth*f; s.rect(wx-L,50,L+12,7,'url(#bpMetal)',1.4); s.line(wx-L,50,wx-L,57,2)
    s.dim(wx-L,50,wx,50,f,off=-12)
    s.line(wx-L,57,wx-L-(gy-57),gy,.8,'#B5562F','5 3'); s.t(wx-L-40,gy-40,'45° RAIN LINE',6.8,'end',600,'#B5562F')
    s.level(36,57,"T.O. CANOPY 9'-6\""); s.level(36,gy-1,"F.F. 0'-0\"")
    s.add(f'<rect x="{wx-L}" y="{gy-4}" width="{L}" height="4" fill="#B5562F" opacity=".25"/>'); s.t(wx-L/2,gy-8,'DRY',6.8,w=700,col='#B5562F')
    return s
NAME={0:'SITE PLAN · APPROACH',1:'SITE PLAN · PARKING',2:'SITE PLAN · STREET EDGE',3:'GENKAN PLAN',4:'GENKAN PLAN · FIRST VIEW',5:'GENKAN PLAN · SHOE STORAGE',6:'FRONT DOOR · PLAN DETAIL',7:'PLAN · GENKAN TO ENGAWA',8:'SECTION A · ENTRY CANOPY',9:'SITE PLAN · ARRIVAL'}
def draw(i,side,o):
    a=side=='A'; n=NAME[i]
    if i==0: s=site(n,'straight' if a else 'bend')
    elif i==1: s=site(n,car='carport' if a else 'garage')
    elif i==2: s=site(n,gate='wall' if a else 'open')
    elif i==3: s=genkan(n,6,7) if a else genkan(n,10,12,bench=True,plant=True)
    elif i==4: s=genkan(n,view='glass' if a else 'calm')
    elif i==5: s=genkan(n,shoes='cubby' if a else 'closet')
    elif i==6: s=door(n,'pivot' if a else 'slide')
    elif i==7: s=engawa(n,'straight' if a else 'wellness')
    elif i==8: s=canopy(n,8 if a else 2)
    else: s=site(n,'bend',gate='wall',calm=True) if a else site(n,'straight',gate='open',glass=True)
    return s.svg()
