# MathPy | CS 403 Final Project

MathPy is a simple, intuitive programming language designed specifically for mathematical computations. It aims to provide an out-of-the-box experience for mathematicians, scientists, and engineers who require a straightforward and efficient tool for numerical analysis, data manipulation, and visualization. MathPy combines the simplicity of high-level languages with the power of mathematical libraries, making it an excellent alternative to tools like MATLAB.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Language Grammar](#language-grammar)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Basic Arithmetic](#basic-arithmetic)
  - [Vectors and Matrices](#vectors-and-matrices)
  - [Control Flow](#control-flow)
  - [Functions](#functions)
  - [Plotting](#plotting)
- [Testing Suite](#testing-suite)
- [Potential Future Additions](#potential-future-additions)

## Introduction

Mathematical computing often requires languages and environments that are both powerful and user-friendly. While tools like MATLAB are widely used, they can sometimes feel cumbersome or unintuitive, especially for users who prefer simplicity and readability. MathPy was created to address this need by providing a language that is:

- **Intuitive**: Easy-to-understand syntax that closely resembles Python.
- **Powerful**: Built on top of robust libraries like NumPy and Matplotlib for numerical computations and plotting.
- **Flexible**: Supports a wide range of mathematical operations, data structures, and control flow constructs.

## Features

- **Basic and Advanced Arithmetic**: Supports scalar operations, vector and matrix arithmetic, and element-wise computations.
- **Data Structures**: Provides lists (vectors), nested lists (matrices), and sets.
- **Control Flow**: Includes `if`, `else`, `for`, and `while` statements for controlling program execution.
- **Functions**: Allows users to define and call custom functions with `def`.
- **Built-in Functions**: Includes common mathematical functions like `sin`, `cos`, `exp`, `log`, and statistical functions like `mean`, `median`, and `std`.
- **Plotting**: Integrated plotting capabilities using Matplotlib with a simple `plot` function.
- **Indexing and Slicing**: Supports accessing elements and subarrays using indexing and slicing syntax.
- **Logical Operations**: Supports logical operators like `and`, `or`, `not`, and comparison operators `==`, `!=`, `<`, `>`, `<=`, `>=`.

## Language Grammar

The following is an overview of MathPy's grammar, presented in a simplified format:

```plaintext
program             : statement_list

statement_list      : { statement }

statement           : assignment_statement
                    | function_definition
                    | if_statement
                    | while_statement
                    | for_statement
                    | return_statement
                    | expression_statement

assignment_statement: ID '=' expression

function_definition : 'def' ID '(' parameter_list ')' ':' statement_list 'end'

parameter_list      : ID { ',' ID }

if_statement        : 'if' expression ':' statement_list [ 'else' ':' statement_list ] 'end'

while_statement     : 'while' expression ':' statement_list 'end'

for_statement       : 'for' ID 'in' expression ':' statement_list 'end'

return_statement    : 'return' [ expression ]

expression_statement: expression

expression          : logical_or

logical_or          : logical_and { 'or' logical_and }

logical_and         : comparison { 'and' comparison }

comparison          : arithmetic_expr { ( '==' | '!=' | '<' | '>' | '<=' | '>=' ) arithmetic_expr }

arithmetic_expr     : term { ( '+' | '-' | '.+' | '.-' | '|' | '&' ) term }

term                : factor { ( '*' | '/' | '.*' | './' ) factor }

factor              : [ ( '+' | '-' | 'not' ) ] power

power               : primary { ( '^' | '.^' ) factor }

primary             : NUMBER
                    | STRING
                    | ID
                    | function_call
                    | list_literal
                    | set_literal
                    | '(' expression ')'

function_call       : ID '(' [ argument_list ] ')'

argument_list       : expression { ',' expression }

list_literal        : '[' [ expression { ',' expression } ] ']'

set_literal         : '{' [ expression { ',' expression } ] '}'
```

## Installation

To use MathPy, ensure you have the following installed on your system:

- Python 3.x
- NumPy
- Matplotlib

### Steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/chase-compton/mathpy.git
    ```
2. **Install Dependencies**:

   ```bash
   cd mathpy
   pip install numpy matplotlib
   ```
## Usage

MathPy scripts are written in files with the `.mpy` extension. To run a MathPy script, use the provided `main.py` file. Below is an example of how to execute a MathPy file:

```bash
python3 main.py examples/test.mpy
```

## Examples

### Basic Arithmetic

Code (basic_arithmetic.mpy):
    
```plaintext
a = 10
b = 5

sum = a + b
difference = a - b
product = a * b
quotient = a / b
power = a ^ b

print("Sum:", sum)
print("Difference:", difference)
print("Product:", product)
print("Quotient:", quotient)
print("Power:", power)
```
Output:

```plaintext
Sum: 15
Difference: 5
Product: 50
Quotient: 2.0
Power: 100000
```

### Vectors and Matrices

Code (vector_matrices.mpy):

```plaintext
# Vectors
v1 = [1, 2, 3]
v2 = [4, 5, 6]

# Element-wise addition
v_sum = v1 .+ v2

# Matrices
A = [
    [1, 2],
    [3, 4]
]

B = [
    [5, 6],
    [7, 8]
]

# Matrix multiplication
C = A * B

print("Vector Sum:", v_sum)
print("Matrix Product:")
print(C)
```
Output:

```plaintext
Vector Sum: [5 7 9]
Matrix Product:
[[19 22]
[43 50]]
```

### Control Flow

If-Else Statement:

```plaintext
x = -5

if x > 0:
    print("Positive")
else:
    print("Non-positive")
end
```
Output:

```plaintext
Non-positive
```
While Loop:

```plaintext
count = 3
while count > 0:
    print("Countdown:", count)
    count = count - 1
end
```
Output:

```plaintext
Countdown: 3
Countdown: 2
Countdown: 1
```
For Loop:

```plaintext
for i in range(0, 5):
    print(i)
end
```
Output:

```plaintext
0
1
2
3
4
```
### Functions

Defining and Using Functions:
Code (factorial.mpy):

```plaintext
def factorial(n):
    result = 1
    while n > 1:
        result = result * n
        n = n - 1
    end
    return result
end

num = 5
fact = factorial(num)
print("Factorial of", num, "is", fact)
```
Output:

```plaintext
Factorial of 5 is 120.0
```
### Plotting

Plotting a Function:

```plaintext
x = linspace(0, 2 * pi, 100)
y = sin(x)
plot(x, y)
```
This will display a plot of the sine function from 0 to (2\pi).


## Testing Suite

To ensure the reliability and correctness of MathPy, a comprehensive testing suite has been implemented using Python’s unittest framework.

### Running the Tests

To run the test suite, execute the following command from the root directory:

```bash
python3 -m unittest discover -s tests
```
These tests compare the output of MathPy scripts with the expected output for various scenarios, including arithmetic operations, control flow constructs, function definitions, and linear algebra operations.

## Potential Future Additions

MathPy is designed to be a simple yet powerful language for mathematical computations. While it already offers a wide array of features, there are many directions in which it could be expanded to enhance its usability and functionality. Below are some ideas for future development:

### 1. **Extended Data Structures**
   - **Dictionaries**: Add native support for key-value pairs, allowing for more dynamic data storage and retrieval.
   - **Tuples**: Introduce immutable sequences for use as fixed-size collections.
   - **Queues/Stacks**: Enable easy implementation of algorithms requiring these structures.

### 2. **Advanced Linear Algebra Operations**
   - Singular Value Decomposition (SVD).
   - QR decomposition.
   - Matrix norms.
   - Sparse matrix operations for handling large datasets efficiently.

### 3. **Built-in Equation Solver**
   - Support solving linear and non-linear equations.
   - Enable symbolic computation to simplify or rearrange equations.
   - Provide tools for calculus, such as differentiation and integration.

### 4. **Enhanced Plotting**
   - Add options for scatter plots, bar charts, and histograms.
   - Enable 3D plotting capabilities for scientific data visualization.
   - Add support for customizing plot styles, titles, and legends.

### 5. **Improved Error Handling**
   - Provide more descriptive error messages, including suggestions for fixing common mistakes.
   - Introduce warnings for potentially unintended behaviors (e.g., division by zero or unused variables).

### 6. **Standard Library Expansion**
   - Include utility functions for common mathematical tasks (e.g., prime factorization, GCD, LCM).
   - Add financial functions like NPV, IRR, and amortization schedules.
   - Support probability and statistics functions such as distributions and hypothesis testing.
