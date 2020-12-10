class Action:
    def __init__(self,
                 _who=None,
                 _how=None,
                 _what=None,
                 _whom=None,
                 _with=None,
                 _case=None):
        self._who = _who
        self._how = _how
        self._what = _what
        self._whom = _whom
        self._with = _with

    def define_who(self, value):
        self._who = value

    def define_how(self, value):
        self._how = value

    def define_what(self, value):
        self._what = value

    def define_whom(self, value):
        self._whom = value

    def define_with(self, value):
        self._with = value

    def print(self, heads=False):
        arrow = ' > ' if heads else ''
        s = 'ACTION: '

        if self._who:
            s += self._who.text + '(who?)' + arrow
        if self._how and self._what:
            s += self._how.text + '(how?)'  + arrow
        if self._who and self._what:
            s += self._what.text + '(what?)' + arrow
        if self._who and self._what and self._whom:
            s += self._whom.text + '(whom?)'
        if self._who and self._what and self._whom and self._with:
            s += arrow + self._with.text + '(with what?)'

        print(s)

    def do(self):
        self.print()
