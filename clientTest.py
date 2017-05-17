import socket
import time
import threading
import sys

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    HOST = '127.0.0.1'
    PORT = 5002
    s.connect((HOST, PORT))

    thread1 = threading.Thread(target = inputThread, args=(s,))
    thread2 = threading.Thread(target = outputThread, args=(s,))
    thread1.daemon = True
    thread2.daemon = True
    thread1.start()
    thread2.start()
    try:
        thread1.join()
        thread2.join()
    except:
        pass


def inputThread(sock):
    while 1:
        try:
            line = raw_input()
            sock.sendall(line)
        except (KeyboardInterrupt, EOFError):
            print "Keyboard interrupted. Disconnecting from server..."
            time.sleep(2)
            break
        except socket.error:
            break
    sock.close()
    sys.exit()

def outputThread(sock):
    while 1:
        try:
            print sock.recv(1024)
        except socket.error:
            print "Disconnected from server. Enter any key to exit."
            break
    sock.close()
    sys.exit()
if __name__ == '__main__':
    main()