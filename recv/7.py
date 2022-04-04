#參考資料 https://stackoverflow.com/questions/14283025/python-3-reading-bytes-from-stdin-pipe-with-readahead?msclkid=e76cd02cb0e311ecb0e1e780bd4ed55b
import sys
from multiprocessing import shared_memory
video = shared_memory.SharedMemory("video"+str(7))
data = sys.stdin.buffer.read()
video.buf[0:1+len(str(len(data)))+len(data)] = bytes(str(len(str(len(data)))),"utf8")+bytes(str(len(data)),"utf8")+data