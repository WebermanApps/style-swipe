from bp import *
SX,SY,SW,SH=14,24,150,150
def grain(s,x,y,w,h,bw=22,dark=False):
    s.rect(x,y,w,h,'#7E8A97' if dark else PAPER,0)
    if dark: s.rect(x,y,w,h,'url(#bpCharr)',0)
    k=0
    while k*bw<w:
        bx=x+k*bw; s.line(bx,y,bx,y+h,1.1)
        if not dark:
            for j in range(3):
                ox=bx+5+j*6; s.path(f'M{ox} {y}C{ox+3} {y+h*.3} {ox-3} {y+h*.6} {ox+1} {y+h}',sw=.5,col=INK2)
        k+=1
    s.rect(x,y,w,h,'none',1.4)
def tiles(s,x,y,w,h,tw,th,fill='url(#bpStip)',stagger=False):
    s.rect(x,y,w,h,fill,0); r=0; yy=y
    while yy<y+h-.1:
        s.line(x,yy,x+w,yy,.8); off=(tw/2 if stagger and r%2 else 0); xx=x-off
        while xx<x+w: 
            if xx>x: s.line(xx,yy,xx,min(yy+th,y+h),.8)
            xx+=tw
        yy+=th; r+=1
    s.rect(x,y,w,h,'none',1.4)
def sect(s,layers,x=196,y=40,w=110,lab_x=316):
    layers=[(t*1.9,f_,l) for t,f_,l in layers]; yy=y
    for t,fill,lab in layers:
        s.rect(x,yy,w,t,fill,1.1)
        if lab: s.note(x+w-6,yy+t/2,lab,lab_x,yy+t/2-3) if False else s.add('')
        yy+=t
    yy=y; ly=y-4
    for t,fill,lab in layers:
        if lab: ly=max(ly+14,yy+t/2); s.line(x+w-4,yy+t/2,x+w+8,ly,.6,INK2); s.add(f'<circle cx="{x+w-4}" cy="{yy+t/2}" r="1.3" fill="{INK}"/>'); s.t(x+w+10,ly+2.5,lab,6.6,'start',600)
        yy+=t
    return yy
def sheet(name,num,swfn,sw_lab,sw_dim,layers,sec_lab,extra=None):
    s=Sheet(name,num,scale='SCALE: 3" = 1\'-0" (DETAIL)',north=False)
    swfn(s,SX,SY,SW,SH); s.t(SX,SY-6,sw_lab,7.5,'start',700)
    s.dim(SX,SY+SH,SX+SW,SY+SH,1,off=12,txt="SAMPLE 2'-0\" x 2'-0\"")
    s.t(186,SY-6,sec_lab,7.5,'start',700)
    bot=sect(s,layers,186,SY+6,62); s.t(186,bot+14,'CUT LAYERS, OUTSIDE TO IN' if 'WALL' in sec_lab or 'ROOF' in sec_lab else 'CUT LAYERS, TOP DOWN',6.5,'start',600,INK2)
    if extra: extra(s)
    return s.svg()
def ft_in(px): return f'{round(px/8,1):g}"'.replace('.0"','"')
P=PAPER
CARDS={
 (0,'A'):lambda:sheet('MATERIAL · PALE HINOKI-STYLE','M-101',lambda s,x,y,w,h:grain(s,x,y,w,h),'ELEVATION · VERTICAL BOARDS','',[(10,'url(#bpPlank)','HINOKI 1x6 T&G'),(6,'url(#bpH)','RAINSCREEN BATTEN'),(22,'url(#bpInsul)','INSULATION'),(22,'url(#bpConc)','POURED WALL')],'SECTION · WALL'),
 (0,'B'):lambda:sheet('MATERIAL · CHARRED TIMBER','M-101',lambda s,x,y,w,h:grain(s,x,y,w,h,dark=True),'ELEVATION · VERTICAL BOARDS','',[(10,'url(#bpCharr)','SHOU-SUGI-BAN 1x6'),(6,'url(#bpH)','RAINSCREEN BATTEN'),(22,'url(#bpInsul)','INSULATION'),(22,'url(#bpConc)','POURED WALL')],'SECTION · WALL'),
 (1,'A'):lambda:sheet('FLOOR · WIDE WOOD PLANKS','M-102',lambda s,x,y,w,h:tiles(s,x,y,w,h,100,15,P,True),'PLAN · 10" PLANKS, FULL LENGTH','',[(8,'url(#bpPlank)','OAK PLANK 3/4"'),(3,'url(#bpH)','UNDERLAY'),(12,'url(#bpH)','PLYWOOD SUBFLOOR'),(30,'url(#bpConc)','SLAB + RADIANT')],'SECTION · FLOOR'),
 (1,'B'):lambda:sheet('FLOOR · HONED STONE','M-102',lambda s,x,y,w,h:tiles(s,x,y,w,h,75,37.5,'url(#bpStip)',True),"PLAN · 24\"x48\" HONED STONE",'',[(10,'url(#bpStip)','STONE 3/4" HONED'),(5,'url(#bpH)','THINSET + MEMBRANE'),(8,P,'MORTAR BED'),(30,'url(#bpConc)','SLAB + RADIANT')],'SECTION · FLOOR'),
 (2,'A'):lambda:sheet('WALL · CLAY PLASTER','M-103',lambda s,x,y,w,h:(s.rect(x,y,w,h,'url(#bpStip)',1.4),s.path(f'M{x+10} {y+40}q30-10 60 0t60 0M{x+10} {y+100}q30-10 60 0t60 0',sw=.5,col=INK2)),'ELEVATION · HAND-TROWELLED','',[(5,'url(#bpStip)','CLAY FINISH 1/8"'),(8,'url(#bpStip)','CLAY BASE COAT'),(10,'url(#bpH)','GYPSUM BOARD'),(30,'url(#bpInsul)','STUDS + INSUL.')],'SECTION · PARTITION'),
 (2,'B'):lambda:sheet('WALL · WOOD SLATS','M-103',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#B9C0C8',0),s.rect(x,y,w,h,'url(#bpInsul)',0),[grain(s,x+k*15,y,10,h,10) for k in range(10)],s.rect(x,y,w,h,'none',1.4)),'ELEVATION · 1x2 SLATS @ 2"','',[(8,'url(#bpPlankV)','WOOD SLAT 1x2'),(6,'url(#bpInsul)','ACOUSTIC FELT'),(10,'url(#bpH)','GYPSUM BOARD'),(30,'url(#bpInsul)','STUDS + INSUL.')],'SECTION · PARTITION'),
 (3,'A'):lambda:sheet('ENGAWA · WOOD BOARDS','M-104',lambda s,x,y,w,h:tiles(s,x,y,w,h,90,12.5,P,True),'PLAN · 5" BOARDS, 1/4" GAPS','',[(8,'url(#bpPlank)','HARDWOOD 5/4x5'),(16,'url(#bpH)','SLEEPERS @ 16"'),(30,'url(#bpConc)','SLAB, SLOPED 1/8"/FT')],'SECTION · ENGAWA'),
 (3,'B'):lambda:sheet('ENGAWA · STONE PAVERS','M-104',lambda s,x,y,w,h:tiles(s,x,y,w,h,75,50,'url(#bpStip)'),"PLAN · 24\"x36\" PAVERS",'',[(12,'url(#bpStip)','STONE PAVER 1-1/4"'),(8,'url(#bpH)','PEDESTALS'),(30,'url(#bpConc)','SLAB, SLOPED 1/8"/FT')],'SECTION · ENGAWA'),
 (4,'A'):lambda:sheet('ROOF · DARK STANDING SEAM','M-105',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#B9C0C8',0),s.rect(x,y,w,h,'url(#bpSeam)',0),[s.line(x+k*16,y,x+k*16,y+h,1.4) for k in range(10)],s.rect(x,y,w,h,'none',1.4)),'ELEVATION · SEAMS @ 16" O.C.','',[(4,'url(#bpMetal)','STEEL PANEL, DARK'),(4,'url(#bpH)','UNDERLAYMENT'),(10,'url(#bpH)','SHEATHING'),(30,'url(#bpInsul)','RAFTERS + INSUL.')],'SECTION · ROOF'),
 (4,'B'):lambda:sheet('ROOF · CLAY TILE','M-105',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#E4E7EA',0),s.rect(x,y,w,h,'url(#bpClay)',0),s.rect(x,y,w,h,'none',1.4)),'ELEVATION · GREY CLAY TILE','',[(12,'url(#bpClay)','CLAY TILE ON BATTENS'),(4,'url(#bpH)','UNDERLAYMENT'),(10,'url(#bpH)','SHEATHING'),(30,'url(#bpInsul)','RAFTERS + INSUL.')],'SECTION · ROOF'),
 (5,'A'):lambda:sheet('COUNTER · STONE SLAB','M-106',lambda s,x,y,w,h:(s.path(f'M{x} {y+30}H{x+w}V{y+h}H{x+w-10}V{y+40}H{x}Z','url(#bpStip)',1.6),s.rect(x+10,y+40,w-30,h-40,'url(#bpPlankV)',.9),s.t(x+60,y+24,'WATERFALL EDGE',7,w=700)),'ELEVATION · ISLAND END','',[(10,'url(#bpStip)','STONE 1-1/4" HONED'),(6,'url(#bpH)','PLY SUBTOP'),(36,'url(#bpPlankV)','CABINET')],'SECTION · COUNTER'),
 (5,'B'):lambda:sheet('COUNTER · WOOD AND STEEL','M-106',lambda s,x,y,w,h:(s.rect(x,y+30,w,6,'url(#bpMetal)',1.6),grain(s,x,y+36,w,h-36,37.5),s.t(x+60,y+24,'STEEL TOP, OILED FRONTS',7,w=700)),'ELEVATION · RUN','',[(4,'url(#bpMetal)','STAINLESS 14 GA.'),(6,'url(#bpH)','PLY SUBTOP'),(36,'url(#bpPlankV)','OILED WOOD FRONT')],'SECTION · COUNTER'),
 (6,'A'):lambda:sheet('BATH · STONE AND WOOD','M-107',lambda s,x,y,w,h:(tiles(s,x,y+90,w,60,75,30,'url(#bpStip)'),grain(s,x+20,y+40,110,40,22),s.rect(x+50,y+30,50,10,P,1.2),s.t(x+75,y+22,'WOOD VANITY',7,w=700)),'ELEVATION · VANITY WALL','',[(10,'url(#bpStip)','STONE FLOOR 3/4"'),(6,'url(#bpH)','MEMBRANE'),(30,'url(#bpConc)','SLAB + RADIANT')],'SECTION · FLOOR'),
 (6,'B'):lambda:sheet('BATH · SOFT TILE','M-107',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#E3E9E4',0),tiles(s,x,y,w,h,12.5,12.5,'none'),),'ELEVATION · 4"x4" HANDMADE TILE','',[(4,'url(#bpTile)','TILE 3/8" GREEN-GREY'),(4,'url(#bpH)','THINSET'),(10,'url(#bpH)','CEMENT BOARD'),(30,'url(#bpInsul)','STUDS')],'SECTION · WALL'),
 (7,'A'):lambda:sheet('DOORS · SLIDING WOOD SCREENS','M-108',lambda s,x,y,w,h:([(s.rect(x+k*75,y,75,h,P,1.6),[s.line(x+k*75,y+j*25,x+k*75+75,y+j*25,.6) for j in range(1,6)],[s.line(x+k*75+j*18.75,y,x+k*75+j*18.75,y+h,.6) for j in range(1,4)]) for k in range(2)]),'ELEVATION · SCREEN PANELS','',[(10,'url(#bpPlankV)','WOOD FRAME 1-3/4"'),(4,P,'PAPER / RICE PANEL'),(10,'url(#bpPlankV)','POCKET IN WALL')],'PLAN · SLIDE INTO POCKET'),
 (7,'B'):lambda:sheet('DOORS · BIG GLASS SLIDERS','M-108',lambda s,x,y,w,h:([(s.rect(x+k*75,y,75,h,'url(#bpGlass)',1.6),s.rect(x+k*75+2,y+2,71,h-4,'none',.6)) for k in range(2)]),'ELEVATION · FULL-HEIGHT GLASS','',[(4,'url(#bpMetal)','THIN FRAME 1"'),(8,'url(#bpGlass)','TRIPLE GLAZING'),(4,'url(#bpMetal)','FLUSH TRACK')],'PLAN · SLIDER JAMB'),
 (8,'A'):lambda:sheet('HARDWARE · WARM BRASS','M-109',lambda s,x,y,w,h:handle(s,x,y,w,h,'#E8DDC2'),'ELEVATION · LEVER + ROSE','',[(6,'url(#bpMetal)','SOLID BRASS, BRUSHED'),(6,P,'UNLACQUERED, PATINAS'),(30,'url(#bpPlankV)','WOOD DOOR')],'SECTION · ROSE'),
 (8,'B'):lambda:sheet('HARDWARE · BLACK IRON','M-109',lambda s,x,y,w,h:handle(s,x,y,w,h,INK),'ELEVATION · LEVER + ROSE','',[(6,'url(#bpMetal)','IRON, MATTE BLACK'),(6,P,'WAX FINISH'),(30,'url(#bpPlankV)','WOOD DOOR')],'SECTION · ROSE'),
 (9,'A'):lambda:palette('PALETTE · LIGHT AND CALM',[('PALE WOOD',lambda s,x,y,w,h:grain(s,x,y,w,h,18)),('CLAY WALL',lambda s,x,y,w,h:s.rect(x,y,w,h,'url(#bpStip)',1.4)),('STONE',lambda s,x,y,w,h:tiles(s,x,y,w,h,36,24,'url(#bpStip)',True)),('BRASS',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#E8DDC2',0),s.rect(x,y,w,h,'url(#bpMetal)',1.4)))]),
 (9,'B'):lambda:palette('PALETTE · DARK AND WARM',[('CHARRED WOOD',lambda s,x,y,w,h:grain(s,x,y,w,h,18,True)),('DARK STONE',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#9AA4AE',0),tiles(s,x,y,w,h,36,24,'url(#bpStip)',True))),('IRON',lambda s,x,y,w,h:(s.rect(x,y,w,h,'#55606C',0),s.rect(x,y,w,h,'url(#bpMetal)',1.4))),('LINEN',lambda s,x,y,w,h:(s.rect(x,y,w,h,'url(#bpTile)',1.4)))]),
}
def handle(s,x,y,w,h,col):
    s.rect(x,y,w,h,'url(#bpPlankV)',1.2); cx,cy=x+40,y+75
    s.add(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{col}" stroke="{INK}" stroke-width="1.4"/><rect x="{cx-4}" y="{cy-5}" width="{w-55}" height="10" rx="5" fill="{col}" stroke="{INK}" stroke-width="1.4"/>')
    s.rect(cx-6,cy+28,12,22,col,1.2,rx=2); s.add(f'<circle cx="{cx}" cy="{cy+36}" r="2.5" fill="{PAPER}" stroke="{INK}"/>')
    s.dim(cx-4,cy+12,x+w-15,cy+12,1,off=22,txt='5-1/2"')
def palette(name,items):
    s=Sheet(name,'M-110',scale='MATERIAL LEGEND · NOT TO SCALE',north=False)
    for k,(lab,fn) in enumerate(items):
        x=14+k*86; fn(s,x,30,76,140); s.t(x+38,184,lab,7.5,w=700); s.t(x+38,194,f'MAT-{k+1:02d}',6.5,w=500,col=INK2)
    return s.svg()
def draw(i,side,o): return CARDS[(i,side)]()
