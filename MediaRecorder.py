#!/usr/bin/env python
# coding: utf-8
    
#參考網站 https://stackoverflow.com/questions/34167691/pipe-opencv-images-to-ffmpeg-using-python
#參考網站 https://stackoverflow.com/questions/5678695/ffmpeg-usage-to-encode-a-video-to-h264-codec-format?msclkid=ad04d267a81711eca7e216cb93656db3
    
def main():
    
    from multiprocessing import shared_memory
    import numpy as np
    from datetime import datetime
    import time
    import subprocess as sp
    import sys, os
    from concurrent.futures import ThreadPoolExecutor
    
    
    # In[ ]:   
    pwd = os.getcwd()    
    max_file = 10   
    fps = 30
       
    imgInfo = shared_memory.SharedMemory(name='imgInfo')
    tmp = np.ndarray((3,), np.int32, buffer=imgInfo.buf)
    info = np.array([0,0,0])
    info[:] = tmp[:]
    del tmp
    imgInfo.close()   

    def command(num):
        return r'ffmpeg -y -f rawvideo -c:v rawvideo -s {}x{} -pix_fmt bgr24 -r {} -i - -t 0.1 -c:v libx264 -b:v 5000k -pix_fmt yuv420p -movflags frag_keyframe+empty_moov+default_base_moof -f mp4 {}\tmp\videos\{}.mp4'.format(info[1] ,info[0] ,fps , pwd, num)
    

    
    
    existing_shm = shared_memory.SharedMemory(name='img')
    img = np.ndarray((info[0],info[1],info[2]), dtype=np.uint8, buffer=existing_shm.buf)
       

    
    def run(n):
        
        while 1 :
            time.sleep(0.01)
            if int(str(round(time.time() * 1000))[-3])==n :
                proc = sp.Popen(command(n), stdin=sp.PIPE, stderr=sp.PIPE, shell=True)
                for i in range(fps//10):
                    time.sleep(1/fps)
                    proc.stdin.write(img.tobytes())
                proc.stdin.close()
                proc.stderr.close()
                proc.kill()         
    
    
    # In[ ]:
    
    
    with ThreadPoolExecutor(max_workers=max_file) as executor:
        for n in range(0,max_file,1):
            executor.submit(run, n)
            time.sleep(0.01)
    
    del img
    existing_shm.close()
    
if __name__=="__main__" :
    #main()
    pass    