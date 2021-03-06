INTEGER =       'INTEGER'
PLUS =          'PLUS'
MINUS =         'MINUS'
MULTIPLY =      'MULTIPLY'
DIVIDE =        'DIVIDE'
EOF =           'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def build_integer(self):
        integer = ''
        while self.current_char is not None and self.current_char.isdigit():
            integer += self.current_char
            self.advance()
        return int(integer)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isdigit():
                token = Token(INTEGER, self.build_integer())
                return token

            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
                self.advance()
                return token

            if self.current_char == '-':
                token = Token(MINUS, self.current_char)
                self.advance()
                return token

            if self.current_char == '*':
                token = Token(MULTIPLY, self.current_char)
                self.advance()
                return token

            if self.current_char == '/':
                token = Token(DIVIDE, self.current_char)
                self.advance()
                return token

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            print(self.current_token)
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()


        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == 'PLUS':
            self.eat(PLUS)
        if op.type == 'MINUS':
            self.eat(MINUS)
        if op.type == 'MULTIPLY':
            self.eat(MULTIPLY)
        if op.type == 'DIVIDE':
            self.eat(DIVIDE)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == 'PLUS':
            result = left.value + right.value
            return result
        if op.type == 'MINUS':
            result = left.value - right.value
            return result
        if op.type == 'MULTIPLY':
            result = left.value * right.value
            return result
        if op.type == 'DIVIDE':
            result = left.value / right.value
            return result


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
