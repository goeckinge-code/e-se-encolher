from PIL import Image, ImageDraw, ImageFilter
import numpy as np, sys
src=Image.open(sys.argv[1]).convert('RGB'); W,H=src.size
AIR=[(360,513),(361,478),(368,475),(400,480),(440,492),(502,511),(504,513)]
def poly(p):
    m=Image.new('L',(W,H),0);ImageDraw.Draw(m).polygon(p,fill=255);return np.asarray(m)>0
air=poly(AIR); wing=np.zeros((H,W),bool); wing[471:546,506:571]=True
k=np.zeros((H,W),bool); k[512:]=True; k|=air|wing
o=np.asarray(src).astype(np.int16); a=o.copy()
r,g,b=o[...,0],o[...,1],o[...,2]
red=(r>140)&(g<140)&(b<140); pink=(r-g>30)&(r-b>30)
yy=np.arange(H)[:,None]+np.zeros((1,W),int)
kill=(~k)|(air&pink&(yy<513))
# letter bottoms just under the cut: red/pink pixels whose pixel 3-4 rows above is letter red
for y in range(512,518):
    cont=(pink[y]|red[y])&(red[y-4]|red[y-3])&~wing[y]&~air[y]
    kill[y]|=cont
a[kill]=255
lum=a.sum(-1); a[lum>3*240]=255
# soften the remaining light-gray halo pixels toward white
out=Image.fromarray(a.astype(np.uint8)).crop((118,466,576,588))
big=out.resize((out.width*3,out.height*3),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2.2,90,2))
big.save('car_full.png'); big.save('car.webp',quality=86)
# wheels (centre/radius in crop coords *3)
