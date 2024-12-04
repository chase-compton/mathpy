import unittest
import os
import sys
from io import StringIO
from contextlib import redirect_stdout
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter


class TestExamples(unittest.TestCase):
    def test_examples(self):
        examples_dir = "tests/inputs/"
        expected_outputs_dir = "tests/outputs/"

        for filename in os.listdir(examples_dir):
            if filename.endswith(".mpy"):
                with self.subTest(filename=filename):
                    # Read the input file
                    with open(os.path.join(examples_dir, filename), "r") as f:
                        code = f.read()

                    # Read the expected output
                    expected_output_file = filename.replace(".mpy", ".txt")
                    with open(
                        os.path.join(expected_outputs_dir, expected_output_file), "r"
                    ) as f:
                        expected_output = f.read()

                    # Redirect stdout to capture the interpreter output
                    with StringIO() as buf, redirect_stdout(buf):
                        # Run the interpreter
                        try:
                            tokens = tokenize(code)
                            parser = Parser(tokens)
                            ast = parser.parse()
                            interpreter = Interpreter()
                            interpreter.interpret(ast)
                        except Exception as e:
                            output = f"Error: {e}"
                        else:
                            output = buf.getvalue()

                    # Compare the output
                    self.assertEqual(output.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
