// 參考網站
/* 
https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Sending_and_Receiving_Binary_Data?msclkid=4b40ee72ad0011ec909e14a6e1075844
https://developer.mozilla.org/en-US/docs/Web/API/Blob
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer
https://www.bennadel.com/blog/3472-downloading-text-using-blobs-url-createobjecturl-and-the-anchor-download-attribute-in-javascript.htm?msclkid=581f7bf0ad0211ec9dad145aa50fc87c
*/

let d;
let byteArray,c,url;
var oReq = new XMLHttpRequest();
oReq.open("GET", "http://127.0.0.1:9999/");
oReq.responseType = "arraybuffer";

oReq.onload = function (oEvent) {
  var arrayBuffer = oReq.response; // Note: not oReq.responseText
  if (arrayBuffer) {
    d = (arrayBuffer);
	byteArray = new Uint8Array(d);
	c = new Blob([d],{type : "text/plain;charset=utf-8"});
	url = URL.createObjectURL(c);
	console.log(d);
	console.log(byteArray);
	console.log(c);
	console.log(url);
	var download = document.querySelector( "a[ download ]" );
	//In HTML :<a href="" download="data.txt" style="width: 100;height: 100;">data download</a>
	download.setAttribute( "href", url );
  }
};
oReq.send(null);
//URL.revokeObjectURL(url)
