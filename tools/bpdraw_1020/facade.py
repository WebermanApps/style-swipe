from bp import *
GY=168
def elev(name,clad='charred',front='wall',eave='thin',light=None,yard=None,num='A-201'):
    s=Sheet(name,num,scale='SCALE: 1/8" = 1\'-0"',north=False); f=4
    s.ground(10,350,GY,12)
    x0,x1,top=84,300,96; fill={'charred':'url(#bpCharr)','plaster':'url(#bpStip)'}[clad]
    s.rect(x0,top,x1-x0,GY-top,fill,1.6)
    if clad=='plaster': s.line(x0,GY-6,x1,GY-6,1.2); s.rect(x0,GY-6,x1-x0,6,'url(#bpPlank)',1)
    # roof: low pitched, deep eaves 7'
    e=7*f; s.path(f'M{x0-e} {top}L{180} {top-30}L{x1+e} {top}',sw=1.8)
    s.path(f'M{x0-e} {top}H{x1+e}',sw=3.2 if eave=='thin' else 1.2)
    if eave=='thick':
        s.rect(x0-e,top-1,x1-x0+2*e,8,'url(#bpPlankV)',1.4)
        for k in range(20): s.rect(x0-e+4+k*13.6,top+7,4,5,INK,0)
    s.add(f'<path d="M{x0-e+8} {top}L180 {top-26}L{x1+e-8} {top}" fill="url(#bpSeam)" opacity=".7"/>')
    if front=='wall':
        s.rect(164,GY-44,32,44,'#E4E7EA',1.6); s.rect(170,GY-40,20,40,PAPER,1.2); s.t(180,GY+20+0,'',6)
        s.note(196,GY-30,'DEEP ENTRY, 6\'-0" RECESS',236,GY-50)
    else:
        s.rect(x0+10,top+8,x1-x0-20,GY-top-8,PAPER,1.2)
        for k in range(25): s.line(x0+14+k*8,top+8,x0+14+k*8,GY,2.2)
        s.rect(164,GY-44,32,44,'none',1.2,dash='3 2'); s.note(120,GY-50,'WOOD SLAT SCREEN, 2" GAPS',200,top-50)
    s.level(12,top,''); s.t(10,top+12,"PLATE",6.6,'start',600,INK2); s.t(10,top+21,"10'-0\"",6.6,'start',600,INK2); s.level(12,GY,''); s.t(10,GY-6,"GRADE 0'-0\"",6.6,'start',600,INK2)
    for gx,l in ((x0,'A'),(180,'B'),(x1,'C')): s.grid(x=gx,lab=l,a=18,b=GY)
    s.dim(x0-e,top,x0,top,f,off=-10) 
    if light=='eaves':
        for k in range(5): x=x0+20+k*44; s.path(f'M{x} {top}L{x-12} {top+22}M{x} {top}L{x+12} {top+22}',sw=.7,col='#B5562F',dash='2 2'); s.add(f'<circle cx="{x}" cy="{top+2}" r="2" fill="#B5562F"/>')
        s.note(x0+20,top+4,'UPLIGHT WASHES SOFFIT',200,top-50)
    if light=='lanterns':
        for k in range(7): x=96+k*34; s.rect(x-3,GY-14,6,14,PAPER,1.1); s.add(f'<circle cx="{x}" cy="{GY-10}" r="2" fill="#B5562F"/>'); s.path(f'M{x-14} {GY}Q{x} {GY-18} {x+14} {GY}',sw=.6,col='#B5562F',dash='2 2')
        s.note(76,GY-12,'LOW LANTERNS 18" HIGH',60,GY+24) if False else s.t(14,GY+26,'',6)
    if clad=='charred': s.note(x1-30,top+40,'CHARRED WOOD',200,top-50) if 'CLADDING' in name else None
    else: s.note(x1-30,top+40,'LIME PLASTER',200,top-50) if 'CLADDING' in name else None
    return s
def eave_detail(name,kind):
    s=Sheet(name,'A-501',scale='SCALE: 3/4" = 1\'-0"',north=False); f=26
    s.rect(250,70,14,130,'url(#bpConc)',1.4); s.t(257,64,'WALL',6.6,w=700)
    if kind=='thin':
        s.path('M40 86L330 70L330 82L52 94Z','url(#bpH)',1.4); s.path('M36 90L48 82L52 94Z',INK,1); s.rect(40,92,210,3,'url(#bpMetal)',.8)
        s.note(44,90,'2" KNIFE EDGE, STEEL',40,140); s.note(150,93,'HIDDEN OUTRIGGERS',150,120)
    else:
        s.path('M40 80L330 64L330 76L40 92Z','url(#bpH)',1.4); s.rect(32,74,12,26,'url(#bpPlankV)',1.6)
        for k in range(6): s.rect(60+k*32,86-k*1.5,10,16,'url(#bpPlankV)',1)
        s.note(38,100,'2x12 TIMBER FASCIA',40,140); s.note(92,98,'EXPOSED RAFTER TAILS',150,124)
    s.dim(40,98,250,98,f/3.5,off=62,txt="7'-0\" EAVE")
    return s
def plan(name,num='A-102'):
    s=Sheet(name,num); return s
def yard_plan(name,ground=None,water=None,trees=1):
    s=Sheet(name,'L-101',scale='SCALE: 1/8" = 1\'-0"'); f=3.4; x0,y0=70,40; w,h=36*f*1.6,28*f*1.35
    s.walls([(x0-10,y0-10),(x0+w+10,y0-10),(x0+w+10,y0+h+10),(x0-10,y0+h+10)],6)
    s.rect(x0-6,y0-6,w+12,h+12,'url(#bpDeck)',0); s.rect(x0,y0,w,h,'none',1.2)
    if ground=='gravel':
        s.rect(x0,y0,w,h,'url(#bpGravel)',0); s.rect(x0+3,y0+3,w-6,h-6,'none',.6,INK2,'1 2'); s.tree(x0+w*.68,y0+h*.4,24); s.note(x0+w*.68+18,y0+h*.4+14,'ONE MAPLE',x0+w+16,y0+h+2)
        s.note(x0+3,y0+h-3,'MOSS EDGE',x0-14,y0+h+20,'end'); s.t(x0+50,y0+20,'RAKED GRAVEL',7,w=700)
    if ground=='lawn':
        s.rect(x0,y0,w,h,'url(#bpGrass)',0); s.rect(x0+w/2-8,y0,16,h,'url(#bpPaver)',1); s.rect(x0,y0+h/2-8,w,16,'url(#bpPaver)',1); s.t(x0+40,y0+24,'LAWN',7.5,w=700); s.note(x0+w/2+8,y0+h/2+8,'STONE PATHS 4\'-0"',x0+w+16,y0+h+2)
    if water=='pool':
        s.rect(x0,y0,w,h,'url(#bpGravel)',0); s.rect(x0+30,y0+24,w-60,h-48,'url(#bpWater)',1.6); s.rect(x0+33,y0+27,w-66,h-54,'none',.6)
        s.note(x0+w-34,y0+h-30,"REFLECTING POOL 12\" DEEP",x0+w+16,y0+h+2); s.tree(x0+18,y0+18,10)
    if water=='stream':
        s.rect(x0,y0,w,h,'url(#bpGravel)',0)
        d=f'M{x0} {y0+30}C{x0+60} {y0+20} {x0+70} {y0+h-30} {x0+130} {y0+h-36}S{x0+w-20} {y0+40} {x0+w} {y0+50}'
        s.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12"/><path d="{d}" fill="none" stroke="{PAPER}" stroke-width="9"/><path d="{d}" fill="none" stroke="{INK2}" stroke-width=".6" stroke-dasharray="3 3"/>')
        s.note(x0+100,y0+h-40,'STONE CHANNEL 12" WIDE',x0+w+16,y0+h+2); s.tree(x0+18,y0+h-18,10)
    s.dim(x0,y0+h+10,x0+w,y0+h+10,f*1.6,off=14,txt="36'-0\""); s.dim(x0+w+10,y0,x0+w+10,y0+h,f*1.35,off=14,txt="28'-0\"")
    s.t(x0+w/2,y0-14,'ENGAWA',6.8,w=700); return s
def pool(name,lap):
    s=Sheet(name,'L-102'); f=4.4
    s.wall(20,40,340,40,7); s.rect(20,44,320,16,'url(#bpDeck)',.8); s.t(30,54,'ENGAWA / WELLNESS',6.8,'start',700)
    s.rect(20,62,320,130,'url(#bpPaver)',0)
    if lap: w,h=60*f,9*f
    else: w,h=32*f,16*f
    x=180-w/2; y=86; s.rect(x-4,y-4,w+8,h+8,PAPER,1); s.rect(x,y,w,h,'url(#bpWater)',1.8)
    if not lap:
        for k in range(4): s.line(x+8+k*7,y,x+8+k*7,y+h,.9)
        s.note(x+20,y+h-6,'STEP-IN EDGE, 4 TREADS',x-10,y+h+40,'end')
    else: s.note(x+w-10,y+h/2,'LAP LANES',x+w-10,y+h+30,'end')
    s.dim(x,y+h,x+w,y+h,f,off=14); s.dim(x+w,y,x+w,y+h,f,off=10)
    s.t(180,y+h/2+3,'POOL',8,w=700); s.grid(x=x,lab='A',a=72,b=y+h+30,r=5.5); s.grid(x=x+w,lab='B',a=72,b=y+h+30,r=5.5)
    return s
def outdoor(name,dining):
    s=Sheet(name,'L-103'); f=4
    s.walls([(30,34),(200,34),(200,90),(30,90)],6); s.room(115,62,'KITCHEN',None,8); s.door(150,90,14,0,-90)
    s.line(20,126,210,126,.9,INK2,'8 3'); s.t(26,122,'EAVE ABOVE',6.6,'start',600,INK2); s.rect(30,94,170,30,'url(#bpDeck)',0)
    s.rect(220,90,120,60,'url(#bpWater)',1.6); s.t(280,124,'POOL',7.5,w=700)
    s.rect(14,130,332,66,'url(#bpGrass)',0)
    if dining:
        s.rect(56,100,110,18,PAPER,1.3)
        for k in range(6):
            for dy in (-6,24): s.rect(60+k*18,100+dy-0,8,5,'none',.7,INK2)
        s.note(160,109,"TABLE 15'x3'-6\", SEATS 12",120,150)
    else:
        cx,cy=280,170; s.add(f'<circle cx="{cx}" cy="{cy}" r="10" fill="url(#bpH)" stroke="{INK}" stroke-width="1.4"/>')
        s.path(f'M{cx-26} {cy+4}A26 26 0 0 1 {cx+26} {cy+4}',sw=6,col=INK2); s.path(f'M{cx-26} {cy+4}A26 26 0 0 1 {cx+26} {cy+4}',sw=4,col=PAPER)
        s.note(cx+8,cy+6,'FIRE PIT + LOW BENCHES',cx-40,cy+24,'end')
    return s
def entry_plan(name,gate):
    s=Sheet(name,'L-104'); s.walls([(150,24),(290,24),(290,80),(150,80)],6); s.room(220,50,'GENKAN',None,8); s.door(212,80,14,0,-90)
    s.line(14,186,346,186,1.4); s.t(40,198,'STREET',7.5,w=700)
    if gate:
        s.wall(14,170,196,170,6); s.wall(232,170,346,170,6); s.rect(192,160,44,20,'none',1,INK,'5 3'); s.door(196,170,16,0,-55,wall=False); s.t(250,163,'ROOFED GATE',7,'start',700)
        for k in range(6): s.add(f'<ellipse cx="{214+(k%2)*6-3}" cy="{154-k*12}" rx="7" ry="4.5" fill="none" stroke="{INK}" stroke-width=".9"/>')
        s.note(222,130,'STEPPING STONES @ 24"',250,120)
    else:
        s.wall(100,90,100,176,6); s.rect(106,96,40,80,'none',1,INK,'5 3'); s.rect(106,82,110,14,'none',1,INK,'5 3'); s.rect(108,98,36,76,'url(#bpPaver)',0); s.rect(110,84,104,10,'url(#bpPaver)',0)
        s.note(146,130,'COVERED WALK, ROOF DASHED',176,130); s.note(100,150,'GARDEN WALL',60,140,'end')
        s.gap(106,170,146,170,7) ; s.wall(14,170,100,170,6); s.wall(146,170,346,170,6)
    s.tree(60,120,14); s.tree(300,130,16); return s
def draw(i,side,o):
    a=side=='A'; N=['STREET ELEVATION','SOUTH ELEVATION · CLADDING','EAVE DETAIL','SITE PLAN · ENTRY','COURTYARD PLAN · GROUND','COURTYARD PLAN · WATER','POOL PLAN','PLAN · OUTDOOR ROOM','STREET ELEVATION · NIGHT','STREET ELEVATION · OVERALL'][i]
    if i==0: s=elev(N,front='wall' if a else 'slats')
    elif i==1: s=elev(N,clad='charred' if a else 'plaster')
    elif i==2: s=eave_detail(N,'thin' if a else 'thick')
    elif i==3: s=entry_plan(N,a)
    elif i==4: s=yard_plan(N,'gravel' if a else 'lawn')
    elif i==5: s=yard_plan(N,water='pool' if a else 'stream')
    elif i==6: s=pool(N,a)
    elif i==7: s=outdoor(N,a)
    elif i==8: s=elev(N,light='lanterns' if a else 'eaves')
    else: s=elev(N,clad='charred',light='lanterns') if a else elev(N,clad='plaster',light='eaves')
    if i==9:
        if a: s.rect(214,GY+1,80,4,'url(#bpWater)',1); s.t(254,GY+22,'MIRROR POOL · GRAVEL',6.8,w=700)
        else: s.t(254,GY+22,'LAWN · STREAM',6.8,w=700)
    return s.svg()
