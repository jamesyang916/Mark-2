import threading
import socket 

class Mobile(object):
    def __init__(self, oInterpret):
        self.oInterpret = oInterpret
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        HOST = ''
        PORT = 5002
        self.sock.bind((HOST,PORT))
        self.sock.listen(10) # arbitrary

    def mobile(self, communication_Event):      
        while communication_Event.is_set():
            try:     
                conn, addr = self.sock.accept()
                print "Client %s connected." %(addr[0],)

                connThread = threading.Thread(target = self.connOperator,
                                                args = (conn, addr,))
                connThread.daemon = True
                connThread.start()
 
            except:
                print "Closing all threads..."
                communication_Event.clear()

    
    def connOperator(self, conn, addr):
        forked_Event = threading.Event()
        forked_Event.set()
        while 1:
            try:
                line = conn.recv(1024) # pause here and send multiple from client
                thread = threading.Thread(target = self.inputOperator,
                                          args = (line, conn, forked_Event,))
                thread.daemon = True
                thread.start()

            except socket.error as e:
                print "Client %s has disconnected." %(addr[0],)
                conn.close()
                break

    def inputOperator(self, line, conn, forked_Event):
        res = self.oInterpret.interpret(line)
        if res == None:
            return
        try:
            if forked_Event.is_set():
                conn.sendall(res)
        
        except socket.error:
            forked_Event.clear()
        
        

if __name__ == "__main__":
    import Interpret
    print "Testing Mobile..."
    oInterpret = Interpret.Interpret()
    oMobile = Mobile(oInterpret)
    communication_Event = threading.Event()
    communication_Event.set()
    print "Objects created."
    oMobile.mobile(communication_Event)
    print "Successful launch."


