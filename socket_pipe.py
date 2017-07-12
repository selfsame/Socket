from Socket.repl import Repl
import socket
import sublime, sublime_plugin

class SocketPipe(Repl):
    def __init__(self, view, host, port, type="tcp", initial=None):
        if type == "tcp":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif type == "tcp6":
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        elif type == "udp":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            raise "Invalid type"
        self.sock.connect((host, port))
        print("Connected SocketPipe to %s:%s" % (host, port))
        
        Repl.__init__(self, view, type, initial)
    
    def on_close(self):
        self.running = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def send(self, s):
        self.record_history(s)
        self.sock.send(s.encode('utf-8'))
        
    def run(self):
        while self.running:
            try:
                read = self.sock.recv(8012)
                self.buffer.append(read.decode('utf8'))
            except socket.error:
                print("connecting...")