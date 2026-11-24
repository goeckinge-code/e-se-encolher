import numpy as np, cv2
from PIL import Image
O='/home/user/e-se-encolher/senna/assets/img/'
S=1600;k=S/1200
h=np.asarray(Image.open('capacete_hd.png').convert('RGB').resize((S,S),Image.LANCZOS)).astype(np.float32)
m=cv2.imread('capacete_mask.png',0).astype(np.float32)/255;m=cv2.resize(m,(S,S),interpolation=cv2.INTER_CUBIC)
yy,xx=np.mgrid[0:S,0:S]
# base arredondada: a borda de baixo sobe nas laterais
bottom=(1072-70*((xx/k-583)/430)**2)*k
m=m*np.clip((bottom-yy)/3+.5,0,1)
# reflexos do fundo rosa: tons magenta viram cinza neutro (o laranja do logo tem b<g e fica)
r,g,b=h[...,0],h[...,1],h[...,2]
mag=np.clip((np.minimum(r-g,b-g+40)-18)/30,0,1)*np.clip((b-g+10)/25,0,1)
lum=(.3*r+.59*g+.11*b)[...,None]
neu=np.concatenate([lum*.92,lum*.95,lum],-1)
h=h*(1-mag[...,None])+neu*mag[...,None]
m=cv2.GaussianBlur(m,(5,5),1.2);m=np.clip((m-.5)*1.5+.5,0,1)
Image.fromarray(np.dstack([h,m*255]).clip(0,255).astype(np.uint8),'RGBA').save(O+'capacete.webp',quality=88,method=6)
c=Image.open(O+'capacete.webp');gr=Image.new('RGB',c.size,(60,140,80));gr.paste(c,(0,0),c);gr.resize((800,800)).save('helm_check.png')
print('ok')
