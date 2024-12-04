import sys
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_file>/<filename>.mpy")
        return

    if not sys.argv[1].endswith(".mpy"):
        print("File must have a .mpy extension")
        return

    if len(sys.argv) > 2:
        print("Too many arguments")
        return

    filename = sys.argv[1]
    try:
        with open(filename, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    tokens = tokenize(code)
    # for token in tokens:
    #     print(token)
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)


if __name__ == "__main__":
    main()
