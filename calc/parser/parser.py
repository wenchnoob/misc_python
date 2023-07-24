'''
Language

PROGRAM -> ASSIGN
ASSIGN -> VARIABLE = ADD | ADD
ADD -> MULT + ADD
MULT -> PRIM * MULT
PRIM -> - NUM | NUM | ( PROGRAM )
NUM -> r'[0-9]+(\.[0-9]+)?'
VARIABLE

'''

from calc.lexer import lexer
from calc.lexer.lexer import Token


class UnexpectedEOF(EOFError):
    pass


class Node:
    class Type:
        VARIABLE = 'VARIABLE'
        NUMERIC = 'NUMERIC'
        PLUS = 'PLUS'
        MINUS = 'MINUS'
        TIMES = 'TIMES'
        DIV = 'DIV'
        NEGATE = 'NEGATE'
        ASSIGN = 'ASSIGN'

    def __init__(self, type, val, children=None):
        if children is None:
            children = []
        self.type = type
        self.val = val
        self.children = children

    def __str__(self):
        return str(self.val)

    def __repr__(self):
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
        return self._assign()

    def _assign(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        if self._lookahead.token_type == Token.Type.VARIABLE:
            _id = Node(Node.Type.VARIABLE, self._eat(Token.Type.VARIABLE).val)
            try:
                self._eat(Token.Type.ASSIGN)
            except UnexpectedEOF:
                return _id
            rhs = self._add()
            return Node(Node.Type.ASSIGN, None, [_id, rhs])
        else:
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
                       else Node.Type.MINUS, None, [lhs, self._add()])
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
                       else Node.Type.DIV, None, [lhs, self._mult()])
        return lhs

    def _primitive(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        if self._lookahead.token_type == Token.Type.MINUS:
            self._eat()
            return Node(Node.Type.NEGATE, None, [self._primitive()])
        elif self._lookahead.token_type == Token.Type.NUMERIC:
            return Node(Node.Type.NUMERIC, self._eat().val)
        elif self._lookahead.token_type == Token.Type.VARIABLE:
            return Node(Node.Type.VARIABLE, self._eat().val)
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
        if self._lookahead is None:
            raise UnexpectedEOF(f'Unexpected end of input')
        if expected is not None and self._lookahead.token_type != expected:
            raise RuntimeError(f'Unexpected token: {self._lookahead}')
        self._next()
        return ret


if __name__ == '__main__':
    parser = None
    while True:
        parser = RDParser(input('> '))
        print(parser.program().__repr__(), end='')

# 12 * -2 + 4 - 3
