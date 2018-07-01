from rpython.rlib.parsing.parsing import *
from rpython.rlib.parsing.ebnfparse import *
# generated code between this line and its other occurence
class KoolToAST(object):
    def visit_program(self, node):
        #auto-generated code, don't edit
        children = []
        expr = self.visit__plus_symbol0(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__plus_symbol0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_stmt(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_stmt(node.children[0]))
        expr = self.visit__plus_symbol0(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__plus_symbol1(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_stmt(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_stmt(node.children[0]))
        expr = self.visit__plus_symbol1(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_block(self, node):
        #auto-generated code, don't edit
        children = []
        expr = self.visit__plus_symbol1(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_stmt(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'block':
            children = []
            children.extend(self.visit_block(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'exprstmt':
            children = []
            children.extend(self.visit_exprstmt(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'ifstmt':
            children = []
            children.extend(self.visit_ifstmt(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'var_decl_list':
            children = []
            children.extend(self.visit_var_decl_list(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_whilestmt(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit_retstmt(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_logic_or(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol0(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_stmt(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit_ifstmt(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 3:
            children = []
            children.extend(self.visit_logic_or(node.children[1]))
            children.extend(self.visit_stmt(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_logic_or(node.children[1]))
        children.extend(self.visit_stmt(node.children[2]))
        expr = self.visit__maybe_symbol0(node.children[3])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_whilestmt(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_logic_or(node.children[1]))
        children.extend(self.visit_stmt(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol1(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend(self.visit_var_decl(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_var_decl(node.children[1]))
        expr = self.visit__star_symbol1(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_var_decl_list(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 3:
            children = []
            children.extend(self.visit_var_decl(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_var_decl(node.children[1]))
        expr = self.visit__star_symbol1(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol2(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_logic_or(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit_var_decl(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__maybe_symbol2(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol3(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend(self.visit_assignment(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_assignment(node.children[1]))
        expr = self.visit__star_symbol3(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_exprstmt(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend(self.visit_assignment(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_assignment(node.children[0]))
        expr = self.visit__star_symbol3(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_assignment(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_logic_or(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol4(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend(self.visit_logic_and(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_logic_and(node.children[1]))
        expr = self.visit__star_symbol4(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_logic_or(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_logic_and(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_logic_and(node.children[0]))
        expr = self.visit__star_symbol4(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol5(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend(self.visit_equality(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_equality(node.children[1]))
        expr = self.visit__star_symbol5(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_logic_and(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_equality(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_equality(node.children[0]))
        expr = self.visit__star_symbol5(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_symeq(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'EQUAL_EQUAL':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol6(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            expr = self.visit_symeq(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            children.extend(self.visit_comparison(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit_symeq(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend(self.visit_comparison(node.children[1]))
        expr = self.visit__star_symbol6(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_equality(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_comparison(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_comparison(node.children[0]))
        expr = self.visit__star_symbol6(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_symcmp(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'GREATER_THAN':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'GT_EQ':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'LESS_THAN':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol7(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            expr = self.visit_symcmp(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            children.extend(self.visit_add(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit_symcmp(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend(self.visit_add(node.children[1]))
        expr = self.visit__star_symbol7(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_comparison(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_add(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_add(node.children[0]))
        expr = self.visit__star_symbol7(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_symadd(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'MINUS':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol8(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            expr = self.visit_symadd(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            children.extend(self.visit_mult(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit_symadd(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend(self.visit_mult(node.children[1]))
        expr = self.visit__star_symbol8(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_add(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_mult(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_mult(node.children[0]))
        expr = self.visit__star_symbol8(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_symmult(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'BACKSLASH':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol9(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            expr = self.visit_symmult(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            children.extend(self.visit_power(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit_symmult(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend(self.visit_power(node.children[1]))
        expr = self.visit__star_symbol9(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_mult(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_power(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_power(node.children[0]))
        expr = self.visit__star_symbol9(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol10(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend(self.visit_unary(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_unary(node.children[1]))
        expr = self.visit__star_symbol10(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_power(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_unary(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_unary(node.children[0]))
        expr = self.visit__star_symbol10(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_symun(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'MINUS':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit_unary(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_primary(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit_symun(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend(self.visit_unary(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit_number(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'DECIMAL':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_float(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit_float(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend([node.children[1]])
        children.extend([node.children[2]])
        return [Nonterminal(node.symbol, children)]
    def visit_primary(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            if node.children[0].symbol == 'FALSE':
                children = []
                children.extend([node.children[0]])
                return [Nonterminal(node.symbol, children)]
            if node.children[0].symbol == 'IDENTIFIER':
                children = []
                children.extend([node.children[0]])
                return [Nonterminal(node.symbol, children)]
            if node.children[0].symbol == 'TRUE':
                children = []
                children.extend([node.children[0]])
                return [Nonterminal(node.symbol, children)]
            children = []
            children.extend(self.visit_number(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_logic_or(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def transform(self, tree):
        #auto-generated code, don't edit
        assert isinstance(tree, Nonterminal)
        assert tree.symbol == 'program'
        r = self.visit_program(tree)
        assert len(r) == 1
        if not we_are_translated():
            try:
                if py.test.config.option.view:
                    r[0].view()
            except AttributeError:
                pass
        return r[0]
parser = PackratParser([Rule('program', [['_plus_symbol0', 'EOF']]),
  Rule('_plus_symbol0', [['stmt', '_plus_symbol0'], ['stmt']]),
  Rule('_plus_symbol1', [['stmt', '_plus_symbol1'], ['stmt']]),
  Rule('block', [['CURL_OPEN', '_plus_symbol1', 'CURL_CLOSE']]),
  Rule('stmt', [['exprstmt'], ['var_decl_list'], ['ifstmt'], ['whilestmt'], ['block']]),
  Rule('retstmt', [['RET', 'logic_or', 'SEMICOLON']]),
  Rule('_maybe_symbol0', [['ELSE', 'stmt']]),
  Rule('ifstmt', [['IF', 'logic_or', 'stmt', '_maybe_symbol0'], ['IF', 'logic_or', 'stmt']]),
  Rule('whilestmt', [['WHILE', 'logic_or', 'stmt']]),
  Rule('_star_symbol1', [['COMMA', 'var_decl', '_star_symbol1'], ['COMMA', 'var_decl']]),
  Rule('var_decl_list', [['VAR', 'var_decl', '_star_symbol1', 'SEMICOLON'], ['VAR', 'var_decl', 'SEMICOLON']]),
  Rule('_maybe_symbol2', [['EQUAL', 'logic_or']]),
  Rule('var_decl', [['IDENTIFIER', '_maybe_symbol2'], ['IDENTIFIER']]),
  Rule('_star_symbol3', [['COMMA', 'assignment', '_star_symbol3'], ['COMMA', 'assignment']]),
  Rule('exprstmt', [['assignment', '_star_symbol3', 'SEMICOLON'], ['assignment', 'SEMICOLON']]),
  Rule('assignment', [['IDENTIFIER', 'EQUAL', 'logic_or']]),
  Rule('_star_symbol4', [['OR', 'logic_and', '_star_symbol4'], ['OR', 'logic_and']]),
  Rule('logic_or', [['logic_and', '_star_symbol4'], ['logic_and']]),
  Rule('_star_symbol5', [['AND', 'equality', '_star_symbol5'], ['AND', 'equality']]),
  Rule('logic_and', [['equality', '_star_symbol5'], ['equality']]),
  Rule('symeq', [['EQUAL_EQUAL'], ['NOT_EQUAL']]),
  Rule('_star_symbol6', [['symeq', 'comparison', '_star_symbol6'], ['symeq', 'comparison']]),
  Rule('equality', [['comparison', '_star_symbol6'], ['comparison']]),
  Rule('symcmp', [['GREATER_THAN'], ['GT_EQ'], ['LESS_THAN'], ['LT_EQ']]),
  Rule('_star_symbol7', [['symcmp', 'add', '_star_symbol7'], ['symcmp', 'add']]),
  Rule('comparison', [['add', '_star_symbol7'], ['add']]),
  Rule('symadd', [['PLUS'], ['MINUS']]),
  Rule('_star_symbol8', [['symadd', 'mult', '_star_symbol8'], ['symadd', 'mult']]),
  Rule('add', [['mult', '_star_symbol8'], ['mult']]),
  Rule('symmult', [['STAR'], ['BACKSLASH']]),
  Rule('_star_symbol9', [['symmult', 'power', '_star_symbol9'], ['symmult', 'power']]),
  Rule('mult', [['power', '_star_symbol9'], ['power']]),
  Rule('_star_symbol10', [['CAP', 'unary', '_star_symbol10'], ['CAP', 'unary']]),
  Rule('power', [['unary', '_star_symbol10'], ['unary']]),
  Rule('symun', [['NOT'], ['MINUS']]),
  Rule('unary', [['symun', 'unary'], ['primary']]),
  Rule('number', [['float'], ['DECIMAL']]),
  Rule('float', [['DECIMAL', 'DOT', 'DECIMAL']]),
  Rule('primary', [['IDENTIFIER'], ['TRUE'], ['FALSE'], ['number'], ['PAREN_OPEN', 'logic_or', 'PAREN_CLOSE']])],
 'program')
def recognize(runner, i):
    #auto-generated code, don't edit
    assert i >= 0
    input = runner.text
    state = 0
    while 1:
        if state == 0:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 0
                return ~i
            if char == ' ':
                state = 1
            elif char == '(':
                state = 2
            elif char == ',':
                state = 3
            elif char == '0':
                state = 4
            elif '1' <= char <= '9':
                state = 5
            elif char == '<':
                state = 6
            elif 'A' <= char <= 'Z':
                state = 7
            elif 'j' <= char <= 'n':
                state = 7
            elif 'p' <= char <= 's':
                state = 7
            elif 'b' <= char <= 'd':
                state = 7
            elif 'x' <= char <= 'z':
                state = 7
            elif char == 'g':
                state = 7
            elif char == 'h':
                state = 7
            elif char == '_':
                state = 7
            elif char == 'u':
                state = 7
            elif char == 't':
                state = 8
            elif char == '+':
                state = 9
            elif char == '/':
                state = 10
            elif char == ';':
                state = 11
            elif char == '[':
                state = 12
            elif char == 'o':
                state = 13
            elif char == 'w':
                state = 14
            elif char == '{':
                state = 15
            elif char == '\n':
                state = 16
            elif char == '*':
                state = 17
            elif char == '.':
                state = 18
            elif char == '>':
                state = 19
            elif char == '^':
                state = 20
            elif char == 'f':
                state = 21
            elif char == 'v':
                state = 22
            elif char == '\t':
                state = 23
            elif char == '\r':
                state = 24
            elif char == '!':
                state = 25
            elif char == ')':
                state = 26
            elif char == '-':
                state = 27
            elif char == '=':
                state = 28
            elif char == ']':
                state = 29
            elif char == 'a':
                state = 30
            elif char == 'e':
                state = 31
            elif char == 'i':
                state = 32
            elif char == '}':
                state = 33
            else:
                break
        if state == 5:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 5
                return i
            if '0' <= char <= '9':
                state = 5
                continue
            else:
                break
        if state == 6:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 6
                return i
            if char == '=':
                state = 57
            else:
                break
        if state == 7:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 7
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 8:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 8
                return i
            if char == 'r':
                state = 54
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'q':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 's' <= char <= 'z':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 13:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 13
                return i
            if char == 'r':
                state = 53
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'q':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 's' <= char <= 'z':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 14:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 14
                return i
            if char == 'h':
                state = 49
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'i' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'g':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 19:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 19
                return i
            if char == '=':
                state = 48
            else:
                break
        if state == 21:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 21
                return i
            if char == 'a':
                state = 44
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'b' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 22:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 22
                return i
            if char == 'a':
                state = 42
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'b' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 25:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 25
                return i
            if char == '=':
                state = 41
            else:
                break
        if state == 28:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 28
                return i
            if char == '=':
                state = 40
            else:
                break
        if state == 30:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 30
                return i
            if char == 'n':
                state = 38
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'm':
                state = 7
                continue
            elif 'o' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 31:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 31
                return i
            if char == 'l':
                state = 35
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'm' <= char <= 'z':
                state = 7
                continue
            elif 'a' <= char <= 'k':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 32:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 32
                return i
            if char == 'f':
                state = 34
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'g' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'e':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 34:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 34
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 35:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 35
                return i
            if char == 's':
                state = 36
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'r':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 't' <= char <= 'z':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 36:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 36
                return i
            if char == 'e':
                state = 37
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'f' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'd':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 37:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 37
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 38:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 38
                return i
            if char == 'd':
                state = 39
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'e' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'c':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 39:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 39
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 42:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 42
                return i
            if char == 'r':
                state = 43
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'q':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 's' <= char <= 'z':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 43:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 43
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 44:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 44
                return i
            if char == 'l':
                state = 45
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'm' <= char <= 'z':
                state = 7
                continue
            elif 'a' <= char <= 'k':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 45:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 45
                return i
            if char == 's':
                state = 46
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'r':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 't' <= char <= 'z':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 46:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 46
                return i
            if char == 'e':
                state = 47
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'f' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'd':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 47:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 47
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 49:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 49
                return i
            if char == 'i':
                state = 50
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'j' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'h':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 50:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 50
                return i
            if char == 'l':
                state = 51
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'm' <= char <= 'z':
                state = 7
                continue
            elif 'a' <= char <= 'k':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 51:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 51
                return i
            if char == 'e':
                state = 52
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'f' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'd':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 52:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 52
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 53:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 53
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 54:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 54
                return i
            if char == 'u':
                state = 55
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 't':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'v' <= char <= 'z':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 55:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 55
                return i
            if char == 'e':
                state = 56
            elif 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'f' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif 'a' <= char <= 'd':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        if state == 56:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 56
                return i
            if 'A' <= char <= 'Z':
                state = 7
                continue
            elif 'a' <= char <= 'z':
                state = 7
                continue
            elif '0' <= char <= '9':
                state = 7
                continue
            elif char == '_':
                state = 7
                continue
            else:
                break
        runner.last_matched_state = state
        runner.last_matched_index = i - 1
        runner.state = state
        if i == len(input):
            return i
        else:
            return ~i
        break
    runner.state = state
    return ~i
lexer = DummyLexer(recognize, DFA(58,
 {(0, '\t'): 23,
  (0, '\n'): 16,
  (0, '\r'): 24,
  (0, ' '): 1,
  (0, '!'): 25,
  (0, '('): 2,
  (0, ')'): 26,
  (0, '*'): 17,
  (0, '+'): 9,
  (0, ','): 3,
  (0, '-'): 27,
  (0, '.'): 18,
  (0, '/'): 10,
  (0, '0'): 4,
  (0, '1'): 5,
  (0, '2'): 5,
  (0, '3'): 5,
  (0, '4'): 5,
  (0, '5'): 5,
  (0, '6'): 5,
  (0, '7'): 5,
  (0, '8'): 5,
  (0, '9'): 5,
  (0, ';'): 11,
  (0, '<'): 6,
  (0, '='): 28,
  (0, '>'): 19,
  (0, 'A'): 7,
  (0, 'B'): 7,
  (0, 'C'): 7,
  (0, 'D'): 7,
  (0, 'E'): 7,
  (0, 'F'): 7,
  (0, 'G'): 7,
  (0, 'H'): 7,
  (0, 'I'): 7,
  (0, 'J'): 7,
  (0, 'K'): 7,
  (0, 'L'): 7,
  (0, 'M'): 7,
  (0, 'N'): 7,
  (0, 'O'): 7,
  (0, 'P'): 7,
  (0, 'Q'): 7,
  (0, 'R'): 7,
  (0, 'S'): 7,
  (0, 'T'): 7,
  (0, 'U'): 7,
  (0, 'V'): 7,
  (0, 'W'): 7,
  (0, 'X'): 7,
  (0, 'Y'): 7,
  (0, 'Z'): 7,
  (0, '['): 12,
  (0, ']'): 29,
  (0, '^'): 20,
  (0, '_'): 7,
  (0, 'a'): 30,
  (0, 'b'): 7,
  (0, 'c'): 7,
  (0, 'd'): 7,
  (0, 'e'): 31,
  (0, 'f'): 21,
  (0, 'g'): 7,
  (0, 'h'): 7,
  (0, 'i'): 32,
  (0, 'j'): 7,
  (0, 'k'): 7,
  (0, 'l'): 7,
  (0, 'm'): 7,
  (0, 'n'): 7,
  (0, 'o'): 13,
  (0, 'p'): 7,
  (0, 'q'): 7,
  (0, 'r'): 7,
  (0, 's'): 7,
  (0, 't'): 8,
  (0, 'u'): 7,
  (0, 'v'): 22,
  (0, 'w'): 14,
  (0, 'x'): 7,
  (0, 'y'): 7,
  (0, 'z'): 7,
  (0, '{'): 15,
  (0, '}'): 33,
  (5, '0'): 5,
  (5, '1'): 5,
  (5, '2'): 5,
  (5, '3'): 5,
  (5, '4'): 5,
  (5, '5'): 5,
  (5, '6'): 5,
  (5, '7'): 5,
  (5, '8'): 5,
  (5, '9'): 5,
  (6, '='): 57,
  (7, '0'): 7,
  (7, '1'): 7,
  (7, '2'): 7,
  (7, '3'): 7,
  (7, '4'): 7,
  (7, '5'): 7,
  (7, '6'): 7,
  (7, '7'): 7,
  (7, '8'): 7,
  (7, '9'): 7,
  (7, 'A'): 7,
  (7, 'B'): 7,
  (7, 'C'): 7,
  (7, 'D'): 7,
  (7, 'E'): 7,
  (7, 'F'): 7,
  (7, 'G'): 7,
  (7, 'H'): 7,
  (7, 'I'): 7,
  (7, 'J'): 7,
  (7, 'K'): 7,
  (7, 'L'): 7,
  (7, 'M'): 7,
  (7, 'N'): 7,
  (7, 'O'): 7,
  (7, 'P'): 7,
  (7, 'Q'): 7,
  (7, 'R'): 7,
  (7, 'S'): 7,
  (7, 'T'): 7,
  (7, 'U'): 7,
  (7, 'V'): 7,
  (7, 'W'): 7,
  (7, 'X'): 7,
  (7, 'Y'): 7,
  (7, 'Z'): 7,
  (7, '_'): 7,
  (7, 'a'): 7,
  (7, 'b'): 7,
  (7, 'c'): 7,
  (7, 'd'): 7,
  (7, 'e'): 7,
  (7, 'f'): 7,
  (7, 'g'): 7,
  (7, 'h'): 7,
  (7, 'i'): 7,
  (7, 'j'): 7,
  (7, 'k'): 7,
  (7, 'l'): 7,
  (7, 'm'): 7,
  (7, 'n'): 7,
  (7, 'o'): 7,
  (7, 'p'): 7,
  (7, 'q'): 7,
  (7, 'r'): 7,
  (7, 's'): 7,
  (7, 't'): 7,
  (7, 'u'): 7,
  (7, 'v'): 7,
  (7, 'w'): 7,
  (7, 'x'): 7,
  (7, 'y'): 7,
  (7, 'z'): 7,
  (8, '0'): 7,
  (8, '1'): 7,
  (8, '2'): 7,
  (8, '3'): 7,
  (8, '4'): 7,
  (8, '5'): 7,
  (8, '6'): 7,
  (8, '7'): 7,
  (8, '8'): 7,
  (8, '9'): 7,
  (8, 'A'): 7,
  (8, 'B'): 7,
  (8, 'C'): 7,
  (8, 'D'): 7,
  (8, 'E'): 7,
  (8, 'F'): 7,
  (8, 'G'): 7,
  (8, 'H'): 7,
  (8, 'I'): 7,
  (8, 'J'): 7,
  (8, 'K'): 7,
  (8, 'L'): 7,
  (8, 'M'): 7,
  (8, 'N'): 7,
  (8, 'O'): 7,
  (8, 'P'): 7,
  (8, 'Q'): 7,
  (8, 'R'): 7,
  (8, 'S'): 7,
  (8, 'T'): 7,
  (8, 'U'): 7,
  (8, 'V'): 7,
  (8, 'W'): 7,
  (8, 'X'): 7,
  (8, 'Y'): 7,
  (8, 'Z'): 7,
  (8, '_'): 7,
  (8, 'a'): 7,
  (8, 'b'): 7,
  (8, 'c'): 7,
  (8, 'd'): 7,
  (8, 'e'): 7,
  (8, 'f'): 7,
  (8, 'g'): 7,
  (8, 'h'): 7,
  (8, 'i'): 7,
  (8, 'j'): 7,
  (8, 'k'): 7,
  (8, 'l'): 7,
  (8, 'm'): 7,
  (8, 'n'): 7,
  (8, 'o'): 7,
  (8, 'p'): 7,
  (8, 'q'): 7,
  (8, 'r'): 54,
  (8, 's'): 7,
  (8, 't'): 7,
  (8, 'u'): 7,
  (8, 'v'): 7,
  (8, 'w'): 7,
  (8, 'x'): 7,
  (8, 'y'): 7,
  (8, 'z'): 7,
  (13, '0'): 7,
  (13, '1'): 7,
  (13, '2'): 7,
  (13, '3'): 7,
  (13, '4'): 7,
  (13, '5'): 7,
  (13, '6'): 7,
  (13, '7'): 7,
  (13, '8'): 7,
  (13, '9'): 7,
  (13, 'A'): 7,
  (13, 'B'): 7,
  (13, 'C'): 7,
  (13, 'D'): 7,
  (13, 'E'): 7,
  (13, 'F'): 7,
  (13, 'G'): 7,
  (13, 'H'): 7,
  (13, 'I'): 7,
  (13, 'J'): 7,
  (13, 'K'): 7,
  (13, 'L'): 7,
  (13, 'M'): 7,
  (13, 'N'): 7,
  (13, 'O'): 7,
  (13, 'P'): 7,
  (13, 'Q'): 7,
  (13, 'R'): 7,
  (13, 'S'): 7,
  (13, 'T'): 7,
  (13, 'U'): 7,
  (13, 'V'): 7,
  (13, 'W'): 7,
  (13, 'X'): 7,
  (13, 'Y'): 7,
  (13, 'Z'): 7,
  (13, '_'): 7,
  (13, 'a'): 7,
  (13, 'b'): 7,
  (13, 'c'): 7,
  (13, 'd'): 7,
  (13, 'e'): 7,
  (13, 'f'): 7,
  (13, 'g'): 7,
  (13, 'h'): 7,
  (13, 'i'): 7,
  (13, 'j'): 7,
  (13, 'k'): 7,
  (13, 'l'): 7,
  (13, 'm'): 7,
  (13, 'n'): 7,
  (13, 'o'): 7,
  (13, 'p'): 7,
  (13, 'q'): 7,
  (13, 'r'): 53,
  (13, 's'): 7,
  (13, 't'): 7,
  (13, 'u'): 7,
  (13, 'v'): 7,
  (13, 'w'): 7,
  (13, 'x'): 7,
  (13, 'y'): 7,
  (13, 'z'): 7,
  (14, '0'): 7,
  (14, '1'): 7,
  (14, '2'): 7,
  (14, '3'): 7,
  (14, '4'): 7,
  (14, '5'): 7,
  (14, '6'): 7,
  (14, '7'): 7,
  (14, '8'): 7,
  (14, '9'): 7,
  (14, 'A'): 7,
  (14, 'B'): 7,
  (14, 'C'): 7,
  (14, 'D'): 7,
  (14, 'E'): 7,
  (14, 'F'): 7,
  (14, 'G'): 7,
  (14, 'H'): 7,
  (14, 'I'): 7,
  (14, 'J'): 7,
  (14, 'K'): 7,
  (14, 'L'): 7,
  (14, 'M'): 7,
  (14, 'N'): 7,
  (14, 'O'): 7,
  (14, 'P'): 7,
  (14, 'Q'): 7,
  (14, 'R'): 7,
  (14, 'S'): 7,
  (14, 'T'): 7,
  (14, 'U'): 7,
  (14, 'V'): 7,
  (14, 'W'): 7,
  (14, 'X'): 7,
  (14, 'Y'): 7,
  (14, 'Z'): 7,
  (14, '_'): 7,
  (14, 'a'): 7,
  (14, 'b'): 7,
  (14, 'c'): 7,
  (14, 'd'): 7,
  (14, 'e'): 7,
  (14, 'f'): 7,
  (14, 'g'): 7,
  (14, 'h'): 49,
  (14, 'i'): 7,
  (14, 'j'): 7,
  (14, 'k'): 7,
  (14, 'l'): 7,
  (14, 'm'): 7,
  (14, 'n'): 7,
  (14, 'o'): 7,
  (14, 'p'): 7,
  (14, 'q'): 7,
  (14, 'r'): 7,
  (14, 's'): 7,
  (14, 't'): 7,
  (14, 'u'): 7,
  (14, 'v'): 7,
  (14, 'w'): 7,
  (14, 'x'): 7,
  (14, 'y'): 7,
  (14, 'z'): 7,
  (19, '='): 48,
  (21, '0'): 7,
  (21, '1'): 7,
  (21, '2'): 7,
  (21, '3'): 7,
  (21, '4'): 7,
  (21, '5'): 7,
  (21, '6'): 7,
  (21, '7'): 7,
  (21, '8'): 7,
  (21, '9'): 7,
  (21, 'A'): 7,
  (21, 'B'): 7,
  (21, 'C'): 7,
  (21, 'D'): 7,
  (21, 'E'): 7,
  (21, 'F'): 7,
  (21, 'G'): 7,
  (21, 'H'): 7,
  (21, 'I'): 7,
  (21, 'J'): 7,
  (21, 'K'): 7,
  (21, 'L'): 7,
  (21, 'M'): 7,
  (21, 'N'): 7,
  (21, 'O'): 7,
  (21, 'P'): 7,
  (21, 'Q'): 7,
  (21, 'R'): 7,
  (21, 'S'): 7,
  (21, 'T'): 7,
  (21, 'U'): 7,
  (21, 'V'): 7,
  (21, 'W'): 7,
  (21, 'X'): 7,
  (21, 'Y'): 7,
  (21, 'Z'): 7,
  (21, '_'): 7,
  (21, 'a'): 44,
  (21, 'b'): 7,
  (21, 'c'): 7,
  (21, 'd'): 7,
  (21, 'e'): 7,
  (21, 'f'): 7,
  (21, 'g'): 7,
  (21, 'h'): 7,
  (21, 'i'): 7,
  (21, 'j'): 7,
  (21, 'k'): 7,
  (21, 'l'): 7,
  (21, 'm'): 7,
  (21, 'n'): 7,
  (21, 'o'): 7,
  (21, 'p'): 7,
  (21, 'q'): 7,
  (21, 'r'): 7,
  (21, 's'): 7,
  (21, 't'): 7,
  (21, 'u'): 7,
  (21, 'v'): 7,
  (21, 'w'): 7,
  (21, 'x'): 7,
  (21, 'y'): 7,
  (21, 'z'): 7,
  (22, '0'): 7,
  (22, '1'): 7,
  (22, '2'): 7,
  (22, '3'): 7,
  (22, '4'): 7,
  (22, '5'): 7,
  (22, '6'): 7,
  (22, '7'): 7,
  (22, '8'): 7,
  (22, '9'): 7,
  (22, 'A'): 7,
  (22, 'B'): 7,
  (22, 'C'): 7,
  (22, 'D'): 7,
  (22, 'E'): 7,
  (22, 'F'): 7,
  (22, 'G'): 7,
  (22, 'H'): 7,
  (22, 'I'): 7,
  (22, 'J'): 7,
  (22, 'K'): 7,
  (22, 'L'): 7,
  (22, 'M'): 7,
  (22, 'N'): 7,
  (22, 'O'): 7,
  (22, 'P'): 7,
  (22, 'Q'): 7,
  (22, 'R'): 7,
  (22, 'S'): 7,
  (22, 'T'): 7,
  (22, 'U'): 7,
  (22, 'V'): 7,
  (22, 'W'): 7,
  (22, 'X'): 7,
  (22, 'Y'): 7,
  (22, 'Z'): 7,
  (22, '_'): 7,
  (22, 'a'): 42,
  (22, 'b'): 7,
  (22, 'c'): 7,
  (22, 'd'): 7,
  (22, 'e'): 7,
  (22, 'f'): 7,
  (22, 'g'): 7,
  (22, 'h'): 7,
  (22, 'i'): 7,
  (22, 'j'): 7,
  (22, 'k'): 7,
  (22, 'l'): 7,
  (22, 'm'): 7,
  (22, 'n'): 7,
  (22, 'o'): 7,
  (22, 'p'): 7,
  (22, 'q'): 7,
  (22, 'r'): 7,
  (22, 's'): 7,
  (22, 't'): 7,
  (22, 'u'): 7,
  (22, 'v'): 7,
  (22, 'w'): 7,
  (22, 'x'): 7,
  (22, 'y'): 7,
  (22, 'z'): 7,
  (25, '='): 41,
  (28, '='): 40,
  (30, '0'): 7,
  (30, '1'): 7,
  (30, '2'): 7,
  (30, '3'): 7,
  (30, '4'): 7,
  (30, '5'): 7,
  (30, '6'): 7,
  (30, '7'): 7,
  (30, '8'): 7,
  (30, '9'): 7,
  (30, 'A'): 7,
  (30, 'B'): 7,
  (30, 'C'): 7,
  (30, 'D'): 7,
  (30, 'E'): 7,
  (30, 'F'): 7,
  (30, 'G'): 7,
  (30, 'H'): 7,
  (30, 'I'): 7,
  (30, 'J'): 7,
  (30, 'K'): 7,
  (30, 'L'): 7,
  (30, 'M'): 7,
  (30, 'N'): 7,
  (30, 'O'): 7,
  (30, 'P'): 7,
  (30, 'Q'): 7,
  (30, 'R'): 7,
  (30, 'S'): 7,
  (30, 'T'): 7,
  (30, 'U'): 7,
  (30, 'V'): 7,
  (30, 'W'): 7,
  (30, 'X'): 7,
  (30, 'Y'): 7,
  (30, 'Z'): 7,
  (30, '_'): 7,
  (30, 'a'): 7,
  (30, 'b'): 7,
  (30, 'c'): 7,
  (30, 'd'): 7,
  (30, 'e'): 7,
  (30, 'f'): 7,
  (30, 'g'): 7,
  (30, 'h'): 7,
  (30, 'i'): 7,
  (30, 'j'): 7,
  (30, 'k'): 7,
  (30, 'l'): 7,
  (30, 'm'): 7,
  (30, 'n'): 38,
  (30, 'o'): 7,
  (30, 'p'): 7,
  (30, 'q'): 7,
  (30, 'r'): 7,
  (30, 's'): 7,
  (30, 't'): 7,
  (30, 'u'): 7,
  (30, 'v'): 7,
  (30, 'w'): 7,
  (30, 'x'): 7,
  (30, 'y'): 7,
  (30, 'z'): 7,
  (31, '0'): 7,
  (31, '1'): 7,
  (31, '2'): 7,
  (31, '3'): 7,
  (31, '4'): 7,
  (31, '5'): 7,
  (31, '6'): 7,
  (31, '7'): 7,
  (31, '8'): 7,
  (31, '9'): 7,
  (31, 'A'): 7,
  (31, 'B'): 7,
  (31, 'C'): 7,
  (31, 'D'): 7,
  (31, 'E'): 7,
  (31, 'F'): 7,
  (31, 'G'): 7,
  (31, 'H'): 7,
  (31, 'I'): 7,
  (31, 'J'): 7,
  (31, 'K'): 7,
  (31, 'L'): 7,
  (31, 'M'): 7,
  (31, 'N'): 7,
  (31, 'O'): 7,
  (31, 'P'): 7,
  (31, 'Q'): 7,
  (31, 'R'): 7,
  (31, 'S'): 7,
  (31, 'T'): 7,
  (31, 'U'): 7,
  (31, 'V'): 7,
  (31, 'W'): 7,
  (31, 'X'): 7,
  (31, 'Y'): 7,
  (31, 'Z'): 7,
  (31, '_'): 7,
  (31, 'a'): 7,
  (31, 'b'): 7,
  (31, 'c'): 7,
  (31, 'd'): 7,
  (31, 'e'): 7,
  (31, 'f'): 7,
  (31, 'g'): 7,
  (31, 'h'): 7,
  (31, 'i'): 7,
  (31, 'j'): 7,
  (31, 'k'): 7,
  (31, 'l'): 35,
  (31, 'm'): 7,
  (31, 'n'): 7,
  (31, 'o'): 7,
  (31, 'p'): 7,
  (31, 'q'): 7,
  (31, 'r'): 7,
  (31, 's'): 7,
  (31, 't'): 7,
  (31, 'u'): 7,
  (31, 'v'): 7,
  (31, 'w'): 7,
  (31, 'x'): 7,
  (31, 'y'): 7,
  (31, 'z'): 7,
  (32, '0'): 7,
  (32, '1'): 7,
  (32, '2'): 7,
  (32, '3'): 7,
  (32, '4'): 7,
  (32, '5'): 7,
  (32, '6'): 7,
  (32, '7'): 7,
  (32, '8'): 7,
  (32, '9'): 7,
  (32, 'A'): 7,
  (32, 'B'): 7,
  (32, 'C'): 7,
  (32, 'D'): 7,
  (32, 'E'): 7,
  (32, 'F'): 7,
  (32, 'G'): 7,
  (32, 'H'): 7,
  (32, 'I'): 7,
  (32, 'J'): 7,
  (32, 'K'): 7,
  (32, 'L'): 7,
  (32, 'M'): 7,
  (32, 'N'): 7,
  (32, 'O'): 7,
  (32, 'P'): 7,
  (32, 'Q'): 7,
  (32, 'R'): 7,
  (32, 'S'): 7,
  (32, 'T'): 7,
  (32, 'U'): 7,
  (32, 'V'): 7,
  (32, 'W'): 7,
  (32, 'X'): 7,
  (32, 'Y'): 7,
  (32, 'Z'): 7,
  (32, '_'): 7,
  (32, 'a'): 7,
  (32, 'b'): 7,
  (32, 'c'): 7,
  (32, 'd'): 7,
  (32, 'e'): 7,
  (32, 'f'): 34,
  (32, 'g'): 7,
  (32, 'h'): 7,
  (32, 'i'): 7,
  (32, 'j'): 7,
  (32, 'k'): 7,
  (32, 'l'): 7,
  (32, 'm'): 7,
  (32, 'n'): 7,
  (32, 'o'): 7,
  (32, 'p'): 7,
  (32, 'q'): 7,
  (32, 'r'): 7,
  (32, 's'): 7,
  (32, 't'): 7,
  (32, 'u'): 7,
  (32, 'v'): 7,
  (32, 'w'): 7,
  (32, 'x'): 7,
  (32, 'y'): 7,
  (32, 'z'): 7,
  (34, '0'): 7,
  (34, '1'): 7,
  (34, '2'): 7,
  (34, '3'): 7,
  (34, '4'): 7,
  (34, '5'): 7,
  (34, '6'): 7,
  (34, '7'): 7,
  (34, '8'): 7,
  (34, '9'): 7,
  (34, 'A'): 7,
  (34, 'B'): 7,
  (34, 'C'): 7,
  (34, 'D'): 7,
  (34, 'E'): 7,
  (34, 'F'): 7,
  (34, 'G'): 7,
  (34, 'H'): 7,
  (34, 'I'): 7,
  (34, 'J'): 7,
  (34, 'K'): 7,
  (34, 'L'): 7,
  (34, 'M'): 7,
  (34, 'N'): 7,
  (34, 'O'): 7,
  (34, 'P'): 7,
  (34, 'Q'): 7,
  (34, 'R'): 7,
  (34, 'S'): 7,
  (34, 'T'): 7,
  (34, 'U'): 7,
  (34, 'V'): 7,
  (34, 'W'): 7,
  (34, 'X'): 7,
  (34, 'Y'): 7,
  (34, 'Z'): 7,
  (34, '_'): 7,
  (34, 'a'): 7,
  (34, 'b'): 7,
  (34, 'c'): 7,
  (34, 'd'): 7,
  (34, 'e'): 7,
  (34, 'f'): 7,
  (34, 'g'): 7,
  (34, 'h'): 7,
  (34, 'i'): 7,
  (34, 'j'): 7,
  (34, 'k'): 7,
  (34, 'l'): 7,
  (34, 'm'): 7,
  (34, 'n'): 7,
  (34, 'o'): 7,
  (34, 'p'): 7,
  (34, 'q'): 7,
  (34, 'r'): 7,
  (34, 's'): 7,
  (34, 't'): 7,
  (34, 'u'): 7,
  (34, 'v'): 7,
  (34, 'w'): 7,
  (34, 'x'): 7,
  (34, 'y'): 7,
  (34, 'z'): 7,
  (35, '0'): 7,
  (35, '1'): 7,
  (35, '2'): 7,
  (35, '3'): 7,
  (35, '4'): 7,
  (35, '5'): 7,
  (35, '6'): 7,
  (35, '7'): 7,
  (35, '8'): 7,
  (35, '9'): 7,
  (35, 'A'): 7,
  (35, 'B'): 7,
  (35, 'C'): 7,
  (35, 'D'): 7,
  (35, 'E'): 7,
  (35, 'F'): 7,
  (35, 'G'): 7,
  (35, 'H'): 7,
  (35, 'I'): 7,
  (35, 'J'): 7,
  (35, 'K'): 7,
  (35, 'L'): 7,
  (35, 'M'): 7,
  (35, 'N'): 7,
  (35, 'O'): 7,
  (35, 'P'): 7,
  (35, 'Q'): 7,
  (35, 'R'): 7,
  (35, 'S'): 7,
  (35, 'T'): 7,
  (35, 'U'): 7,
  (35, 'V'): 7,
  (35, 'W'): 7,
  (35, 'X'): 7,
  (35, 'Y'): 7,
  (35, 'Z'): 7,
  (35, '_'): 7,
  (35, 'a'): 7,
  (35, 'b'): 7,
  (35, 'c'): 7,
  (35, 'd'): 7,
  (35, 'e'): 7,
  (35, 'f'): 7,
  (35, 'g'): 7,
  (35, 'h'): 7,
  (35, 'i'): 7,
  (35, 'j'): 7,
  (35, 'k'): 7,
  (35, 'l'): 7,
  (35, 'm'): 7,
  (35, 'n'): 7,
  (35, 'o'): 7,
  (35, 'p'): 7,
  (35, 'q'): 7,
  (35, 'r'): 7,
  (35, 's'): 36,
  (35, 't'): 7,
  (35, 'u'): 7,
  (35, 'v'): 7,
  (35, 'w'): 7,
  (35, 'x'): 7,
  (35, 'y'): 7,
  (35, 'z'): 7,
  (36, '0'): 7,
  (36, '1'): 7,
  (36, '2'): 7,
  (36, '3'): 7,
  (36, '4'): 7,
  (36, '5'): 7,
  (36, '6'): 7,
  (36, '7'): 7,
  (36, '8'): 7,
  (36, '9'): 7,
  (36, 'A'): 7,
  (36, 'B'): 7,
  (36, 'C'): 7,
  (36, 'D'): 7,
  (36, 'E'): 7,
  (36, 'F'): 7,
  (36, 'G'): 7,
  (36, 'H'): 7,
  (36, 'I'): 7,
  (36, 'J'): 7,
  (36, 'K'): 7,
  (36, 'L'): 7,
  (36, 'M'): 7,
  (36, 'N'): 7,
  (36, 'O'): 7,
  (36, 'P'): 7,
  (36, 'Q'): 7,
  (36, 'R'): 7,
  (36, 'S'): 7,
  (36, 'T'): 7,
  (36, 'U'): 7,
  (36, 'V'): 7,
  (36, 'W'): 7,
  (36, 'X'): 7,
  (36, 'Y'): 7,
  (36, 'Z'): 7,
  (36, '_'): 7,
  (36, 'a'): 7,
  (36, 'b'): 7,
  (36, 'c'): 7,
  (36, 'd'): 7,
  (36, 'e'): 37,
  (36, 'f'): 7,
  (36, 'g'): 7,
  (36, 'h'): 7,
  (36, 'i'): 7,
  (36, 'j'): 7,
  (36, 'k'): 7,
  (36, 'l'): 7,
  (36, 'm'): 7,
  (36, 'n'): 7,
  (36, 'o'): 7,
  (36, 'p'): 7,
  (36, 'q'): 7,
  (36, 'r'): 7,
  (36, 's'): 7,
  (36, 't'): 7,
  (36, 'u'): 7,
  (36, 'v'): 7,
  (36, 'w'): 7,
  (36, 'x'): 7,
  (36, 'y'): 7,
  (36, 'z'): 7,
  (37, '0'): 7,
  (37, '1'): 7,
  (37, '2'): 7,
  (37, '3'): 7,
  (37, '4'): 7,
  (37, '5'): 7,
  (37, '6'): 7,
  (37, '7'): 7,
  (37, '8'): 7,
  (37, '9'): 7,
  (37, 'A'): 7,
  (37, 'B'): 7,
  (37, 'C'): 7,
  (37, 'D'): 7,
  (37, 'E'): 7,
  (37, 'F'): 7,
  (37, 'G'): 7,
  (37, 'H'): 7,
  (37, 'I'): 7,
  (37, 'J'): 7,
  (37, 'K'): 7,
  (37, 'L'): 7,
  (37, 'M'): 7,
  (37, 'N'): 7,
  (37, 'O'): 7,
  (37, 'P'): 7,
  (37, 'Q'): 7,
  (37, 'R'): 7,
  (37, 'S'): 7,
  (37, 'T'): 7,
  (37, 'U'): 7,
  (37, 'V'): 7,
  (37, 'W'): 7,
  (37, 'X'): 7,
  (37, 'Y'): 7,
  (37, 'Z'): 7,
  (37, '_'): 7,
  (37, 'a'): 7,
  (37, 'b'): 7,
  (37, 'c'): 7,
  (37, 'd'): 7,
  (37, 'e'): 7,
  (37, 'f'): 7,
  (37, 'g'): 7,
  (37, 'h'): 7,
  (37, 'i'): 7,
  (37, 'j'): 7,
  (37, 'k'): 7,
  (37, 'l'): 7,
  (37, 'm'): 7,
  (37, 'n'): 7,
  (37, 'o'): 7,
  (37, 'p'): 7,
  (37, 'q'): 7,
  (37, 'r'): 7,
  (37, 's'): 7,
  (37, 't'): 7,
  (37, 'u'): 7,
  (37, 'v'): 7,
  (37, 'w'): 7,
  (37, 'x'): 7,
  (37, 'y'): 7,
  (37, 'z'): 7,
  (38, '0'): 7,
  (38, '1'): 7,
  (38, '2'): 7,
  (38, '3'): 7,
  (38, '4'): 7,
  (38, '5'): 7,
  (38, '6'): 7,
  (38, '7'): 7,
  (38, '8'): 7,
  (38, '9'): 7,
  (38, 'A'): 7,
  (38, 'B'): 7,
  (38, 'C'): 7,
  (38, 'D'): 7,
  (38, 'E'): 7,
  (38, 'F'): 7,
  (38, 'G'): 7,
  (38, 'H'): 7,
  (38, 'I'): 7,
  (38, 'J'): 7,
  (38, 'K'): 7,
  (38, 'L'): 7,
  (38, 'M'): 7,
  (38, 'N'): 7,
  (38, 'O'): 7,
  (38, 'P'): 7,
  (38, 'Q'): 7,
  (38, 'R'): 7,
  (38, 'S'): 7,
  (38, 'T'): 7,
  (38, 'U'): 7,
  (38, 'V'): 7,
  (38, 'W'): 7,
  (38, 'X'): 7,
  (38, 'Y'): 7,
  (38, 'Z'): 7,
  (38, '_'): 7,
  (38, 'a'): 7,
  (38, 'b'): 7,
  (38, 'c'): 7,
  (38, 'd'): 39,
  (38, 'e'): 7,
  (38, 'f'): 7,
  (38, 'g'): 7,
  (38, 'h'): 7,
  (38, 'i'): 7,
  (38, 'j'): 7,
  (38, 'k'): 7,
  (38, 'l'): 7,
  (38, 'm'): 7,
  (38, 'n'): 7,
  (38, 'o'): 7,
  (38, 'p'): 7,
  (38, 'q'): 7,
  (38, 'r'): 7,
  (38, 's'): 7,
  (38, 't'): 7,
  (38, 'u'): 7,
  (38, 'v'): 7,
  (38, 'w'): 7,
  (38, 'x'): 7,
  (38, 'y'): 7,
  (38, 'z'): 7,
  (39, '0'): 7,
  (39, '1'): 7,
  (39, '2'): 7,
  (39, '3'): 7,
  (39, '4'): 7,
  (39, '5'): 7,
  (39, '6'): 7,
  (39, '7'): 7,
  (39, '8'): 7,
  (39, '9'): 7,
  (39, 'A'): 7,
  (39, 'B'): 7,
  (39, 'C'): 7,
  (39, 'D'): 7,
  (39, 'E'): 7,
  (39, 'F'): 7,
  (39, 'G'): 7,
  (39, 'H'): 7,
  (39, 'I'): 7,
  (39, 'J'): 7,
  (39, 'K'): 7,
  (39, 'L'): 7,
  (39, 'M'): 7,
  (39, 'N'): 7,
  (39, 'O'): 7,
  (39, 'P'): 7,
  (39, 'Q'): 7,
  (39, 'R'): 7,
  (39, 'S'): 7,
  (39, 'T'): 7,
  (39, 'U'): 7,
  (39, 'V'): 7,
  (39, 'W'): 7,
  (39, 'X'): 7,
  (39, 'Y'): 7,
  (39, 'Z'): 7,
  (39, '_'): 7,
  (39, 'a'): 7,
  (39, 'b'): 7,
  (39, 'c'): 7,
  (39, 'd'): 7,
  (39, 'e'): 7,
  (39, 'f'): 7,
  (39, 'g'): 7,
  (39, 'h'): 7,
  (39, 'i'): 7,
  (39, 'j'): 7,
  (39, 'k'): 7,
  (39, 'l'): 7,
  (39, 'm'): 7,
  (39, 'n'): 7,
  (39, 'o'): 7,
  (39, 'p'): 7,
  (39, 'q'): 7,
  (39, 'r'): 7,
  (39, 's'): 7,
  (39, 't'): 7,
  (39, 'u'): 7,
  (39, 'v'): 7,
  (39, 'w'): 7,
  (39, 'x'): 7,
  (39, 'y'): 7,
  (39, 'z'): 7,
  (42, '0'): 7,
  (42, '1'): 7,
  (42, '2'): 7,
  (42, '3'): 7,
  (42, '4'): 7,
  (42, '5'): 7,
  (42, '6'): 7,
  (42, '7'): 7,
  (42, '8'): 7,
  (42, '9'): 7,
  (42, 'A'): 7,
  (42, 'B'): 7,
  (42, 'C'): 7,
  (42, 'D'): 7,
  (42, 'E'): 7,
  (42, 'F'): 7,
  (42, 'G'): 7,
  (42, 'H'): 7,
  (42, 'I'): 7,
  (42, 'J'): 7,
  (42, 'K'): 7,
  (42, 'L'): 7,
  (42, 'M'): 7,
  (42, 'N'): 7,
  (42, 'O'): 7,
  (42, 'P'): 7,
  (42, 'Q'): 7,
  (42, 'R'): 7,
  (42, 'S'): 7,
  (42, 'T'): 7,
  (42, 'U'): 7,
  (42, 'V'): 7,
  (42, 'W'): 7,
  (42, 'X'): 7,
  (42, 'Y'): 7,
  (42, 'Z'): 7,
  (42, '_'): 7,
  (42, 'a'): 7,
  (42, 'b'): 7,
  (42, 'c'): 7,
  (42, 'd'): 7,
  (42, 'e'): 7,
  (42, 'f'): 7,
  (42, 'g'): 7,
  (42, 'h'): 7,
  (42, 'i'): 7,
  (42, 'j'): 7,
  (42, 'k'): 7,
  (42, 'l'): 7,
  (42, 'm'): 7,
  (42, 'n'): 7,
  (42, 'o'): 7,
  (42, 'p'): 7,
  (42, 'q'): 7,
  (42, 'r'): 43,
  (42, 's'): 7,
  (42, 't'): 7,
  (42, 'u'): 7,
  (42, 'v'): 7,
  (42, 'w'): 7,
  (42, 'x'): 7,
  (42, 'y'): 7,
  (42, 'z'): 7,
  (43, '0'): 7,
  (43, '1'): 7,
  (43, '2'): 7,
  (43, '3'): 7,
  (43, '4'): 7,
  (43, '5'): 7,
  (43, '6'): 7,
  (43, '7'): 7,
  (43, '8'): 7,
  (43, '9'): 7,
  (43, 'A'): 7,
  (43, 'B'): 7,
  (43, 'C'): 7,
  (43, 'D'): 7,
  (43, 'E'): 7,
  (43, 'F'): 7,
  (43, 'G'): 7,
  (43, 'H'): 7,
  (43, 'I'): 7,
  (43, 'J'): 7,
  (43, 'K'): 7,
  (43, 'L'): 7,
  (43, 'M'): 7,
  (43, 'N'): 7,
  (43, 'O'): 7,
  (43, 'P'): 7,
  (43, 'Q'): 7,
  (43, 'R'): 7,
  (43, 'S'): 7,
  (43, 'T'): 7,
  (43, 'U'): 7,
  (43, 'V'): 7,
  (43, 'W'): 7,
  (43, 'X'): 7,
  (43, 'Y'): 7,
  (43, 'Z'): 7,
  (43, '_'): 7,
  (43, 'a'): 7,
  (43, 'b'): 7,
  (43, 'c'): 7,
  (43, 'd'): 7,
  (43, 'e'): 7,
  (43, 'f'): 7,
  (43, 'g'): 7,
  (43, 'h'): 7,
  (43, 'i'): 7,
  (43, 'j'): 7,
  (43, 'k'): 7,
  (43, 'l'): 7,
  (43, 'm'): 7,
  (43, 'n'): 7,
  (43, 'o'): 7,
  (43, 'p'): 7,
  (43, 'q'): 7,
  (43, 'r'): 7,
  (43, 's'): 7,
  (43, 't'): 7,
  (43, 'u'): 7,
  (43, 'v'): 7,
  (43, 'w'): 7,
  (43, 'x'): 7,
  (43, 'y'): 7,
  (43, 'z'): 7,
  (44, '0'): 7,
  (44, '1'): 7,
  (44, '2'): 7,
  (44, '3'): 7,
  (44, '4'): 7,
  (44, '5'): 7,
  (44, '6'): 7,
  (44, '7'): 7,
  (44, '8'): 7,
  (44, '9'): 7,
  (44, 'A'): 7,
  (44, 'B'): 7,
  (44, 'C'): 7,
  (44, 'D'): 7,
  (44, 'E'): 7,
  (44, 'F'): 7,
  (44, 'G'): 7,
  (44, 'H'): 7,
  (44, 'I'): 7,
  (44, 'J'): 7,
  (44, 'K'): 7,
  (44, 'L'): 7,
  (44, 'M'): 7,
  (44, 'N'): 7,
  (44, 'O'): 7,
  (44, 'P'): 7,
  (44, 'Q'): 7,
  (44, 'R'): 7,
  (44, 'S'): 7,
  (44, 'T'): 7,
  (44, 'U'): 7,
  (44, 'V'): 7,
  (44, 'W'): 7,
  (44, 'X'): 7,
  (44, 'Y'): 7,
  (44, 'Z'): 7,
  (44, '_'): 7,
  (44, 'a'): 7,
  (44, 'b'): 7,
  (44, 'c'): 7,
  (44, 'd'): 7,
  (44, 'e'): 7,
  (44, 'f'): 7,
  (44, 'g'): 7,
  (44, 'h'): 7,
  (44, 'i'): 7,
  (44, 'j'): 7,
  (44, 'k'): 7,
  (44, 'l'): 45,
  (44, 'm'): 7,
  (44, 'n'): 7,
  (44, 'o'): 7,
  (44, 'p'): 7,
  (44, 'q'): 7,
  (44, 'r'): 7,
  (44, 's'): 7,
  (44, 't'): 7,
  (44, 'u'): 7,
  (44, 'v'): 7,
  (44, 'w'): 7,
  (44, 'x'): 7,
  (44, 'y'): 7,
  (44, 'z'): 7,
  (45, '0'): 7,
  (45, '1'): 7,
  (45, '2'): 7,
  (45, '3'): 7,
  (45, '4'): 7,
  (45, '5'): 7,
  (45, '6'): 7,
  (45, '7'): 7,
  (45, '8'): 7,
  (45, '9'): 7,
  (45, 'A'): 7,
  (45, 'B'): 7,
  (45, 'C'): 7,
  (45, 'D'): 7,
  (45, 'E'): 7,
  (45, 'F'): 7,
  (45, 'G'): 7,
  (45, 'H'): 7,
  (45, 'I'): 7,
  (45, 'J'): 7,
  (45, 'K'): 7,
  (45, 'L'): 7,
  (45, 'M'): 7,
  (45, 'N'): 7,
  (45, 'O'): 7,
  (45, 'P'): 7,
  (45, 'Q'): 7,
  (45, 'R'): 7,
  (45, 'S'): 7,
  (45, 'T'): 7,
  (45, 'U'): 7,
  (45, 'V'): 7,
  (45, 'W'): 7,
  (45, 'X'): 7,
  (45, 'Y'): 7,
  (45, 'Z'): 7,
  (45, '_'): 7,
  (45, 'a'): 7,
  (45, 'b'): 7,
  (45, 'c'): 7,
  (45, 'd'): 7,
  (45, 'e'): 7,
  (45, 'f'): 7,
  (45, 'g'): 7,
  (45, 'h'): 7,
  (45, 'i'): 7,
  (45, 'j'): 7,
  (45, 'k'): 7,
  (45, 'l'): 7,
  (45, 'm'): 7,
  (45, 'n'): 7,
  (45, 'o'): 7,
  (45, 'p'): 7,
  (45, 'q'): 7,
  (45, 'r'): 7,
  (45, 's'): 46,
  (45, 't'): 7,
  (45, 'u'): 7,
  (45, 'v'): 7,
  (45, 'w'): 7,
  (45, 'x'): 7,
  (45, 'y'): 7,
  (45, 'z'): 7,
  (46, '0'): 7,
  (46, '1'): 7,
  (46, '2'): 7,
  (46, '3'): 7,
  (46, '4'): 7,
  (46, '5'): 7,
  (46, '6'): 7,
  (46, '7'): 7,
  (46, '8'): 7,
  (46, '9'): 7,
  (46, 'A'): 7,
  (46, 'B'): 7,
  (46, 'C'): 7,
  (46, 'D'): 7,
  (46, 'E'): 7,
  (46, 'F'): 7,
  (46, 'G'): 7,
  (46, 'H'): 7,
  (46, 'I'): 7,
  (46, 'J'): 7,
  (46, 'K'): 7,
  (46, 'L'): 7,
  (46, 'M'): 7,
  (46, 'N'): 7,
  (46, 'O'): 7,
  (46, 'P'): 7,
  (46, 'Q'): 7,
  (46, 'R'): 7,
  (46, 'S'): 7,
  (46, 'T'): 7,
  (46, 'U'): 7,
  (46, 'V'): 7,
  (46, 'W'): 7,
  (46, 'X'): 7,
  (46, 'Y'): 7,
  (46, 'Z'): 7,
  (46, '_'): 7,
  (46, 'a'): 7,
  (46, 'b'): 7,
  (46, 'c'): 7,
  (46, 'd'): 7,
  (46, 'e'): 47,
  (46, 'f'): 7,
  (46, 'g'): 7,
  (46, 'h'): 7,
  (46, 'i'): 7,
  (46, 'j'): 7,
  (46, 'k'): 7,
  (46, 'l'): 7,
  (46, 'm'): 7,
  (46, 'n'): 7,
  (46, 'o'): 7,
  (46, 'p'): 7,
  (46, 'q'): 7,
  (46, 'r'): 7,
  (46, 's'): 7,
  (46, 't'): 7,
  (46, 'u'): 7,
  (46, 'v'): 7,
  (46, 'w'): 7,
  (46, 'x'): 7,
  (46, 'y'): 7,
  (46, 'z'): 7,
  (47, '0'): 7,
  (47, '1'): 7,
  (47, '2'): 7,
  (47, '3'): 7,
  (47, '4'): 7,
  (47, '5'): 7,
  (47, '6'): 7,
  (47, '7'): 7,
  (47, '8'): 7,
  (47, '9'): 7,
  (47, 'A'): 7,
  (47, 'B'): 7,
  (47, 'C'): 7,
  (47, 'D'): 7,
  (47, 'E'): 7,
  (47, 'F'): 7,
  (47, 'G'): 7,
  (47, 'H'): 7,
  (47, 'I'): 7,
  (47, 'J'): 7,
  (47, 'K'): 7,
  (47, 'L'): 7,
  (47, 'M'): 7,
  (47, 'N'): 7,
  (47, 'O'): 7,
  (47, 'P'): 7,
  (47, 'Q'): 7,
  (47, 'R'): 7,
  (47, 'S'): 7,
  (47, 'T'): 7,
  (47, 'U'): 7,
  (47, 'V'): 7,
  (47, 'W'): 7,
  (47, 'X'): 7,
  (47, 'Y'): 7,
  (47, 'Z'): 7,
  (47, '_'): 7,
  (47, 'a'): 7,
  (47, 'b'): 7,
  (47, 'c'): 7,
  (47, 'd'): 7,
  (47, 'e'): 7,
  (47, 'f'): 7,
  (47, 'g'): 7,
  (47, 'h'): 7,
  (47, 'i'): 7,
  (47, 'j'): 7,
  (47, 'k'): 7,
  (47, 'l'): 7,
  (47, 'm'): 7,
  (47, 'n'): 7,
  (47, 'o'): 7,
  (47, 'p'): 7,
  (47, 'q'): 7,
  (47, 'r'): 7,
  (47, 's'): 7,
  (47, 't'): 7,
  (47, 'u'): 7,
  (47, 'v'): 7,
  (47, 'w'): 7,
  (47, 'x'): 7,
  (47, 'y'): 7,
  (47, 'z'): 7,
  (49, '0'): 7,
  (49, '1'): 7,
  (49, '2'): 7,
  (49, '3'): 7,
  (49, '4'): 7,
  (49, '5'): 7,
  (49, '6'): 7,
  (49, '7'): 7,
  (49, '8'): 7,
  (49, '9'): 7,
  (49, 'A'): 7,
  (49, 'B'): 7,
  (49, 'C'): 7,
  (49, 'D'): 7,
  (49, 'E'): 7,
  (49, 'F'): 7,
  (49, 'G'): 7,
  (49, 'H'): 7,
  (49, 'I'): 7,
  (49, 'J'): 7,
  (49, 'K'): 7,
  (49, 'L'): 7,
  (49, 'M'): 7,
  (49, 'N'): 7,
  (49, 'O'): 7,
  (49, 'P'): 7,
  (49, 'Q'): 7,
  (49, 'R'): 7,
  (49, 'S'): 7,
  (49, 'T'): 7,
  (49, 'U'): 7,
  (49, 'V'): 7,
  (49, 'W'): 7,
  (49, 'X'): 7,
  (49, 'Y'): 7,
  (49, 'Z'): 7,
  (49, '_'): 7,
  (49, 'a'): 7,
  (49, 'b'): 7,
  (49, 'c'): 7,
  (49, 'd'): 7,
  (49, 'e'): 7,
  (49, 'f'): 7,
  (49, 'g'): 7,
  (49, 'h'): 7,
  (49, 'i'): 50,
  (49, 'j'): 7,
  (49, 'k'): 7,
  (49, 'l'): 7,
  (49, 'm'): 7,
  (49, 'n'): 7,
  (49, 'o'): 7,
  (49, 'p'): 7,
  (49, 'q'): 7,
  (49, 'r'): 7,
  (49, 's'): 7,
  (49, 't'): 7,
  (49, 'u'): 7,
  (49, 'v'): 7,
  (49, 'w'): 7,
  (49, 'x'): 7,
  (49, 'y'): 7,
  (49, 'z'): 7,
  (50, '0'): 7,
  (50, '1'): 7,
  (50, '2'): 7,
  (50, '3'): 7,
  (50, '4'): 7,
  (50, '5'): 7,
  (50, '6'): 7,
  (50, '7'): 7,
  (50, '8'): 7,
  (50, '9'): 7,
  (50, 'A'): 7,
  (50, 'B'): 7,
  (50, 'C'): 7,
  (50, 'D'): 7,
  (50, 'E'): 7,
  (50, 'F'): 7,
  (50, 'G'): 7,
  (50, 'H'): 7,
  (50, 'I'): 7,
  (50, 'J'): 7,
  (50, 'K'): 7,
  (50, 'L'): 7,
  (50, 'M'): 7,
  (50, 'N'): 7,
  (50, 'O'): 7,
  (50, 'P'): 7,
  (50, 'Q'): 7,
  (50, 'R'): 7,
  (50, 'S'): 7,
  (50, 'T'): 7,
  (50, 'U'): 7,
  (50, 'V'): 7,
  (50, 'W'): 7,
  (50, 'X'): 7,
  (50, 'Y'): 7,
  (50, 'Z'): 7,
  (50, '_'): 7,
  (50, 'a'): 7,
  (50, 'b'): 7,
  (50, 'c'): 7,
  (50, 'd'): 7,
  (50, 'e'): 7,
  (50, 'f'): 7,
  (50, 'g'): 7,
  (50, 'h'): 7,
  (50, 'i'): 7,
  (50, 'j'): 7,
  (50, 'k'): 7,
  (50, 'l'): 51,
  (50, 'm'): 7,
  (50, 'n'): 7,
  (50, 'o'): 7,
  (50, 'p'): 7,
  (50, 'q'): 7,
  (50, 'r'): 7,
  (50, 's'): 7,
  (50, 't'): 7,
  (50, 'u'): 7,
  (50, 'v'): 7,
  (50, 'w'): 7,
  (50, 'x'): 7,
  (50, 'y'): 7,
  (50, 'z'): 7,
  (51, '0'): 7,
  (51, '1'): 7,
  (51, '2'): 7,
  (51, '3'): 7,
  (51, '4'): 7,
  (51, '5'): 7,
  (51, '6'): 7,
  (51, '7'): 7,
  (51, '8'): 7,
  (51, '9'): 7,
  (51, 'A'): 7,
  (51, 'B'): 7,
  (51, 'C'): 7,
  (51, 'D'): 7,
  (51, 'E'): 7,
  (51, 'F'): 7,
  (51, 'G'): 7,
  (51, 'H'): 7,
  (51, 'I'): 7,
  (51, 'J'): 7,
  (51, 'K'): 7,
  (51, 'L'): 7,
  (51, 'M'): 7,
  (51, 'N'): 7,
  (51, 'O'): 7,
  (51, 'P'): 7,
  (51, 'Q'): 7,
  (51, 'R'): 7,
  (51, 'S'): 7,
  (51, 'T'): 7,
  (51, 'U'): 7,
  (51, 'V'): 7,
  (51, 'W'): 7,
  (51, 'X'): 7,
  (51, 'Y'): 7,
  (51, 'Z'): 7,
  (51, '_'): 7,
  (51, 'a'): 7,
  (51, 'b'): 7,
  (51, 'c'): 7,
  (51, 'd'): 7,
  (51, 'e'): 52,
  (51, 'f'): 7,
  (51, 'g'): 7,
  (51, 'h'): 7,
  (51, 'i'): 7,
  (51, 'j'): 7,
  (51, 'k'): 7,
  (51, 'l'): 7,
  (51, 'm'): 7,
  (51, 'n'): 7,
  (51, 'o'): 7,
  (51, 'p'): 7,
  (51, 'q'): 7,
  (51, 'r'): 7,
  (51, 's'): 7,
  (51, 't'): 7,
  (51, 'u'): 7,
  (51, 'v'): 7,
  (51, 'w'): 7,
  (51, 'x'): 7,
  (51, 'y'): 7,
  (51, 'z'): 7,
  (52, '0'): 7,
  (52, '1'): 7,
  (52, '2'): 7,
  (52, '3'): 7,
  (52, '4'): 7,
  (52, '5'): 7,
  (52, '6'): 7,
  (52, '7'): 7,
  (52, '8'): 7,
  (52, '9'): 7,
  (52, 'A'): 7,
  (52, 'B'): 7,
  (52, 'C'): 7,
  (52, 'D'): 7,
  (52, 'E'): 7,
  (52, 'F'): 7,
  (52, 'G'): 7,
  (52, 'H'): 7,
  (52, 'I'): 7,
  (52, 'J'): 7,
  (52, 'K'): 7,
  (52, 'L'): 7,
  (52, 'M'): 7,
  (52, 'N'): 7,
  (52, 'O'): 7,
  (52, 'P'): 7,
  (52, 'Q'): 7,
  (52, 'R'): 7,
  (52, 'S'): 7,
  (52, 'T'): 7,
  (52, 'U'): 7,
  (52, 'V'): 7,
  (52, 'W'): 7,
  (52, 'X'): 7,
  (52, 'Y'): 7,
  (52, 'Z'): 7,
  (52, '_'): 7,
  (52, 'a'): 7,
  (52, 'b'): 7,
  (52, 'c'): 7,
  (52, 'd'): 7,
  (52, 'e'): 7,
  (52, 'f'): 7,
  (52, 'g'): 7,
  (52, 'h'): 7,
  (52, 'i'): 7,
  (52, 'j'): 7,
  (52, 'k'): 7,
  (52, 'l'): 7,
  (52, 'm'): 7,
  (52, 'n'): 7,
  (52, 'o'): 7,
  (52, 'p'): 7,
  (52, 'q'): 7,
  (52, 'r'): 7,
  (52, 's'): 7,
  (52, 't'): 7,
  (52, 'u'): 7,
  (52, 'v'): 7,
  (52, 'w'): 7,
  (52, 'x'): 7,
  (52, 'y'): 7,
  (52, 'z'): 7,
  (53, '0'): 7,
  (53, '1'): 7,
  (53, '2'): 7,
  (53, '3'): 7,
  (53, '4'): 7,
  (53, '5'): 7,
  (53, '6'): 7,
  (53, '7'): 7,
  (53, '8'): 7,
  (53, '9'): 7,
  (53, 'A'): 7,
  (53, 'B'): 7,
  (53, 'C'): 7,
  (53, 'D'): 7,
  (53, 'E'): 7,
  (53, 'F'): 7,
  (53, 'G'): 7,
  (53, 'H'): 7,
  (53, 'I'): 7,
  (53, 'J'): 7,
  (53, 'K'): 7,
  (53, 'L'): 7,
  (53, 'M'): 7,
  (53, 'N'): 7,
  (53, 'O'): 7,
  (53, 'P'): 7,
  (53, 'Q'): 7,
  (53, 'R'): 7,
  (53, 'S'): 7,
  (53, 'T'): 7,
  (53, 'U'): 7,
  (53, 'V'): 7,
  (53, 'W'): 7,
  (53, 'X'): 7,
  (53, 'Y'): 7,
  (53, 'Z'): 7,
  (53, '_'): 7,
  (53, 'a'): 7,
  (53, 'b'): 7,
  (53, 'c'): 7,
  (53, 'd'): 7,
  (53, 'e'): 7,
  (53, 'f'): 7,
  (53, 'g'): 7,
  (53, 'h'): 7,
  (53, 'i'): 7,
  (53, 'j'): 7,
  (53, 'k'): 7,
  (53, 'l'): 7,
  (53, 'm'): 7,
  (53, 'n'): 7,
  (53, 'o'): 7,
  (53, 'p'): 7,
  (53, 'q'): 7,
  (53, 'r'): 7,
  (53, 's'): 7,
  (53, 't'): 7,
  (53, 'u'): 7,
  (53, 'v'): 7,
  (53, 'w'): 7,
  (53, 'x'): 7,
  (53, 'y'): 7,
  (53, 'z'): 7,
  (54, '0'): 7,
  (54, '1'): 7,
  (54, '2'): 7,
  (54, '3'): 7,
  (54, '4'): 7,
  (54, '5'): 7,
  (54, '6'): 7,
  (54, '7'): 7,
  (54, '8'): 7,
  (54, '9'): 7,
  (54, 'A'): 7,
  (54, 'B'): 7,
  (54, 'C'): 7,
  (54, 'D'): 7,
  (54, 'E'): 7,
  (54, 'F'): 7,
  (54, 'G'): 7,
  (54, 'H'): 7,
  (54, 'I'): 7,
  (54, 'J'): 7,
  (54, 'K'): 7,
  (54, 'L'): 7,
  (54, 'M'): 7,
  (54, 'N'): 7,
  (54, 'O'): 7,
  (54, 'P'): 7,
  (54, 'Q'): 7,
  (54, 'R'): 7,
  (54, 'S'): 7,
  (54, 'T'): 7,
  (54, 'U'): 7,
  (54, 'V'): 7,
  (54, 'W'): 7,
  (54, 'X'): 7,
  (54, 'Y'): 7,
  (54, 'Z'): 7,
  (54, '_'): 7,
  (54, 'a'): 7,
  (54, 'b'): 7,
  (54, 'c'): 7,
  (54, 'd'): 7,
  (54, 'e'): 7,
  (54, 'f'): 7,
  (54, 'g'): 7,
  (54, 'h'): 7,
  (54, 'i'): 7,
  (54, 'j'): 7,
  (54, 'k'): 7,
  (54, 'l'): 7,
  (54, 'm'): 7,
  (54, 'n'): 7,
  (54, 'o'): 7,
  (54, 'p'): 7,
  (54, 'q'): 7,
  (54, 'r'): 7,
  (54, 's'): 7,
  (54, 't'): 7,
  (54, 'u'): 55,
  (54, 'v'): 7,
  (54, 'w'): 7,
  (54, 'x'): 7,
  (54, 'y'): 7,
  (54, 'z'): 7,
  (55, '0'): 7,
  (55, '1'): 7,
  (55, '2'): 7,
  (55, '3'): 7,
  (55, '4'): 7,
  (55, '5'): 7,
  (55, '6'): 7,
  (55, '7'): 7,
  (55, '8'): 7,
  (55, '9'): 7,
  (55, 'A'): 7,
  (55, 'B'): 7,
  (55, 'C'): 7,
  (55, 'D'): 7,
  (55, 'E'): 7,
  (55, 'F'): 7,
  (55, 'G'): 7,
  (55, 'H'): 7,
  (55, 'I'): 7,
  (55, 'J'): 7,
  (55, 'K'): 7,
  (55, 'L'): 7,
  (55, 'M'): 7,
  (55, 'N'): 7,
  (55, 'O'): 7,
  (55, 'P'): 7,
  (55, 'Q'): 7,
  (55, 'R'): 7,
  (55, 'S'): 7,
  (55, 'T'): 7,
  (55, 'U'): 7,
  (55, 'V'): 7,
  (55, 'W'): 7,
  (55, 'X'): 7,
  (55, 'Y'): 7,
  (55, 'Z'): 7,
  (55, '_'): 7,
  (55, 'a'): 7,
  (55, 'b'): 7,
  (55, 'c'): 7,
  (55, 'd'): 7,
  (55, 'e'): 56,
  (55, 'f'): 7,
  (55, 'g'): 7,
  (55, 'h'): 7,
  (55, 'i'): 7,
  (55, 'j'): 7,
  (55, 'k'): 7,
  (55, 'l'): 7,
  (55, 'm'): 7,
  (55, 'n'): 7,
  (55, 'o'): 7,
  (55, 'p'): 7,
  (55, 'q'): 7,
  (55, 'r'): 7,
  (55, 's'): 7,
  (55, 't'): 7,
  (55, 'u'): 7,
  (55, 'v'): 7,
  (55, 'w'): 7,
  (55, 'x'): 7,
  (55, 'y'): 7,
  (55, 'z'): 7,
  (56, '0'): 7,
  (56, '1'): 7,
  (56, '2'): 7,
  (56, '3'): 7,
  (56, '4'): 7,
  (56, '5'): 7,
  (56, '6'): 7,
  (56, '7'): 7,
  (56, '8'): 7,
  (56, '9'): 7,
  (56, 'A'): 7,
  (56, 'B'): 7,
  (56, 'C'): 7,
  (56, 'D'): 7,
  (56, 'E'): 7,
  (56, 'F'): 7,
  (56, 'G'): 7,
  (56, 'H'): 7,
  (56, 'I'): 7,
  (56, 'J'): 7,
  (56, 'K'): 7,
  (56, 'L'): 7,
  (56, 'M'): 7,
  (56, 'N'): 7,
  (56, 'O'): 7,
  (56, 'P'): 7,
  (56, 'Q'): 7,
  (56, 'R'): 7,
  (56, 'S'): 7,
  (56, 'T'): 7,
  (56, 'U'): 7,
  (56, 'V'): 7,
  (56, 'W'): 7,
  (56, 'X'): 7,
  (56, 'Y'): 7,
  (56, 'Z'): 7,
  (56, '_'): 7,
  (56, 'a'): 7,
  (56, 'b'): 7,
  (56, 'c'): 7,
  (56, 'd'): 7,
  (56, 'e'): 7,
  (56, 'f'): 7,
  (56, 'g'): 7,
  (56, 'h'): 7,
  (56, 'i'): 7,
  (56, 'j'): 7,
  (56, 'k'): 7,
  (56, 'l'): 7,
  (56, 'm'): 7,
  (56, 'n'): 7,
  (56, 'o'): 7,
  (56, 'p'): 7,
  (56, 'q'): 7,
  (56, 'r'): 7,
  (56, 's'): 7,
  (56, 't'): 7,
  (56, 'u'): 7,
  (56, 'v'): 7,
  (56, 'w'): 7,
  (56, 'x'): 7,
  (56, 'y'): 7,
  (56, 'z'): 7},
 set([1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      30,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57]),
 set([1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      30,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57]),
 ['0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, start|, 0, 0, 0, 0, 0, start|, 0, start|, 0, 0, 0',
  'IGNORE',
  'PAREN_OPEN',
  'COMMA',
  'DECIMAL',
  'DECIMAL',
  'LESS_THAN',
  'IDENTIFIER',
  'IDENTIFIER',
  'PLUS',
  'BACKSLASH',
  'SEMICOLON',
  'SQUARE_OPEN',
  'IDENTIFIER',
  'IDENTIFIER',
  'CURL_OPEN',
  'IGNORE',
  'STAR',
  'DOT',
  'GREATER_THAN',
  'CAP',
  'IDENTIFIER',
  'IDENTIFIER',
  'IGNORE',
  'IGNORE',
  'NOT',
  'PAREN_CLOSE',
  'MINUS',
  'EQUAL',
  'SQUARE_CLOSE',
  'IDENTIFIER',
  'IDENTIFIER',
  'IDENTIFIER',
  'CURL_CLOSE',
  'IF',
  'IDENTIFIER',
  'IDENTIFIER',
  'ELSE',
  'IDENTIFIER',
  'AND',
  'EQUAL_EQUAL',
  'NOT_EQUAL',
  'IDENTIFIER',
  'VAR',
  'IDENTIFIER',
  'IDENTIFIER',
  'IDENTIFIER',
  'FALSE',
  'GT_EQ',
  'IDENTIFIER',
  'IDENTIFIER',
  'IDENTIFIER',
  'WHILE',
  'OR',
  'IDENTIFIER',
  'IDENTIFIER',
  'TRUE',
  'LT_EQ']), {'IGNORE': None})
# generated code between this line and its other occurence
