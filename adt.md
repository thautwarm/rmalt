Simple ADT Examples
==============================

Here is an example written in 3 different languages, you can choose one to start with.

- [F#](https://github.com/thautwarm/rmalt/blob/master/adt.md#fsharp)

- [Scala](https://github.com/thautwarm/rmalt/blob/master/adt.md#scala)

- [Python](https://github.com/thautwarm/rmalt/blob/master/adt.md#python)


If you're a user of `Haskell`, you don't need to view this page at all :-).



FSharp
------------

```f#

module Hello

type Op = Add | Sub | Mul | Div
type Expr = 
    | BinOp of Expr * Op * Expr
    | Int   of int

let rec interpret = function
    | BinOp(l, op, r) ->
        let l = interpret(l) in
        let r = interpret(r) in 
            match op with
            | Add -> l + r
            | Sub -> l - r
            | Mul -> l * r
            | Div -> l / r 
    | Int i -> i

// #load "adt-intro.fsx" 
open Hello
interpret(BinOp(Int 1, Add, Int 2));;
// => 3

``` 


Scala
---------------

```scala

object Hello{

    class Op
    case class Add() extends Op
    case class Sub() extends Op
    case class Mul() extends Op
    case class Div() extends Op

    class Expr
    case class BinOp(l: Expr, op: Op, r:Expr) extends Expr
    case class Int_(i: Int) extends Expr

    def interpret(expr: Expr) : Int = {
        expr match {
            case BinOp(l, op, r) =>
                val lv = interpret(l)
                val rv = interpret(r)
                op match {
                    case _: Add => lv + rv
                    case _: Mul => lv * rv 
                    case _: Sub => lv - rv 
                    case _: Div => lv / rv
                }
            case Int_(i) => i 
        }
    }
}

import Hello._
interpret(BinOp(Int_(1), Add(), Int_(2)))
// => 3
```

Python
----------------------

```Python
from Redy.ADT.Core import data
import operator

@data
class Op:
    Add: ...
    Sub: ...
    Mul: ...
    Div: ...

@data
class Expr:
    Int  : lambda i: i
    BinOp: lambda l, op, r: (l, op, r)

def interpret(expr: Expr):
    kind, *args = expr
    if kind is Expr.Int:
        (i, ) = args
        return i
    elif kind is Expr.BinOp:
        l, op, r = args
        l, r = map(interpret, (l, r))
        return {
                Op.Add: operator.add,
                Op.Sub: operator.sub,
                Op.Mul: operator.mul,
                Op.Div: operator.floordiv
               }[op](l, r) 
    else: raise TypeError

interpret(Expr.BinOp(Expr.Int(1), Op.Add, Expr.Int(2)))
# => 3
```