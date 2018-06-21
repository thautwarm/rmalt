from Redy.Magic.Pattern import Pattern
from .asdl import *
from Redy.Opt.ConstExpr import constexpr, const

try:
    from Redy.Opt.ConstExpr import feature
except:
    from Redy.Opt.ConstExpr import optimize as feature


@Pattern
def visit(a: ASDL, ctx):
    return type(a)


@visit.case(ASDL.Symbol)
def visit(a: ASDL.Symbol, ctx):
    return ctx[a.name]


@visit.case(ASDL.List)
def visit(a: ASDL.List, ctx: dict):
    if not a.args:
        return []
    return [visit(each, ctx) for each in a.args]


@visit.case(ASDL.Tuple)
def visit(a: ASDL.Tuple, ctx: dict):
    if not a.args:
        return ()

    return tuple(visit(each, ctx) for each in a.args)


@visit.case(ASDL.Const)
@feature
def visit_const(a: ASDL.Const, ctx: dict):
    if a is constexpr[ASDL.Const.false]:
        return False
    elif a is constexpr[ASDL.Const.true]:
        return True
    elif a is constexpr[ASDL.Const.nil]:
        return None
    else:
        return a[1]


@visit.case(ASDL.Call)
def visit(a: ASDL.Call, ctx: dict):
    fn = visit(a.fn, ctx)
    arg = a.arg
    if arg:
        return fn(visit(a.arg, ctx.copy()))
    return fn()


@visit.case(ASDL.Pair)
def visit(a: ASDL.Pair, ctx: dict):
    return (visit(a.key, ctx), visit(a.value, ctx))


@visit.case(ASDL.Dict)
def visit(a: ASDL.Dict, ctx: dict):
    if not a.args:
        return {}
    return {k: v for k, v in (visit(each, ctx) for each in a.args)}


@visit.case(ASDL.Block)
def visit(a: ASDL.Block, ctx: dict):
    res = None
    for each in a.stmts:
        res = visit(each, ctx)
    return res


_undef = object()


@visit.case(ASDL.Map)
@feature
def visit_map(a: ASDL.Map, ctx: dict):
    if visit(a.case, ctx):
        return visit(a.do, ctx)

    return constexpr[_undef]


@visit.case(ASDL.Cond)
@feature
def visit_cond(a: ASDL.Cond, ctx: dict):
    constant: const = _undef
    for each in a.maps:
        v = visit(each, ctx)
        if v is not constant:
            return v


@visit.case(ASDL.Assign)
def visit(a: ASDL.Assign, ctx: dict):
    ctx[a.target] = visit(a.expr, ctx)


@record
class Function:
    arg: ...
    body: ...
    ctx: ...

    def __call__(self, arg):
        return visit(self.body, {**self.ctx, self.arg: arg})

    def __str__(self):
        return 'Fn({})<id={}>'.format(self.arg, id(self))


@record
class Thunk:
    body: ...
    ctx: ...

    def __call__(self):
        return visit(self.body, self.ctx.copy())

    def __str__(self):
        return 'Thunk<id={}>'.format(id(self))


@visit.case(ASDL.Lambda)
def visit(a: ASDL.Lambda, ctx: dict):
    if len(a.params) is 0:
        return Thunk()
    h, *ps = a.params

    if ps:
        return Function(h, ASDL.Lambda(ps, a.body), ctx)

    return Function(h, a.body, ctx)
