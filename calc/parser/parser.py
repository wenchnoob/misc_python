from calc.lexer import lexer
from calc.lexer.lexer import Token


class Node:
    class Type:
        NUMERIC = 'NUMERIC'
        PLUS = 'PLUS'
        MINUS = 'MINUS'
        TIMES = 'TIMES'
        DIV = 'DIV'
        NEGATE = 'NEGATE'

    def __init__(self, type, val, children=[]):
        self.type = type
        self.val = val
        self.children = children

    def __str__(self):
        return self._rec_str(0)

    def _rec_str(self, d):
        tabs = '\t' * d
        t = f'{tabs}(type={self.type}, val={self.val})\n'
        for child in self.children:
            t += child._rec_str(d + 1)
        return t


class RDParser:
    def __init__(self, text, strategy=lexer.RegexLexer):
        self._lexer = strategy(text)
        self._lookahead = self._lexer.next_token()

    def program(self):
        return self._add()

    def _add(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        lhs = self._mult()

        while self._lookahead is not None and \
                (self._lookahead.token_type == Token.Type.PLUS
                 or self._lookahead.token_type == Token.Type.MINUS):
            lhs = Node(Node.Type.PLUS
                       if self._eat().token_type == Token.Type.PLUS
                       else Node.Type.MINUS, None, [lhs, self._mult()])
        return lhs

    def _mult(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        lhs = self._primitive()
        while self._lookahead is not None and \
                (self._lookahead.token_type == Token.Type.TIMES
                 or self._lookahead.token_type == Token.Type.DIV):
            lhs = Node(Node.Type.TIMES
                       if self._eat().token_type == Token.Type.TIMES
                       else Node.Type.DIV, None, [lhs, self._primitive()])
        return lhs

    def _primitive(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        if self._lookahead.token_type == Token.Type.MINUS:
            self._eat()
            return Node(Node.Type.NEGATE, None,  [self._primitive()])
        elif self._lookahead.token_type == Token.Type.NUMERIC:
            return Node(Node.Type.NUMERIC, int(self._eat().val))
        elif self._lookahead.token_type == Token.Type.LPAREN:
            self._eat(Token.Type.LPAREN)
            res = self.program()
            self._eat(Token.Type.RPAREN)
            return res
        else:
            raise RuntimeError(f'Unxepected token: {self._lookahead}')

    def _next(self):
        self._lookahead = self._lexer.next_token()

    def _eat(self, expected=None):
        ret = self._lookahead
        if expected is not None and self._lookahead.token_type != expected:
            raise RuntimeError(f'Unexpected token: {self._lookahead}')
        self._next()
        return ret


if __name__ == '__main__':
    parser = None
    while True:
        parser = RDParser(input('> '))
        print(parser.program())

# 12 * -2 + 4 - 3