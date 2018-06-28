from Redy.Tools.PathLib import Path
from .visitor import *
import rbnf.zero as ze
import sys
import io
import warnings
import readline
from .std import std

warnings.filterwarnings('ignore')


# with Path('./rmalt').into('malt.rbnf').open('r') as f:
#     rbnf = f.read()

ze_exp = ze.compile('import rmalt.malt.[*]', use='Grammar')

KeyWords = ['let', 'include', 'not', 'cond', 'true', 'false', 'nil', 'or', 'and']


class Completer:
    def __init__(self):
        self.choices = []
        self.previous = []


@feature
def err_write(info):
    if constexpr[isinstance(sys.stderr, io.BufferedWriter)]:
        if isinstance(info, str):
            info = info.encode()
        return sys.stderr.write(info)
    else:
        if isinstance(info, bytes):
            info = info.decode()
        return sys.stderr.write(info)


@feature
def completer(text, state):
    options = tuple(option for option in KeyWords if option.startswith(text))

    if state < len(options):
        return options[state]
    else:
        return None


def main():
    ctx = dict(__name__=__name__, __file__=__file__)
    ctx.update(std)
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    count_parentheses = 0
    cache = []

    def active():
        nonlocal count_parentheses
        try:
            it = ze_exp.match(' '.join(cache))
            if it is None:
                raise Exception
            if it.state.end_index != len(it.tokens):
                idx = min(it.state.max_fetched, len(it.tokens)-1)
                tk = it.tokens[idx]
                raise SyntaxError("line {}, column {}".format(tk.lineno, tk.colno))
            res = visit(it.result, ctx)
            
            if res is not None:
                print('=> ', res)
        except Exception as e:
            err_write(e.__class__.__name__ + ':' + str(e) + '\n')

        cache.clear()
        count_parentheses = 0

    while True:
        line: str = input('malt> ' if not cache else '      ')
        
        if line.endswith(';;'):
            line = line[:-2]
            if not line and not cache:
                continue
            cache.append(line)
            active()
        else:
            cache.append(line)


if __name__ == '__main__':
    main()
