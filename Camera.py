#!/usr/bin/env python
# coding: utf-8

def main(ctr) :   
    # In[ ]:
    
    #參考網站 https://blog.csdn.net/keenweiwei/article/details/42454791?msclkid=14800b1bae9e11ecacd8991edd7f8cfb
    #參考網站 https://shengyu7697.github.io/python-opencv-save-video/?msclkid=3c0972b1a78111eca3c8f235e5711f99
    from multiprocessing import shared_memory, Value
    import cv2
    import numpy as np
    
    
    cv2.destroyAllWindows()
    # In[ ]:
    
    
    img = 0
    shape_img = 0
    size = 0
    W_and_H = 0
    typ = 0
    
    
    # In[ ]:


    # GET IMG WIDTH AND HEIGHT
    video = cv2.VideoCapture(0)
    height = int(video.get(4))
    width = int(video.get(3))
    fps = int(video.get(5))
    video.release()
    shape_img = (height,width,3)
    size = np.zeros(shape_img,dtype=np.uint8).nbytes
    typ = np.uint8
    W_and_H = (width,height)
    cv2.destroyAllWindows()
    
    r = shared_memory.SharedMemory(name='r')
    g = shared_memory.SharedMemory(name='g')
    b = shared_memory.SharedMemory(name='b')
    
    # In[ ]:
    

    info = np.array([shape_img[0],shape_img[1],shape_img[2]],dtype=np.int32)
    imgInfo = shared_memory.SharedMemory("imgInfo")    
    tmp = np.ndarray((3,), info.dtype, buffer=imgInfo.buf)
    tmp[:] = info[:]
    del tmp
    cv2.destroyAllWindows()
    
    def hash(v):
        a = v[0:1]
        b = v[1:5]
        b = int(b)
        if a==b"+":
            pass
        else:
            b *= -1
        return b            
    # In[ ]:
    def poc(img):
        img = np.array(img,dtype="int32")
        #newimg = np.copy(img)
        newimg = img
        
        B = newimg[:,:,0:1]
        G = newimg[:,:,1:2]
        R = newimg[:,:,2:3]
        
        R += hash(r.buf[0:5])
        G += hash(g.buf[0:5])
        B += hash(b.buf[0:5])
        
        newimg = np.concatenate([B,G,R],axis=2)
        newimg = np.where(newimg>255,255,newimg)
        newimg = np.where(newimg<0,0,newimg)
        newimg = np.array(newimg,dtype="uint8")
        
        return newimg
    
    
    # In[ ]:
    cv2.destroyAllWindows()
    # In[ ]:
    
    img = shared_memory.SharedMemory("img")
    
    tmp = np.ndarray(shape_img, dtype=typ, buffer=img.buf)
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            if not ctr.value :
                break
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break  
            frame = poc(frame)    
            tmp[:] = frame[:]
            if cv2.waitKey(1) == ord('q'):
                break
        # Release everything if job is finished
    except Exception as e:     
        cap.release()
        cv2.destroyAllWindows()
    
    # In[ ]:
    
    
    del tmp
    img.close()
    
    
    # In[ ]:
    
    
    # ffmpeg -i C:\Users\sky66\Downloads\output1.mp4 -c:v libx264  -t 1 -y C:\Users\sky66\Downloads\output3.mp4
    
    
    # In[ ]:
    
    print("Camera break")
    imgInfo.close()

    
if __name__=="__main__":
    main()    