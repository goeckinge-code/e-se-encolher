import numpy as np, cv2
from PIL import Image
f=np.asarray(Image.open('rosto_src.jpg').convert('RGB')).astype(np.float32)
k=f[...,2]-np.maximum(f[...,0],f[...,1])
k=cv2.GaussianBlur(k,(3,3),0)
a=1-np.clip((k-18)/(52-18),0,1)                 # céu -> 0, pessoa -> 1
m=(a>0.5).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(m);keep=1+np.argmax(st[1:,4])
solid=(lab==keep).astype(np.uint8)
solid=cv2.morphologyEx(solid,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
c,_=cv2.findContours(solid,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);fillm=np.zeros_like(solid);cv2.drawContours(fillm,c,-1,1,-1)
# alfa: interior sólido, borda (cabelo) suave pela chave
near=cv2.dilate(fillm,np.ones((9,9),np.uint8))
alpha=np.where(cv2.erode(fillm,np.ones((5,5),np.uint8))>0,1.0,a*near)
np.save('rosto_alpha.npy',alpha.astype(np.float32))
# prévia
rgb=f.copy();sp=np.maximum(rgb[...,0],rgb[...,1])+8;rgb[...,2]=np.where(alpha<.98,np.minimum(rgb[...,2],sp),rgb[...,2])
t=np.full_like(rgb,(239,232,218));Image.fromarray((rgb*alpha[...,None]+t*(1-alpha[...,None])).astype(np.uint8)).save('rosto_cut_prev.png')
print('ok')
