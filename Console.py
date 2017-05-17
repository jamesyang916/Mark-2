import threading

class Console(object):
    def __init__(self, oInterpret):
        self.oInterpret = oInterpret

    '''
    Fork every input.
    '''
    def console(self, communication_Event):
        forked_Event = threading.Event()
        forked_Event.set()
        while communication_Event.is_set():
            try:
                line = raw_input()
                thread = threading.Thread(target = self.inputOperator, name = 'forked_console',
                                            args = (line, forked_Event,))
                thread.daemon = True
                thread.start()
            except (KeyboardInterrupt, EOFError):
                print "Closing all threads..."
                communication_Event.clear()

    '''
    Interprets input and prints the result.
    '''
    def inputOperator(self, line, forked_Event):
        res = self.oInterpret.interpret(line)
        if res == None:
            return
        try:
            if forked_Event.is_set():
                print res
        except KeyboardInterrupt:
            print "KeyboardInterrupt exception."
            forked_Event.clear()
           
                

if __name__ == '__main__':
    import Interpret
    print "Testing Console..."
    oInterpret = Interpret.Interpret()
    oConsole = Console(oInterpret)
    print "Objects created."
    oConsole.console()
    print "Successful launch."