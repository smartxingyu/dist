# encoding=utf-8
import os
import socket
import json

class Client:
    maList = []
    macNum = 0
    def __init__(self):
        pass
    def configure(self):
        m=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        m.connect(("127.0.0.1",1234))
        m.send("new client".encode("gb2312"))
        msg=m.recv(1024)
        msg=json.loads(msg.decode("gb2312"))
        self.maList.append(msg[0])
        self.maList.append(msg[1])
        self.macNum = msg[2]
        m.close()
    def write(self, src):
        print("File is", src)
        toIp = self.maList[0]
        toPort = self.maList[1]
        print("Send to", toIp, toPort)
        self.send(src.encode("gb2312"), toIp, toPort)
    def send(self, src, ip, port):
         clsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clsoc.connect((ip, int(port)))
         fp = open(src, 'rb')
         formStr = "WRITFILE,%04d" % len(src)
         print("formStr", formStr, len(formStr))
         clsoc.send(formStr.encode("gb2312"))
         resdata = clsoc.recv(1024)
         resdata = resdata.decode("gb2312")
         if resdata.startswith('OK'):
             print("OK")
         print("sending....", src)
         clsoc.send(src)
         print("sending data....")
         while True:
            data = fp.read(4096)
            if not data:
                break
            while len(data) > 0:
                sent = clsoc.send(data)
                data = data[sent:]
         print("Fished to send ", src)
         fp.close()
    def fetch(self, src):
        toIp = self.maList[0]
        toPort = self.maList[1]
        print("fetch from", toIp, toPort)
        self.get(src, toIp, toPort)
    def get(self, src, ip, port):
        clsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clsoc.connect((ip, int(port)))
        formStr = "FETCFILE,%04d" % len(src)
        print("formStr", formStr)
        clsoc.send(formStr.encode("gb2312"))
        resdata = clsoc.recv(1024)
        resdata = resdata.decode("gb2312")
        if resdata.startswith('OK'):
            print("OK")
        print("sending....", src)
        clsoc.send(src.encode("gb2312"))
        print("fetching data....")
        ffile = src[src.rindex('\\') + 1:]
        fp = open(ffile, 'wb')
        while True:
            data = clsoc.recv(1024)
            if not data: break
            fp.write(data)
        fp.flush()
        fp.close()
        print("finished!",ffile)
    def Getfilelist(self):
        toIp = self.maList[0]
        toPort = self.maList[1]
        clsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clsoc.connect((toIp, int(toPort)))
        clsoc.send("get filelist".encode("gb2312"))
        filelist = clsoc.recv(1024)
        filelist = json.loads(filelist.decode("gb2312"))
        print(filelist)
        clsoc.close()
if __name__ == "__main__":
    mac = Client()
    mac.configure()
    src = "\\word.txt"
    mac.Getfilelist()
    # mac.write(src)
    mac.fetch(src)