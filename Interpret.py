# Input Interpreter
import string
import threading

# for updateDict only
import os.path
import time

class Interpret(object):
    # Wikipedia
    # Wolfram Q35XX4-9AG2KK3Q9L
    # last resort: Google Search API:
    # collect data from very first link: all sentences w/ highlighted words.
    # "..."\n(source1)\n"..."\n(source2)\n"

    def __init__(self):
        self.options = {}
        self.oldTime = 0.0
        self.buildDict()

    def updateDict(self, communication_Event):
        while communication_Event.is_set():
            newTime = os.path.getmtime('Database.txt')
            if newTime > self.oldTime:
                print "Updating database..."
                self.buildDict()
                print "Done."
            time.sleep(1.5)

    def buildDict(self):
        with open('Database.txt') as f:
            for line in f:
                arr = line.split('$$')
                if len(arr) != 2:
                    continue
                self.options[arr[0]] = arr[1]
        self.oldTime = os.path.getmtime('Database.txt')
            
    def interpret(self, m):
        ##### Special Commmands #####

        # print working threads
        if m == '-p threads':
            threadLst = threading.enumerate()
            return "%s threads working: %s" %(len(threadLst), threadLst,)

        ##### Normal Process ####
        msg = m.lower().translate(None, string.punctuation)
        try:
            res = self.options[msg]
        except KeyError:
            res = 'No information.'
        
        return res

if __name__ == "__main__":
    communication_Event = threading.Event()
    communication_Event.set()
    oInterpret = Interpret()
    oInterpret.updateDict(communication_Event)

