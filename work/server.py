# encoding=utf-8
import os, sys
import socket
class DataServer:
    port = 10000
    def __init__(self):
        pass
    def run(self):
        dsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dsoc.bind(('localhost', self.port))
        print("listening at", self.port)
        while True:
            dsoc.listen(1)
            conn, addr = dsoc.accept()
            print("connected", addr)
            databuf = conn.recv(13)
            databuf=databuf.decode("gb2312")
            print("received", databuf)
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
                fp = open(filename, 'wb')
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
                fp = open(filename, 'rb')
                while True:
                    data = fp.read(4096)
                    if not data:
                        break
                    while len(data) > 0:
                        sent = conn.send(data)
                        data = data[sent:]
                print("Fished to send ", filename)
            conn.close()
    def setPort(self, port):
        self.port = int(port)
if __name__ == "__main__":
     ds = DataServer()
     ds.setPort(sys.argv[1])
     ds.run()
