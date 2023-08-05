from calc.lexer import lexer
from calc.lexer.lexer import Token
import unittest


class TestLexer(unittest.TestCase):

    def setUp(self):
        pass

    def test_regex_lexes_expr(self):
        tokens = lexer.RegexLexer("3 * (5 + 4) / 2 - 1").tokens()
        expected = [Token(Token.Type.NUMERIC, '3'),
                    Token(Token.Type.TIMES, '*'),
                    Token(Token.Type.LPAREN, '('),
                    Token(Token.Type.NUMERIC, '5'),
                    Token(Token.Type.PLUS, '+'),
                    Token(Token.Type.NUMERIC, '4'),
                    Token(Token.Type.RPAREN, ')'),
                    Token(Token.Type.DIV, '/'),
                    Token(Token.Type.NUMERIC, '2'),
                    Token(Token.Type.MINUS, '-'),
                    Token(Token.Type.NUMERIC, '1')]
        self.assertEqual(expected, tokens)

    def test_regex_lexes_plus(self):
        tokens = lexer.RegexLexer("123 + 5").tokens()
        expected = [Token(Token.Type.NUMERIC, '123'),
                    Token(Token.Type.PLUS, '+'),
                    Token(Token.Type.NUMERIC, '5')]
        self.assertEqual(expected, tokens)

    def test_regex_lexes_minus(self):
        tokens = lexer.RegexLexer("687 - 789").tokens()
        expected = [Token(Token.Type.NUMERIC, '687'),
                    Token(Token.Type.MINUS, '-'),
                    Token(Token.Type.NUMERIC, '789')]
        self.assertEqual(expected, tokens)

    def test_regex_lexes_times(self):
        tokens = lexer.RegexLexer("25 * 56").tokens()
        expected = [Token(Token.Type.NUMERIC, '25'),
                    Token(Token.Type.TIMES, '*'),
                    Token(Token.Type.NUMERIC, '56')]
        self.assertEqual(expected, tokens)

    def test_regex_lexes_div(self):
        tokens = lexer.RegexLexer("289 / 76").tokens()
        expected = [Token(Token.Type.NUMERIC, '289'),
                    Token(Token.Type.DIV, '/'),
                    Token(Token.Type.NUMERIC, '76')]
        self.assertEqual(expected, tokens)


if __name__ == '__main__':
    unittest.main()
