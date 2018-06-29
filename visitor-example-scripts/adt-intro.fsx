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
