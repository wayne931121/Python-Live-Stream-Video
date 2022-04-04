#參考資料:https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c#:~:text=If%20you%27re%20working%20on%20the%20CLI%20and%20only,kill%20it%20with%3A%20kill%20%24%20%28pgrep%20-f%20flask%29
#參考資料:https://www.twilio.com/blog/how-run-flask-application?msclkid=3d0bef50b28411ec8dfc6d8561fb8725
#參考資料:http://www.coolpython.net/flask_tutorial/deep-learn/flask-multi-thread-or-single-thread.html?msclkid=1f24a95fb28411ec88cb43d02913d47f
#參考資料:https://flask-headers.readthedocs.io/en/latest/?msclkid=7627fd68b28411ecb9f40d157577d674
#參考網站:https://stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess?msclkid=06636291b29111ec86d93cd2d5680b40
# pip install flask-headers
from flask import Flask, request, render_template
from multiprocessing import shared_memory
import os

def server(HOST, PORT, height, width):
    
    flag = shared_memory.SharedMemory(name='flag')
    r = shared_memory.SharedMemory(name='r')
    g = shared_memory.SharedMemory(name='g')
    b = shared_memory.SharedMemory(name='b')
    max_file = 10
    videos = [shared_memory.SharedMemory("video"+str(_)) for _ in range(max_file)]  

    def hash(data):
        """
        This function will return currect videos datas.
        
        The datas will encode in this way :
        
        datas = "I am datas" => "I am datas"             ## len(data)  in range 0~(2^10-1).    
        datas = bytes(datas, "utf-8") => b"I am datas" 
        
        lenght = len(datas)  => 10                       ## len(lenght)  in range 0~9.
        lenght = str(lenght) => "10"
        lenght = bytes(lenght, "utf-8") => b"10"
        
        top = len(lenght)                                ## len(top) is 1.
        top = str(top)
        top = bytes(top, "utf-8")
        
        result = top+ lenght+ datas                      ## output: b"210I am datas" (b"2"+ b"10"+ b"I am datas")
        """
        d = int(data[0:1])
        dd = int(data[1:1+d])
        ddd = data[1+d:1+d+dd]
        return ddd    
    
    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return render_template("index.html", camera_data = {"height":height, "width":width, "url":("{}:{}".format(HOST,PORT)) })
        
    @app.route("/<source>", methods=['GET'])
    def index_get(source):
        with open(os.getcwd()+"\\templates\\"+source, "rb") as f:
            data = f.read()
        return data    
        
    @app.route("/shutdown", methods=['GET'])
    def shutdown():
        flag.buf[0:1]=b"0"
        flag.close()
        return "<h1>The Server is shutdown</h1>"          

    @app.route('/videos/<case>', methods=['GET'])
    def Video(case):
        return hash(videos[int(case)].buf.tobytes())   
        
    @app.route('/RGB/<case>', methods=['GET'])
    def RGB(case):
        case = case.split("_")
        color = case[0]
        value = bytes("%04d"%abs(int(case[1])), "utf8")
        dress = bytes("","utf8")
        
        if int(case[1])>0 :
            dress = bytes("+","utf8")
        else:
            dress = bytes("-","utf8")
            
        if color=="r" :
            r.buf[0:5] = dress+value        
        elif color=="g" :
            g.buf[0:5] = dress+value  
        elif color=="b" :
            b.buf[0:5] = dress+value              
            
        return ",".join(case)     
        
    app.config['TEMPLATES_AUTO_RELOAD'] = True      
    app.jinja_env.auto_reload = True
    
    try:
        app.run(host=HOST, port=PORT, threaded=True,debug=True)
        #app.run(host=HOST, port=PORT, threaded=True)
    except:
        pass    

def main(HOST, PORT, height, width):
    import subprocess as sp
    proc = sp.Popen("python HttpServer.py --run 1 --host {} --port {} --height {} --width {}".format(HOST,PORT,height,width), stdout=sp.DEVNULL, stderr=sp.STDOUT, shell=True)
    
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run", help="run server")
parser.add_argument("--host")
parser.add_argument("--port")
parser.add_argument("--height")
parser.add_argument("--width")
args = parser.parse_args()

if(args.run):
    server(args.host, args.port, args.height, args.width)  