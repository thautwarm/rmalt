from typing import Optional, Tuple

from Redy.Magic.Classic import record
from Redy.ADT.Core import data
from Redy.ADT import traits




class ASDL:

    @data
    class Const(traits.Im, traits.ConsInd, traits.Dense):
        num: lambda _: str(_)
        str: lambda _: _
        true: ...
        false: ...
        nil: ...


    @record
    class Include:
        path: str

    @record
    class Assign:
        target: str
        expr: ...

    @record
    class Cond:
        maps: Optional[Tuple['ASDL', ...]]

    @record
    class Block:
        stmts: Optional[Tuple['ASDL', ...]]

    @record
    class Symbol:
        name: str

    @record
    class Map:
        case: ...
        do: ...


    @record
    class Call:
        fn: ...
        arg: ...

    @record
    class Tuple:
        args: Optional[Tuple['ASDL', ...]]


    @record
    class List:
        args: Optional[Tuple['ASDL', ...]]

    @record
    class Pair:
        key: ...
        value: ...

    @record
    class Dict:
        args: Optional[Tuple['ASDL.Pair', ...]]

    @record
    class Lambda:
        params: Optional[Tuple['ASDL', ...]]
        body: ...

    @record
    class InfixDef:
        op: ...
        priority: ...

