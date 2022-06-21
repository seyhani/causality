class WordList:
    def __init__(self, words=None):
        if words is None:
            words = []
        self.words = words

    def is_empty(self):
        return len(self.words) == 0

    def add(self, word):
        self.words.append(word)

    def total_len(self):
        return sum(list(map(len, self.words)))

    def __str__(self):
        return ", ".join(self.words)
