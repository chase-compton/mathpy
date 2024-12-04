import re

# Token specification
TOKEN_SPECIFICATION = [
    ("NUMBER", r"\d+(\.\d+)?"),  # Integer or decimal number
    ("STRING", r'"[^"\n]*"'),  # String literal
    ("COMPARE", r"==|!=|<=|>=|<|>"),  # Comparison operators
    ("ASSIGN", r"="),  # Assignment operator
    ("END", r";"),  # Statement terminator
    ("EOP", r"\.\+|\.\-|\.\*|\.\/|\.\^"),  # Element-wise operators
    ("OP", r"\+|\-|\*|\/|\^|\||&"),  # Operators
    ("ID", r"[A-Za-z_]\w*"),  # Identifiers
    ("LPAREN", r"\("),  # Left parenthesis
    ("RPAREN", r"\)"),  # Right parenthesis
    ("LBRACKET", r"\["),  # Left bracket
    ("RBRACKET", r"\]"),  # Right bracket
    ("LBRACE", r"\{"),  # Left brace
    ("RBRACE", r"\}"),  # Right brace
    ("COMMA", r","),  # Comma
    ("COLON", r":"),  # Colon
    ("NEWLINE", r"\n"),  # Line endings
    ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
    ("COMMENT", r"\#.*"),  # Comment
]
# Compile the regular expressions
TOKEN_REGEX = "|".join("(?P<%s>%s)" % pair for pair in TOKEN_SPECIFICATION)
get_token = re.compile(TOKEN_REGEX).match

KEYWORDS = {
    "def",
    "if",
    "else",
    "for",
    "while",
    "return",
    "and",
    "or",
    "not",
    "in",
    "end",
}


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, Line: {self.line}, Column: {self.column})"


def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    pos = 0
    mo = get_token(code)
    while mo is not None:
        typ = mo.lastgroup
        value = mo.group(typ)
        if typ == "NEWLINE":
            line_start = mo.end()
            line_num += 1
        elif typ == "SKIP" or typ == "COMMENT":
            pass
        elif typ == "ID" and value in KEYWORDS:
            typ = value
        else:
            pass
        if typ not in ("SKIP", "COMMENT"):
            column = mo.start() - line_start
            tokens.append(Token(typ, value, line_num, column))
        pos = mo.end()
        mo = get_token(code, pos)
    if pos != len(code):
        raise SyntaxError(f"Unexpected character {code[pos]} at position {pos}")
    # Add EOF token
    tokens.append(Token("EOF", None, line_num, pos - line_start))
    return tokens
