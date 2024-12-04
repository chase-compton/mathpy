from ast_nodes import *
from lexer import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self, msg="Invalid syntax"):
        line = self.current_token.line
        column = self.current_token.column
        token_value = self.current_token.value
        raise SyntaxError(
            f"Error at line {line}, column {column}: {msg}. Unexpected token: {token_value}"
        )

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def parse(self):
        nodes = self.program()
        return nodes

    def program(self):
        """program : statement_list"""
        nodes = self.statement_list()
        return nodes

    def statement_list(self, end_tokens=[]):
        """statement_list : { statement }"""
        nodes = []
        while self.current_token.type not in ["EOF"] + end_tokens:
            while self.current_token.type == "NEWLINE":
                self.eat("NEWLINE")
            if self.current_token.type in end_tokens:
                break
            node = self.statement()
            if node is not None:
                nodes.append(node)
            # Do not raise an error if node is None
        return nodes

    def statement(self):
        """
        statement : assignment_statement
                | function_definition
                | if_statement
                | while_statement
                | for_statement
                | return_statement
                | expression_statement
        """
        if self.current_token.type == "EOF":
            return None
        elif self.current_token.type == "ID":
            if self.peek().type == "ASSIGN":
                return self.assignment_statement()
            else:
                return self.expression_statement()
        elif self.current_token.type == "def":
            return self.function_definition()
        elif self.current_token.type == "if":
            return self.if_statement()
        elif self.current_token.type == "while":
            return self.while_statement()
        elif self.current_token.type == "for":
            return self.for_statement()
        elif self.current_token.type == "return":
            return self.return_statement()
        elif self.current_token.type == "NEWLINE":
            self.eat("NEWLINE")
            return None  # Skip empty lines
        else:
            # If none of the above, and not EOF, raise an error
            self.error(
                f"Unexpected token '{self.current_token.value}' at line {self.current_token.line}"
            )

    def assignment_statement(self):
        """assignment_statement : ID ASSIGN expression"""
        left = Variable(self.current_token.value)
        self.eat("ID")
        self.eat("ASSIGN")
        right = self.expression()
        # Consume any NEWLINE tokens after an assignment
        while self.current_token.type == "NEWLINE":
            self.eat("NEWLINE")
        return Assign(left, right)

    def function_definition(self):
        """function_definition : def ID LPAREN parameter_list RPAREN COLON statement_list end"""
        self.eat("def")
        func_name = self.current_token.value
        self.eat("ID")
        self.eat("LPAREN")
        params = self.parameter_list()
        self.eat("RPAREN")
        self.eat("COLON")
        body = self.statement_list(end_tokens=["end"])
        self.eat("end")
        return FunctionDef(func_name, params, body)

    def parameter_list(self):
        """parameter_list : ID { COMMA ID }"""
        params = []
        if self.current_token.type == "ID":
            params.append(self.current_token.value)
            self.eat("ID")
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                params.append(self.current_token.value)
                self.eat("ID")
        return params

    def if_statement(self):
        """if_statement : if expression COLON statement_list [ else COLON statement_list ] end"""
        self.eat("if")
        condition = self.expression()
        self.eat("COLON")
        true_block = self.statement_list(end_tokens=["else", "end"])
        false_block = None
        if self.current_token.type == "else":
            self.eat("else")
            self.eat("COLON")
            false_block = self.statement_list(end_tokens=["end"])
        self.eat("end")
        return If(condition, true_block, false_block)

    def while_statement(self):
        """while_statement : while expression COLON statement_list end"""
        self.eat("while")
        condition = self.expression()
        self.eat("COLON")
        body = self.statement_list(end_tokens=["end"])
        self.eat("end")
        return While(condition, body)

    def for_statement(self):
        """for_statement : for ID in expression COLON statement_list end"""
        self.eat("for")
        var = self.current_token.value
        self.eat("ID")
        self.eat("in")
        iterable = self.expression()
        self.eat("COLON")
        body = self.statement_list(end_tokens=["end"])
        self.eat("end")
        return For(var, iterable, body)

    def return_statement(self):
        """return_statement : return [expression]"""
        self.eat("return")
        if self.current_token.type != "NEWLINE":
            expr = self.expression()
        else:
            expr = None
        return Return(expr)

    def expression_statement(self):
        expr = self.expression()
        # Consume any NEWLINE or END tokens after an expression
        while self.current_token.type == "NEWLINE" or self.current_token.type == "END":
            self.eat(self.current_token.type)
        return expr

    def expression(self):
        """expression : logical_or"""
        return self.logical_or()

    def logical_or(self):
        """logical_or : logical_and { 'or' logical_and }"""
        node = self.logical_and()
        while self.current_token.type == "or":
            token = self.current_token
            self.eat("or")
            node = BinOp(left=node, op=token, right=self.logical_and())
        return node

    def logical_and(self):
        """logical_and : comparison { 'and' comparison }"""
        node = self.comparison()
        while self.current_token.type == "and":
            token = self.current_token
            self.eat("and")
            node = BinOp(left=node, op=token, right=self.comparison())
        return node

    def comparison(self):
        """comparison : arithmetic_expr { ( '==' | '!=' | '<' | '>' | '<=' | '>=' ) arithmetic_expr }"""
        node = self.arithmetic_expr()
        while self.current_token.type == "COMPARE":
            token = self.current_token
            self.eat("COMPARE")
            node = BinOp(left=node, op=token, right=self.arithmetic_expr())
        return node

    def arithmetic_expr(self):
        """arithmetic_expr : term { ( '+' | '-' | '.+' | '.-' | '|' | '&' ) term }"""
        node = self.term()
        while self.current_token.type in ("OP", "EOP") and self.current_token.value in (
            "+",
            "-",
            ".+",
            ".-",
            "|",
            "&",
        ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def term(self):
        """term : factor { ( '*' | '/' | '.*' | './' ) factor }"""
        node = self.factor()
        while self.current_token.type in ("OP", "EOP") and self.current_token.value in (
            "*",
            "/",
            ".*",
            "./",
        ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        """factor : ( '+' | '-' | 'not' ) factor | power"""
        token = self.current_token
        if token.type in ("OP", "EOP") and token.value in ("+", "-"):
            self.eat(token.type)
            node = UnaryOp(op=token, expr=self.factor())
            return node
        elif token.type == "not":
            self.eat("not")
            return UnaryOp(op=token, expr=self.factor())
        else:
            return self.power()

    def power(self):
        """power : primary { ( '^' | '.^' ) factor }"""
        node = self.primary()
        while self.current_token.type in ("OP", "EOP") and self.current_token.value in (
            "^",
            ".^",
        ):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def primary(self):
        """primary : NUMBER | STRING | ID | LPAREN expression RPAREN | list_literal | function_call | subscript"""
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(token.value)
        elif token.type == "STRING":
            self.eat("STRING")
            return String(token.value.strip('"'))
        elif token.type == "ID":
            if self.peek().type == "LPAREN":
                return self.function_call()
            elif self.peek().type == "LBRACKET":
                return self.subscript()
            else:
                self.eat("ID")
                return Variable(token.value)
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expression()
            self.eat("RPAREN")
            return node
        elif token.type == "LBRACKET":
            return self.list_literal()
        elif token.type == "LBRACE":
            return self.set_literal()
        else:
            self.error("Invalid syntax in primary")

    def list_literal(self):
        """list_literal : LBRACKET [ expression { COMMA expression } ] RBRACKET"""
        elements = []
        self.eat("LBRACKET")
        while self.current_token.type != "RBRACKET":
            # Skip newlines before element
            while self.current_token.type == "NEWLINE":
                self.eat("NEWLINE")
            # If we reach the closing bracket after newlines, break
            if self.current_token.type == "RBRACKET":
                break
            # Parse the element
            element = self.expression()
            elements.append(element)
            # Skip newlines after element
            while self.current_token.type == "NEWLINE":
                self.eat("NEWLINE")
            if self.current_token.type == "COMMA":
                self.eat("COMMA")
            elif self.current_token.type == "RBRACKET":
                break
            else:
                self.error("Expected comma or closing bracket in list")
        self.eat("RBRACKET")
        return ListLiteral(elements)

    def function_call(self):
        """function_call : ID LPAREN arguments RPAREN"""
        func_name = self.current_token.value
        self.eat("ID")
        self.eat("LPAREN")
        args = self.arguments()
        self.eat("RPAREN")
        return FunctionCall(func_name, args)

    def arguments(self):
        """arguments : [ expression { COMMA expression } ]"""
        args = []
        if self.current_token.type != "RPAREN":
            args.append(self.expression())
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                args.append(self.expression())
        return args

    def peek(self):
        """Look ahead to the next token without consuming the current one."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        else:
            return Token(
                "EOF", None, self.current_token.line, self.current_token.column
            )

    def set_literal(self):
        """set_literal : LBRACE [ expression { COMMA expression } ] RBRACE"""
        elements = []
        self.eat("LBRACE")
        while self.current_token.type != "RBRACE":
            # Skip newlines before element
            while self.current_token.type == "NEWLINE":
                self.eat("NEWLINE")
            if self.current_token.type == "RBRACE":
                break
            element = self.expression()
            elements.append(element)
            # Skip newlines after element
            while self.current_token.type == "NEWLINE":
                self.eat("NEWLINE")
            if self.current_token.type == "COMMA":
                self.eat("COMMA")
            elif self.current_token.type == "RBRACE":
                break
            else:
                self.error("Expected comma or closing brace in set")
        self.eat("RBRACE")
        return SetLiteral(elements)

    def subscript(self):
        """subscript : ID LBRACKET subscript_index RBRACKET"""
        var_name = self.current_token.value
        self.eat("ID")
        self.eat("LBRACKET")
        indices = self.subscript_index()
        self.eat("RBRACKET")
        # Ensure indices is a list
        if not isinstance(indices, list):
            indices = [indices]
        return Subscript(Variable(var_name), indices)

    def subscript_index(self):
        """subscript_index : ( [expression] COLON [expression] ) { COMMA ( [expression] COLON [expression] ) }"""
        indices = []
        while True:
            if self.current_token.type == "COLON":
                # Slice with omitted start
                self.eat("COLON")
                start = None
                if self.current_token.type not in ("COMMA", "RBRACKET"):
                    end = self.expression()
                else:
                    end = None
                indices.append(Slice(start, end))
            else:
                start = self.expression()
                if self.current_token.type == "COLON":
                    self.eat("COLON")
                    if self.current_token.type not in ("COMMA", "RBRACKET"):
                        end = self.expression()
                    else:
                        end = None
                    indices.append(Slice(start, end))
                else:
                    indices.append(start)
            if self.current_token.type == "COMMA":
                self.eat("COMMA")
            else:
                break
        return indices
