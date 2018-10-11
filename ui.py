import html

class UI:

    def __init__(self):
        pass

    def display(self, *args):
        print(*args)

    def input(self, args=None):
        return input(args)

    def displayHTMLchars(self, s):
        self.display(html.unescape(s))