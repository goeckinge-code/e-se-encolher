import numpy as np, cv2, sys
from PIL import Image
from scipy import ndimage as ndi
src,out=sys.argv[1],sys.argv[2]
im=np.asarray(Image.open(src).convert('RGB')).astype(np.uint8); H,W=im.shape[:2]
lum=im.astype(int).sum(-1)/3
bright=(lum>=246).astype(np.uint8)
dark=cv2.morphologyEx(1-bright,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
lab,n=ndi.label(1-dark)
border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
car=ndi.binary_fill_holes(~np.isin(lab,list(border)))
yy,xx=np.mgrid[0:H,0:W]
wheels=((xx-305)**2+(yy-247)**2<=99**2)|((xx-1205)**2+(yy-238)**2<=101**2)
car&=(yy<=318)|wheels            # sem a sombra do chão
car=ndi.binary_opening(car,iterations=2)
lab2,n2=ndi.label(car); sizes=ndi.sum(car,lab2,range(1,n2+1))
car=np.isin(lab2,[i+1 for i,s in enumerate(sizes) if s>2000])
a=cv2.GaussianBlur((car*255).astype(np.uint8),(5,5),1.2)
a=np.clip((a.astype(int)-40)*1.25,0,255).astype(np.uint8)   # borda levemente para dentro
Image.fromarray(np.dstack([im,a]),'RGBA').save(out,quality=88,method=6)
