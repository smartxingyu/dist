# encoding=utf-8
import os, sys
import socket
import threading
import json
from threading import *
from time import strftime,gmtime
class DataServer:
    port = 10000
    def __init__(self):
        pass
    def create(self):
        masterlink=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        masterlink.connect(("127.0.0.1",1234))
        messg="new server,%04d"%self.port
        masterlink.send(messg.encode("gb2312"))
        masterlink.close()

    def GetFileList(self,dir, fileList):
        newDir = dir
        if os.path.isfile(dir):
            fileList.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.GetFileList(newDir, fileList)
        return fileList
    def clientthread(self, conn):
        databuf = conn.recv(13)
        databuf = databuf.decode("gb2312")
        print("received", databuf)
        if databuf=="get filelist":
            f = []
            conn.send(json.dumps(self.GetFileList("file",f)).encode("gb2312"))
            print("send filelist success")
        if databuf.startswith('WRITFILE'):
            print("OPS == write file")
            dlist = databuf.split(',')
            fnamelen = int(dlist[1])
            conn.send('OK'.encode("gb2312"))
            print("filenamelen is", fnamelen)
            filename = conn.recv(fnamelen)
            filename = filename.decode("gb2312")
            filename = filename[filename.rindex('\\') + 1:]
            print("file is", filename)
            fp = open("file\\" + filename, 'wb')
            while True:
                data = conn.recv(1024)
                if not data: break
                fp.write(data)
            fp.flush()
            fp.close()
            print("finished!", filename)
        if databuf.startswith('FETCFILE'):
            print("OPS == fetch file")
            dlist = databuf.split(',')
            fnamelen = int(dlist[1])
            conn.send('OK'.encode("gb2312"))
            print("filenamelen is", fnamelen)
            filename = conn.recv(fnamelen)
            filename = filename.decode("gb2312")
            filename = filename[filename.rindex('\\') + 1:]
            print("file is", filename)
            fp = open("file\\"+filename, 'rb')
            while True:
                data = fp.read(4096)
                if not data:
                    break
                while len(data) > 0:
                    sent = conn.send(data)
                    data = data[sent:]
            print("Fished to send ", filename)
        conn.close()
    def run(self):
        dsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dsoc.bind(('localhost', self.port))
        print("listening at", self.port)
        dsoc.listen(5)
        while True:
            conn, addr = dsoc.accept()
            print("connected", addr)
            threading.Thread(target=self.clientthread(conn), args=(conn)).start()
    def setPort(self, port):
        self.port = int(port)
if __name__ == "__main__":
     ds = DataServer()
     ds.setPort(sys.argv[1])
     ds.create()
     ds.run()
