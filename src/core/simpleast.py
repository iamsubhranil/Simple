import sys

import lexer
from lexer import Symbol, Nonterminal, Token
from strtbl import get_string, register_string
from simplenodes import *
from simplecfg import find_basic_blocks, bb_to_cfg, print_cfg, view_cfg, \
    find_reaching_definitions, find_available_expressions, \
    find_dominators, find_back_edges, get_natural_loop, \
    insert_preheader, optimize_loop_invariants, find_live_variables, \
    eliminate_dead_code, rebuild_all, eliminate_dead_blocks

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def disp(s):
    print(s, end=' ')

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
            p.statements.append(child.visit(self))
        return p

    def visit_stmt(self, node):
        return node.children[0].visit(self)

    def visit_whilestmt(self, node):
        cond = node.children[0].visit(self)
        then = node.children[1].visit(self)
        return WhileStatement(self.context, cond, then)

    def visit_forstmt(self, node):
        init = None
        cond = None
        incr = None
        if node.children[0]:
            init = node.children[0].visit(self)
        if node.children[1]:
            cond = node.children[1].visit(self)
        if node.children[2]:
            incr = node.children[2].visit(self)
        block = node.children[3].visit(self)
        return ForStatement(self.context, init, cond, incr, block)

    def visit_ifstmt(self, node):
        exp = node.children[0].visit(self)
        then = node.children[1].visit(self)
        elsest = None
        if len(node.children) == 3:
            elsest = node.children[2].visit(self)
        return IfStatement(self.context, exp, then, elsest)

    def visit_block(self, node):
        b = BlockStatement(self.context)
        for child in node.children:
            b.statements.append(child.visit(self))
        return b

    def visit_exprstmt(self, node):
        e = ExpressionStatement(self.context)
        for child in node.children:
            e.exprs.append(child.visit(self))
        return e

    def visit_var_decl_list(self, node):
        e = ExpressionStatement(self.context)
        for child in node.children:
            j = child.visit(self)
            if j is not None:
                e.exprs.append(j)
        return e

    def visit_var_decl(self, node):
        s, pos = node.children[0].visit(self)
        self.context.declare(s, pos)
        if len(node.children) == 2:
            #disp(" = ")
            exp = node.children[1].visit(self)
            self.context.update_assignment(s, exp, pos)
            ve = VariableExpression(self.context, s, pos)
            return AssignmentStatement(self.context, pos, ve, exp)
        return None

    def visit_assignment(self, node):
        i, pos = node.children[0].visit(self)
        j = node.children[1].visit(self)
        ve = VariableExpression(self.context, i, pos)
        return AssignmentStatement(self.context, pos, ve, j)

    def visit_IDENTIFIER(self, node):
        return register_string(node.additional_info.strip()), node.token.source_pos

    def visit_binary(self, node):
        j = node.children[0].visit(self)
        i = 1
        while i < len(node.children):
            k = node.children[i + 1].visit(self)
            sym = node.children[i].symbol
            validator = self.validators[sym]
            rt = self.return_type[sym]
            #function = self.function['OR']
            j = BinaryExpression(self.context, j, k, rt, validator, node.children[i].additional_info)
            i = i + 2
        return j

    def visit_logic_or(self, node):
        return self.visit_binary(node)

    def visit_logic_and(self, node):
        return self.visit_binary(node)

    def visit_equality(self, node):
        return self.visit_binary(node)

    def visit_comparison(self, node):
        return self.visit_binary(node)

    def visit_add(self, node):
        return self.visit_binary(node)

    def visit_mult(self, node):
        return self.visit_binary(node)

    def visit_power(self, node):
        return self.visit_binary(node)

    def visit_unary(self, node):
        i = None
        for child in node.children:
            if isinstance(child, Symbol):
                i = UnaryExpression(self.context, i, self.return_type[child.symbol], \
                    self.validators[child.symbol], child.additional_info)
            else:
                i = child.visit(self)
        return i

    def visit_primary(self, node, refd = 0):
        child = node.children[0]
        if child.symbol == 'IDENTIFIER':
            s, pos = self.visit_IDENTIFIER(child)
            return VariableExpression(self.context, s, pos)
        return child.visit(self)

    def visit_FALSE(self, node):
        return ConstantExpression(self.context, False, bool)

    def visit_TRUE(self, node):
        return ConstantExpression(self.context, True, bool)

    def visit_number(self, node):
        return node.children[0].visit(self)

    def visit_float(self, node):
        s = float(node.children[0].additional_info
                  + "." +
                  node.children[2].additional_info)
        return ConstantExpression(self.context, float(s), float)

    def visit_DECIMAL(self, node):
        return ConstantExpression(self.context, int(node.additional_info), int)

def optimization(name, phase, cfg, basic_blocks, function):
        print("\nOptimization (Phase ", str(phase) + ")")
        print("=======================\n")
        print(name)
        print("=" * len(name), "\n")
        for bb in basic_blocks:
            function(bb)
        print("\nAfter", name)
        print("=====", "=" * len(name), "\n")
        print("\nBasic blocks")
        print("=============\n")
        print(basic_blocks)
        cfg = bb_to_cfg(basic_blocks)
        print("\nCFG (adjacency matrix)")
        print("=======================\n")
        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks, name)

def entry_point(argv):
    # parser, lexer, transformer = make_kool_parser()
    disp("Initializing..\n")
    f = open(argv[1], "r")
    source = f.read()
    tokens = lexer.lex(source)
    disp("\nTokens : ")
    disp(str(tokens))
    disp("\n\n")
    try:
        res = lexer.generate_program(tokens)
        disp("TransformedTree : ")
        disp(str(res))
        res.view()
        disp("\n\n")
        cg = KoolAstGen()
        program = cg.visit_program(res)
        program.validate()
        print("\n\n")
        print("Restructured program")
        print("====================\n")
        print(program)
        program.compile()
        print("Generated instructions")
        print("======================\n")
        for i in program.instructions:
            print(i)
        basic_blocks = find_basic_blocks(program.instructions)
        print("\nBasic blocks")
        print("=============\n")
        print(basic_blocks)
        cfg = bb_to_cfg(basic_blocks)
        print("\nCFG (adjacency matrix)")
        print("=======================\n")
        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks)

        print("\nFinding dominator tree")
        print("=======================")
        dom = find_dominators(cfg, basic_blocks)
        i = 0
        for bb in basic_blocks:
            print(bb, " Dominators :", dom[i])
            i = i + 1

        print("\nFinding back edges")
        print("===================")
        back_edges = find_back_edges(cfg, dom)
        print(back_edges)
        loops = []
        for be in back_edges:
            loop = get_natural_loop(cfg, be[0], be[1])
            print("Loop :", loop)
            loops.append(loop)

        i = 0
        while i < len(loops):
            print("\nInitializing loop", i)
            print("====================")
            basic_blocks, cfg, dom, back_edges, loops = insert_preheader(cfg, basic_blocks, loops, i)

            #print "\nAfter Initializing preheader"
            #print "============================"
            #print_cfg(cfg, basic_blocks)
            #view_cfg(cfg, basic_blocks)
            i = i + 1

        print("\nReaching definitions")
        print("=====================")
        find_reaching_definitions(cfg, basic_blocks)
        for bb in basic_blocks:
            print(bb, "Inset : ", bb.inreachset)

        print("\nAvailable expressions")
        print("======================")
        find_available_expressions(cfg, basic_blocks)
        for bb in basic_blocks:
            print(bb, "Avail" + str(bb.inavailset))

        print("\nLive variables")
        print("================")
        find_live_variables(cfg, basic_blocks)
        for bb in basic_blocks:
            if bb.outliveset != None:
                print(bb, "LiveOut : {", end=' ')
                for i in bb.outliveset:
                    print(get_string(i), end=' ')
                print("}")

        #optimization("Copy propagation", 0, cfg, basic_blocks, lambda x : x.propagate_copy())

        i = 0
        while i < len(loops):
            print("\nOptimizing loop invariants (loop:", loops[i], ")")
            print("==============================")
            basic_blocks, cfg, dom, back_edges, loops = optimize_loop_invariants(cfg, basic_blocks, dom, back_edges, loops, i)
            i = i + 1

        print("\nReevaluating dataflow")
        print("=====================\n")
        find_reaching_definitions(cfg, basic_blocks)
        find_available_expressions(cfg, basic_blocks)
        find_live_variables(cfg, basic_blocks)

        i = 0
        while i < len(loops):
            print("\nSearching for induction variables (loop:", loops[i], ")")
            print("===================================")
            var = []
            lp = []
            for bi in loops[i]:
                lp.append(basic_blocks[bi])
            for bi in loops[i]:
                var.append(basic_blocks[bi].find_induction_variables(lp))
            print("Induction variables :", end=' ') #var,
            for v in var:
                for w in v:
                    print(get_string(w[0]), end=' ')
            i = i + 1

        optimization("Common Subexpression Elimination", 1, cfg, basic_blocks, lambda x : x.eliminate_cse())
        optimization("Copy propagation", 2, cfg, basic_blocks, lambda x : x.propagate_copy())
        optimization("Constant Folding", 3, cfg, basic_blocks, lambda x : x.fold_constants())
        # Constant folding may have modified the cfg
        # Let's rebuild
        basic_blocks, cfg, dom, back_edges, loops = rebuild_all(basic_blocks)
        # Some expressions can still be optimized after performing a different optimization
        # What is the correct order of optimization then?
        #optimization("Common Subexpression Elimination", 4, cfg, basic_blocks, lambda x : x.eliminate_cse())

        print("\nReaching definitions")
        print("=====================")
        find_reaching_definitions(cfg, basic_blocks)
        for bb in basic_blocks:
            print(bb, "Inset : ", bb.inreachset)

        print("\nAvailable expressions")
        print("======================")
        find_available_expressions(cfg, basic_blocks)
        for bb in basic_blocks:
            print(bb, "Avail" + str(bb.inavailset))

        print("\nLive variables")
        print("================")
        find_live_variables(cfg, basic_blocks)
        for bb in basic_blocks:
            if bb.outliveset != None:
                print(bb, "LiveOut : {", end=' ')
                for i in bb.outliveset:
                    print(get_string(i), end=' ')
                print("}")

        print("\nAfter eliminating dead code")
        print("============================\n")

        basic_blocks, cfg, dom, back_edges, loops = eliminate_dead_code(basic_blocks, cfg, dom, back_edges, loops)

        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks)

        print("\nAfter eliminating dead blocks")
        print("==============================\n")

        basic_blocks, cfg, dom, back_edges, loops = eliminate_dead_blocks(basic_blocks, cfg, dom, back_edges, loops)

        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks)

    except RuntimeError as e:
        disp("\n\n")
        disp(e.nice_error_message(f.name, source))
    print("\nExecution completed!")
    return 0

def target(driver, args):
    driver.exe_name = 'kool-%(backend)s'
    return entry_point, None

if __name__ == '__main__':
    entry_point(sys.argv)
