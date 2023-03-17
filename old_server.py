import socket
import threading
import os

class httpServer(object):
    def __init__(self,host="localhost",port=449):
        print("Serving on '{0}' port '{1}'.".format(host,port))
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host,port))
    def listen(self):
        self.socket.listen(1)
        while True:
            client,address=self.socket.accept()
            #client.settimeout(5)
            threading.Thread(target=self.thread,args=(client,address)).start()
    def parse(self,request):
        try:
            fields = request.split("\r\n")
            fields = fields[1:]
            output = {}
            output["Mode"]=request.split("\r\n")[0].split(" ")[0]
            output["File"]=request.split("\r\n")[0].split(" /")[1].split(" ")[0]
            for field in fields:
                if not field:
                    continue
                key,value = field.split(':',1)
                output[key] = value.strip()
            return output
        except Exception as e:
            return
    def response(self,request):
        try:
            request=self.parse(request)
            mode=request["Mode"]
            print(mode)
            requestFile=request["File"]
            print("Requested file '{0}'.".format(requestFile))
            if requestFile=="":
                requestFile="index.html"
            file=open(os.path.join(os.getcwd(),"access",requestFile),"rb")
            data=file.read()
            if file!=None:
                file.close()
            if requestFile.endswith(".htm"):
                fileType="text/htm"
            elif requestFile.endswith(".jpg"):
                fileType="image/jpg"
            elif requestFile.endswith(".png"):
                fileType="image/png"
            elif requestFile.endswith(".htm"):
                fileType="text/htm"
            else:
                fileType="text/html"
            response=("HTTP/1.1 200 OK\n"+"Content-Type: "+fileType+"\n\n").encode("utf-8")+data
        except Exception as e:
            print(e)
            response=("HTTP/1.1 200 OK\n\n"+'404 not found').encode()
        return response

    def thread(self,client,address):
        request=client.recv(1024).decode("utf-8")
        print(request)
        response=self.response(request)
        client.send(response)
        client.close()
            
 
'''while True:
    connection,address = sock.accept()
    requests = connection.recv(1024).decode('utf-8')
    try:
        requests=request.parse(requests)
    except Exception as e:
        print(e)
    #mode,file=requests["Mode"],requests["File"]
    #print("Request:",mode,",",file)
    connection.send("HTTP/1.1 200 OK\n\n".encode()+b'200 OK')
    connection.close()'''
if __name__ == "__main__":
    httpServer('localhost',80).listen()
