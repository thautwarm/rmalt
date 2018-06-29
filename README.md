The Malt Programming Language Implementation Tutorials

- 这是一个实现语言的教程。 我想我明确地说一句话，这个教程是如此简短、完整、充满美感和容易学习，以至于你会在同学/同事们苦恼地使用`Antlr4`、 `Yacc/Lex`时太快地结束工作而被误以为在划水。

- 本教程只实现了一个解释器，你尽可以把它做成什么奇怪的编译器。[LLVM是极好的](https://github.com/f0rki/mapping-high-level-constructs-to-llvm-ir)。


## 马特语言， 只需要四分之一个整日，你就能实现！

[而这个方法只需要十分钟就能掌握](https://github.com/thautwarm/RBNF)

- 语法介绍见[document](./malt-syntax.rst).

- 运行方法(需要Python3.6+)

    ```
    pip install -U Redy rbnf
    python test.py
    ```
    
    即可进入repl。

- 特性:

    - 自动柯里化
    - (局部)自定义新运算符和修改运算符
    - First-class Expression
    - 使用Lambda而非函数
    - 该语言设计者想出的非常智障的分句标志(`|`)

    其中前两个特性属于本人对malt的改进。

## 为什么我能在短短几个小时内实现它？

- `Malt` is simple
- I use [rbnf](https://github.com/thautwarm/RBNF), which is an alternative of `RegExp` tools, and can help you solve any text processing tasks no matter how difficult you once thought it to be.

## 实现指南

`rmalt` 是一个非常经典的解释器实现, 在利用`rbnf`解析输入字串后, 字串被转为目标语言(例如`Python`)内部的`AST/ASDL`表示.

例如，`Let`作为一个语法和语义的结构，其定义方式如下

```
Let ::= 'let' Identifier as target '=' Expr as body
         rewrite ASDL.Let(target, body)
```

这是一段`rbnf`代码, 表示输入的[Tokenizer](https://github.com/thautwarm/RBNF/blob/master/rbnf/Tokenizer.py)列表是如何匹配`Let`结构的。  

`Identifier`和`Expr`都是其他和`Let`类似的[MetaVariable](https://en.wikipedia.org/wiki/Metavariable), 表示在此调用其他结构的匹配规则。

`as`表示将匹配到的结果进行一个局部绑定，最终我们将利用这些结果构成一个`Let`的语义结构`ASDL.Let(target, body)`, 如果你理解[ADT](https://en.wikipedia.org/wiki/Algebraic_data_type)或者[Case Class](https://docs.scala-lang.org/tour/case-classes.html), 那此处的构造对你应该不是难事，否则我建议你看看这个[附加指南](./adt.md).

在你构建好这些`AST`或`ASDL`后，你需要编写一个所谓的`abstract machine`来解释你的结构，通常而言用所谓的`visitor`模式便可以解决，简介的例子可见于[附加指南](./adt.md)的`interpret`函数，也可看看[rmalt的visitor](https://github.com/thautwarm/rmalt/blob/master/rmalt/visitor.py).

## Related

See rbnf syntaxes of `malt` here:
- [https://github.com/thautwarm/rmalt/blob/master/rmalt/malt.rbnf](https://github.com/thautwarm/rmalt/blob/master/rmalt/malt.rbnf)

What is `rbnf`?

- See [https://github.com/thautwarm/RBNF](https://github.com/thautwarm/RBNF).

- It's (**more than**) a parser generator, and a solution to text with very complex structure.


Run the `repl` with `python test.py` with following requirements
- (`Redy>=0.1.23, rbnf>=0.1.8`)! 


Oh you mean this repo is too informal? It's unnecessary to write a `setup` file cause it's just an example to bring you a piece about how to write programming langauge!





