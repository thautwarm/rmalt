from toolz import curry
import operator

op_priorities = {
    '>>': 1,
    '.': 1,

    'or': 2,
    'and': 3,

    '>': 4,
    '<': 4,
    '<=': 4,
    '>=': 4,
    '==': 4,


    "+": 5,
    "-": 5,
    '@': 10,
    "*": 10,
    "/": 10,
    "//": 10,




    '%': 10,
    '**': 15,
    '^': 15,

    '??': 20,

}

std = {
    'neg': curry(lambda a: -a),
    'not': curry(lambda a: not a),

    '+': curry(operator.add),
    '-': curry(operator.sub),
    '/': curry(operator.truediv),
    '//': curry(operator.floordiv),

    '>': curry(operator.gt),
    '<': curry(operator.lt),
    '>=': curry(operator.ge),
    '<=':curry(operator.le),
    '==': curry(operator.eq),



    'or': curry(lambda a, b: a or b),
    'and': curry(lambda a, b: a and b),

    '*': curry(operator.mul),
    '%': curry(operator.mod),
    '>>': curry(lambda a, b:b(a)),
    '.': curry(lambda a, b: lambda x: a(b(x))),
    '??': curry(lambda a, b: a if a else b),
}