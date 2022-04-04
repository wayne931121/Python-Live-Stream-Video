// 參考網站
/* 
https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Sending_and_Receiving_Binary_Data?msclkid=4b40ee72ad0011ec909e14a6e1075844
https://developer.mozilla.org/en-US/docs/Web/API/Blob
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer
https://www.bennadel.com/blog/3472-downloading-text-using-blobs-url-createobjecturl-and-the-anchor-download-attribute-in-javascript.htm?msclkid=581f7bf0ad0211ec9dad145aa50fc87c
*/

const videoTag = document.getElementById("my-video");
const HostPort = document.getElementById("HostPort").innerHTML;
const r = document.getElementById("r");
const g = document.getElementById("g");
const b = document.getElementById("b");
const Source = document.getElementById("Source");
const Height = document.getElementById("Height");
const Width = document.getElementById("Width");
let src,h,w,tt,tim = 0;
let myMediaSource = new MediaSource();
let SourceBuffer;
let datas;
let url; 
let ArrayBufferResult;
let mimeCodec = 'video/mp4; codecs="avc1.42E01E"';
/*mimeCodec = 'video/mp4; codecs="avc1.42E01E,mp4a.40.2"'; /* 'video/mp4; codecs="avc1.42E01E,mp4a.40.2"' */

// stream video 編號 延遲
let delay = 2;

// 直播當前時間點
let i = 2;

// setInterval(should_I_Append,100);
let ViewVideoTime ;

//如果影片目前時間點和直播時間點差太多，就跳去直播時間點。詳情請見 FetchAB(url)
let detectSecond = 0.1;

//串流影片名稱與「時間 Time」的對應和請求方式，詳情請見 should_I_Append()
let t = -1;

function shutdown(){}
function FetchAB(url){
    try{
        fetch(url, {method: 'GET',})
    	    .then(function(response){return response.arrayBuffer();})
    		.then( (data)=>{datas=data
			                //如果影片目前時間點和直播時間點差太多，就跳去直播時間點。
			                if(i-videoTag.currentTime>detectSecond){videoTag.currentTime=i}
			                SourceBuffer.timestampOffset = i;
			                SourceBuffer.appendBuffer(data);
							// 每段buffer影片間隔是0.1秒
	                        i+=0.1;}) 
		}			
	catch(error){
        console.log(error);
        console.log(1); 		
		}
}


function Video(){
    //初始化 Video		
    url = URL.createObjectURL(myMediaSource);
    videoTag.src = url;
	
    myMediaSource.addEventListener('sourceopen', ()=>{
    SourceBuffer = myMediaSource.addSourceBuffer(mimeCodec);
	ViewVideoTime = setInterval(should_I_Append,50);
	videoTag.play();
	document.body.click()
    } );
		
}

function should_I_Append(){
      //串流影片名稱與時間的對應和請求方式
      a=new Date().getMilliseconds();a=(a-a%100)/100
	  tt = a
	  if(tt>t || (tt==0 && t==9)){
	  //if((i-10)>0){SourceBuffer.remove(i-10,i-5)}
	  t = tt;
	  //console.log(t);console.log(tt);
	  // tim是mp4檔案的編號
	  if(t>=delay){tim = t-delay;}
	  else{tim=10+t-delay;}
	  ///////////////////////////////////////////////////////////////////////////////////////////////
      FetchAB("http://"+HostPort+"/videos/"+tim);}
} 

function video_size(){
    h = document.getElementById("h").innerHTML;
    w = document.getElementById("w").innerHTML;
      
    h = parseInt(h, 10);
    w = parseInt(w, 10);
    //w是h的幾倍，h乘以多少會變成w
    scale = w/h;
    
    h = (window.innerHeight)*2/3;
    w = h*scale;
    
    h = parseInt(h, 10);
    w = parseInt(w, 10);
    
    Height.value = h;
    Width.value = w;
    videoTag.height = Height.value;
    videoTag.width = Width.value;
     videoTag.height = 600;
    videoTag.width =600; 
}

function chg(str){
    var oReq = new XMLHttpRequest();
    oReq.open("GET", "http://"+HostPort+"/RGB/"+str);
    oReq.send(null);
}


Video(); 
video_size(); 
r.onchange=()=>{chg("r_"+r.value)};
g.onchange=()=>{chg("g_"+g.value)};
b.onchange=()=>{chg("b_"+b.value)};

 
function stream(){
  //跳去直播時間點。
  videoTag.currentTime=i;
}

function Play(){
  videoTag.play();
}

function Stop(){
  clearInterval(ViewVideoTime);
  myMediaSource.endOfStream(); 
}  

function Pause(){
  videoTag.pause();  
}

function Reset(){
  video_size(); 
  r.value = 0;
  g.value = 0;
  b.value = 0;  
  chg("r_"+r.value);
  chg("g_"+g.value);
  chg("b_"+b.value);
  }
function Apply(){
  try{
    videoTag.height = Height.value;
    videoTag.width = Width.value;  }
  catch(err){
  }
}   
