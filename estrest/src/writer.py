LINE_BREAK_THRESHOLD = 100
PAGE_BREAK_THRESHOLD = 50


class AlignWriter:
    def __init__(self):
        self.out = ''

    def begin(self):
        self.out += "\n\\begin{align*} \n"

    def add_title(self, line):
        self.add_line("& {} &".format(line))

    def add_sub_title(self, line):
        self.add_line("& \\ \\ {} &".format(line))

    def add_simple_line(self, line):
        self.add_line("& \\qquad {}".format(line))

    def add_line(self, line):
        self.out += "\t {} \\\\ \n".format(line)

    def end(self):
        self.out += "\\end{align*} \n"


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


class EquationWriter(AlignWriter):
    def __init__(self):
        super().__init__()

    def write_words(self, words: WordList):
        line_words = WordList()
        for word in words.words:
            if len(word) + line_words.total_len() <= LINE_BREAK_THRESHOLD:
                line_words.add(word)
            else:
                self.add_simple_line(line_words)
                line_words = WordList([word])
        if not line_words.is_empty():
            self.add_simple_line(line_words)

