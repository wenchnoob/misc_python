import re


class Token:
    class Type:
        VARIABLE = 'VARIABLE'
        NUMERIC = 'NUMERIC'
        PLUS = 'PLUS'
        MINUS = 'MINUS'
        TIMES = 'TIMES'
        DIV = 'DIV'
        LPAREN = 'LPAREN'
        RPAREN = 'RPAREN'
        ASSIGN = 'ASSIGN'
        LT = 'LT'
        GT = 'GT'
        EQ = 'EQ'
        LTEQ = 'LTEQ'
        GTEQ = 'GTEQ'
        NOTEQ = 'NOTEQ'
        TRUE = 'TRUE'
        FALSE = 'FALSE'
        NOT = 'NOT'

    def __init__(self, token_type, val=''):
        match token_type:
            case Token.Type.PLUS:
                val = '+'
            case Token.Type.MINUS:
                val = '-'
            case Token.Type.TIMES:
                val = '*'
            case Token.Type.DIV:
                val = '/'
            case Token.Type.LPAREN:
                val = '('
            case Token.Type.RPAREN:
                val = ')'
            case Token.Type.ASSIGN:
                val = '='
        self.token_type = token_type
        self.val = int(val) if token_type == Token.Type.NUMERIC else \
            bool(val) if (token_type == Token.Type.TRUE or token_type == Token.Type.FALSE) else val

    def __str__(self):
        return self.val

    def __repr__(self):
        return f'(type={self.token_type}, val={self.val})'

    def __hash__(self):
        return hash(self)

    def __eq__(self, other):
        return isinstance(other, Token) and self.token_type == other.token_type and self.val == other.val


class RegexLexer():
    _PATTERNS = [
        (re.compile(r'true'), Token.Type.TRUE),
        (re.compile(r'false'), Token.Type.FALSE),
        (re.compile(r'[_A-z]+[_A-z0-9]*'), Token.Type.VARIABLE),
        (re.compile(r'[0-9]+(\.[0-9]+)?'), Token.Type.NUMERIC),
        (re.compile(r'<='), Token.Type.LTEQ),
        (re.compile(r'>='), Token.Type.GTEQ),
        (re.compile(r'=='), Token.Type.EQ),
        (re.compile(r'!='), Token.Type.NOTEQ),
        (re.compile(r'!'), Token.Type.NOT),
        (re.compile(r'<'), Token.Type.LT),
        (re.compile(r'>'), Token.Type.GT),
        (re.compile(r'\+'), Token.Type.PLUS),
        (re.compile(r'-'), Token.Type.MINUS),
        (re.compile(r'\*'), Token.Type.TIMES),
        (re.compile(r'/'), Token.Type.DIV),
        (re.compile(r'\('), Token.Type.LPAREN),
        (re.compile(r'\)'), Token.Type.RPAREN),
        (re.compile(r'='), Token.Type.ASSIGN),
        (re.compile(r'\s'), None)
    ]

    def __init__(self, text):
        self.cursor = 0
        self.prev = []
        self.next = []
        self.text = text

    def next_token(self):
        if self.cursor >= len(self.text):
            return None

        if len(self.next) > 0:
            token = self.next.pop()
            self.prev.append(token)
            return token

        token = self._get_token()
        self.prev.append(token)
        return token

    def _get_token(self):
        for pattern in RegexLexer._PATTERNS:
            m = pattern[0].match(self.text, self.cursor)
            if m is not None:
                self.cursor = m.end()
                if pattern[1] is None:
                    return self._get_token()
                return Token(pattern[1], m.group())

        if self.cursor >= len(self.text):
            raise  RuntimeError('Unexpected EOF')

        msg = f'Unexpected character: {self.text[self.cursor]}'
        self.cursor = len(self.text)
        raise RuntimeError(msg)

    def backtrack(self, amt=1):
        # print(self.prev)
        while amt > 0 and len(self.prev) > 0:
            self.next.append(self.prev.pop())
            amt -= 1

    def tokens(self):
        tokens = []
        while self.cursor < len(self.text):
            tokens.append(self.next_token())
        return tokens


if __name__ == '__main__':
    lexer = None
    while True:
        lexer = RegexLexer(input('> '))
        print(lexer.tokens())
