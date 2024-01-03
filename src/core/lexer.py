class Token(object):
    def __init__(self, name, source, source_pos):
        self.name = name
        self.source = source
        self.source_pos = source_pos

    def copy(self):
        return self.__class__(self.name, self.source, self.source_pos)

    def __eq__(self, other):
        # for testing only
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # for testing only
        return not self == other

    def __repr__(self):
        return "Token(%r, %r, %r)" % (self.name, self.source, self.source_pos)

class SourcePos(object):
    """An object to record position in source code."""
    def __init__(self, i, lineno, columnno):
        self.i = i                  # index in source string
        self.lineno = lineno        # line number in source
        self.columnno = columnno    # column in line

    def copy(self):
        return SourcePos(self.i, self.lineno, self.columnno)

    def __eq__(self, other):
        # for testing only
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # for testing only
        return not self == other

    def __repr__(self):
        return "SourcePos(%r, %r, %r)" % (self.i, self.lineno, self.columnno)

class Node(object):
    def view(self):
        from dotviewer import graphclient
        from graphcontentpage import GraphContentPage
        content = ["digraph G{"]
        content.extend(self.dot())
        content.append("}")
        graphclient.display_page(GraphContentPage("\n".join(content)))

class Symbol(Node):

    def __init__(self, token):
        self.symbol = token.name
        self.additional_info = token.source
        self.token = token

    def getsourcepos(self):
        return self.token.source_pos

    def __repr__(self):
        return "Symbol(%r, %r)" % (self.symbol, self.additional_info)

    def dot(self):
        symbol = (self.symbol.replace("\\", "\\\\").replace('"', '\\"')
                                                   .replace('\n', '\\l'))
        addinfo = str(self.additional_info).replace('"', "'") or "_"
        yield ('"%s" [shape=box,label="%s\\n%s"];' % (
            id(self), symbol,
            repr(addinfo).replace('"', '').replace("\\", "\\\\")))

    def visit(self, visitor):
        method = getattr(visitor, "visit_" + self.symbol, None)
        if method is None:
            return self
        return method(self)

class Nonterminal(Node):
    def __init__(self, symbol, children):
        self.children = children
        self.symbol = symbol

    def getsourcepos(self):
        try:
            return self.children[0].getsourcepos()
        except IndexError:
            raise

    def __str__(self):
        print((self.symbol, self.children))
        return "%s(%s)" % (self.symbol, ", ".join([str(c) for c in self.children]))

    def __repr__(self):
        return "Nonterminal(%r, %r)" % (self.symbol, self.children)

    def dot(self):
        yield '"%s" [label="%s"];' % (id(self), self.symbol)
        for child in self.children:
            yield '"%s" -> "%s";' % (id(self), id(child))
            if isinstance(child, Node):
                for line in child.dot():
                    yield line
            else:
                yield '"%s" [label="%s"];' % (
                    id(child),
                    repr(child).replace('"', '').replace("\\", "\\\\"))

    def visit(self, visitor):
        general = getattr(visitor, "visit", None)
        if general is None:
            return getattr(visitor, "visit_" + self.symbol)(self)
        else:
            specific = getattr(visitor, "visit_" + self.symbol, None)
            if specific is None:
                return general(self)
            else:
                return specific(self)

def lex(contents):
    token_types = {"+": "PLUS", "-": "MINUS", "*": "STAR", "/": "BACKSLASH",
                   "%": "PERCEN", "=": "EQUAL", ">": "GREATER_THAN",
                   "<": "LESS_THAN", ">=": "GT_EQ", "<=": "LT_EQ",
                   "==": "EQUAL_EQUAL", "!=": "NOT_EQUAL", "^": "CAP",
                   "!": "NOT", "(": "PAREN_OPEN", ")": "PAREN_CLOSE",
                   "{": "CURL_OPEN", "}": "CURL_CLOSE", "[": "SQUARE_OPEN", "]": "SQUARE_CLOSE",
                   ",": "COMMA", ";": "SEMICOLON", ".": "DOT"}

    keywords = ["while", "if", "for", "else", "var", "true", "false", "or", "and"]
    ignore = [' ', '\t', '\n', '\r']
    # token = (type, str)
    size = len(contents)
    i = 0

    tokens = []
    line = 0
    char = 0
    lastlineend = 0
    while i < size:
        if contents[i] in ignore:
            while i < size and contents[i] in ignore:
                if contents[i] == '\n':
                    line += 1
                    lastlineend = i
                    char = 0
                i += 1
        elif contents[i] in list(token_types.keys()):
            t = contents[i]
            char = i - lastlineend
            if i < size and contents[i:i + 2] in list(token_types.keys()):
                t = contents[i:i + 2]
            tokens.append(Token(token_types[t], t, SourcePos(i, line, char)))
            i += len(t)
        elif contents[i].isalpha() or contents[i].isdigit():
            j = i
            char = i - lastlineend
            while j < size and (contents[j].isalpha() or contents[j].isdigit()):
                j += 1
            part = contents[i:j]
            if part in keywords:
                tokens.append(Token(part.upper(), part, SourcePos(i, line, char)))
            else:
                tokens.append(Token("DECIMAL" if part.isdigit() else "IDENTIFIER", part, SourcePos(i, line, char)))
            i = j
        else:
            raise RuntimeError("Invalid character", contents[i])
    return tokens

def expect(tokens, char):
    if tokens[0].name != char:
        raise RuntimeError("Expected " + str(char) + ", Received: " + str(tokens[0].name))
    return tokens.pop(0)

def generate_nonterminal(tokens, base, match, next_, name, expect_end=None, capture_match=False):
    children = [base]
    if type(match) == str:
        match = [match]
    while tokens[0].name in match:
        t = tokens.pop(0)
        if capture_match:
            children.append(Symbol(t))
        children.append(next_(tokens))
    if expect_end:
        expect(tokens, expect_end)
    return Nonterminal(name, children)

def generate_nonterminal_binary(tokens, match, next_, name, expect_end=None):
    return generate_nonterminal(tokens, next_(tokens), match, next_, name, expect_end)

def generate_binexpr(tokens, match, next_, name):
    return generate_nonterminal(tokens, next_(tokens), match, next_, name, None, True)

def generate_float(tokens):
    return Nonterminal('float', [Symbol(expect(tokens, 'DECIMAL')), Symbol(expect(tokens, 'DOT')), Symbol(expect(tokens, 'DECIMAL'))])

def generate_number(tokens):
    if len(tokens) > 1 and tokens[1].name == 'DOT':
        return Nonterminal('number', [generate_float(tokens)])
    return Nonterminal('number', [Symbol(expect(tokens, 'DECIMAL'))])

def generate_primary(tokens):
    if tokens[0].name in ['IDENTIFIER', 'TRUE', 'FALSE']:
        return Nonterminal('primary', [Symbol(tokens.pop(0))])
    if tokens[0].name == 'PAREN_OPEN':
        tokens.pop(0)
        expr = generate_logic_or(tokens)
        expect(tokens, 'PAREN_CLOSE')
        return Nonterminal('primary', [expr])
    return Nonterminal('primary', [generate_number(tokens)])

def generate_unary(tokens):
    if tokens[0].name in ['NOT', 'MINUS']:
        return Nonterminal('unary', [tokens.pop(0), generate_unary(tokens)])
    return Nonterminal('unary', [generate_primary(tokens)])

def generate_power(tokens):
    return generate_binexpr(tokens, ['CAP'], generate_unary, 'power')

def generate_mult(tokens):
    return generate_binexpr(tokens, ['STAR', 'BACKSLASH'], generate_power, 'mult')

def generate_add(tokens):
    return generate_binexpr(tokens, ['PLUS', 'MINUS'], generate_mult, 'add')

def generate_comparison(tokens):
    return generate_binexpr(tokens, ['GREATER_THAN', 'GT_EQ', 'LESS_THAN', 'LT_EQ'], generate_add, 'comparison')

def generate_equality(tokens):
    return generate_binexpr(tokens, ['EQUAL_EQUAL', 'NOT_EQUAL'], generate_comparison, 'equality')

def generate_logic_and(tokens):
    return generate_binexpr(tokens, 'AND', generate_equality, 'logic_and')

def generate_logic_or(tokens):
    return generate_binexpr(tokens, 'OR', generate_logic_and, 'logic_or')

def generate_assignment(tokens):
    children = [Symbol(expect(tokens, 'IDENTIFIER'))]
    expect(tokens, 'EQUAL')
    children.append(generate_logic_or(tokens))
    return Nonterminal('assignment', children)

def generate_exprstmt(tokens):
    return generate_nonterminal_binary(tokens, 'COMMA', generate_assignment, 'exprstmt')

def generate_var_decl(tokens):
    children = [Symbol(expect(tokens, 'IDENTIFIER'))]
    if tokens[0].name == 'EQUAL':
        tokens.pop(0)
        children.append(generate_logic_or(tokens))
    return Nonterminal('var_decl', children)

def generate_var_decl_list(tokens):
    tokens.pop(0)
    return generate_nonterminal_binary(tokens, 'COMMA', generate_var_decl, 'var_decl_list')

def generate_while(tokens):
    tokens.pop(0)
    children = [generate_logic_or(tokens), generate_stmt(tokens)]
    return Nonterminal('whilestmt', children)

def generate_if(tokens):
    tokens.pop(0)
    children = []
    children.append(generate_logic_or(tokens))
    children.append(generate_stmt(tokens))
    if tokens[0].name == 'ELSE':
        tokens.pop(0)
        children.append(generate_stmt(tokens))
    return Nonterminal('ifstmt', children)

def generate_for(tokens):
    tokens.pop(0)
    expect(tokens, 'PAREN_OPEN')
    children = []
    if tokens[0].name != 'SEMICOLON':
        if tokens[0].name == 'VAR':
            children.append(generate_var_decl_list(tokens))
        else:
            children.append(generate_exprstmt(tokens))
    else:
        children.append(None)
    expect(tokens, 'SEMICOLON')
    if tokens[0].name != 'SEMICOLON':
        children.append(generate_logic_or(tokens))
    else:
        children.append(None)
    expect(tokens, 'SEMICOLON')
    if tokens[0].name != 'PAREN_CLOSE':
        children.append(generate_exprstmt(tokens))
    else:
        children.append(None)
    expect(tokens, 'PAREN_CLOSE')
    children.append(generate_stmt(tokens))
    return Nonterminal('forstmt', children)

def generate_block(tokens):
    tokens.pop(0)
    children = []
    while tokens[0].name != 'CURL_CLOSE':
        children.append(generate_stmt(tokens))
    tokens.pop(0)
    return Nonterminal('block', children)

def generate_stmt(tokens):
    child = []
    if tokens[0].name == 'IF':
        child.append(generate_if(tokens))
    elif tokens[0].name == 'WHILE':
        child.append(generate_while(tokens))
    elif tokens[0].name == 'VAR':
        child.append(generate_var_decl_list(tokens))
    elif tokens[0].name == 'CURL_OPEN':
        child.append(generate_block(tokens))
    elif tokens[0].name == 'FOR':
        child.append(generate_for(tokens))
    else:
        child.append(generate_exprstmt(tokens))
    return Nonterminal('stmt', child)

def generate_stmts(tokens):
    stmts = []
    while len(tokens):
        stmts.append(generate_stmt(tokens))
    return stmts

def generate_program(tokens):
    return Nonterminal('program', generate_stmts(tokens))

if __name__ == "__main__":
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    name = sys.argv[1]
    with open(name, "r") as f:
        tokens = lex(f.read())
        tree = generate_program(tokens)
        print((str(tree)))
        tree.view()
