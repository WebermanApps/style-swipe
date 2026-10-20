# Construction-drawing SVG kit for Weberman Residence blueprint decks (Swatch, Oct 20 2026)
import math
INK='#2E3D4F'; INK2='#5B6B7C'; BG='#FBF8F1'; PAPER='#FFFFFF'; W,H=360,240
def ft(v):
    v=round(v*2)/2; f=int(v); i=int(round((v-f)*12))
    return f"{f}'-{i}\""
DEFS=f'''<defs>
<pattern id="bpH" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="bpEarth" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M0 10L10 0M-2 2L2 -2M8 12L12 8" stroke="{INK2}" stroke-width=".7"/><path d="M0 4L4 0" stroke="{INK2}" stroke-width=".5"/></pattern>
<pattern id="bpConc" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="3" cy="4" r=".8" fill="{INK2}"/><circle cx="10" cy="9" r=".6" fill="{INK2}"/><path d="M6 11l2 1.5-2.4.4z" fill="none" stroke="{INK2}" stroke-width=".5"/><circle cx="11" cy="2" r=".5" fill="{INK2}"/></pattern>
<pattern id="bpStip" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="2" r=".55" fill="{INK2}"/><circle cx="5.5" cy="6" r=".55" fill="{INK2}"/><circle cx="6" cy="1.5" r=".4" fill="{INK2}"/><circle cx="2.5" cy="6.5" r=".35" fill="{INK2}"/></pattern>
<pattern id="bpGrass" width="18" height="14" patternUnits="userSpaceOnUse"><path d="M3 10l1.5-3 1.5 3M12 4l1.5-3 1.5 3" fill="none" stroke="{INK2}" stroke-width=".5" opacity=".7"/></pattern>
<pattern id="bpGravel" width="10" height="5" patternUnits="userSpaceOnUse"><path d="M0 2.5q2.5-2 5 0t5 0" fill="none" stroke="{INK2}" stroke-width=".55"/></pattern>
<pattern id="bpWater" width="16" height="8" patternUnits="userSpaceOnUse"><path d="M1 4q3-2 6 0M9 7q3-2 6 0" fill="none" stroke="{INK2}" stroke-width=".6"/></pattern>
<pattern id="bpTile" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 0H8M0 0V8" stroke="{INK2}" stroke-width=".55"/></pattern>
<pattern id="bpTatami" width="24" height="12" patternUnits="userSpaceOnUse"><rect x=".5" y=".5" width="23" height="11" fill="none" stroke="{INK2}" stroke-width=".7"/><path d="M0 6H24" stroke="{INK2}" stroke-width=".25"/></pattern>
<pattern id="bpPlank" width="40" height="6" patternUnits="userSpaceOnUse"><path d="M0 6H40M14 0V6" stroke="{INK2}" stroke-width=".55"/></pattern>
<pattern id="bpPlankV" width="6" height="40" patternUnits="userSpaceOnUse"><path d="M6 0V40M0 22H6" stroke="{INK2}" stroke-width=".55"/></pattern>
<pattern id="bpDeck" width="5" height="30" patternUnits="userSpaceOnUse"><path d="M5 0V30" stroke="{INK2}" stroke-width=".6"/></pattern>
<pattern id="bpPaver" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 12H24M0 0V12M12 0V12" stroke="{INK2}" stroke-width=".6"/></pattern>
<pattern id="bpMetal" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="3" stroke="{INK}" stroke-width=".9"/></pattern>
<pattern id="bpGlass" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="3" stroke="{INK2}" stroke-width=".6"/></pattern>
<pattern id="bpCharr" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#B9C0C8"/><path d="M0 0V6" stroke="{INK}" stroke-width="1.6"/><path d="M3 1l1 1M3 4l1 1" stroke="{INK}" stroke-width=".6"/></pattern>
<pattern id="bpSeam" width="8" height="10" patternUnits="userSpaceOnUse"><path d="M8 0V10" stroke="{INK}" stroke-width=".9"/></pattern>
<pattern id="bpClay" width="12" height="7" patternUnits="userSpaceOnUse"><path d="M0 7q3-6 6 0q3-6 6 0" fill="none" stroke="{INK}" stroke-width=".7"/></pattern>
<pattern id="bpInsul" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M0 5q2.5-5 5 0t5 0" fill="none" stroke="{INK2}" stroke-width=".7"/></pattern>
</defs>'''
class Sheet:
    def __init__(s,name,num='A-101',scale='SCALE: 1/8" = 1\'-0"',north=True,nx=338,ny=26):
        s.e=[];s.name=name;s.num=num;s.scale=scale;s.north=north;s.nx=nx;s.ny=ny
    def add(s,x): s.e.append(x); return s
    def t(s,x,y,txt,sz=8,anc='middle',w=600,col=INK,rot=0,ital=False):
        txt=str(txt).replace('&','&amp;'); sz=round(sz*1.12,2); tr=f' transform="rotate({rot} {x} {y})"' if rot else ''
        st=' font-style="italic"' if ital else ''
        return s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" text-anchor="{anc}" font-weight="{w}" fill="{col}" stroke="{BG}" stroke-width="2.6" paint-order="stroke" stroke-linejoin="round"{st}{tr}>{txt}</text>')
    def line(s,x1,y1,x2,y2,w=1,col=INK,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>')
    def rect(s,x,y,w,h,fill='none',sw=1,col=INK,dash=None,rx=0):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{d}/>')
    def path(s,d,fill='none',sw=1,col=INK,dash=None):
        dd=f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{dd} stroke-linejoin="round"/>')
    # thick poured wall (hatched) along an axis
    def wall(s,x1,y1,x2,y2,t=6):
        if y1==y2: x,y,w,h=min(x1,x2)-t/2,y1-t/2,abs(x2-x1)+t,t
        else: x,y,w,h=x1-t/2,min(y1,y2)-t/2,t,abs(y2-y1)+t
        s.rect(x,y,w,h,PAPER,0); return s.rect(x,y,w,h,'url(#bpH)',1.4)
    def walls(s,pts,t=6,close=True):
        P=pts+([pts[0]] if close else [])
        for a,b in zip(P,P[1:]): s.wall(a[0],a[1],b[0],b[1],t)
        return s
    def part(s,x1,y1,x2,y2,w=1.5): return s.line(x1,y1,x2,y2,w)
    def gap(s,x1,y1,x2,y2,t=7):  # clear an opening in a wall
        if y1==y2: return s.rect(min(x1,x2),y1-t/2-.8,abs(x2-x1),t+1.6,BG,0)
        return s.rect(x1-t/2-.8,min(y1,y2),t+1.6,abs(y2-y1),BG,0)
    def door(s,hx,hy,r,a0,a1,t=6,wall=True):
        # hinge at (hx,hy); leaf drawn at angle a1 (deg), arc from a0 to a1; opening along a0
        ex,ey=hx+r*math.cos(math.radians(a0)),hy+r*math.sin(math.radians(a0))
        lx,ly=hx+r*math.cos(math.radians(a1)),hy+r*math.sin(math.radians(a1))
        if wall: s.gap(hx,hy,ex,ey,t+.5)
        sweep=1 if (a1-a0)%360<180 else 0
        s.path(f'M{ex:.1f} {ey:.1f}A{r} {r} 0 0 {1-sweep} {lx:.1f} {ly:.1f}',sw=.7,col=INK2)
        return s.line(hx,hy,lx,ly,1.6)
    def win(s,x1,y1,x2,y2,t=6):
        s.gap(x1,y1,x2,y2,t)
        if y1==y2:
            s.rect(min(x1,x2),y1-t/2,abs(x2-x1),t,PAPER,.9)
            for o in (-t/2,0,t/2): s.line(x1,y1+o,x2,y2+o,.8)
        else:
            s.rect(x1-t/2,min(y1,y2),t,abs(y2-y1),PAPER,.9)
            for o in (-t/2,0,t/2): s.line(x1+o,y1,x2+o,y2,.8)
        return s
    def room(s,x,y,name,size=None,sz=8.5):
        s.t(x,y,name,sz,w=700)
        if size: s.t(x,y+sz+1.5,size,sz-1.5,w=500,col=INK2)
        return s
    def dim(s,x1,y1,x2,y2,f,off=-10,txt=None,sz=7.5):
        L=math.hypot(x2-x1,y2-y1); txt=txt or ft(L/f); sg=1 if off>0 else -1
        if y1==y2:
            y=y1+off; s.line(x1,y,x2,y,.7)
            for x in (x1,x2): s.line(x,y1+sg*2,x,y+sg*3,.5,INK2); s.line(x-2.5,y+2.5,x+2.5,y-2.5,1.3)
            s.rect((x1+x2)/2-len(txt)*2.2,y-sz,len(txt)*4.4,sz-1,BG,0)
            return s.t((x1+x2)/2,y-2,txt,sz,w=500)
        x=x1+off; s.line(x,y1,x,y2,.7)
        for y in (y1,y2): s.line(x1+sg*2,y,x+sg*3,y,.5,INK2); s.line(x-2.5,y+2.5,x+2.5,y-2.5,1.3)
        s.rect(x-sz,(y1+y2)/2-len(txt)*2.2,sz-1,len(txt)*4.4,BG,0)
        return s.t(x-2,(y1+y2)/2,txt,sz,w=500,rot=-90)
    def grid(s,x=None,y=None,lab='1',a=14,b=200,r=6):
        if x is not None:
            s.line(x,a+r,x,b,.5,INK2,'6 2 1 2'); s.add(f'<circle cx="{x}" cy="{a}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width=".9"/>'); return s.t(x,a+2.6,lab,7.5)
        s.line(a+r,y,b,y,.5,INK2,'6 2 1 2'); s.add(f'<circle cx="{a}" cy="{y}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width=".9"/>'); return s.t(a,y+2.6,lab,7.5)
    def arrow(s,d,col='#B5562F',w=1.4):
        s.path(d,sw=w,col=col,dash='4 2.5'); return s
    def head(s,x,y,ang,col='#B5562F'):
        a=math.radians(ang); p=[(x,y),(x-7*math.cos(a)+3.5*math.sin(a),y-7*math.sin(a)-3.5*math.cos(a)),(x-7*math.cos(a)-3.5*math.sin(a),y-7*math.sin(a)+3.5*math.cos(a))]
        return s.add('<path d="M%.1f %.1fL%.1f %.1fL%.1f %.1fz" fill="%s"/>'%(p[0]+p[1]+p[2]+(col,)))
    def note(s,x,y,txt,tx,ty,anc='start'):
        s.line(x,y,tx,ty,.6,INK2); s.add(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{INK}"/>')
        return s.t(tx+(2 if anc=='start' else -2),ty+3,txt,7.5,anc,500)
    def ground(s,x1,x2,y,depth=10):
        s.rect(x1,y,x2-x1,depth,'url(#bpEarth)',0); return s.line(x1,y,x2,y,1.8)
    def level(s,x,y,txt):
        s.add(f'<g><circle cx="{x}" cy="{y}" r="3.2" fill="{PAPER}" stroke="{INK}" stroke-width=".8"/><path d="M{x} {y-3.2}A3.2 3.2 0 0 1 {x+3.2} {y}H{x}zM{x} {y+3.2}A3.2 3.2 0 0 1 {x-3.2} {y}H{x}z" fill="{INK}"/></g>')
        s.line(x+4,y,x+16,y,.6,INK2,'3 2'); return s.t(x+18,y-3,txt,7,'start',500)
    def cut(s,x,y1,y2,lab='A'):
        s.line(x,y1,x,y2,.9,INK,'10 3 2 3')
        for y,d in ((y1,-1),(y2,1)):
            s.add(f'<circle cx="{x}" cy="{y+d*6}" r="5.5" fill="{PAPER}" stroke="{INK}" stroke-width=".9"/><path d="M{x-5.5} {y+d*6}H{x+5.5}" stroke="{INK}" stroke-width=".6"/>')
            s.t(x,y+d*6-1,lab,5.5); s.t(x,y+d*6+5,'A-3',4.5,w=500)
        return s
    def tree(s,x,y,r=14):
        s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK2}" stroke-width=".8" stroke-dasharray="3 1.5"/><circle cx="{x}" cy="{y}" r="1.6" fill="{INK2}"/>')
        return s.path(f'M{x-r*.6} {y}H{x+r*.6}M{x} {y-r*.6}V{y+r*.6}',sw=.5,col=INK2)
    def svg(s):
        nb=''
        if s.north:
            x,y=s.nx,s.ny
            nb=f'<g><circle cx="{x}" cy="{y}" r="9" fill="{PAPER}" stroke="{INK}" stroke-width=".9"/><path d="M{x} {y-8}L{x+4} {y+6}L{x} {y+3}z" fill="{INK}"/><path d="M{x} {y-8}L{x-4} {y+6}L{x} {y+3}z" fill="none" stroke="{INK}" stroke-width=".8"/><text x="{x}" y="{y-11}" font-size="7.5" font-weight="700" text-anchor="middle" fill="{INK}">N</text></g>'
        tb=(f'<g><rect x="6" y="206" width="348" height="29" fill="{PAPER}" stroke="{INK}" stroke-width="1"/><line x1="196" y1="206" x2="196" y2="235" stroke="{INK}" stroke-width=".8"/><line x1="318" y1="206" x2="318" y2="235" stroke="{INK}" stroke-width=".8"/>'
            f'<text x="12" y="218" font-size="7.5" font-weight="700" fill="{INK}" letter-spacing=".2">{s.name}</text><text x="12" y="230" font-size="7" font-weight="500" fill="{INK2}">{s.scale}</text>'
            f'<text x="202" y="218" font-size="8" font-weight="700" fill="{INK}" letter-spacing=".3">WEBERMAN RESIDENCE</text><text x="202" y="230" font-size="7" font-weight="500" fill="{INK2}">BLUEPRINT · OCT 20</text>'
            f'<text x="336" y="219" font-size="6.5" font-weight="500" text-anchor="middle" fill="{INK2}">SHEET</text><text x="336" y="231" font-size="8.5" font-weight="700" text-anchor="middle" fill="{INK}">{s.num}</text></g>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Construction drawing" font-family="Helvetica,Arial,sans-serif" style="display:block;background:{BG}">'
                f'<rect width="{W}" height="{H}" fill="{BG}"/><rect x="3" y="3" width="354" height="234" fill="none" stroke="{INK}" stroke-width=".6"/>{DEFS}'+''.join(s.e)+nb+tb+'</svg>')
