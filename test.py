from Redy.Tools.PathLib import Path
import rbnf.zero as ze

with Path('./rmalt').into('malt.rbnf').open('r') as f:
    rbnf = f.read()
ze_exp = ze.compile(rbnf, use='Grammar')

x = ze_exp.match("""
  let x = "123" 
| let y = 2
| {1: 2}
| cond{
      x => 1
    | y => 10
    | z => 10 + 2 * 10 ^ 15 - 9
    }
""")
print(x.result)


