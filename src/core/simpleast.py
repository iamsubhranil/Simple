from rpython.rlib.parsing.parsing import *
from rpython.rlib.parsing.ebnfparse import *
from rpython.rlib.parsing.lexer import *

from lexpar import parser, lexer, KoolToAST
from strtbl import get_string, register_string
from simplenodes import *
from simplecfg import find_basic_blocks, bb_to_cfg, print_cfg, view_cfg, find_reaching_definitions, find_available_expressions

def disp(s):
    print s,

def check_if_number(expr):
    t = expr.return_type()
    return t == int or t == float or t == VariableExpression

def check_if_bool(expr):
    t = expr.return_type()
    return t == bool or t == VariableExpression

def numeric_higher_type(x, y):
    a = type(x)
    b = type(y)
    if a is float or b is float:
        return float
    return int

def always_boolean_type(x, y):
    return bool

def numeric_or_boolean(sym, exp):
    if sym == 'NOT':
        return bool
    return exp.return_type()

class KoolAstGen(object):

    def __init__(self, source = None):
        self.context = CompilationContext(None, 'GLOBAL')
        self.validators = {'PLUS' : check_if_number,
                           'MINUS' : check_if_number,
                           'BACKSLASH' : check_if_number,
                           'STAR' : check_if_number,
                           'CAP' : check_if_number,
                           'EQUAL_EQUAL' : check_if_number,
                           'NOT_EQUAL' : check_if_number,
                           'GREATER_THAN' : check_if_number,
                           'LESS_THAN' : check_if_number,
                           'GT_EQ' : check_if_number,
                           'LT_EQ' : check_if_number,
                           'NOT' : check_if_bool,
                           'OR' : check_if_bool,
                           'AND' : check_if_bool}
        self.return_type = {'PLUS' : numeric_higher_type,
                           'MINUS' : numeric_higher_type,
                           'BACKSLASH' : numeric_higher_type,
                           'STAR' : numeric_higher_type,
                           'CAP' : numeric_higher_type,
                           'EQUAL_EQUAL' : always_boolean_type,
                           'NOT_EQUAL' : always_boolean_type,
                           'GREATER_THAN' : always_boolean_type,
                           'LESS_THAN' : always_boolean_type,
                           'GT_EQ' : always_boolean_type,
                           'LT_EQ' : always_boolean_type,
                           'NOT' : numeric_or_boolean,
                           'OR' : always_boolean_type,
                           'AND' : always_boolean_type}

    def visit_program(self, node):
        p = Program(self.context)
        for child in node.children:
            p.statements.append(self.visit_stmt(child))
        return p

    def visit_stmt(self, node):
        child = node.children[0]
        if child.symbol == 'var_decl_list':
            return self.visit_var_decl_list(child)
        elif child.symbol == 'exprstmt':
            return self.visit_expr_stmt(child)
        elif child.symbol == 'ifstmt':
            return self.visit_ifstmt(child)
        elif child.symbol == 'whilestmt':
            return self.visit_whilestmt(child)
        elif child.symbol == 'block':
            return self.visit_block(child)

    def visit_whilestmt(self, node):
        cond = self.visit_logic_or(node.children[0])
        then = self.visit_stmt(node.children[1])
        return WhileStatement(self.context, cond, then)

    def visit_ifstmt(self, node):
        exp = self.visit_logic_or(node.children[0])
        then = self.visit_stmt(node.children[1])
        elsest = None
        if len(node.children) == 3:
            elsest = self.visit_stmt(node.children[2])
        return IfStatement(self.context, exp, then, elsest)

    def visit_block(self, node):
        b = BlockStatement(self.context)
        for child in node.children:
            b.statements.append(self.visit_stmt(child))
        return b

    def visit_expr_stmt(self, node):
        e = ExpressionStatement(self.context)
        for child in node.children:
            e.exprs.append(self.visit_assignment(child))
        return e

    def visit_var_decl_list(self, node):
        e = ExpressionStatement(self.context)
        for child in node.children:
            j = self.visit_var_decl(child)
            if j is not None:
                e.exprs.append(j)
        return e

    def visit_var_decl(self, node):
        s, pos = self.visit_IDENTIFIER(node.children[0])
        self.context.declare(s, pos)
        if len(node.children) == 2:
            #disp(" = ")
            exp = self.visit_logic_or(node.children[1])
            self.context.update_assignment(s, exp, pos)
            ve = VariableExpression(self.context, s, pos)
            return AssignmentStatement(self.context, pos, ve, exp)
        return None

    def visit_assignment(self, node):
        i, pos = self.visit_IDENTIFIER(node.children[0])
        j = self.visit_logic_or(node.children[1])
        ve = VariableExpression(self.context, i, pos)
        return AssignmentStatement(self.context, pos, ve, j)

    def visit_IDENTIFIER(self, node):
        return register_string(node.additional_info.strip()), node.token.source_pos

    def visit_logic_or(self, node):
        j = self.visit_logic_and(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_logic_and(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators['OR']
            rt = self.return_type['OR']
            #function = self.function['OR']
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_logic_and(self, node):
        j = self.visit_equality(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_equality(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators['AND']
            rt = self.return_type['AND']
            #function = self.function['AND']
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_equality(self, node):
        j = self.visit_comparison(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_comparison(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators[sym]
            rt = self.return_type[sym]
            #function = self.function[sym]
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_comparison(self, node):
        j = self.visit_add(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_add(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators[sym]
            rt = self.return_type[sym]
            #function = self.function[sym]
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_add(self, node):
        j = self.visit_mult(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_mult(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators[sym]
            rt = self.return_type[sym]
            #function = self.function[sym]
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_mult(self, node):
        j = self.visit_power(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_power(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators[sym]
            rt = self.return_type[sym]
            #function = self.function[sym]
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_power(self, node):
        j = self.visit_unary(node.children[0])
        i = 1
        while i < len(node.children):
            k = self.visit_unary(node.children[i + 1])
            sym = node.children[i].symbol
            validator = self.validators[sym]
            rt = self.return_type[sym]
            #function = self.function[sym]
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_unary(self, node):
        i = None
        for child in node.children:
            if isinstance(child, Symbol):
                i = UnaryExpression(self.context, i, self.return_type[child.symbol], \
                    self.validators[child.symbol], child.additional_info)
            elif child.symbol == 'unary':
                i = self.visit_unary(child)
            else:
                i = self.visit_primary(child)
        return i

    def visit_primary(self, node, refd = 0):
        for child in node.children:
            if child.symbol == 'IDENTIFIER':
                s, pos = self.visit_IDENTIFIER(child)
                return VariableExpression(self.context, s, pos)
            elif child.symbol == 'number':
                return self.visit_number(child)
            elif child.symbol == 'TRUE':
                return ConstantExpression(self.context, False, bool)
            elif child.symbol == 'FALSE':
                return ConstantExpression(self.context, False, bool)
                #disp("\nLOAD_SUPER ")
                #self.visit_call(child.children[0])
            else:
                return self.visit_logic_or(child)

    def visit_number(self, node):
        if node.children[0].symbol == 'float':
            return self.visit_float(node.children[0])
        else:
            return self.visit_DECIMAL(node.children[0])

    def visit_float(self, node):
        s = float(node.children[0].additional_info
                  + "." +
                  node.children[2].additional_info)
        return ConstantExpression(self.context, s, float)

    def visit_DECIMAL(self, node):
        return ConstantExpression(self.context, int(node.additional_info), int)

def optimization(name, phase, cfg, basic_blocks, function):
        print "\nOptimization (Phase ", str(phase) + ")"
        print "=======================\n"
        print name
        print "=" * len(name), "\n"
        for bb in basic_blocks:
            function(bb)
        print "\nAfter", name
        print "=====", "=" * len(name), "\n"
        print "\nBasic blocks"
        print "=============\n"
        print basic_blocks
        cfg = bb_to_cfg(basic_blocks)
        print "\nCFG (adjacency matrix)"
        print "=======================\n"
        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks)

def entry_point(argv):
    # parser, lexer, transformer = make_kool_parser()
    disp("Initializing..\n")
    f = open(argv[1], "r")
    source = f.read()
    tokens = lexer.tokenize(source, True)
    if not we_are_translated():
        disp("\nTokens : ")
        disp(str(tokens))
    disp("\n\n")
    try:
        nt = parser.parse(tokens, False)
        if not we_are_translated():
            disp("ParseTree : ")
            disp(str(nt))
            disp("\n\n")
        res = KoolToAST()
        res = res.transform(nt)
        if not we_are_translated():
            disp("TransformedTree : ")
            disp(str(res))
            res.view()
            disp("\n\n")
        cg = KoolAstGen()
        program = cg.visit_program(res)
        program.validate()
        print "\n\n"
        print "Restructured program"
        print "====================\n"
        print program
        program.compile()
        print "Generated instructions"
        print "======================\n"
        for i in program.instructions:
            print i
        basic_blocks = find_basic_blocks(program.instructions)
        print "\nBasic blocks"
        print "=============\n"
        print basic_blocks
        cfg = bb_to_cfg(basic_blocks)
        print "\nCFG (adjacency matrix)"
        print "=======================\n"
        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks)
        print "\nReaching definitions"
        print "====================="
        find_reaching_definitions(cfg, basic_blocks)
        for bb in basic_blocks:
            print bb, "Inset : ", bb.inreachset

        print "\nAvailable expressions"
        print "======================"
        find_available_expressions(cfg, basic_blocks)
        for bb in basic_blocks:
            print bb, "Avail" + str(bb.inavailset)

        optimization("Common Subexpression Elimination", 1, cfg, basic_blocks, lambda x : x.eliminate_cse())
        optimization("Copy propagation", 2, cfg, basic_blocks, lambda x : x.propagate_copy())
        optimization("Constant Folding", 1, cfg, basic_blocks, lambda x : x.fold_constants())
    except ParseError as e:
        disp("\n\n")
        if we_are_translated():
            disp(e.nice_error_message())
        else:
            disp(e.nice_error_message(f.name, source))
    print "\nExecution completed!"
    return 0

def target(driver, args):
    driver.exe_name = 'kool-%(backend)s'
    return entry_point, args

if __name__ == '__main__':
    import sys
    entry_point(sys.argv)
