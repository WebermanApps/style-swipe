#!/usr/bin/env python3
"""Build Style Swipe deck smart-upkeep-1 (40 pairs, ~30 logo pairs) and save every logo/application SVG to
/workspace/brand/smart-upkeep/logos/. Run from the style-swipe repo root."""
import json, os, random, datetime as dt
DID="smart-upkeep-1"; OUT="/workspace/brand/smart-upkeep/logos"
TEAL="#4F8A8B"; LAGOON="#05668D"; JUNGLE="#0B6E4F"; TERRA="#C1502E"; INK="#1F1F1F"; CREAM="#FAF6EE"; GREY="#737373"
FONTS={"khand":("Khand",700),"hind":("Hind",600),"inter":("Inter",700),"dmsans":("DM Sans",700),"manrope":("Manrope",800),"outfit":("Outfit",700),"worksans":("Work Sans",600)}
# ---- symbols, drawn in a 48x48 box ----
def sym(kind,c,ink=INK,sw=4):
    S={
    "house-check":f'<path d="M6 22 L24 7 L42 22 V42 H6 Z" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/><path d="M15 27 L21 33 L33 21" fill="none" stroke="{c}" stroke-width="{sw+.5}" stroke-linecap="round" stroke-linejoin="round"/>',
    "roofline":f'<path d="M4 28 L24 10 L44 28" fill="none" stroke="{ink}" stroke-width="{sw+1}" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 36 H36" stroke="{c}" stroke-width="{sw+1}" stroke-linecap="round"/>',
    "wrench":f'<path d="M30 8 a9 9 0 0 0 -8 12 L8 34 a4 4 0 0 0 6 6 L28 26 a9 9 0 0 0 12 -8 l-6 2 -4 -4 2 -6 Z" fill="{c}"/>',
    "monthly-dot":f'<rect x="7" y="10" width="34" height="31" rx="5" fill="none" stroke="{ink}" stroke-width="{sw}"/><path d="M7 19 H41 M16 6 V13 M32 6 V13" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/><circle cx="31" cy="31" r="5" fill="{c}"/>',
    "filter-grid":"".join(f'<rect x="{8+i*11}" y="{8+j*11}" width="9" height="9" rx="1.5" fill="{c if (i,j)==(2,0) else ink}"/>' for i in range(3) for j in range(3)),
    "drop":f'<path d="M24 5 C24 5 10 21 10 30 a14 14 0 0 0 28 0 C38 21 24 5 24 5 Z" fill="none" stroke="{ink}" stroke-width="{sw}"/><path d="M18 31 L23 36 L31 27" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>',
    "leaf":f'<path d="M8 40 C8 18 22 8 42 8 C42 28 30 40 8 40 Z" fill="{c}"/><path d="M10 38 L30 18" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
    "su":f'<rect x="3" y="3" width="42" height="42" rx="10" fill="none" stroke="{ink}" stroke-width="{sw}"/><text x="24" y="33" text-anchor="middle" font-family="Khand" font-weight="700" font-size="26" fill="{ink}">S<tspan fill="{c}">U</tspan></text>',
    "key":f'<circle cx="16" cy="24" r="9" fill="none" stroke="{ink}" stroke-width="{sw}"/><path d="M25 24 H43 M37 24 V31 M42 24 V29" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
    "house-dot":f'<path d="M6 22 L24 7 L42 22 V42 H6 Z" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/><circle cx="24" cy="30" r="6" fill="{c}"/>',
    "check-ring":f'<circle cx="24" cy="24" r="19" fill="none" stroke="{ink}" stroke-width="{sw}"/><path d="M15 25 L21 31 L33 18" fill="none" stroke="{c}" stroke-width="{sw+.5}" stroke-linecap="round" stroke-linejoin="round"/>',
    "crest":f'<path d="M24 3 L42 10 V24 C42 35 33 42 24 45 C15 42 6 35 6 24 V10 Z" fill="#1E1B16" stroke="#C9A24A" stroke-width="2.5"/><text x="24" y="31" text-anchor="middle" font-family="Georgia,serif" font-size="16" fill="#C9A24A">SU</text>',
    }
    return S[kind]
def casefy(t,case): return t.upper() if case=="upper" else t.lower() if case=="lower" else t
def wordmark(font="khand",case="title",layout="line",accent=None,c=TEAL,ink=INK,size=34,track=None):
    fam,w=FONTS[font]; a,b=casefy("Smart",case),casefy("Upkeep",case)
    tr=track if track is not None else (2 if case=="upper" else 0)
    ca=ink; cb=c if accent=="second" else ink
    if layout=="stack": return f'<text font-family="{fam}" font-weight="{w}" font-size="{size}" letter-spacing="{tr}" fill="{ca}"><tspan x="0" dy="0">{a}</tspan><tspan x="0" dy="{size*.95:.0f}" fill="{cb}">{b}</tspan></text>', size*1.95
    sep=" " if case!="lower" or True else ""
    return f'<text font-family="{fam}" font-weight="{w}" font-size="{size}" letter-spacing="{tr}" fill="{ca}">{a}{sep}<tspan fill="{cb}">{b}</tspan></text>', size
def approx_w(font,case,layout,size,track):
    k={"khand":.42,"hind":.55,"inter":.6,"dmsans":.58,"manrope":.62,"outfit":.56,"worksans":.58}[font]*(1.12 if case=="upper" else 1)
    n=6 if layout=="stack" else 12
    return n*size*k+n*track
def logo_svg(symbol=None,c=TEAL,font="khand",case="title",layout="line",accent=None,ink=INK,size=34,track=None,bg="none",sym_side="left"):
    tr=track if track is not None else (2 if case=="upper" else 0)
    wm,h=wordmark(font,case,layout,accent,c,ink,size,tr); ww=approx_w(font,case,layout,size,tr)
    ss=h*1.05 if layout=="stack" else size*1.25
    if symbol and sym_side=="top":
        W=max(ww,ss)+20; H=ss+h+26
        body=f'<g transform="translate({(W-ss)/2:.1f},8) scale({ss/48:.3f})">{sym(symbol,c,ink)}</g><g transform="translate({(W-ww)/2:.1f},{ss+12+size*.8:.1f})">{wm}</g>'
    else:
        off=(ss+12) if symbol else 0; W=off+ww+16; H=max(ss,h)+16
        body=(f'<g transform="translate(8,{(H-ss)/2:.1f}) scale({ss/48:.3f})">{sym(symbol,c,ink)}</g>' if symbol else "")+f'<g transform="translate({8+off:.1f},{(H-h)/2+size*.8:.1f})">{wm}</g>'
    rect=f'<rect width="100%" height="100%" fill="{bg}"/>' if bg!="none" else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">{rect}{body}</svg>'
def icon_svg(symbol,c,mode="white",r=22):
    bg,ink,acc={"white":("#FFFFFF",INK,c),"fill":(c,"#FFFFFF","#FFFFFF"),"cream":(CREAM,INK,c)}[mode]
    stroke='' if mode!="white" else ' stroke="#E5E5E5" stroke-width="2"'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"><rect x="1" y="1" width="98" height="98" rx="{r}" fill="{bg}"{stroke}/><g transform="translate(22,22) scale(1.17)">{sym(symbol,acc,ink)}</g></svg>'
def inner(svg):  # strip outer svg for nesting
    a=svg.index(">")+1; return svg[a:-6], svg[svg.index('viewBox="')+9:].split('"')[0]
def nest(svg,x,y,w):
    body,vb=inner(svg); _,_,W,H=map(float,vb.split()); h=w*H/W
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{vb}">{body}</svg>', h
def app_scene(kind,logo,icon,c):
    if kind=="van":
        lg,_=nest(logo,40,52,150)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="{CREAM}"/><path d="M14 40 Q14 26 28 26 H196 L246 66 H284 Q290 66 290 74 V136 H14 Z" fill="#FFFFFF" stroke="#BDBDBD" stroke-width="2"/><path d="M198 32 L240 66 H198 Z" fill="#D5DEE2"/><rect x="14" y="118" width="276" height="5" fill="{c}"/><rect x="196" y="70" width="2" height="62" fill="#BDBDBD"/>{lg}<text x="42" y="112" font-family="Hind" font-size="10" fill="{GREY}">Monthly home maintenance · smartupkeep.com</text><circle cx="70" cy="138" r="17" fill="#333"/><circle cx="240" cy="138" r="17" fill="#333"/></svg>'
    if kind=="polo":
        ic,_=nest(icon,170,62,24)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="{CREAM}"/><path d="M95 22 L125 12 Q150 30 175 12 L205 22 L250 58 L228 86 L210 72 V166 H90 V72 L72 86 L50 58 Z" fill="#F4F1EA" stroke="#BDBDBD" stroke-width="2"/><path d="M135 14 L150 40 L165 14" fill="none" stroke="#BDBDBD" stroke-width="2"/>{ic}<text x="182" y="98" text-anchor="middle" font-family="Khand" font-weight="700" font-size="9" fill="{INK}">SMART UPKEEP</text></svg>'
    if kind=="sign":
        lg,h=nest(logo,85,40,130)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="#E9F0E4"/><rect y="140" width="300" height="30" fill="#9DBB8A"/><path d="M95 120 V166 M205 120 V166" stroke="#888" stroke-width="3"/><rect x="72" y="26" width="156" height="98" rx="4" fill="#FFFFFF" stroke="#CCCCCC"/>{lg}<text x="150" y="{48+h:.0f}" text-anchor="middle" font-family="Hind" font-weight="600" font-size="10" fill="{INK}">This home is looked after monthly</text><rect x="72" y="112" width="156" height="12" fill="{c}"/></svg>'
    if kind=="phone":
        ic,_=nest(icon,148,96,38)
        apps="".join(f'<rect x="{62+(i%4)*43}" y="{54+(i//4)*42}" width="38" height="38" rx="9" fill="{col}"/>' for i,col in enumerate(["#D8D8D8","#CFE3F7","#F8D9C4","#DDEDD5","#E9E4F5","#F5E9C8","#D8D8D8"]) if i!=6)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="{CREAM}"/><rect x="50" y="8" width="200" height="200" rx="26" fill="#EEF3F6" stroke="#9E9E9E" stroke-width="3"/><text x="150" y="36" text-anchor="middle" font-family="Hind" font-weight="600" font-size="12" fill="{INK}">9:41</text>{apps}{ic}<text x="167" y="146" text-anchor="middle" font-family="Hind" font-size="8" fill="{INK}">Smart Upkeep</text></svg>'
    if kind=="sizes":
        a,_=nest(icon,20,40,96); b,_=nest(icon,140,72,32); d,_=nest(icon,196,80,16)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="{CREAM}"/>{a}{b}{d}<rect x="230" y="70" width="60" height="36" rx="6" fill="#FFFFFF" stroke="#DDD"/><svg x="236" y="80" width="16" height="16" viewBox="0 0 100 100">{inner(icon)[0]}</svg><text x="256" y="92" font-family="Hind" font-size="8" fill="{INK}">Smart…</text><text x="20" y="152" font-family="Hind" font-size="10" fill="{GREY}">96 · 32 · 16 px, and a browser tab</text></svg>'
    if kind=="lockup-a":
        lg,h=nest(logo,16,44,160)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="#FFFFFF"/>{lg}<rect x="184" y="48" width="1.5" height="{h-8:.0f}" fill="#CCCCCC"/><text x="194" y="{44+h*.62:.0f}" font-family="Hind" font-weight="600" font-size="16" fill="{c}">Home Record</text><text x="16" y="140" font-family="Hind" font-size="10" fill="{GREY}">Company | product, side by side</text></svg>'
    if kind=="lockup-b":
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170"><rect width="300" height="170" fill="#FFFFFF"/><text x="150" y="70" text-anchor="middle" font-family="Khand" font-weight="700" font-size="40" fill="{INK}">Home Record</text><text x="150" y="96" text-anchor="middle" font-family="Hind" font-weight="600" font-size="12" letter-spacing="2" fill="{GREY}">BY SMART UPKEEP</text><rect x="120" y="108" width="60" height="3" fill="{c}"/><text x="150" y="146" text-anchor="middle" font-family="Hind" font-size="10" fill="{GREY}">Product first, company as endorsement</text></svg>'
saved={}
def save(name,svg):
    open(f"{OUT}/{name}.svg","w").write(svg); saved[name]=svg; return svg
def L(i,label,desc,tags,feel,svg,bg="#FFFFFF"):
    save(i,svg); return {"id":"su1_"+i,"label":label,"desc":desc,"tags":tags+[feel],"feeling":feel,"file":f"{OUT}/{i}.svg","visual":{"type":"hm","m":"svg","svg":svg,"bg":bg}}
pairs=[]
def add(cat,a,b,ask=None,purpose="refine"): pairs.append({"category":cat,"app":"Smart Upkeep","ask":ask,"optionA":a,"optionB":b,"purpose":purpose})
LG="Logo: Wordmark"
# --- wordmark fonts (6) ---
add(LG,L("wm_khand_title","Khand, Title Case","Condensed Khand, 'Smart Upkeep'. Max's brand face.",["clear","direct"],"crew",logo_svg(font="khand")),
       L("wm_hind_title","Hind, Title Case","Rounder Hind semibold, softer.",["friendly","calm"],"neighbor",logo_svg(font="hind",size=30)),"Which Wordmark Font?")
add(LG,L("wm_inter_title","Inter, Title Case","Neutral modern sans, very 'app'.",["clear","modern"],"system",logo_svg(font="inter",size=28)),
       L("wm_dmsans_title","DM Sans, Title Case","Geometric, friendly round letters.",["friendly","modern"],"neighbor",logo_svg(font="dmsans",size=28)),"Which Wordmark Font?")
add(LG,L("wm_manrope_title","Manrope, Title Case","Wide, calm, a bit premium-quiet.",["calm","premium-quiet"],"concierge",logo_svg(font="manrope",size=26)),
       L("wm_outfit_title","Outfit, Title Case","Clean geometric, simple and light.",["minimal","clear"],"system",logo_svg(font="outfit",size=28)),"Which Wordmark Font?")
# --- case (4) ---
add(LG,L("wm_khand_upper","SMART UPKEEP (Caps)","All caps Khand, tracked out.",["direct","bold"],"crew",logo_svg(font="khand",case="upper",size=30)),
       L("wm_khand_lower","smart upkeep (Lowercase)","All lowercase, relaxed.",["friendly","casual"],"neighbor",logo_svg(font="khand",case="lower")),"Which Case?")
add(LG,L("wm_hind_upper","SMART UPKEEP In Hind Caps","Hind caps, wide tracking, quiet.",["calm","premium-quiet"],"concierge",logo_svg(font="hind",case="upper",size=24,track=4)),
       L("wm_inter_lower","smart upkeep In Inter Lowercase","Lowercase Inter, tech-app feel.",["modern","minimal"],"system",logo_svg(font="inter",case="lower",size=28)),"Which Case?")
# --- one-line vs stacked (3) ---
add(LG,L("lay_line_house","One Line With House-Check","Mark left, name on one line.",["clear","organized"],"system",logo_svg("house-check")),
       L("lay_stack_house","Stacked With House-Check","Mark left, Smart over Upkeep.",["compact","bold"],"crew",logo_svg("house-check",layout="stack",size=26)),"One Line Or Stacked?")
add(LG,L("lay_top_roof","Mark On Top, Centered","Roofline above a centered name.",["calm","balanced"],"concierge",logo_svg("roofline",sym_side="top",size=30)),
       L("lay_line_roof","Roofline, One Line","Roofline left of the name.",["clear","direct"],"system",logo_svg("roofline")),"Which Layout?")
add(LG,L("lay_accent_second","Upkeep In Teal","Two-tone: 'Upkeep' in the accent.",["clear","friendly"],"neighbor",logo_svg(accent="second")),
       L("lay_mono","All Black","Single color, no accent in the word.",["minimal","direct"],"crew",logo_svg()),"Two-Tone Or One Color?")
# --- symbols (10) ---
S2="Logo: Symbol"
def SL(k,label,desc,tags,feel,c=TEAL): return L("sym_"+k+("" if c==TEAL else "_"+c[1:]),label,desc,tags,feel,logo_svg(k,c=c))
add(S2,SL("house-check","House + Check","Outline house with a teal check.",["clear","friendly"],"system"),SL("roofline","Roofline + Ground Line","Just a roof and a line: abstract.",["minimal","calm"],"concierge"),"Which Symbol?")
add(S2,SL("wrench","Wrench","Solid wrench: trade, hands-on.",["industrial","direct"],"crew"),SL("monthly-dot","Calendar + Monthly Dot","Calendar with one dot: the monthly visit.",["organized","clear"],"system"),"Which Symbol?")
add(S2,SL("filter-grid","Filter Grid","3x3 grid, one cell teal: a filter, a checklist.",["organized","modern"],"system"),SL("drop","Drop + Check","Water drop with a check: water heater, leaks.",["calm","natural"],"neighbor"),"Which Symbol?")
add(S2,SL("leaf","Leaf","A leaf: natural, low-key.",["natural","calm"],"neighbor",JUNGLE),SL("su","SU Monogram","S and U in a rounded square.",["bold","modern"],"crew"),"Which Symbol?")
add(S2,SL("key","Key","A simple key: trusted with your house.",["calm","personal"],"concierge"),SL("house-dot","House + Dot","House outline with one solid dot.",["minimal","calm"],"system"),"Which Symbol?")
add(S2,SL("check-ring","Check In A Ring","Plain check in a circle: 'done'.",["clear","direct"],"crew"),L("sym_none","No Symbol, Name Only","Wordmark alone, no mark.",["minimal","direct"],"system",logo_svg(font="khand",case="upper",size=30)),"Symbol Or Name Only?")
add(S2,L("sym_house_su","House-Check vs SU: House","House + check mark.",["clear","friendly"],"neighbor",logo_svg("house-check",font="hind",size=30)),
       L("sym_su_hind","House-Check vs SU: SU","SU monogram with Hind name.",["modern","bold"],"system",logo_svg("su",font="hind",size=30)),"Which Symbol?")
add(S2,L("sym_crest","Gold Crest (Check)","Dark shield, gold serif SU. Overt luxe.",["luxe","gold","dark","formal"],"concierge",logo_svg("crest",ink="#1E1B16",font="manrope",size=24,c="#C9A24A"),bg="#F3EFE6"),
       L("sym_key_quiet","Quiet Key (Check)","Key mark, Manrope, quiet premium.",["calm","premium-quiet"],"concierge",logo_svg("key",font="manrope",size=24)),"Overt Luxe Or Quiet Premium?","check")
# --- accent colors (4) ---
AC="Logo: Accent Color"
add(AC,L("ac_teal","Muted Teal (Explainer)","House-check in the explainer teal #4F8A8B.",["calm","clear"],"system",logo_svg("house-check",accent="second",c=TEAL)),
       L("ac_terra","Terracotta","Same logo in terracotta #C1502E.",["warm","friendly"],"neighbor",logo_svg("house-check",accent="second",c=TERRA)),"Which Accent?")
add(AC,L("ac_lagoon","Lagoon","Lagoon blue #05668D.",["clear","calm"],"system",logo_svg("house-check",accent="second",c=LAGOON)),
       L("ac_jungle","Jungle","Jungle green #0B6E4F: 'done' green.",["natural","honest"],"crew",logo_svg("house-check",accent="second",c=JUNGLE)),"Which Accent?")
add(AC,L("ac_black","Black Only","No accent color at all.",["minimal","direct"],"crew",logo_svg("house-check",c=INK)),
       L("ac_teal_only","Teal Check Only","Black logo, only the check in teal.",["calm","minimal"],"concierge",logo_svg("house-check",c=TEAL)),"Which Accent?")
add(AC,L("ac_gold_black","Gold On Black (Check)","Gold wordmark on near-black.",["luxe","gold","dark"],"concierge",logo_svg("house-check",c="#C9A24A",ink="#C9A24A",bg="#1E1B16"),bg="#1E1B16"),
       L("ac_teal_cream","Teal On Cream","Teal and black on warm cream.",["light","calm","premium-quiet"],"concierge",logo_svg("house-check",accent="second",bg=CREAM),bg=CREAM),"Overt Luxe Or Quiet Premium?","check")
# --- app icon & favicon (3) ---
IC="Logo: App Icon & Favicon"
def IS(k,label,desc,tags,feel,sy,mode,c=TEAL):
    ic=save(f"icon_{sy}_{mode}",icon_svg(sy,c,mode)); return L(k,label,desc,tags,feel,app_scene("sizes",None,ic,c),bg=CREAM)
add(IC,IS("ic_house_white","House-Check, White Tile","White icon tile, black house, teal check.",["clear","light"],"system","house-check","white"),
       IS("ic_house_fill","House-Check, Teal Tile","Solid teal tile, white house.",["bold","friendly"],"neighbor","house-check","fill"),"Which App Icon?")
add(IC,IS("ic_su_white","SU, White Tile","SU monogram on white.",["modern","clear"],"crew","su","white"),
       IS("ic_dot_cream","Monthly Dot, Cream Tile","Calendar dot on cream.",["calm","organized"],"system","monthly-dot","cream"),"Which App Icon?")
add(IC,IS("ic_roof_fill","Roofline, Teal Tile","Roofline on teal: reads at 16px?",["minimal","calm"],"concierge","roofline","fill"),
       IS("ic_grid_white","Filter Grid, White Tile","Grid on white: crisp when tiny.",["organized","modern"],"system","filter-grid","white"),"Which Reads Best Small?")
# --- applications (4 + lockup 2) ---
AP="Logo: In The Real World"
base=saved["lay_line_house"]; ic_h=saved["icon_house-check_white"]; ic_f=saved["icon_house-check_fill"]
add(AP,L("van_line","Van Door: One-Line Logo","One-line logo on a white van, thin teal stripe.",["clear","minimal"],"system",app_scene("van",base,ic_h,TEAL),bg=CREAM),
       L("van_stack","Van Door: Stacked, Bigger","Stacked logo, bigger, jungle stripe.",["bold","direct"],"crew",app_scene("van",saved["lay_stack_house"],ic_h,JUNGLE),bg=CREAM),"Which Van Door?")
add(AP,L("polo_chest","Polo: Icon + Small Caps","Small icon tile and SMART UPKEEP under it on the chest.",["minimal","calm"],"concierge",app_scene("polo",base,ic_f,TEAL),bg=CREAM),
       L("sign_yard","Yard Sign: Logo + Line","White yard sign, logo and 'This home is looked after monthly'.",["friendly","clear"],"neighbor",app_scene("sign",base,ic_h,TEAL),bg="#E9F0E4"),"Which Touchpoint Feels Most Like It?")
add(AP,L("phone_white","Home Screen: White Tile","White icon on a phone home screen.",["clear","light"],"system",app_scene("phone",base,ic_h,TEAL),bg=CREAM),
       L("phone_fill","Home Screen: Teal Tile","Teal icon on a phone home screen.",["bold","friendly"],"neighbor",app_scene("phone",base,ic_f,TEAL),bg=CREAM),"Which Icon On The Home Screen?")
add("Logo: Home Record Lockup",L("lock_side","Smart Upkeep | Home Record","Company logo with the product beside it.",["clear","organized"],"system",app_scene("lockup-a",base,ic_h,TEAL)),
       L("lock_endorse","Home Record, By Smart Upkeep","Product leads; company as a small endorsement.",["calm","premium-quiet"],"concierge",app_scene("lockup-b",base,ic_h,TEAL)),"How Should Home Record Sit With Smart Upkeep?")
# ---- SmartKeep logos A and E (Up Keep agent, /workspace/smartkeep/logos/) refined: outlined Khand paths, 'up' under a roof chevron ----
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
_F={'k':TTFont('/usr/share/fonts/truetype/sand-box/google/Khand/Khand-Bold.ttf'),'h':TTFont('/usr/share/fonts/truetype/sand-box/google/Hind/Hind-SemiBold.ttf')}
def _tp(t,x,y,size,f='k',track=0):
    font=_F[f];gs=font.getGlyphSet();cm=font.getBestCmap();sc=size/font['head'].unitsPerEm;out=[]
    for ch in t:
        g=cm[ord(ch)];pen=SVGPathPen(gs);gs[g].draw(TransformPen(pen,(sc,0,0,-sc,x,y)));out.append(pen.getCommands());x+=gs[g].width*sc+track
    return ' '.join(out),x-track
def _xh(S): return _F['k']['OS/2'].sxHeight*S/_F['k']['head'].unitsPerEm
def roofmark(words=("smart","up","keep"),upcol=GREY,roof=INK,ink=INK,tag=None,tagcol=GREY,bg="#FFFFFF",S=200,roof_on=1):
    x=80;y=300;b='';gap=S*.06
    for i,wd in enumerate(words):
        d,x2=_tp(wd,x,y,S);col=upcol if i==roof_on else ink;b+=f'<path d="{d}" fill="{col}"/>'
        if i==roof_on:
            cx=(x+x2)/2;half=(x2-x)/2+S*.02;top=y-_xh(S)-S*.40;base=y-_xh(S)-S*.12
            b+=f'<polyline points="{cx-half:.1f},{base:.1f} {cx:.1f},{top:.1f} {cx+half:.1f},{base:.1f}" fill="none" stroke="{roof}" stroke-width="{S*.075:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        x=x2+gap
    xe=x-gap;H=400
    if tag:
        ts=34;tr=ts*.12;tw=_tp(tag,0,0,ts,'h',tr)[1];d,_=_tp(tag,80+(xe-80-tw)/2,412,ts,'h',tr)
        b+=f'<rect x="80" y="352" width="{xe-80:.0f}" height="2" fill="#E5E5E5"/><path d="{d}" fill="{tagcol}"/>';H=480
    W=int(xe+80);return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{bg}"/>{b}</svg>'
RM="Logo: SmartKeep A & E, Refined"
add(RM,L("A_original","A As Chosen: Grey 'up' Under A Roof","SmartKeep logo A: lowercase Khand smartupkeep, 'up' in grey under a roof chevron.",["clear","minimal"],"system",roofmark()),
       L("A_teal","A Refined: Teal 'up' And Roof","Same mark, 'up' and roof in the explainer teal.",["calm","friendly"],"neighbor",roofmark(upcol=TEAL,roof=TEAL)),"Logo A: Grey Or Teal?")
add(RM,L("A_teal_roofblack","A Refined: Teal 'up', Black Roof","Teal 'up', roof stays black.",["clear","calm"],"system",roofmark(upcol=TEAL)),
       L("new_housecheck_vs_A","New: House-Check + Khand Title","Separate house-check symbol, 'Smart Upkeep' in Khand.",["clear","organized"],"system",logo_svg("house-check",accent="second")),"Roof In The Word, Or A Separate Symbol?")
add(RM,L("E_monthly","E Refined: 'Monthly Home Maintenance'","Logo E lockup on cream, teal 'up', plainer tagline.",["clear","direct"],"crew",roofmark(upcol=TEAL,roof=TEAL,tag="MONTHLY HOME MAINTENANCE",bg=CREAM),bg=CREAM),
       L("E_ai","E As Chosen: 'AI-Powered Home Maintenance'","Logo E: same lockup, original AI tagline, grey 'up'.",["modern"],"system",roofmark(tag="AI-POWERED HOME MAINTENANCE",bg=CREAM),bg=CREAM),"Which Tagline Under Logo E?")
add(RM,L("A_jungle","A Refined: Jungle 'up'","Roof mark with 'up' in jungle green.",["natural","honest"],"crew",roofmark(upcol=JUNGLE,roof=JUNGLE)),
       L("new_roofline_top","New: Roofline Over A Centered Name","Separate roofline mark over a centered 'Smart Upkeep'.",["calm","balanced"],"concierge",logo_svg("roofline",sym_side="top",size=30)),"Roof In The Word Or Roof On Top?")
add(RM,L("E_terra","E Refined: Terracotta 'up', 'Your House, Handled'","Lockup E with terracotta 'up' and a warmer tagline.",["warm","friendly"],"neighbor",roofmark(upcol=TERRA,tag="YOUR HOUSE, HANDLED")),
       L("new_su_lockup","New: SU Monogram Lockup","SU monogram with Khand caps name.",["bold","modern"],"crew",logo_svg("su",font="khand",case="upper",size=30)),"Logo E Or A New Lockup?")
NM="Name: SmartKeep Or Smart Upkeep"
add(NM,L("name_smartkeep_roof","smartkeep (Roof Over 'keep')","Same roof style, name 'smartkeep'.",["minimal","direct"],"system",roofmark(words=("smart","keep"),upcol=TEAL,roof=TEAL,roof_on=1)),
       L("name_smartupkeep_roof","smartupkeep (Roof Over 'up')","Logo A refined, name 'smartupkeep'.",["clear","friendly"],"system",roofmark(upcol=TEAL,roof=TEAL)),"Which Name Reads Better?")
add(NM,L("name_SmartKeep_title","SmartKeep, Khand Title","'SmartKeep' as one word, house-check mark.",["minimal","modern"],"system",logo_svg("house-check").replace(">Smart <tspan",">Smart<tspan").replace(">Upkeep</tspan>",">Keep</tspan>")),
       L("name_SmartUpkeep_title","Smart Upkeep, Khand Title","'Smart Upkeep' as two words, same mark.",["clear","direct"],"system",logo_svg("house-check")),"SmartKeep Or Smart Upkeep?")
# ================= House-that-spells-UP mark (Max: the house in the middle reads as 'UP') =================
def upmark(c=TEAL, ink=INK, sw=7, style="outline", leg="obvious", roof="both", p="plain", house_col=None, letter_col=None, roof_col=None, join="round"):
    """100x100 mark: roof chevron over a U and a P drawn as the walls of a house.
    leg: obvious (letters bold, roof thinner) | subtle (letters thin & grey-ish, roof heavy)
    roof: both (roof over U and P) | u (roof only over the U)
    p: plain | door (P stem is a door) | chimney (P stem pokes through the roof as a chimney)"""
    hc=house_col or ink; lc=letter_col or ink; rc=roof_col or c
    lw = sw*(1.15 if leg=="obvious" else .6); rw = sw*(.85 if leg=="obvious" else 1.35)
    if leg=="subtle" and not letter_col: lc=GREY
    lj = 'stroke-linejoin="%s" stroke-linecap="%s"'%(join, "round" if join=="round" else "square")
    U = "M20 46 V74 Q20 88 34 88 Q48 88 48 74 V46"
    P = "M60 88 V46 H72 Q86 46 86 59 Q86 72 72 72 H60"
    rpts = "8,44 50,12 92,44" if roof=="both" else "12,44 34,24 56,44"
    out=""
    if style=="solid":
        out+=f'<path d="M8 44 L50 12 L92 44 V94 H8 Z" fill="{rc}"/>'
        out+=f'<path d="{U}" fill="none" stroke="#FFFFFF" stroke-width="{lw}" {lj}/><path d="{P}" fill="none" stroke="#FFFFFF" stroke-width="{lw}" {lj}/>'
        return out
    out+=f'<polyline points="{rpts}" fill="none" stroke="{rc}" stroke-width="{rw}" {lj}/>'
    if p=="chimney": out+=f'<path d="M74 30 V18 H82 V36" fill="none" stroke="{rc}" stroke-width="{rw*.8}" {lj}/>'
    out+=f'<path d="{U}" fill="none" stroke="{lc}" stroke-width="{lw}" {lj}/><path d="{P}" fill="none" stroke="{lc}" stroke-width="{lw}" {lj}/>'
    if p=="door": out+=f'<rect x="64" y="76" width="9" height="14" rx="1.5" fill="{rc}"/>'
    if hc and style=="house": out+=f'<path d="M8 44 V94 H92 V44" fill="none" stroke="{hc}" stroke-width="{sw*.5}" {lj}/>'
    return out
def word_paths(t, x, y, S, f='k', col=INK, track=0):
    d,x2=_tp(t,x,y,S,f,track); return f'<path d="{d}" fill="{col}"/>', x2
def up_logo(case="upper", font='k', mark=None, layout="inline", ink=INK, bg="#FFFFFF", S=120, track=None, gapk=.12, mk_scale=1.0):
    """SMART [house=UP] KEEP, outlined text. layout inline | stack | symbol (mark left + 'Smart Upkeep')"""
    mark = mark or upmark()
    a,b = ("SMART","KEEP") if case=="upper" else ("smart","keep") if case=="lower" else ("Smart","Keep")
    tr = (S*.04 if case=="upper" else 0) if track is None else track
    capH=_F[font]['OS/2'].sCapHeight*S/_F[font]['head'].unitsPerEm; xh=_F[font]['OS/2'].sxHeight*S/_F[font]['head'].unitsPerEm
    th = capH if case!="lower" else xh
    ms = th*1.55*mk_scale
    body=""; x=30; y=30+ms
    if layout=="inline":
        p1,x = word_paths(a,x,y,S,font,ink,tr); body+=p1; x+=S*gapk
        body+=f'<g transform="translate({x:.1f},{y-ms*.94:.1f}) scale({ms/100:.3f})">{mark}</g>'; x+=ms+S*gapk*.6
        p2,x = word_paths(b,x,y,S,font,ink,tr); body+=p2; W=x+30; H=y+30
    elif layout=="stack":
        ms2=ms*1.5; p1,x1 = word_paths(a,30,30+th,S,font,ink,tr)
        body+=p1; y2=30+th+S*.25+ms2*.94
        body+=f'<g transform="translate(30,{y2-ms2*.94:.1f}) scale({ms2/100:.3f})">{mark}</g>'
        p2,x2 = word_paths(b,30+ms2+S*.08,y2,S,font,ink,tr); body+=p2; W=max(x1,x2)+30; H=y2+30
    else:  # symbol: big mark left, 'Smart Upkeep' wordmark (shows the mark as a standalone symbol)
        ms2=ms*1.6; body+=f'<g transform="translate(30,30) scale({ms2/100:.3f})">{mark}</g>'
        p1,x1 = word_paths("Smart Upkeep",30+ms2+S*.15,30+ms2*.72,S,font,ink,0); body+=p1; W=x1+30; H=ms2+60
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}"><rect width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>{body}</svg>'
def up_icon(mark, mode="white", r=22, c=TEAL):
    bg={"white":"#FFFFFF","cream":CREAM,"fill":c}[mode]; st=' stroke="#E5E5E5" stroke-width="2"' if mode!="fill" else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"><rect x="1" y="1" width="98" height="98" rx="{r}" fill="{bg}"{st}/><g transform="translate(16,14) scale(.68)">{mark}</g></svg>'
UPC="Logo: House = UP"
OLD={"Logo: Wordmark","Logo: Symbol","Logo: Accent Color","Logo: App Icon & Favicon","Logo: In The Real World","Logo: Home Record Lockup"}
pairs[:]=[p for p in pairs if p["category"] not in OLD]
M=upmark  # shorthand
def U_(i,label,desc,tags,feel,svg,bg="#FFFFFF"): return L("up_"+i,label,desc,tags,feel,svg,bg)
std=up_logo()
# --- legibility of UP (5) ---
add(UPC,U_("obvious","UP Obvious","Bold U and P, light roof: you read 'UP' first.",["clear","direct"],"crew",up_logo(mark=M(leg="obvious"))),
        U_("subtle","UP Subtle","Heavy roof, thin grey letters: a house first, 'UP' second.",["calm","minimal"],"concierge",up_logo(mark=M(leg="subtle"))),"How Obvious Should 'UP' Be?")
add(UPC,U_("roof_both","Roof Over U And P","One roof over the whole word.",["clear","balanced"],"system",up_logo(mark=M(roof="both"))),
        U_("roof_u","Roof Over The U Only","Small roof over the U; the P stands beside it.",["friendly","playful-light"],"neighbor",up_logo(mark=M(roof="u"))),"Where Does The Roof Sit?")
add(UPC,U_("p_door","P With A Door","A small teal door at the foot of the P.",["friendly","warm"],"neighbor",up_logo(mark=M(p="door"))),
        U_("p_chimney","P As A Chimney","The P's stem pokes up through the roof as a chimney.",["clever","friendly"],"neighbor",up_logo(mark=M(p="chimney"))),"Door Or Chimney?")
add(UPC,U_("plain","Plain U And P","No extras: roof, U, P.",["minimal","clear"],"system",up_logo(mark=M())),
        U_("house_walls","U And P Inside House Walls","Thin house walls drawn around the letters.",["organized","clear"],"system",up_logo(mark=M(style="house"))),"Plain Or With Walls?")
add(UPC,U_("lower","smart [up] keep, Lowercase","Lowercase Khand around the mark.",["friendly","calm"],"neighbor",up_logo(case="lower")),
        U_("upper","SMART [UP] KEEP, Caps","Caps Khand around the mark.",["direct","bold"],"crew",std),"Lowercase Or Caps?")
# --- weight / outline vs solid (4) ---
add(UPC,U_("thin","Thin Stroke","Light 5-unit stroke: airy, modern.",["light","minimal"],"concierge",up_logo(mark=M(sw=5))),
        U_("heavy","Heavy Stroke","Thick 10-unit stroke: sturdy, sign-like.",["bold","industrial"],"crew",up_logo(mark=M(sw=10))),"Stroke Weight?")
add(UPC,U_("outline","Outline House","Outlined roof and letters.",["light","clear"],"system",up_logo(mark=M())),
        U_("solid","Solid House, Letters Cut Out","Solid teal house with U and P cut out in white.",["bold","friendly"],"neighbor",up_logo(mark=M(style="solid"))),"Outline Or Solid?")
add(UPC,U_("solid_black","Solid Black House","Solid black house, white U and P.",["bold","direct"],"crew",up_logo(mark=M(style="solid",roof_col=INK))),
        U_("solid_teal_lower","Solid Teal, Lowercase Name","Solid teal house with lowercase words.",["friendly","calm"],"neighbor",up_logo(case="lower",mark=M(style="solid"))),"Which Solid Version?")
add(UPC,U_("round","Rounded Joins","Rounded corners and ends: softer.",["friendly","calm"],"neighbor",up_logo(mark=M(join="round"))),
        U_("square","Square Joins","Sharp mitred corners: crisper, more 'built'.",["direct","industrial"],"crew",up_logo(mark=M(join="miter"))),"Round Or Square Corners?")
# --- color (4) ---
add(UPC,U_("acc_house","Accent On The Roof Only","Teal roof; letters and words black.",["calm","clear"],"system",up_logo(mark=M())),
        U_("acc_whole","Whole Mark In Teal","Roof and U/P all teal; words black.",["friendly","clear"],"neighbor",up_logo(mark=M(letter_col=TEAL))),"Accent On The Roof Or The Whole Mark?")
add(UPC,U_("terra","Terracotta Roof","Same mark, terracotta roof.",["warm","friendly"],"neighbor",up_logo(mark=M(c=TERRA))),
        U_("jungle","Jungle Roof","Same mark, jungle green roof.",["natural","honest"],"crew",up_logo(mark=M(c=JUNGLE))),"Which Accent?")
add(UPC,U_("lagoon","Lagoon Roof","Same mark, lagoon roof.",["clear","calm"],"system",up_logo(mark=M(c=LAGOON))),
        U_("teal","Explainer Teal Roof","Same mark, the explainer's muted teal.",["calm","clear"],"system",up_logo(mark=M(c=TEAL))),"Lagoon Or Teal?")
add(UPC,U_("black","Black Only","One color: no accent.",["minimal","direct"],"crew",up_logo(mark=M(c=INK))),
        U_("teal_cream","Teal On Cream","Teal roof on warm cream.",["light","premium-quiet"],"concierge",up_logo(mark=M(),bg=CREAM),bg=CREAM),"Black Only Or Teal On Cream?")
# --- composition (4) ---
add(UPC,U_("inline","One Line: SMART [UP] KEEP","Mark sits inside the name on one line.",["clear","direct"],"system",std),
        U_("stack","Stacked: SMART / [UP] KEEP","SMART on top, the house and KEEP below.",["compact","bold"],"crew",up_logo(layout="stack")),"One Line Or Stacked?")
add(UPC,U_("in_word","Mark Inside The Name","The house is the 'UP' in the name.",["clever","clear"],"system",std),
        U_("as_symbol","Mark As A Separate Symbol","House-UP mark left of 'Smart Upkeep'.",["clear","organized"],"system",up_logo(layout="symbol")),"Inside The Name Or Beside It?")
add(UPC,U_("hind","Hind Words Around The Mark","Rounder Hind letters for SMART and KEEP.",["friendly","calm"],"neighbor",up_logo(font='h',S=110)),
        U_("khand","Khand Words Around The Mark","Condensed Khand caps.",["direct","clear"],"crew",std),"Khand Or Hind?")
add(UPC,U_("tight","Tight Spacing","Words hug the house.",["compact","bold"],"crew",up_logo(gapk=.05)),
        U_("airy","Airy Spacing","More room around the house.",["calm","premium-quiet"],"concierge",up_logo(gapk=.25)),"Tight Or Airy?")
# --- small sizes (3) ---
def SZ(i,label,desc,tags,feel,mark,mode):
    ic=save(f"up_icon_{i}",up_icon(mark,mode)); return U_("sz_"+i,label,desc,tags,feel,app_scene("sizes",None,ic,TEAL),bg=CREAM)
add("Logo: UP At Small Sizes",SZ("outline","Outline UP Icon","Outline mark on white at 96, 32 and 16 px.",["light","clear"],"system",M(sw=8),"white"),
        SZ("solid","Solid UP Icon","Solid teal house, white U/P, at 96, 32 and 16 px.",["bold","clear"],"neighbor",M(style="solid"),"white"),"Which Still Reads 'UP' At 16 px?")
add("Logo: UP At Small Sizes",SZ("heavy_cream","Heavy UP On Cream","Extra-heavy strokes so 'UP' survives tiny sizes.",["bold","direct"],"crew",M(sw=12),"cream"),
        SZ("roof_only","Roof Only (No Letters) At Small Sizes","Drop the letters below 32 px: just a roof.",["minimal","calm"],"concierge",'<polyline points="12,60 50,26 88,60" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'%TEAL,"white"),"Keep The Letters Small, Or Just The Roof?")
add("Logo: UP At Small Sizes",SZ("fill_white","Teal Tile, White UP","Solid teal tile, white outline UP.",["bold","friendly"],"neighbor",M(c="#FFFFFF",letter_col="#FFFFFF"),"fill"),
        SZ("white_teal","White Tile, Teal Roof","White tile, black UP, teal roof.",["light","clear"],"system",M(sw=9),"white"),"Which App Icon?")
# --- real world (4) ---
ic_o=save("up_icon_app_outline",up_icon(M(sw=9),"white")); ic_s=save("up_icon_app_solid",up_icon(M(style="solid"),"white"))
RW="Logo: House = UP In The Real World"
add(RW,U_("van_inline","Van: SMART [UP] KEEP One Line","One-line logo on a white van door.",["clear","minimal"],"system",app_scene("van",std,ic_o,TEAL),bg=CREAM),
        U_("van_stack","Van: Stacked, Bigger","Stacked logo, bigger on the door.",["bold","direct"],"crew",app_scene("van",up_logo(layout="stack"),ic_o,TEAL),bg=CREAM),"Which Van Door?")
add(RW,U_("polo_outline","Polo: Outline UP Icon","Outline UP tile on the chest.",["minimal","calm"],"concierge",app_scene("polo",std,ic_o,TEAL),bg=CREAM),
        U_("polo_solid","Polo: Solid UP Icon","Solid teal UP tile on the chest.",["bold","friendly"],"neighbor",app_scene("polo",std,ic_s,TEAL),bg=CREAM),"Which Polo?")
add(RW,U_("sign_inline","Yard Sign: One Line","SMART [UP] KEEP on a white yard sign.",["clear","friendly"],"neighbor",app_scene("sign",std,ic_o,TEAL),bg="#E9F0E4"),
        U_("sign_symbol","Yard Sign: Mark + Smart Upkeep","Mark beside 'Smart Upkeep'.",["clear","organized"],"system",app_scene("sign",up_logo(layout="symbol"),ic_o,TEAL),bg="#E9F0E4"),"Which Yard Sign?")
add(RW,U_("phone_outline","Home Screen: Outline UP","Outline UP icon among other apps.",["light","clear"],"system",app_scene("phone",std,ic_o,TEAL),bg=CREAM),
        U_("phone_solid","Home Screen: Solid UP","Solid teal UP icon among other apps.",["bold","friendly"],"neighbor",app_scene("phone",std,ic_s,TEAL),bg=CREAM),"Which Icon On The Phone?")
add("Logo: Home Record Lockup",U_("lock_side","SMART [UP] KEEP | Home Record","Company mark with the product beside it.",["clear","organized"],"system",app_scene("lockup-a",std,ic_o,TEAL)),
        U_("lock_endorse","Home Record, By Smart Upkeep","Product leads; company endorses.",["calm","premium-quiet"],"concierge",app_scene("lockup-b",std,ic_o,TEAL)),"How Should Home Record Sit With Smart Upkeep?")
# --- checks (2) ---
add("Logo: Check",U_("chk_wrench","Wrench Mark (Unrelated Symbol)","Wrench symbol + 'Smart Upkeep' instead of the house-UP.",["industrial"],"crew",logo_svg("wrench")),
        U_("chk_up","House-UP Mark","The house that spells UP.",["clear","clever"],"system",up_logo(layout="symbol")),"Does The House-UP Beat A Generic Symbol?","check")
add("Logo: Check",U_("chk_gold","Gold Crest On Black (Luxe)","Dark shield, gold serif: overt luxe.",["luxe","gold","dark","formal"],"concierge",logo_svg("crest",ink="#C9A24A",c="#C9A24A",font="manrope",size=24,bg="#1E1B16"),bg="#1E1B16"),
        U_("chk_quiet","House-UP On Cream (Quiet)","House-UP in teal on cream: quiet premium.",["calm","premium-quiet"],"concierge",up_logo(mark=M(),bg=CREAM),bg=CREAM),"Overt Luxe Or Quiet Premium?","check")
DROP=set()
pairs=[p for p in pairs if p and p['optionA']['id'] not in DROP]
# --- taglines (4) ---
def T(i,label,line,body,feel,tags,font="khand"):
    return {"id":"su1_"+i,"label":label,"desc":line,"tags":tags+[feel],"feeling":feel,"visual":{"type":"hm","m":"tag","line":line,"body":body,"font":font,"acc":TEAL,"where":"Under the Smart Upkeep logo"}}
add("Tagline",T("tg_system","System: Every System, On Schedule","Every system. On schedule.","Your Home Record: furnace, water heater, AC, panel. Next visit Tue, Nov 4.","system",["clear","organized"]),
    T("tg_neighbor","Neighbor: Your House, Handled","Your house, handled.","Hi Sarah, Danny from Smart Upkeep. Filter's swapped, all good. See you next month.","neighbor",["friendly","warm"]),"Which Tagline?")
add("Tagline",T("tg_crew","Crew: Monthly Maintenance, Done Right","Monthly maintenance, done right.","Done: filter, flush, 6 smoke detectors. Photos in the app.","crew",["direct","honest"]),
    T("tg_concierge","Concierge: Upkeep You Never Think About","Upkeep you never think about.","Your visit is done and your Home Record is up to date. Nothing needs you.","concierge",["calm","premium-quiet"]),"Which Tagline?")
add("Tagline",T("tg_smart","System: Smart About Your Home","Smart about your home.","AI labels every system you photograph. We keep it all on record.","system",["clear","modern"]),
    T("tg_crew2","Crew: Show Up. Upkeep. Repeat.","Show up. Upkeep. Repeat.","Same tech, same day, every month.","crew",["direct","industrial"]),"Which Tagline?")
add("Tagline",T("tg_neighbor2","Neighbor: Small Visits, Big Peace Of Mind","Small visits. Big peace of mind.","A quick visit each month so the big things never surprise you.","neighbor",["friendly","calm"]),
    T("tg_concierge2","Concierge: Your Home, Looked After","Your home, looked after.","We look after the house. You live in it.","concierge",["calm","personal"]),"Which Tagline?")
# --- swipe controls (2) ---
EARTH=["#3F6E7D","#5A7D4F","#B5523B","#A0703C"]
C=lambda i,l,desc,tags,**k:{"id":"su1_"+i,"label":l,"desc":desc,"tags":tags,"feeling":None,"visual":{"type":"controls","words":["This","Both","Love","That"],"icons":["◀","⇄","❤","▶"],"colors":EARTH,"bg":"#FAF6EE","font":"Hind","stampov":"word","press":None,**k}}
add("Swipe Controls",C("sc_teal_round","Teal Round Outline","Round outline buttons in Smart Upkeep teal.",["calm","clear"],fmt="round",style="outline",press="fill",colors=[TEAL]*4,hint="edges"),
    C("sc_earth_pill","Earthy Pills Outline","Max's earthy pills, outline until pressed.",["warm","natural"],fmt="pill",style="outline",press="fill",hint="edges"),"Which Swipe Controls?")
add("Swipe Controls",C("sc_khand","Khand Words, Square","Square Khand-caps buttons.",["direct","bold"],fmt="square",style="outline",font="Khand",hint="edges"),
    C("sc_icons","Icons Only, Round","Round icon-only buttons.",["minimal","modern"],fmt="round",style="outline",words=["","","",""],hint="edges"),"Which Swipe Controls?")
# order: start with logos, avoid same category twice in a row
random.seed(7); first=pairs[:2]; rest=pairs[2:]; random.shuffle(rest); seq=first+rest; order=[]
while seq:
    k=next((i for i,p in enumerate(seq) if not order or p["category"]!=order[-1]["category"]),0); order.append(seq.pop(k))
from trim_deck import DECK_SIZE, select, save_overflow  # decks are 25 pairs; extras go to banks/overflow
order, _cut = select(order, DECK_SIZE); save_overflow(DID, _cut)
for i,p in enumerate(order,1):
    p.update(id=f"{DID}-{i:02d}",retest=False,repeat=False); p["ask"]=p["ask"] or "Which Fits Smart Upkeep?"
alloc={}; feel={}
for p in order:
    alloc[p["category"]]=alloc.get(p["category"],0)+1
    for s in "AB":
        f=p["option"+s].get("feeling")
        if f: feel[f]=feel.get(f,0)+1
NC={"name":"Smart Upkeep","checked":"2026-10-11","verdict":"Not clear. Needs a real USPTO trademark search and a lawyer's look before committing.",
 "findings":["SMART UPKEEP, INC. is an ACTIVE Florida corporation (Coral Springs, filed Nov 14, 2013; annual reports through 2025). Its line of business wasn't shown.",
  "A 'Smart Upkeep' app (warranty, renewal and asset vault, including home appliance and HVAC servicing records) is promoted on YouTube: same name, overlapping use (home records).",
  "Dreizler (industrial burners, Europe) markets a 'SmartUpKeep' maintenance technology: different industry and region.",
  "'Smart upkeep' is also used as a generic phrase and hashtag by home and roofing content sites, so it may be weak as a mark.",
  "SmartKeep (the Up Keep agent's working name): smartkeep.com has been registered since 2007 and runs a live 'SmartKeep' site; smartkeep.app has been registered since 2020 with a live 'SmartKeep' login. SmartKeep Solutions SRL (Romania) is a software and e-commerce company, and 'Smart Keeping' (Brazil) is a maintenance app for clinical equipment. That is a heavier conflict than Smart Upkeep, and both .com and .app are taken.",
  "smartupkeep.com is REGISTERED (since Dec 15, 2022, renews Dec 15, 2026, transfer-locked) but has no live site. smartupkeep.co and getsmartupkeep.com didn't resolve. Availability of smartupkeep.app is unclear."]}
deck={"date":DID,"version":4,"owner":"Max Weberman","format":"pairs","english_only":True,"light_only":True,
 "title":"Smart Upkeep: Logo Choices","brands":["Smart Upkeep: home maintenance membership (product: Home Record)","Base: light cream, black/white/grey, Khand/Hind; accents muted teal #4F8A8B, lagoon, jungle, terracotta"],
 "generated_at":dt.datetime.now().astimezone().isoformat(timespec="seconds"),"feelings":{"neighbor":"Trusted neighbor","system":"Calm organized system","concierge":"Quiet premium concierge","crew":"No-nonsense pro crew"},
 "feeling_counts":feel,"allocation":alloc,"apps":{"Smart Upkeep":len(order)},"pair_mix":{"refine":sum(p["purpose"]=="refine" for p in order),"check":sum(p["purpose"]=="check" for p in order)},
 "name_check":NC,"logo_files":OUT,"freshness":{"option_slots":2*len(order),"never_shown_before":2*len(order),"share":1.0},"warnings":[],"pairs":order}
keep={p["option"+k]["id"][4:] for p in order for k in "AB"}
for f in os.listdir(OUT):
    n=f[:-4]
    if f.endswith(".svg") and n not in keep and not n.startswith("up_icon"): os.remove(os.path.join(OUT,f))
json.dump(deck,open(f"decks/{DID}.json","w"),indent=1,ensure_ascii=False)
print(len(order),"pairs",alloc,deck["pair_mix"],feel,len(saved),"svgs")
