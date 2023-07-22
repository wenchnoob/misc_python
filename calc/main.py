from calc.interpreter.interpreter import Interpreter


def main():
    if __name__ == '__main__':
        while True:
            inp = input('> ')
            if inp == 'exit':
                break
            interpreter = Interpreter(inp)
            result = interpreter.interpret()
            print(result, end='')


if __name__ == '__main__':
    main()
