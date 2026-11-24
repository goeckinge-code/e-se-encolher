import numpy as np, cv2, sys
from PIL import Image
im=cv2.imread('capacete_src.jpg');H,W=im.shape[:2]
geo=np.zeros((H,W),np.uint8)
pts=[]
cx,cy,ax,ay=583,600,482,548
for t in np.linspace(np.pi,2*np.pi,120):pts.append((cx+ax*np.cos(t),cy+ay*np.sin(t)))   # casco (metade de cima)
for y in np.linspace(600,1075,40):                                                        # laterais afinando até a base
    k=(y-600)/475;hw=482-70*k**1.6;pts.append((cx+hw,y))
pts+= [(cx-412+30,1078),(cx+412-30,1078)][::-1]
for y in np.linspace(1075,600,40):
    k=(y-600)/475;hw=482-70*k**1.6;pts.append((cx-hw,y))
cv2.fillPoly(geo,[np.array(pts,np.int32)],255)
fg=cv2.erode(geo,np.ones((41,41),np.uint8));out=cv2.dilate(geo,np.ones((25,25),np.uint8))
mask=np.full((H,W),cv2.GC_BGD,np.uint8);mask[out>0]=cv2.GC_PR_BGD;mask[geo>0]=cv2.GC_PR_FGD;mask[fg>0]=cv2.GC_FGD
b=np.zeros((1,65));f=np.zeros((1,65));cv2.grabCut(im,mask,None,b,f,5,cv2.GC_INIT_WITH_MASK)
m=np.where((mask==1)|(mask==3),255,0).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((11,11),np.uint8));m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((7,7),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(m);k=1+np.argmax(st[1:,4]);m=np.where(lab==k,255,0).astype(np.uint8)
c,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);m=np.zeros_like(m);cv2.drawContours(m,c,-1,255,-1)
cv2.imwrite('capacete_mask.png',m)
rgb=cv2.cvtColor(im,cv2.COLOR_BGR2RGB);a=cv2.GaussianBlur(m,(5,5),1.5)[...,None]/255
t=np.full_like(rgb,(239,232,218));Image.fromarray((rgb*a+t*(1-a)).astype(np.uint8)).resize((600,600)).save('capacete_cut_prev.png')
