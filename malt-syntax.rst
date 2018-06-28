Syntax Of Malt Language
=================================

Literal
---------------

* NamedConst
    
    * ``true``
    * ``false``
    * ``nil``

* Number

    * int: ``1, -2, ...``

    * float: ``1.0, -5.0, ...``

* String : ``"a\"b", ...``

Symbol
---------------

* Identifier: just like `java`.
* Infix operator as identifier: `(+), (-), (+.+), (and)`.

.. code ::

    malt> infix <.> 1
           | let (<.>) = (a, b) -> (a, b)
           | 1 <.> 2 ;;
    =>  (1, 2)
    malt> let (<<.>>) = (a) -> ((<.>) a ). ((<.>) a)
           | 1 <<.>> 2 ;;
    =>  (1, (1, 2))


Statements
--------------------

* In ``repl``, just like that in ML languages, you should use ``;;`` to end a session. 

In Malt, ``|`` represents the delimiter.

.. code ::

    rmalt> let y = 1
           |   let g = y + 1
           |   y ;;

We'll get the symbol ``x`` valued ``2``.

There is no ``return`` keyword in Malt and the end of a suite will decide whether to return something.


Function, Lambda, Currying, Compose and Pipeline
---------------------------------------------------------

When you want to define a function, just bind a ``lambda``.

.. code ::
    
    malt> let double = (a) -> a * 2
           | double 10 ;;
    => 20

    # Compose
    malt> let dd = double . double 
           | dd 10 ;;
    => 40

    # Pipeline
    malt> 10 >> double >> double ;;
    => 40

    # Currying
    malt> let fm = map (x) -> x + 1
           | fm [1, 2, 3] ;;
    => [2, 3, 4]
    

Custom Operator
----------------------

Define custom operator.

.. code ::

    rmalt> infix `add` 3
           | let (`add`) = (l, r) -> l + r - l/r
           | 1 + 2 `add` 3 + 4 ;;
    => 9.571428571428571

    rmalt> infix .. 1
           | let (..) = (l, r) -> cond{ 
                 l > r => [] 
               | true  => l::(l+1 .. r)
           }
           | 1..10 >> (map (x)-> x % 2)
    => [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]


And you can get current priority of any operator:

.. code ::
    
    rmalt> infix +;;
    => 5

Finally, you can define your own operator by using following characters:

.. code ::

    '*' | '^' | '%' | '&' | '@' | '$' | '+' | '/' | '>' | '<' | '=' | '.' | '?' | '!' | '::'


Conditional Branches
------------------------

That's just ``if-elif``.

.. code ::

    cond {
        case1 => expr1
        | case2 => expr2
        ...
    }


Collections
------------------------

* Malt's ``list``  is the **linkedlist**, not Python's ``list``(dynamic array).

.. code ::

    rmalt> 1::[1, 2, 3];;
    => [1, 1, 2, 3]

``list`` is the linkedlist.

.. code ::

    rmalt> 1::[1, 2, 3];;
    => [1, 1, 2, 3]
    rmalt> list (1, 2, 3)
    => [1, 2, 3]
    

* Malt's ``tuple`` is Python's ``tuple``.

* Malt's ``dict`` is Python's ``dict``.

.. code ::

    rmalt> my_d = {
            1: {let g = 1 | g + 1}
           }
           | my_d;;
    => {1: 2}



