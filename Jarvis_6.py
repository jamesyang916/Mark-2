# Jarvis_6
import threading
import Interpret
import Mobile
import Console
import sys
import time
import signal # Linux only
import platform # check platform

# Master Operator
class Jarvis(object):    
    # Jarvis Object Instantiation
    def __init__(self):
        self.oInterpret = None
        self.oMobile = None
        self.oConsole = None
        #self.notifier = None

    def setup(self):
        print "Creating Interpret and Stream objects..."
        # Create Interpret Object
        self.oInterpret = Interpret.Interpret()

        # Create Stream Object
        self.oMobile = Mobile.Mobile(self.oInterpret)
        self.oConsole = Console.Console(self.oInterpret)

        # Create Notifying Object
        #self.notifier = threading.Thread(target=self.notify)

        # Wifi Control on Interpret and Output

        print "Task Completed."       

    def initiate(self):
        print 'Initiating objects...'
        communication_Event = threading.Event()
        communication_Event.set()

        mobileThread = threading.Thread(target = self.oMobile.mobile, name = "Mobile",
                                        args = (communication_Event,))
        consoleThread = threading.Thread(target = self.oConsole.console, name = "Console",
                                         args = (communication_Event,))

        mobileThread.daemon = True
        consoleThread.daemon = True

        mobileThread.start()
        consoleThread.start()
        
        print 'Done.'
        
        if platform.system() == 'Linux':
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.pause()

        else:
            try:
                consoleThread.join() # order matters
                mobileThread.join()
            except:
                print "Shutting down Mark-2..."
                time.sleep(1.5)
                sys.exit(0)

    def signal_handler(self, signal, frame):
        print "Shutting down Mark-2..."
        time.sleep(1.5)
        sys.exit(0)
        


        
    
        
   
        
        
        