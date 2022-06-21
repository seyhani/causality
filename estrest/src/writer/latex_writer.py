from writer.word_list import WordList

LINE_BREAK_THRESHOLD = 100


class LatexWriter:
    def __init__(self):
        self.out = ''

    def begin(self):
        self.out += "\n\\begin{align*} \n"

    def write_title(self, line):
        self.write_line("& {} &".format(line))

    def write_sub_title(self, line):
        self.write_line("& \\ \\ {} &".format(line))

    def write_line(self, line):
        self.out += "\t {} \\\\ \n".format(line)

    def write_tabbed_line(self, line):
        self.write_line("& \\qquad {}".format(line))

    def end(self):
        self.out += "\\end{align*} \n"

    def write_words(self, words: WordList):
        line_words = WordList()
        for word in words.words:
            if len(word) + line_words.total_len() <= LINE_BREAK_THRESHOLD:
                line_words.add(word)
            else:
                self.write_tabbed_line(line_words)
                line_words = WordList([word])
        if not line_words.is_empty():
            self.write_tabbed_line(line_words)
