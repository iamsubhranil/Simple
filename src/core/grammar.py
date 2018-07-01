from __future__ import print_function

from rpython.rlib.parsing.parsing import *
from rpython.rlib.parsing.ebnfparse import *
import sys

def make_kool_parser():
    #LONGQUOTED = parse_regex(r'"[^\"]*(\\\"?[^\"]+)*(\\\")?"')
    #QUOTEDQUOTE = parse_regex("""'"'""")
    #COMMENT = parse_regex("#[^\\n]*\\n")
    #names1 = ['DECIMAL', 'IDENTIFIER', 'QUOTE', 'QUOTE', 
    #          'EQUALS', 'COMMA', 'LET',
    #          'IGNORE', 'IGNORE', 'IGNORE', 'IGNORE']
    #regexs1 = [DECIMAL, IDENTIFIER, LONGQUOTED, QUOTEDQUOTE, COMMENT,
    #           StringExpression('\n'), StringExpression(' '),
    #           StringExpression('\t')]
    regex = [('VAR', parse_regex("var")),
            # ('PUB', parse_regex("pub")),
            # ('PRIV', parse_regex("priv")),
            # ('PROC', parse_regex("proc")),
            # ('OBJ', parse_regex("obj")),
            # ('FN', parse_regex("fn")),
             ('IF', parse_regex("if")),
             ('TRUE', parse_regex("true")),
             ('FALSE', parse_regex("false")),
            # ('NIL', parse_regex("nil")),
            # ('THIS', parse_regex("this")),
            # ('SUPER', parse_regex("super")),
             ('ELSE', parse_regex("else")),
             ('WHILE', parse_regex("while")),
             ('OR', parse_regex("or")),
             ('AND', parse_regex("and")),
            # ('RET', parse_regex("ret")),
            # ('NEW', parse_regex("new")), # Not used
            # ('FROM', parse_regex("from")), # Not used
            # ('IMPORT', parse_regex("import")), # Not used

             ('EQUAL', parse_regex("=")),
             ('EQUAL_EQUAL', parse_regex("==")),
             ('NOT', parse_regex("!")),
             ('NOT_EQUAL', parse_regex("!=")),
             ('GREATER_THAN', parse_regex(">")),
             ('GT_EQ', parse_regex(">=")),
             ('LESS_THAN', parse_regex("<")),
             ('LT_EQ', parse_regex("<=")),

             ('DOT', parse_regex("\.")),
             ('COMMA', parse_regex(",")),
             ('SEMICOLON', parse_regex(";")),

             ('PLUS', parse_regex("\+")),
             ('MINUS', parse_regex("-")),
             ('STAR', parse_regex("\*")),
             ('BACKSLASH', parse_regex("/")),
             ('CAP', parse_regex("\^")),

             ('PAREN_OPEN', parse_regex("\(")),
             ('PAREN_CLOSE', parse_regex("\)")),
             ('CURL_OPEN', parse_regex("{")),
             ('CURL_CLOSE', parse_regex("}")),
             ('SQUARE_OPEN', parse_regex("\[")),
             ('SQUARE_CLOSE', parse_regex("\]")),

             ('DECIMAL', parse_regex("0|[1-9][0-9]*")),
             ('IDENTIFIER', parse_regex("([a-zA-Z]|_)[a-zA-Z0-9_]*")),

             ('IGNORE', StringExpression('\n')),
             ('IGNORE', StringExpression('\r')),
             ('IGNORE', StringExpression('\t')),
             ('IGNORE', StringExpression(' '))]
    names1, regexs1 = zip(*regex)
    source = """
            program: stmt+ [EOF];

            block: [CURL_OPEN] stmt+ [CURL_CLOSE];

            stmt: exprstmt
                | var_decl_list
                | ifstmt
                | whilestmt
                | block;

            retstmt: [RET] logic_or [SEMICOLON];

            ifstmt: [IF] logic_or stmt ([ELSE] stmt)?;

            whilestmt: [WHILE] logic_or stmt;

            var_decl_list: [VAR] var_decl ([COMMA] var_decl)* [SEMICOLON];
            var_decl: IDENTIFIER ([EQUAL] logic_or)?;

            exprstmt: assignment ([COMMA] assignment)* [SEMICOLON];

            assignment: IDENTIFIER [EQUAL] logic_or;

            logic_or: logic_and ([OR] logic_and)*;
            logic_and: equality ([AND] equality)*;

            symeq: EQUAL_EQUAL | NOT_EQUAL;
            equality: comparison (>symeq< comparison)*;
            symcmp: GREATER_THAN | GT_EQ | LESS_THAN | LT_EQ;
            comparison: add (>symcmp< add)*;

            symadd: PLUS | MINUS;
            add: mult (>symadd< mult)*;
            symmult: STAR | BACKSLASH;
            mult: power (>symmult< power)*;
            power: unary (CAP unary)*;

            symun: NOT | MINUS;
            unary: (>symun< unary) | primary;

            number: float | DECIMAL;
            float: DECIMAL DOT DECIMAL;

            primary: IDENTIFIER
                | TRUE
                | FALSE
                | number
                | [PAREN_OPEN] logic_or [PAREN_CLOSE];
    """
    try:
        rs, rules, transformer = parse_ebnf(source)
    except ParseError as e:
        print(e.nice_error_message("grammar", source))
        sys.exit(1)
    if len(rs) > 0:
        names2, regexs2 = zip(*rs)
    else:
        names2 = ()
        regexs2 = ()
    lexer = Lexer(regexs2 + regexs1, names2 + names1,
                  ignore=['IGNORE'])
    parser = PackratParser(rules, "program")
    return parser, lexer, transformer

if __name__ == '__main__':
    f = py.path.local("lexpar.py")
    oldcontent = f.read()
    s = "# GENERATED CODE BETWEEN THIS LINE AND ITS OTHER OCCURENCE\n".lower()
    pre, gen, after = oldcontent.split(s)

    parser, lexer, ToAST = make_kool_parser()
    transformer = ToAST.source
    newcontent = "%s%s%s\nparser = %r\n%s\n%s%s" % (
            pre, s, transformer.replace("ToAST", "KoolToAST"),
            parser, lexer.get_dummy_repr(), s, after)
    print(newcontent)
    f.write(newcontent)

