'''
Language

PROGRAM -> ASSIGN
ASSIGN -> VARIABLE = RELATIONAL_EXPRESSION | RELATIONAL_EXPRESSION
EQUALITY_EXPRESSION -> RELATIONAL_EXPRESSION ( == | != ) RELATIONAL_EXPRESSION
RELATIONAL_EXPRESSION -> ADD ( < | <= | >= | > ) ADD
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
        LT = 'LT'
        GT = 'GT'
        EQ = 'EQ'
        LTEQ = 'LTEQ'
        GTEQ = 'GTEQ'
        NOTEQ = 'NOTEQ'
        NOT = 'NOT'
        BOOL = 'BOOL'

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

            if self._lookahead is not None and self._lookahead.token_type == Token.Type.ASSIGN:
                self._eat(Token.Type.ASSIGN)
                rhs = self._assign()
                return Node(Node.Type.ASSIGN, None, [_id, rhs])
            elif self._lookahead is None:
                return _id
            else:
                self._backtrack()
                return self._equality_expression()
        else:
            return self._equality_expression()

    def _equality_expression(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        lhs = self._relation_expression()

        while self._lookahead is not None and \
                (self._lookahead.token_type == Token.Type.EQ
                 or self._lookahead.token_type == Token.Type.NOTEQ):
            lhs = Node(Node.Type.EQ
                       if self._eat().token_type == Token.Type.EQ
                       else Node.Type.NOTEQ, None, [lhs, self._relation_expression()])
        return lhs

    def _relation_expression(self):
        if self._lookahead is None:
            raise RuntimeError('Unexpected EOF')

        lhs = self._add()

        while self._lookahead is not None and \
                (self._lookahead.token_type == Token.Type.LT
                 or self._lookahead.token_type == Token.Type.GT
                 or self._lookahead.token_type == Token.Type.LTEQ
                 or self._lookahead.token_type == Token.Type.GTEQ):
            cur_token = self._eat()
            match cur_token.token_type:
                case Token.Type.LT:
                    lhs = Node(Node.Type.LT, None, [lhs, self._add()])
                case Token.Type.GT:
                    lhs = Node(Node.Type.GT, None, [lhs, self._add()])
                case Token.Type.LTEQ:
                    lhs = Node(Node.Type.LTEQ, None, [lhs, self._add()])
                case Token.Type.GTEQ:
                    lhs = Node(Node.Type.GTEQ, None, [lhs, self._add()])
                case _:
                    raise RuntimeError('How did this even happen? :/')

        return lhs


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
        elif self._lookahead.token_type == Token.Type.NOT:
            self._eat()
            return Node(Node.Type.NOT, None, [self._primitive()])
        elif self._lookahead.token_type == Token.Type.NUMERIC:
            return Node(Node.Type.NUMERIC, self._eat().val)
        elif self._lookahead.token_type == Token.Type.VARIABLE:
            return Node(Node.Type.VARIABLE, self._eat().val)
        elif (self._lookahead.token_type == Token.Type.TRUE
              or self._lookahead.token_type == Token.Type.FALSE):
            return Node(Node.Type.BOOL, self._eat().val)
        elif self._lookahead.token_type == Token.Type.LPAREN:
            self._eat(Token.Type.LPAREN)
            res = self.program()
            self._eat(Token.Type.RPAREN)
            return res
        else:
            raise RuntimeError(f'Unexpected token: {self._lookahead.__repr__()}')

    def _next(self):
        self._lookahead = self._lexer.next_token()

    def _backtrack(self):
        # our current lookahead, is already consumed by the lexer
        # so to get our previous look ahead we have to go back two (2)
        # previous tokens
        self._lexer.backtrack(2)
        self._lookahead = self._lexer.next_token()

    def _eat(self, expected=None):
        ret = self._lookahead
        if self._lookahead is None:
            raise UnexpectedEOF(f'Unexpected end of input')
        if expected is not None and self._lookahead.token_type != expected:
            raise RuntimeError(f'Unexpected token: {self._lookahead.__repr__()}')
        self._next()
        return ret


if __name__ == '__main__':
    parser = None
    while True:
        parser = RDParser(input('> '))
        print(parser.program().__repr__(), end='')

# 12 * -2 + 4 - 3
