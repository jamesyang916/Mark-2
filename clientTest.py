import socket
import time
import threading
import sys
import signal
import platform

class Client(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        HOST = '127.0.0.1'
        PORT = 5002
        self.sock.connect((HOST, PORT))
      
    def run(self):
        thread1 = threading.Thread(target = self.inputThread)
        thread2 = threading.Thread(target = self.outputThread)
        thread1.daemon = True
        thread2.daemon = True
        thread1.start()
        thread2.start()
      
        if platform.system() == 'Linux':
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.pause()
        else:
            try:
                thread1.join()
                thread2.join()
            except:
                time.sleep(1.5)
                sys.exit(0)
  
    def inputThread(self):
        while 1:
            try:
                line = raw_input()
                self.sock.sendall(line)
            except (KeyboardInterrupt, EOFError):
                print "Disconnecting from server..."
                break
            except socket.error:
                print "Socket error. Press ctrl+c to exit."
                break
        self.sock.close()
        sys.exit()
  
    def outputThread(self):
        while 1:
            try:
                line = self.sock.recv(1024)
                if not line:
                    raise socket.error
                print line
            except socket.error:
                print "Socket error. Press ctrl+c to exit."
                break
        self.sock.close()
        sys.exit()
      
    def signal_handler(self, signal, frame):
        print "Disconnecting from server..."
        self.sock.close()
        time.sleep(1.5)
        sys.exit(0)
        
if __name__ == '__main__':
    oClient = Client()
    oClient.run()