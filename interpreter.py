from ast_nodes import *
import numpy as np
import operator
import math
import matplotlib.pyplot as plt


class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Name {name} is not defined")

    def set(self, name, value):
        self.vars[name] = value

    def update(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.update(name, value)
        else:
            self.vars[name] = value


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtins()

    def setup_builtins(self):
        # Add built-in functions to the global environment
        self.global_env.vars.update(
            {
                "print": print,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "ln": np.log,
                "log10": np.log10,
                "log2": np.log2,
                "sqrt": np.sqrt,
                "range": self.range_wrapper,
                "zeros": self.zeros_wrapper,
                "ones": self.ones_wrapper,
                "linspace": self.linspace_wrapper,
                "pi": math.pi,
                "mean": np.mean,
                "median": np.median,
                "std": np.std,
                "det": np.linalg.det,
                "inv": np.linalg.inv,
                "eig": np.linalg.eig,
                "ceil": np.ceil,
                "floor": np.floor,
                "abs": np.abs,
                "round": np.round,
                "True": True,
                "False": False,
            }
        )

    def visit(self, node, env):
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name, self.generic_visit)
        return method(node, env)

    def generic_visit(self, node, env):
        raise Exception(f"No visit_{type(node).__name__} method")

    def interpret(self, nodes):
        for node in nodes:
            self.visit(node, self.global_env)

    # Visitor methods for AST nodes
    def visit_Number(self, node, env):
        value_str = str(node.value)
        if "." in value_str:
            return float(value_str)
        else:
            return int(value_str)

    def visit_String(self, node, env):
        return node.value

    def visit_BinOp(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op_value = node.op.value

        if isinstance(left, set) and isinstance(right, set):
            if op_value == "|":
                return left.union(right)
            elif op_value == "&":
                return left.intersection(right)
            elif op_value == "-":
                return left.difference(right)
            else:
                raise Exception(f"Unsupported set operator {op_value}")
        elif op_value in ("and", "or"):
            left = bool(left)
            right = bool(right)
            if op_value == "and":
                return left and right
            elif op_value == "or":
                return left or right
        elif node.op.type == "COMPARE":
            ops = {
                "==": operator.eq,
                "!=": operator.ne,
                "<": operator.lt,
                ">": operator.gt,
                "<=": operator.le,
                ">=": operator.ge,
            }
            return ops[op_value](left, right)
        else:
            ops = {
                "+": operator.add,
                "-": operator.sub,
                "*": self.multiply,
                "/": operator.truediv,
                "^": operator.pow,
                ".+": self.elementwise_add,
                ".-": self.elementwise_sub,
                ".*": self.elementwise_mul,
                "./": self.elementwise_div,
                ".^": self.elementwise_pow,
            }

            if op_value in ops:
                result = ops[op_value](left, right)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                return result
            else:
                raise Exception(f"Unsupported operator {op_value}")

    def multiply(self, a, b):
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            return np.dot(a, b)
        else:
            return a * b

    def elementwise_add(self, a, b):
        return np.add(a, b)

    def elementwise_sub(self, a, b):
        return np.subtract(a, b)

    def elementwise_mul(self, a, b):
        return np.multiply(a, b)

    def elementwise_div(self, a, b):
        return np.divide(a, b)

    def elementwise_pow(self, a, b):
        return np.power(a, b)

    def visit_UnaryOp(self, node, env):
        expr = self.visit(node.expr, env)
        op_value = node.op.value if hasattr(node.op, "value") else node.op.type
        if op_value == "+":
            return +expr
        elif op_value == "-":
            return -expr
        elif op_value == "not":
            return not expr
        else:
            raise Exception(f"Unsupported unary operator {op_value}")

    def visit_Variable(self, node, env):
        return env.get(node.name)

    def visit_Assign(self, node, env):
        var_name = node.left.name
        value = self.visit(node.right, env)
        env.set(var_name, value)

    def visit_Compound(self, node, env):
        for child in node.children:
            self.visit(child, env)

    def visit_NoOp(self, node, env):
        pass

    def visit_If(self, node, env):
        condition = self.visit(node.condition, env)
        if condition:
            for stmt in node.true_block:
                self.visit(stmt, env)
        elif node.false_block:
            for stmt in node.false_block:
                self.visit(stmt, env)

    def visit_While(self, node, env):
        while self.visit(node.condition, env):
            for stmt in node.body:
                self.visit(stmt, env)

    def visit_For(self, node, env):
        iterable = self.visit(node.iterable, env)
        for value in iterable:
            env.set(node.var, value)
            for stmt in node.body:
                self.visit(stmt, env)

    def visit_FunctionDef(self, node, env):
        func_name = node.name
        env.set(func_name, node)

    def visit_FunctionCall(self, node, env):
        func_name = node.name
        args = [self.visit(arg, env) for arg in node.args]

        if func_name == "plot":
            # Handle the 'plot' function
            if len(args) == 1:
                plt.plot(args[0])
            elif len(args) == 2:
                plt.plot(args[0], args[1])
            else:
                raise Exception(f"plot() takes 1 or 2 arguments ({len(args)} given)")
            plt.show()
        else:
            func = env.get(func_name)
            if isinstance(func, FunctionDef):
                # User-defined function
                func_env = Environment(parent=env)
                for param, arg in zip(func.params, args):
                    func_env.set(param, arg)
                try:
                    for stmt in func.body:
                        self.visit(stmt, func_env)
                except ReturnException as e:
                    return e.value
                # If no return statement, return None
                return None
            elif callable(func):
                # Built-in function
                return func(*args)
            else:
                raise Exception(f"{func_name} is not a function")

    def visit_ListLiteral(self, node, env):
        elements = [self.visit(element, env) for element in node.elements]
        return np.array(elements)

    def visit_SetLiteral(self, node, env):
        elements = set()
        for element in node.elements:
            value = self.visit(element, env)
            elements.add(value)
        return elements

    def visit_Subscript(self, node, env):
        var = self.visit(node.var, env)
        if not isinstance(node.index, list):
            indices = [node.index]
        else:
            indices = node.index

        evaluated_indices = []
        for idx_node in indices:
            if isinstance(idx_node, Slice):
                start = self.visit(idx_node.start, env) if idx_node.start else None
                end = self.visit(idx_node.end, env) if idx_node.end else None
                if isinstance(start, float):
                    start = int(start)
                if isinstance(end, float):
                    end = int(end)
                evaluated_indices.append(slice(start, end))
            else:
                index = self.visit(idx_node, env)
                if isinstance(index, float):
                    index = int(index)
                evaluated_indices.append(index)

        # For a single index, don't convert it to a tuple
        if len(evaluated_indices) == 1:
            index = evaluated_indices[0]
        else:
            index = tuple(evaluated_indices)
        try:
            return var[index]
        except (IndexError, TypeError) as e:
            raise Exception(f"Subscript error: {e}")

    def linspace_wrapper(self, start, stop, num):
        return np.linspace(start, stop, int(num))

    def range_wrapper(self, *args):
        if len(args) == 1:
            return np.arange(args[0])
        elif len(args) == 2:
            return np.arange(args[0], args[1])
        elif len(args) == 3:
            return np.arange(args[0], args[1], args[2])
        else:
            raise Exception(f"range() takes 1 to 3 arguments ({len(args)} given)")

    def zeros_wrapper(self, *args):
        if len(args) == 1:
            return np.zeros(int(args[0]))
        else:

            return np.zeros(tuple(map(int, args)))

    def ones_wrapper(self, *args):
        if len(args) == 1:
            return np.ones(int(args[0]))
        else:
            return np.ones(tuple(map(int, args)))

    def visit_Return(self, node, env):
        value = self.visit(node.expr, env) if node.expr else None
        raise ReturnException(value)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
