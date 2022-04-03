#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install opencv-python==3.4.16.57
#參考資料  https://stackoverflow.com/questions/41385708/multiprocessing-example-giving-attributeerror

from multiprocessing import  shared_memory, Value, Process
import os, signal, platform
import time
import Camera # 1. Open Camera, copy frame to shared memory
import HttpServer # 3. Create Http Server for index.html, port 8080
import MediaRecorder # 2. Record Video to Http Server via ffmpeg


CameraIsOpen = Value("i", 1)
img, imgInfo, height, width, flag, r, g, b = [0]*8

# In[ ]:



def EvenListener():
    while 1:
        time.sleep(0.1)    
        if flag.buf[0:1]==b"0" or CameraIsOpen.value==0:
            raise I_WILL_BROKEN_IT


def getInfo():
    global img, imgInfo, width, height, flag, videos, r, g, b
    import cv2
    import numpy as np   
    cv2.destroyAllWindows()   
    img = 0
    shape_img = 0
    size = 0
    W_and_H = 0
    typ = 0
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
    info = np.array([shape_img[0],shape_img[1],shape_img[2]],dtype=np.int32)
    imgInfo = shared_memory.SharedMemory(create=True, size=info.nbytes, name="imgInfo")   
    tmp = np.ndarray((3,), info.dtype, buffer=imgInfo.buf)
    tmp[:] = info[:]
    del tmp
    cv2.destroyAllWindows()  
    img = shared_memory.SharedMemory(create=True, size=size, name="img")
    
    flag = shared_memory.SharedMemory(create=True, size=10, name="flag") 
    flag.buf[0:1]=b"1"
    
    r = shared_memory.SharedMemory(create=True, size=5, name='r')
    g = shared_memory.SharedMemory(create=True, size=5, name='g')
    b = shared_memory.SharedMemory(create=True, size=5, name='b')
    r.buf[0:5]=b"+0000"
    g.buf[0:5]=b"+0000"
    b.buf[0:5]=b"+0000"


# In[ ]:


def main():
    print("注意： \n 運行此Python時，請確保在CMD運行Python的當前工作資料夾和此\"Main.py\"檔案的位置相同，否則將會運行失敗。")
    print("注意： \n Server正在準備開啟。若要停止 Server，請至 Server 啟動後的網頁按下 Shutdown Server 按鈕，或在 cmd 按下 Ctrl+C 。")
    getInfo()
    
    camera = Process(target=Camera.main, args=(CameraIsOpen,) )
    camera.start()
    
    recorder = Process(target=MediaRecorder.main, args=() )
    recorder.start()
    
    host = "127.0.0.1"
    port = 8080
    httpserver = Process(target=HttpServer.main, args=(host, port, height, width) )
    httpserver.start()
    
    time.sleep(1)
    
    print("\nServer Is Starting, Wait 1 Minutes please.\n")
    
    try:
        import webbrowser
        webbrowser.open("http://{}:{}".format(host,port), new=0, autoraise=True)
        EvenListener()
    except:
      CameraIsOpen.value = 0
      
      imgInfo.close()
      imgInfo.unlink()
      
      img.close()
      img.unlink() 
      
      flag.close()
      flag.unlink()
      
      r.close()
      r.unlink()
      
      g.close()
      g.unlink()
      
      b.close()
      b.unlink()
      
      camera.terminate()
      recorder.terminate()
      httpserver.terminate()
      
      print("\nFinish\n")


# In[ ]:


if __name__=="__main__":
    main()






