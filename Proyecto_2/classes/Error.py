class Error():
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Error({self.value}, {self.line}, {self.column})"