import sys,json,base64,importlib,os,shutil
sys.path.insert(0,'/workspace/style-swipe/tools/bpdraw_1020')
MOD={'weberman-entry-and-arrival-ak7w2q':'entry','weberman-kitchen-and-dining-pbq2df':'kitchen','weberman-wellness-wing-details-tconfm':'well','wellness-wing-j5ydko':'well_j5','house-materials-97q3xx':'mats','facade-and-garden-hack27':'facade','courtyard-shape-vj2dp5':'court'}
CSS_OLD='.oimg svg{display:block;height:120px!important;width:auto!important;max-width:100%;margin:0 auto}'
CSS_NEW='.oimg svg{display:block;height:auto!important;width:100%!important;max-width:100%;margin:0 auto}'
dec=json.JSONDecoder()
for slug,mn in MOD.items():
    m=importlib.import_module(mn)
    h=open(f'/workspace/bpdraw-1020/src/{slug}/index.html').read()
    i=h.index('const CARDS=')+len('const CARDS='); arr,end=dec.raw_decode(h,i)
    inline=arr[0]['A']['img'].startswith('<svg')
    for k,c in enumerate(arr):
        for side in 'AB':
            svg=m.draw(k,side,c[side])
            c[side]['img']=svg if inline else 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    h=h[:i]+json.dumps(arr)+h[end:]
    if inline:
        assert h.count(CSS_OLD)==1; h=h.replace(CSS_OLD,CSS_NEW)
    os.makedirs(f'/workspace/bpdraw-1020/out/{slug}',exist_ok=True)
    open(f'/workspace/bpdraw-1020/out/{slug}/index.html','w').write(h); print(slug,inline,len(h))
