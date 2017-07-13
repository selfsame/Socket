import threading
import errno
import sublime, sublime_plugin
import re

class Repl(threading.Thread):
    def __init__(self, view, type="none", initial=None):
        threading.Thread.__init__(self)
        self.running = True
        self.view = view
        self.written_characters = 0
        self.buffer = []
        self.prompt = 6
        self.hist = 0
        self.history = []

        if(initial):
            self.send(initial)
    
    def go(self):
        self.setup_view()
        self.update_view()
        self.start()

    def setup_view(self):
        self.view.set_scratch(True)
        self.view.settings().set("socket", True)
        self.view.settings().set("scope_name", "source.clojure")
        self.view.settings().set("line_numbers", False)
        self.view.settings().set("gutter", False)
        self.view.settings().set("word_wrap", False)

    def update_view(self):
        res = self.carraige_return(self.escape_ansi("".join(self.buffer)))
        if res != "":
            self.view.run_command("socket_insert_text", {"content": res})
        self.buffer = []
        if self.running:
            sublime.set_timeout(self.update_view, 100)
        
    def on_close(self):
        self.running = False
    
    def record_history(self, s):
        rx = re.search("[\\n]*$", s)
        if rx:
            s = s[:len(rx.group()) * -1]
        hlen = len(self.history)
        if s != "" and (hlen == 0 or (hlen > 0 and s != self.history[hlen-1])):
            self.history.append(s)
            self.hist = 0

    def send(self, s):
        self.record_history(s)
        self.sock.send(s.encode('utf-8'))
        
    def write(self, s):
        self.buffer.append(s)
        
    def bump(self, s):
        self.written_characters += len(s)
        
    def run(self):
        pass

    def escape_ansi(self, s):
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', s)

    def carraige_return(self, s):
        ansi_escape = re.compile(r'\r\n')
        return ansi_escape.sub('\n', s)