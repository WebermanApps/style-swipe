import sys,json,importlib
sys.path.insert(0,'.')
m=importlib.import_module(sys.argv[1]); cards=json.load(open(sys.argv[2]))
out=['<html><body style="margin:0;background:#eee;width:390px">']
for i,c in enumerate(cards):
    for side in 'AB':
        out.append(f'<div style="margin:8px;width:330px;font:12px sans-serif">{c["topic"]} {side}: {c[side]["label"]}'+m.draw(i,side,c[side])+'</div>')
open(sys.argv[3],'w').write(''.join(out)+'</body></html>')
