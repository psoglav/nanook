import termcolor as tc


class Act(object):
    root = None  # я [бью] эльфа
    xcomp = None  # я решил [ретироваться]

    subj = None  # [я] бью эльфа
    obj = None  # я бью [эльфа]
    iobj = None  # я бью эльфа [секирой]

    def detect_root(self, tokens):
        candidates = [t for t in tokens if t.rel == 'root']

        if not len(candidates):
            candidates = [t for t in tokens if t.head_id == '1_0']

        if not len(candidates):
            self.root = None
            return

        self.root = Act.patch_token(candidates[0], tokens)

    def detect_subject(self, tokens):
        if not self.root:
            return
        else:
            for t in tokens:
                if self.is_subject(t):
                    self.subj = Act.patch_token(t, tokens)

    def detect_object(self, tokens):
        if not self.root:
            return
        else:
            for t in tokens:
                if self.is_object(t):
                    self.obj = Act.patch_token(t, tokens)

    def detect_xcomp(self, tokens):
        if not self.root:
            return
        else:
            for t in tokens:
                if self.is_xcomp(t):
                    self.xcomp = Act.patch_token(t, tokens)

    def is_subject(self, t):
        return Act.points_to(t, self.root['token']) and Act.has_any(t, ['nsubj', 'nsubj:pass'])

    def is_object(self, t):
        return Act.points_to(t, self.root['token']) and Act.has_any(t, ['obj'])

    def is_xcomp(self, t):
        return Act.points_to(t, self.root['token']) and Act.has_any(t, ['xcomp'])

    @staticmethod
    def get_leaves(head, tokens):
        return [t for t in tokens if Act.points_to(t, head)]

    @staticmethod
    def points_to(token, head):
        return head.id == token.head_id

    @staticmethod
    def has_any(token, rels):
        return token.rel in rels

    @staticmethod
    def get_related(token, tokens):
        return [t for t in Act.get_leaves(token, tokens) if t.rel == 'conj']

    @staticmethod
    def get_related_deep(token, tokens):
        related = Act.get_related(token, tokens)

        if not len(related):
            return []

        for rel in related:
            related.extend(Act.get_related_deep(rel, related))

        return related

    @staticmethod
    def get_relation_tags(tokens):
        return [t.rel for t in tokens]

    @staticmethod
    def patch_token(token, tokens):
        return {
            "token": token,
            "related": Act.get_related_deep(token, tokens)
        }

    @staticmethod
    def merge_with_related(patched_token):
        tokens = [patched_token['token']]
        s = patched_token['token'].text

        if len(patched_token['related']):
            for rel in patched_token['related']:
                tokens.append(rel)
                s += ', ' + rel.text

        return tokens, s

    def compose(self):
        arrow = tc.colored(' --> ', 'red')
        _object = ''
        xcomp = ''

        if not self.root or not self.subj:
            return

        subj = Act.merge_with_related(self.subj)[1]
        action = self.root['token'].text
        
        if self.xcomp:
            xcomp = self.xcomp['token'].text

        if self.obj:
            _object = Act.merge_with_related(self.obj)[1]

        return (subj + arrow + action + ['', arrow + xcomp][bool(xcomp)] + ['', arrow + _object][bool(_object)]).strip()
