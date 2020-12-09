class Action:
    def __init__(self, who=None, how=None, what=None, whom=None):
        self.who = who
        self.how = how
        self.what = what
        self.whom = whom

    def define_who(self, value):
        self.who = value

    def define_how(self, value):
        self.how = value

    def define_what(self, value):
        self.what = value

    def define_whom(self, value):
        self.whom = value

    def print(self):
        s = self.who['text'] + ' --> '
        s += self.how['text'] + ' '
        s += self.what['text'] + ' --> '
        s += self.whom['text']

        print(s)

    def do(self):
        self.print()
