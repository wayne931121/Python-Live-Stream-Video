#參考資料 https://stackoverflow.com/questions/14283025/python-3-reading-bytes-from-stdin-pipe-with-readahead?msclkid=e76cd02cb0e311ecb0e1e780bd4ed55b

with open("Main.py","r",encoding="utf8") as f:
  data = f.read()
  print(data)
  
for i in range(10):
  with open(str(i)+".py" , "w", encoding="utf8") as f:
    f.write(data%i)  