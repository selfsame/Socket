import subprocess
import pty, os, re, io
from Socket.repl import Repl
import sublime, sublime_plugin

class SubprocessPipe(Repl):
    def __init__(self, view, cmd, args=[], initial=None):
        primary, secondary = pty.openpty()
        self.proc = subprocess.Popen([cmd] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True)
        view.settings().set("pipe", True)
        Repl.__init__(self, view, type, initial)
        
    def on_close(self):
        self.running = False
    
    def send(self, str):
        self.record_history(str)
        self.proc.stdin.write(str.encode('utf8'))
        self.proc.stdin.flush()
        
    def run(self):
        #input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        while self.running:
            read = self.proc.stdout.read(1) # TODO stderr?
            try:
                self.buffer.append(read.decode('utf8'))
            except UnicodeDecodeError:
                self.buffer.append(str(read)[2:-1])