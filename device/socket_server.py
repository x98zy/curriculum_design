# coding=utf-8

import socket,select
from PIL import Image
from io import BytesIO
import os
from threading import Thread,RLock


res=b'' #数据保存缓存
start_index,end_index=None,None #图片起始位，结束位

def draw_jpeg():
    global start_index,end_index,res
    print(len(res))
    try:
        start_index=res.index(b"\xff\xd8")
    except Exception as e:
        pass
    try:
        end_index=res.index(b"\xff\xd9")
    except Exception as e:
        pass
    if start_index and end_index:
        con = res[start_index:end_index + 2]
        hexdata = con.hex()
        hexdata.replace("\r\n", "")
        pic = bytes.fromhex(hexdata)
        bytes_stream = BytesIO(pic)
        jpg = Image.open(bytes_stream)
        try:
            jpg.save("../media/video.jpg", "JPEG")
        except OSError as e:
            pass
        try:
            res=res[end_index+2:]
        except Exception as e:
            pass
        start_index, end_index = None, None



def ReceiveData():
    global res
    s = socket.socket()
    # host = socket.gethostname()
    host = '0.0.0.0'
    print(host)
    port = 81
    s.bind((host, port))
    s.listen(5)
    inputs = [s]
    while True:
        rs, ws, es = select.select(inputs, [], [])
        for r in rs:
            if r is s:
                c, addr = s.accept()
                inputs.append(c)
                print(addr)
            else:
                try:
                    data = r.recv(1024)
                    disconnected = not data
                except:
                    disconnected = True
                if disconnected:
                    inputs.remove(r)
                else:
                    res += data
                    thread1=Thread(target=draw_jpeg,args=())
                    thread1.start()


ReceiveData()
