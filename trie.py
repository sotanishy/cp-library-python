class Trie:
    class Node:
        def __init__(self):
            self.child = [-1] * 26
            self.is_end = False
            self.count = 0

    def __init__(self):
        self.nodes = [self.Node()]

    def add(self, s, i):
        node = 0
        for c in s:
            c = ord(c) - ord('a')
            if self.nodes[node].child[c] == -1:
                self.nodes[node].child[c] = len(self.nodes)
                self.nodes.append(self.Node())
            self.nodes[node].count += 1
            node = self.nodes[node].child[c]
        self.nodes[node].is_end = True

    def query(self, s):
        node = 0
        for c in s:
            c = ord(c) - ord('a')
            if self.nodes[node].child[c] == -1:
                return 0
            node = self.nodes[node].child[c]
        return self.nodes[node].count