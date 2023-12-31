from calc.parser import parser
from calc.parser.parser import Node, UnexpectedEOF

_lookup_table = {}


def _preload():
    _lookup_table['vars'] = []


def _add_var(node):
    lhs = node.children[0]
    rhs = node.children[1]
    _lookup_table[lhs.val] = _interpret(rhs)
    if 'vars' in _lookup_table and isinstance(_lookup_table['vars'], list):
        _lookup_table['vars'].append(lhs.val)
    return _lookup_table[lhs.val]


def _get_var(node):
    # if node.val == 'vars':
    #     _vars = list(_lookup_table.keys())
    #     if 'vars' in _vars:
    #         _vars.remove('vars')
    #     return _vars

    if node.val not in _lookup_table:
        raise NameError(f'Unknown variable: {node.val}')
    return _lookup_table[node.val]


def _bin_op(node):
    lhs = _interpret(node.children[0]).val
    rhs = _interpret(node.children[1]).val
    match node.type:
        case Node.Type.PLUS:
            return Node.Type.NUMERIC, lhs + rhs
        case Node.Type.MINUS:
            return Node.Type.NUMERIC, lhs - rhs
        case Node.Type.TIMES:
            return Node.Type.NUMERIC, lhs * rhs
        case Node.Type.DIV:
            return Node.Type.NUMERIC, lhs / rhs
        case Node.Type.LT:
            return Node.Type.BOOL, lhs < rhs
        case Node.Type.GT:
            return Node.Type.BOOL, lhs > rhs
        case Node.Type.LTEQ:
            return Node.Type.BOOL, lhs <= rhs
        case Node.Type.GTEQ:
            return Node.Type.BOOL, lhs >= rhs
        case Node.Type.EQ:
            return Node.Type.BOOL, lhs == rhs
        case Node.Type.NOTEQ:
            return Node.Type.BOOL, lhs != rhs
        case _:
            raise RuntimeError(f'Unsupported node type {node.type}, how did this happen? :)')


def _interpret(node):
    match node.type:
        case Node.Type.ASSIGN:
            return _add_var(node)
        case Node.Type.VARIABLE:
            return _get_var(node)
        case Node.Type.NUMERIC:
            return node
        case Node.Type.BOOL:
            return node
        case Node.Type.NEGATE:
            return Node(Node.Type.NUMERIC, _interpret(node.children[0]).val * -1)
        case Node.Type.NOT:
            return Node(Node.Type.BOOL, not _interpret(node.children[0]).val)
        case (Node.Type.PLUS | Node.Type.MINUS | Node.Type.TIMES | Node.Type.DIV
              | Node.Type.LT | Node.Type.GT | Node.Type.LTEQ | Node.Type.GTEQ | Node.Type.EQ | Node.Type.NOTEQ):
            return Node(*_bin_op(node))
        case _:
            raise RuntimeError(f'Unsupported node type {node.type}')


class Interpreter:
    def __init__(self, text, strategy=parser.RDParser):
        self.program = strategy(text).program()

    def interpret(self):
        return _interpret(self.program)


if __name__ == '__main__':
    _preload()
    while True:
        inp = input('> ')
        if inp == 'exit':
            break
        try:
            interpreter = Interpreter(inp)
            result = interpreter.interpret()
            print(result)
        except (UnexpectedEOF, RuntimeError, NameError) as e:
            print(e.__repr__())
