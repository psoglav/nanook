class Act(object):
    def detect_root(self, tokens):
        candidates = [t for t in tokens if t.rel == 'root']

        if not len(candidates):
            candidates = [t for t in tokens if t.head_id == '1_0']

        if not len(candidates):
            print(tokens)
            self.root = None
            return

        self.root = Act.patch_token(candidates[0], tokens)

    def detect_subject(self, tokens):
        if not self.root:
            return
        else:
            for t in tokens:
                if self.is_subject(t):
                    self.subject = Act.patch_token(t, tokens)

    def detect_object(self, tokens):
        if not self.root:
            return
        else:
            for t in tokens:
                if self.is_object(t):
                    self.object = Act.patch_token(t, tokens)

    def is_subject(self, t):
        return Act.points_to(t, self.root['token']) and Act.has_any(t, ['nsubj', 'nsubj:pass'])

    def is_object(self, t):
        return Act.points_to(t, self.root['token']) and Act.has_any(t, ['obj'])

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
    def patch_token(token, tokens):
        return {
            "token": token,
            "related": Act.get_related(token, tokens)
        }

    @staticmethod
    def merge_with_related(patched_token):
        tokens = patched_token['token']
        s = patched_token['token'].text

        if len(patched_token['related']):
            for rel in patched_token['related']:
                tokens.append(rel)
                s += ', ' + rel.text

        return tokens, s

    def print(self):
        if not self.root:
            return

        subject = self.subject['token'].text

        if len(self.subject['related']):
            for rel in self.subject['related']:
                subject += ', ' + rel.text

        action = self.root['token'].text

        print(subject + ' --> ' + action)
