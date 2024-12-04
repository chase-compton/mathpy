class ASTNode:
    pass


class Number(ASTNode):
    def __init__(self, value):
        self.value = float(value)


class String(ASTNode):
    def __init__(self, value):
        self.value = value


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class Assign(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Compound(ASTNode):
    def __init__(self):
        self.children = []


class NoOp(ASTNode):
    pass


class If(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class For(ASTNode):
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body


class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements


class SetLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements


class Subscript(ASTNode):
    def __init__(self, var, index):
        self.var = var
        self.index = index


class Slice(ASTNode):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Return(ASTNode):
    def __init__(self, expr):
        self.expr = expr
