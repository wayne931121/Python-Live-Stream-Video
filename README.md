# Python-Live-Stream-Video-Http-Server
Live Stream Video, using python ffmpeg opencv.
Test on win10.(Not Included Audio.)

簡單的來說，程式碼是這樣運作的 :


Phone Camera >> DroidCam >>
wifi or usb>> DroidCam Client >>

// 以上是實體別人寫好的部分
// 以下是自己寫的程式碼部分
// Server

Python OpenCV >> Python Shared Memory >>
Python MediaRecorder.py >> CMD FFMPEG >>
Python Shared Memory >> 
Python Flask Http Server >>

// 以下是客戶端 
// Client

<< Client Browser Javascript Ajax >>
Html Video >> User Screen


環境配置需求

手機
照相、錄影等相機功能
DroidCam (Wifi or usb(If you using usb, remember to open you android phone allow usb debug in devolop mode.)  )

電腦
DroidCam Client
ffmpeg (要設環境變數)
python : (詳情可見setup.bat)
    opencv
    flask
