from sys import argv
import pdb

argc = len(argv)


def say_hi(name = "World"):
    print(f'Hello {name}!')


def say_bye(name = "World"):
    print(f'Bye {name}!')


def test():
    print('Test')


def mult(x, y):
    return x * y

def add(x, y):
    return x + y


def main():
    print(f'argc = {argc}')
    if argc < 2:
        print("No arguments passed") # print help message
    else:
        if argv[1] == '--help' and argc == 2:
            pass # print help message
        elif argv[1] == 'hi':
            if argc >= 3:
                say_hi(argv[2])
            else:
                say_hi()

        elif argv[1] == 'bye':
            if argc >= 3:
                say_hi(argv[2])
            else:
                say_hi()

        elif argv[1] == 'test':
            test()

        elif argv[1] == 'op':
            src = int(argv[2])
            track = int(src)
            i = 3
            while i < argc:
                if argv[i] == 'mult':
                    track = mult(track, int(argv[i+1]))
                elif argv[i] == 'add':
                    track = add(track, int(argv[i+1]))
                elif argv[i] == 'sq':
                    track = track ** 2
                    i -= 1
                i += 2
            print(track) # write to file
        else:
            print('Unrecognized args')


def non_null(func):

    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise AssertionError("Null argument passed to non null parameter.")
        for key in kwargs.keys():
            if kwargs[key] is None:
                raise AssertionError("Null keyword argument passed to non null parameter.")

        return func(*args, **kwargs)

    return wrapper


@non_null
def mult(x, y):
    return x * y
#
# print(mult(2, 3))
# print(mult(2, None))


def numeric(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if type(arg) is not int:
                raise AssertionError("Arguments must be integers")
        for key in kwargs.keys():
            if type(kwargs[key]) is not int:
                raise AssertionError("Arguments must be integers")
        return func(*args, **kwargs)
    return wrapper


def wenchy(func):
    def wrapper(*args, **kwargs):
        kwargs['name'] = 'Wenchy'
        return func(*args, **kwargs)
    return wrapper

def not_wenchy(func):
    def wrapper(*args, **kwargs):
        kwargs['name'] = 'Not Wenchy'
        return func(*args, **kwargs)
    return wrapper

@wenchy
@not_wenchy
def hello(name):
    print(f'Hello {name}!')


@not_wenchy
@wenchy
def hello_2(name):
    print(f'Hello {name}!')

if __name__ == '__main__':
    hello(name='mike')
    hello_2(name='Mike')

