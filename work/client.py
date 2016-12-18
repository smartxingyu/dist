# encoding=utf-8
import os
import socket
import hashlib
class Configuration:
    count = 0
    clist = []
    def __init__(self):
        self.readPath("conf.txt")
    def readPath(self, pStr):
        self.pathStr = pStr
        fp = open(self.pathStr, 'r')
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.rstrip()
            self.clist.append(line)
            self.count = self.count + 1
    def getCount(self):
         return self.count
    def getList(self):
        return self.clist
class Client:
    maList = []
    macNum = 0
    def __init__(self):
        conf = Configuration()
        self.maList = conf.getList()
        self.macNum = conf.getCount()
    def write(self, src):
        srcHash = self.hash(src.encode("gb2312"))
        print("File is", src)
        locatedNum = srcHash % self.macNum
        print("Location machine number is", locatedNum)
        IPort = self.maList[locatedNum].split(',')
        toIp = IPort[0]
        toPort = IPort[1]
        print("Send to", toIp, toPort)
        self.send(src.encode("gb2312"), toIp, toPort)
    def hash(self, src):
        md5 = hashlib.md5()
        md5.update(src)
        return int(md5.hexdigest()[-4:], 16)
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
        srcHash = self.hash(src.encode("gb2312"))
        locatedNum = srcHash % self.macNum
        IPort = self.maList[locatedNum].split(',')
        toIp = IPort[0]
        toPort = IPort[1]
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
            print("fetching", data[-8:])
            fp.flush()
            fp.close()
            print("finished!", src)
if __name__ == "__main__":
    mac = Client()
    src = "d:\\word.txt"
    mac.write(src)
    mac.fetch(src)