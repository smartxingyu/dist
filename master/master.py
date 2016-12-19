# encoding=utf-8
import os, sys
import socket
import json
class master:
    port = 1234
    count = 0
    clist = []
    connect_number=0
    def __init__(self):
        pass
    def run(self):
        conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        conn.bind(("localhost",self.port))
        print("listen at ",self.port)
        conn.listen(5)
        while True:
            ack,addr=conn.accept()
            print("connect",addr)
            databuff=ack.recv(1024)
            databuff=databuff.decode("gb2312")
            if databuff.startswith("new server"):
                dlist = databuff.split(',')
                self.clist.append([addr[0],dlist[1],0])
                print("add server success")
                print(self.clist)
            if databuff=="new client":
                self.count=self.count+1
                for i in self.clist:
                    print("new client")
                    if i[2]<5:
                        ack.send(json.dumps([i[0],i[1],self.count]).encode("gb2312"))
                        break
if __name__ == "__main__":
     ds = master()
     # ds.setPort(sys.argv[1])
     ds.run()