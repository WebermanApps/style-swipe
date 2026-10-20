from bp import *
f=2.6; CX,CY=180-18*2.6,58; CW,CH=36*f,28*f; D=15*f  # courtyard origin & wing depth
def base(name):
    s=Sheet(name,'A-100'); return s
def wingN(s,x0,x1,lbl='LIVING / KITCHEN'):
    y0=CY-D; s.walls([(x0,y0),(x1,y0),(x1,CY),(x0,CY)],5)
    for w in (x0+12,x1-30): s.win(w,y0,w+16,y0,5)
    s.part((x0+x1)/2+10,y0,(x0+x1)/2+10,CY); s.door((x0+x1)/2+10,CY-2,9,-90,-180,wall=False)
    s.win(CX+6,CY,CX+CW-6,CY,5)
    s.room((x0+x1)/2-12,y0+D/2+2,lbl.split(' / ')[0],ft((x1-x0)/f).split('-')[0]+"x15'",7.5)
def wingW(s,y0,y1,lbl='KIDS'):
    x0=CX-D; s.walls([(x0,y0),(CX,y0),(CX,y1),(x0,y1)],5)
    s.part(x0,(y0+y1)/2,CX,(y0+y1)/2); s.win(x0,y0+10,x0,y0+24,5); s.door(CX,(y0+y1)/2+4,9,90,180)
    s.room(x0+D/2,(y0+y1)/2-12,lbl,"15'x"+ft((y1-y0)/f).split('-')[0],7.5)
def wingE(s,y0,y1,lbl='PRIMARY'):
    x0=CX+CW; s.walls([(x0,y0),(x0+D,y0),(x0+D,y1),(x0,y1)],5)
    s.win(x0+D,y0+12,x0+D,y0+28,5); s.door(x0,(y0+y1)/2-4,9,-90,0)
    s.room(x0+D/2,(y0+y1)/2+2,lbl,"15'x"+ft((y1-y0)/f).split('-')[0],7.5)
def wingS(s,x0,x1,y0,lbl='WELLNESS'):
    s.walls([(x0,y0),(x1,y0),(x1,y0+D),(x0,y0+D)],5); s.part(x0+30,y0,x0+30,y0+D)
    s.door(x0+30,y0+D-2,8,-90,-180,wall=False); s.win(x1-30,y0+D,x1-12,y0+D,5)
    s.room((x0+x1)/2+12,y0+D/2+2,lbl,ft((x1-x0)/f).split('-')[0]+"x15'",7.5)
def yard(s,open_s=True):
    s.rect(CX+3,CY+3,CW-6,CH-6,'url(#bpGravel)',0)
    s.rect(CX+5,CY+5,CW-10,CH-10,'none',.5,INK2,'3 2'); s.t(CX+CW/2,CY+CH/2-2,'COURTYARD',8,w=700); s.t(CX+CW/2,CY+CH/2+8,"36'-0\" x 28'-0\"",7,w=500,col=INK2)
    s.dim(CX,CY+CH,CX+CW,CY+CH,f,off=14 if open_s else 0) if open_s else None
    s.grid(x=CX,lab='B',a=12,b=196); s.grid(x=CX+CW,lab='C',a=12,b=196); s.grid(y=CY,lab='1',a=16,b=300); s.grid(y=CY+CH,lab='2',a=16,b=300)
def pool(s,y):
    s.rect(CX+10,y,CW-20,14,'url(#bpWater)',1.2); s.t(CX+CW/2,y+24,"POOL 30'-0\" x 6'-0\"",7,w=500,col=INK2)
def loft(s,x,y,w,h):
    s.rect(x+4,y+4,w-8,h-8,'none',.9,INK,'5 3'); s.path(f'M{x+4} {y+4}L{x+w-4} {y+h-4}M{x+w-4} {y+4}L{x+4} {y+h-4}',sw=.5,col=INK2,dash='4 3')
    s.t(x+w/2,y+h-9,"LOFT ABOVE",6.8,w=700)
def L_loft():
    s=base('COURTYARD PLAN · L + KIDS\' LOFT'); y1=CY+CH+D
    wingN(s,CX-D,CX+CW); wingW(s,CY,y1,'KIDS'); loft(s,CX-D,CY+CH/2,D,CH/2+D); yard(s); s.note(CX+CW+2,CY+CH/2,'OPEN',CX+CW+10,CY+CH/2-14); s.note(CX+CW/2,CY+CH+2,'OPEN TO POOL',CX+CW/2+20,CY+CH+30)
    s.dim(CX-D,CY-D,CX+CW,CY-D,f,off=-8); return s
def U():
    s=base('COURTYARD PLAN · OPEN U'); y1=CY+CH
    wingN(s,CX-D,CX+CW+D); wingW(s,CY,y1+D*0.6); wingE(s,CY,y1+D*0.6); yard(s); pool(s,CY+CH+D*.6+12)
    s.dim(CX-D,CY-D,CX+CW+D,CY-D,f,off=-8); return s
def O(loftp=False):
    s=base("COURTYARD PLAN · O"+(" + KIDS' LOFT" if loftp else ", FOUR WINGS"))
    wingN(s,CX-D,CX+CW+D); wingW(s,CY,CY+CH); wingE(s,CY,CY+CH); wingS(s,CX-D,CX+CW+D,CY+CH); yard(s,False)
    s.dim(CX-D,CY-D,CX+CW+D,CY-D,f,off=-8); s.dim(CX+CW+D,CY-D,CX+CW+D,CY+CH+D,f,off=10)
    s.path(f'M{CX} {CY+6}H{CX+CW}',sw=.5,col=INK2,dash='2 2')
    if loftp: loft(s,CX-D,CY,D,CH)
    else: s.t(CX+CW/2,CY+12,'ENGAWA',6.8,w=700,col=INK2)
    return s
def U_link():
    s=base('COURTYARD PLAN · U + LINKED WING'); y1=CY+CH
    wingN(s,CX-D,CX+CW+D); wingW(s,CY,y1); wingE(s,CY,y1); yard(s,False)
    ys=y1+18; wingS(s,CX-6,CX+CW+6,ys,'POOL + WELLNESS')
    s.rect(CX+CW/2-9,y1+2.5,18,ys-y1-5,'url(#bpDeck)',.9); s.note(CX+CW/2+9,y1+9,"ENGAWA LINK 7'-6\"",CX+CW+D-2,y1+9)
    s.dim(CX-D,CY-D,CX+CW+D,CY-D,f,off=-8); return s
def decide():
    s=base('COURTYARD PLAN · BLUEPRINT TBD')
    for (x,y,w,h) in ((CX-D,CY-D,CW+2*D,D),(CX-D,CY,D,CH),(CX+CW,CY,D,CH),(CX-D,CY+CH,CW+2*D,D)):
        s.rect(x,y,w,h,'none',.9,INK2,'5 3')
    yard(s,False); s.t(CX+CW/2,CY-D/2+3,'WINGS TBD',8,w=700,col=INK2); s.t(CX+CW/2,CY+CH+D/2+3,'PER SHAPING PICKS',7.5,w=600,col=INK2)
    s.dim(CX-D,CY-D,CX+CW+D,CY-D,f,off=-8,txt="66'-0\" MAX"); return s
MAP={"L + kids' loft":L_loft,"Open U":U,"Closed O, four wings":O,"U + linked fourth wing":U_link,"O + kids' loft":lambda:O(True),"Machan decides":decide}
def draw(card,side,o): return MAP[o['label']]().svg()
