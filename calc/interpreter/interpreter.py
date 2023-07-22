from calc.parser import parser
from calc.parser.parser import Node


def _bin_op(node):
    lhs = _interpret(node.children[0]).val
    rhs = _interpret(node.children[1]).val
    match node.type:
        case Node.Type.PLUS:
            return lhs + rhs
        case Node.Type.MINUS:
            return lhs - rhs
        case Node.Type.TIMES:
            return lhs * rhs
        case Node.Type.DIV:
            return lhs / rhs
        case _:
            raise RuntimeError(f'Unsupported node type {node.type}, how did this happen? :)')


def _interpret(node):
    match node.type:
        case Node.Type.NUMERIC:
            return node
        case Node.Type.NEGATE:
            return Node(Node.Type.NUMERIC, _interpret(node.children[0]).val * -1)
        case Node.Type.PLUS:
            return Node(Node.Type.NUMERIC, _bin_op(node))
        case Node.Type.MINUS:
            return Node(Node.Type.NUMERIC, _bin_op(node))
        case Node.Type.TIMES:
            return Node(Node.Type.NUMERIC, _bin_op(node))
        case Node.Type.DIV:
            return Node(Node.Type.NUMERIC, _bin_op(node))
        case _:
            raise RuntimeError(f'Unsupported node type {node.type}')


class Interpreter:
    def __init__(self, text, strategy=parser.RDParser):
        self.program = strategy(text).program()

    def interpret(self):
        return _interpret(self.program)


if __name__ == '__main__':
    while True:
        inp = input('> ')
        if inp == 'exit':
            break
        interpreter = Interpreter(inp)
        result = interpreter.interpret()
        print(result, end='')
