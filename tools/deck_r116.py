#!/usr/bin/env python3
"""Team Improvement Deck round three (Max, Oct 17 2026 20:52 ICT) -> one idempotent block <!--mw-r116-->...<!--/mw-r116-->
in index.template.html and every deck page (same pattern as deck_endfix.py):
 - R116 deck look: vote buttons get 10px corners (match the 10px deck cards); the caption panel under deck pictures
   (title + text + tags below the picture) is a light cream band #FAF6EE.
 - R115 audio cards mixed into video decks: the play button is its own 44px round control. Every pointer/mouse/touch/
   click/key event on it is stopped at window capture (before any card, swipe or vote handler), so it never votes,
   selects or swipes the tile. Playing a sound pauses videos and starting a video stops sounds.
 - R114 standalone keep-or-delete decks: deck.keep_delete:true (with deck.cards) = single-item Keep / Delete cards
   (Delete on the left/left swipe, Keep on the right; Hold/Love hidden); results carry mode:'keep-delete', keep[], delete[].
 - Household refresh pages: 9179619 squared pick cards; R89 + R116 say deck cards are 10px -> that override goes back to 10px.
Pages are locked: unlock in a mkdir -m 700 dir under /workspace, run on those files, relock, copy back.
Usage: python3 tools/deck_r116.py [files...]   (default: template + all deck pages; never decks/index.html or share-x3l9xcxc1eut/)"""
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!--mw-r116-->", "<!--/mw-r116-->"
EXCLUDE = ("share-x3l9xcxc1eut/", "decks/index.html")
SQ = "html body .card.card,html body .opt.opt,html body .vis.vis,html body .stamp.stamp,html body .carding .card{border-radius:0!important}"
RD = "html body .card.card,html body .opt.opt,html body .vis.vis,html body .stamp.stamp,html body .carding .card{border-radius:10px!important}"
BLOCK = START + r"""
<style id="mw-r116-css">
/* R116 vote buttons: 10px corners like the deck cards */
.controls button,#controls button,#controls3 button,.controls.v3 button,.controls.v4 button{border-radius:10px!important}
/* R116 caption panel under deck pictures: light cream band */
.opt .mw-cap{display:flex;flex-direction:column;gap:4px;min-width:0}
.opt:not(.novis) .mw-cap{background:#FAF6EE;margin:0 -8px -8px;padding:8px 10px 10px;border-top:1px solid #EFE8DA;border-radius:0 0 8px 8px;flex:1 0 auto}
.opt .mw-cap h3,.opt .mw-cap p{margin:0}
/* R115 play button: its own 44px control */
.v-sound .play{width:44px!important;height:44px!important;min-width:44px!important;min-height:44px!important;padding:0!important;border-radius:50%!important;flex:none;align-self:center;position:relative;z-index:6;gap:0;touch-action:manipulation}
.v-sound .play .pi{font-size:18px;line-height:1}
.v-sound .play .pl{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* R114 keep/delete cards */
body.mw-kd #bMaybe,body.mw-kd #bLove,body.mw-kd .stamp.maybe,body.mw-kd .stamp.love{display:none!important}
body.mw-kd #bNo{background:#FFFFFF;color:#9B2C1F;border-color:#9B2C1F}
body.mw-kd #bYes{background:#0B6E4F;color:#FFFFFF;border-color:#0B6E4F}
</style>
<script>(()=>{
/* R116 caption band: wrap title, text and tags under the picture */
try{const _oh=optHtml;optHtml=function(o,s){const h=String(_oh.apply(this,arguments));return h.replace(/(<h3>[\s\S]*)<\/div>\s*$/,'<div class="mw-cap">$1</div></div>')}}catch(e){}
/* R115 play button never reaches the card: stopped at window capture, before every card/swipe/vote/key handler */
const isPlay=e=>!!(e.target&&e.target.closest&&e.target.closest('.play'));
['pointerdown','pointerup','pointermove','mousedown','mouseup','touchstart','touchend','click','dblclick','keydown','keyup'].forEach(t=>
 window.addEventListener(t,e=>{if(!isPlay(e))return;e.stopPropagation();
  if(t==='click'){try{document.querySelectorAll('video').forEach(v=>{try{v.pause()}catch(_){}})}catch(_){}try{onPlayTap(e)}catch(_){}}},{capture:true,passive:t!=='click'&&t!=='keydown'}));
document.addEventListener('play',e=>{if(e.target&&e.target.tagName==='VIDEO'){try{stopAllAudio()}catch(_){}}},true);
/* R114 keep/delete mode */
const kd=()=>{try{return !!(deck&&single&&(deck.keep_delete||deck.mode==='keep-delete'))}catch(e){return false}};
function kdUi(){const on=kd();document.body.classList.toggle('mw-kd',on);if(!on)return;
 const n=document.getElementById('bNo'),y=document.getElementById('bYes');if(n)n.textContent='Delete';if(y)y.textContent='Keep';
 try{LBL.no='Delete';LBL.yes='Keep'}catch(e){}
 const h=document.querySelector('#card h2');if(h)h.textContent='Keep Or Delete?';
 const s=document.querySelector('#card .stamp.no');if(s)s.textContent='DELETE';
 const hi=document.getElementById('hint');if(hi)hi.textContent='Swipe left = Delete, right = Keep. Arrow keys: \u2190 Delete, \u2192 Keep.'}
try{const _sd=setDeck;setDeck=function(){const x=_sd.apply(this,arguments);try{kdUi()}catch(e){}return x}}catch(e){}
try{const _r=render;render=function(){const x=_r.apply(this,arguments);try{kdUi()}catch(e){}return x}}catch(e){}
try{const _sr=submitResults;submitResults=function(){const r=_sr.apply(this,arguments);try{if(kd()&&r){r.mode='keep-delete';
 const lab=id=>{const c=items.find(i=>i.id===id);return c?c.option.label:id};
 r.keep=picks.filter(p=>p.answer==='yes').map(p=>lab(p.card_id));r.delete=picks.filter(p=>p.answer==='no').map(p=>lab(p.card_id))}}catch(e){}return r}}catch(e){}
})();</script>
""" + END
def patch(s):
    s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    s2 = s2.replace(SQ, RD)
    if "function showEnd" in s2 and "function optHtml" in s2:
        i = s2.rindex("</body>"); s2 = s2[:i] + BLOCK + "\n" + s2[i:]
    return s2, s2 != s
if __name__ == "__main__":
    if not sys.argv[1:]: os.chdir(ROOT)
    fs = sys.argv[1:] or ["index.template.html", "index.html"] + sorted(glob.glob("*/index.html"))
    n = 0
    for f in fs:
        if any(x in f for x in EXCLUDE): continue
        t = open(f, encoding="utf-8").read()
        if "const D=" in t: print("LOCKED, skipped:", f); continue
        t2, ch = patch(t)
        if ch: open(f, "w", encoding="utf-8").write(t2); n += 1
    print(f"deck_r116: patched {n} file(s)")
