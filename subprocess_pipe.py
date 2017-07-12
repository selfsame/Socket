import subprocess
import pty, os, re
from Socket.repl import Repl
import sublime, sublime_plugin

class SubprocessPipe(Repl):
    def __init__(self, view, cmd, args=[], initial=None):
        primary, secondary = pty.openpty()
        self.proc = subprocess.Popen([cmd] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True)
        Repl.__init__(self, view, type, initial)
        
    def on_close(self):
        self.running = False
    
    def send(self, str):
        self.record_history(str)
        self.proc.stdin.write(str.encode('utf8'))
        self.proc.stdin.flush()
        #self.proc.communicate(str.encode('utf8'))
        
    def run(self):
        while self.running:
            read = self.proc.stdout.readline() # TODO stderr?
            self.buffer.append(self.carraige_return(self.escape_ansi(read.decode('utf8'))))

    def escape_ansi(self, s):
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', s)

    def carraige_return(self, s):
        ansi_escape = re.compile(r'\r\n')
        return ansi_escape.sub('\n', s)