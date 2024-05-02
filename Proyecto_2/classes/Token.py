class Token():
    def __init__(self, name, value, line, column):
        self.name = name
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.name}, {self.value}, {self.line}, {self.column})"

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def get_line(self):
        return self.line

    def set_line(self, line):
        self.line = line
    
    def get_column(self):
        return self.column

    def set_column(self, column):
        self.column = column