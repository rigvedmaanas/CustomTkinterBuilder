class CodeGenerator:
    def __init__(self, indentation="\t"):
        self.indentation = indentation
        self.indent_level = 0
        self.code = ""

    def indent(self):
        self.indent_level += 1

    def detent(self):
        self.indent_level -= 1

    def add_line(self, line):
        self.code += (self.indentation * self.indent_level) + line + "\n"

    def get_code(self):
        return self.code
