from typing import Generic, Iterable, TypeVar, Optional, Iterator
from functools import reduce
from Redy.Magic.Classic import  record

@record
class Operator:
        box: ...

T = TypeVar('T')

op_priorities = {
    "+": 1,
    "-": 1,
    '@': 5,

    "*": 10,
    "/": 10,
    "//": 10,
    '%':10,

    '**': 15,
    '^': 15,

}

class TwoSideLink(Iterable, Generic[T]):

    def __init__(self, content: T, prev: 'Optional[TwoSideLink[T]]' = None, next: 'Optional[TwoSideLink]' = None):
        self.content: T = content
        self.next = next
        self.prev = prev

    def __iter__(self) -> 'Iterator[TwoSideLink[T]]':
        yield self
        if self.next:
            yield from self.next

    def __str__(self):
        return 'L<{}>'.format(self.content)

    __repr__ = __str__

    @classmethod
    def from_iter(cls, iterable: 'Iterable') -> 'Optional[TwoSideLink]':
        if not iterable:
            return None
        s_iterable = iter(iterable)
        try:
            fst = cls(next(s_iterable))
        except StopIteration:
            return None

        reduce(lambda a, b: setattr(a, "next", cls(b)) or setattr(a.next, "prev", a) or a.next, s_iterable, fst)
        return fst


def bin_expr_reduce(func, seq: 'TwoSideLink'):
    def sort_by_func(e: 'TwoSideLink'):
        return op_priorities[e.content.box.name]

    op_nodes = (each for each in seq if isinstance(each.content, Operator))

    op_nodes = sorted(op_nodes, key=sort_by_func, reverse=True)
    bin_expr = None
    for each in op_nodes:
        bin_expr = func(each.content.box, each.prev.content, each.next.content)
        each.content = bin_expr
        try:
            each.prev.prev.next = each
            each.prev = each.prev.prev
        except AttributeError:
            pass

        try:
            each.next.next.prev = each
            each.next = each.next.next
        except AttributeError:
            pass

    return bin_expr


# s = TwoSideLink.from_iter([3, "-", 2, "*", 4, '/', 5])
#
# from Redy.Magic.Classic import record
#
#
# @record
# class Fn:
#     op: str
#     a: str
#     b: str
#
#     def __str__(self):
#         return '({} {} {})'.format(self.op, self.a, self.b)
#
#     __repr__ = __str__
#
# print(bin_expr_reduce(Fn, s))
#

