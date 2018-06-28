from toolz import curry
import operator
from functools import reduce
from Redy.ADT.Core import data
from Redy.ADT import traits
from Redy.Opt.ConstExpr import const, optimize
from collections import Generator, Iterator

@data
class LinkedList(traits.Im, traits.ConsInd, traits.Dense):
    Nil: ...
    Cons: lambda head, tail: ...


@optimize
def __str__(self):
    _Nil: const = LinkedList.Nil
    if self is _Nil:
        return '[]'
    head = self
    
    fmts = []
    _append = fmts.append
    while head is not _Nil:
        _, value, head = head
        _append(str(value))
    
    return '[{}]'.format(', '.join(fmts))

LinkedList.__str__ = __str__


def map_(f):
    Nil = LinkedList.Nil
    def call(seq):
        if isinstance(seq, LinkedList):
            if seq is Nil:
                return Nil
            _, head, tail = seq
            return LinkedList.Cons(f(head), call(tail))
        return map(f, seq)

    return call

@optimize
def to_linked_list(seq):
    nil: const = LinkedList.Nil
    cons: const = LinkedList.Cons
    if isinstance(seq, LinkedList):
        return seq 
    elif isinstance(seq, (Generator, Iterator)):
        return to_linked_list(tuple(seq))

    else:
        tail = nil
        for each in reversed(seq):
            tail = cons(each, tail)

        return tail

@optimize
def index_(seq, i):
    Nil: const = LinkedList.Nil
    if isinstance(seq, LinkedList):
        while seq is not Nil:
            _, value, seq = seq
            if i is 0:
                return value
            i -= 1
        raise IndexError("Index out of range.")
    return seq[i]


op_priorities = {
    '>>': 1,
    '.': 1,
   '::': 1,

    'or': 2,
    'and': 3,

    '>': 4,
    '<': 4,
    '<=': 4,
    '>=': 4,
    '==': 4,



    "+": 5,
    '++': 5,
    "-": 5,
    '@': 10,
    "*": 10,
    "/": 10,
    "//": 10,




    '%': 10,
    '**': 15,
    '^': 15,

    '??': 20,
     '!!': 20


}


@optimize
def concat(l, r):
    Nil: const = LinkedList.Nil
    Cons: const = LinkedList.Cons
    if l is Nil:
        return r
    _, h, t = l
    return Cons(h, concat(t, r))




std = {
    'map': map_,
    'list': to_linked_list,

    'neg': curry(lambda a: -a),
    'not': curry(lambda a: not a),

    '+': curry(operator.add),
    '++': curry(concat),
    '::': curry(LinkedList.Cons),
    '-': curry(operator.sub),
    '/': curry(operator.truediv),
    '//': curry(operator.floordiv),

    '>': curry(operator.gt),
    '<': curry(operator.lt),
    '>=': curry(operator.ge),
    '<=':curry(operator.le),
    '==': curry(operator.eq),

    '!!': curry(index_),


    'or': curry(lambda a, b: a or b),
    'and': curry(lambda a, b: a and b),

    '*': curry(operator.mul),
    '%': curry(operator.mod),
    '>>': curry(lambda a, b:b(a)),
    '.': curry(lambda a, b: lambda x: a(b(x))),
    '??': curry(lambda a, b: a if a else b),
}