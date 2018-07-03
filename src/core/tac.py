from strtbl import get_string, register_string
from display import *

class Atom(object):

    def __init__(self):
        self.name = 'Atom'

    # The set of reaching definitions 
    # given as one argument, the 
    # return value will be either 
    # a constant value,
    # or None if the atom can not be
    # evaluated due to multiple
    # reaching definitions
    def fold_constants(self, inset):
        print "Override this"

    # The set of reaching definitions
    # given as the argument.
    # The return value will be the
    # replaced expression if possible,
    # otherwise the expression itself
    def propagate_copy(self, inset):
        print "Override this"

class Var(Atom):

    def __init__(self, sid):
        self.name = 'AtomVar'
        self.sid = sid

    def __repr__(self):
        return get_string(self.sid)

    def nocolor(self):
        return str(self)

    def find_only_definition(self, inset):
        assert isinstance(inset, set)
        i = 0
        res = None
        for expr in inset:
            lhs = expr.lhs
            if lhs.sid == self.sid:
                if i > 0:
                    res = None
                    break
                i = i + 1
                res  = expr.rhs
        return res

    def fold_constants(self, inset):
        res = self.find_only_definition(inset)
        if res is not None and isinstance(res, Const):
            print "Found only def of (", self, ") at (", res, ")"
            return res.value
        return None

    # The set of reaching definitions
    # given as the argument.
    # The return value will be the
    # replaced variable if possible,
    # otherwise the variable itself
    def propagate_copy(self, inset):
        res = self.find_only_definition(inset)
        if res is not None:
            if isinstance(res, Var): # The only definition is of the form x = y
                v = res.find_only_definition(inset) # Try to find the only definition of y
                if v is not None: # y is only defined once, hence return directly
                    return res
        return self

class Const(Atom):

    def __init__(self, value):
        self.name = 'AtomConst'
        self.value = value

    def __repr__(self):
        return str(self.value)

    def nocolor(self):
        return str(self)

    def fold_constants(self, inset):
        return self.value

    def propagate_copy(self, inset):
        return self

class AtomicOp(Atom):

    def __init__(self):
        self.name = 'AtomicOp'

def func_not(val):
    return not val

def func_neg(val):
    return -val

class UnOp(AtomicOp):

    def __init__(self, right, op):
        self.name = 'AtomicOp' + str(op)
        self.right = right
        self.op = op
        self.function = {'!' : func_not,
                         '-' : func_neg}

    def __repr__(self):
        return sbold(str(self.op)) + ' ' + str(self.right)

    def nocolor(self):
        return str(self.op) + ' ' + self.right.nocolor()

    def fold_constants(self, inset):
        val = self.right.fold_constants()
        if val is not None:
            return self.function[self.op](val)
        return None

    def propagate_copy(self, inset):
        if isinstance(self.right, Var):
            self.right = self.right.propagate_copy(inset)
        return self

def func_gt(x, y):
    return x > y

def func_gte(x, y):
    return x >= y

def func_lt(x, y):
    return x < y

def func_lte(x, y):
    return x <= y

def func_eq(x, y):
    return x == y

def func_ne(x, y):
    return x != y

def func_add(x, y):
    return x + y

def func_sub(x, y):
    return x - y

def func_mul(x, y):
    return x * y

def func_div(x, y):
    return x / y

def func_pow(x, y):
    return x ** y

def func_and(x, y):
    return x and y

def func_or(x, y):
    return x or y

class BinOp(AtomicOp):

    def __init__(self, left, right, op):
        self.name = 'AtomicOp' + str(op)
        self.left = left
        self.right = right
        self.op = op
        self.function = {'>' : func_gt,
                         '>=' : func_gte,
                         '<' : func_lt,
                         '<=' : func_lte,
                         '==' : func_eq,
                         '!=' : func_ne,
                         '+' : func_add,
                         '-' : func_sub,
                         '*' : func_mul,
                         '/' : func_div,
                         '^' : func_pow,
                         'and' : func_and,
                         'or' : func_or}

    def __repr__(self):
        return str(self.left) + ' ' + cmgn(str(self.op)) + ' ' + str(self.right)

    def nocolor(self):
        return self.left.nocolor() + ' ' + str(self.op) + ' ' + self.right.nocolor()

    def fold_constants(self, inset):
        lval = self.left.fold_constants(inset)
        rval = self.right.fold_constants(inset)
        if lval is not None and rval is not None:
            return self.function[self.op](lval, rval)
        return None

    def propagate_copy(self, inset):
        if isinstance(self.left, Var):
            self.left = self.left.propagate_copy(inset)
        if isinstance(self.right, Var):
            self.right = self.right.propagate_copy(inset)
        return self

class Tac(object):

    def __init__(self):
        # A tac with everything set
        # to none represents end of
        # statements

        # A dictionary of the labels
        # and the corresponding
        # jump instructions to this
        # tac.
        # Each item has the form
        # targetof[ins] = somelabel
        # to later retrieve labels
        # using the parent
        self.targetof = {}
        # If this instruction is
        # a conditional jump, then
        # this variable contains its
        # destination when the condition
        # is true.
        # An unconditional jump
        # instruction has all
        # variables unset except
        # this one.
        self.destination = None
        # The instruction which represents
        # the destination.
        self.destination_ins = None
        # If this instruction is a
        # conditional jump, then this
        # variable contains its destination
        # when the condition is false
        self.else_destination = None
        # Instruction containing the
        # else destination
        self.else_destination_ins = None
        # Left hand side of the
        # instruction.
        # If it is a conditional
        # jump, then it is set to
        # None.
        self.lhs = None
        # Right hand side of the
        # instruction.
        # If it is a conditional
        # jump, then it is set to
        # the condition.
        self.rhs = None

    def __repr__(self):
        s = ''
        i = 0
        for target in self.targetof:
            if i > 0:
                s = s + ', '
            s = s + cblue(self.targetof[target])
            i = i + 1
        if i > 0:
            s = s + ': '
        if self.destination is None and self.lhs is None and self.rhs is None: #end
            s = s + ' end'
        elif self.rhs is None: # unconditonal jump
            s = s + cgrn('goto ') + cblue(self.destination)
        elif self.lhs is None: # conditional jump
            s = s + cylw('if ') + str(self.rhs) + cgrn(' goto ') + cblue(self.destination)
            s = s + cred(' else') + cgrn(' goto ') + cblue(self.else_destination)
        else: # usual assignment
            s = s + str(self.lhs) + sbold(' = ') + str(self.rhs)

        return s

    def nocolor(self):
        s = ''
        #i = 0
        #for target in self.targetof:
        #    if i > 0:
        #        s = s + ', '
        #    s = s + self.targetof[target]
        #    i = i + 1
        #if i > 0:
        #    s = s + ': '
        if self.destination is None and self.lhs is None and self.rhs is None: #end
            s = s + ' end'
        elif self.rhs is None: # unconditonal jump
            s = s + 'goto ' + self.destination
        elif self.lhs is None: # conditional jump
            s = s + 'if ' + self.rhs.nocolor() + ' goto ' + self.destination
            s = s + ' else goto ' + self.else_destination
        else: # usual assignment
            s = s + self.lhs.nocolor() + ' = ' + self.rhs.nocolor()

        return s

    def is_branch(self):
        if self.rhs is None: # unconditional jump
            return True
        elif self.lhs is None: # conditional jump
            return True
        return False

    # Tries to fold the constants in the instructions
    # and updates the instruction if necessary
    def fold_constants(self, inset):
        if self.lhs is not None: # assignment
            val = self.rhs.fold_constants(inset)
            if val is not None:
                self.rhs = Const(val)
        elif self.rhs is not None: # conditional jump
            val = self.rhs.fold_constants(inset)
            if val is not None:
                if val is True: # condition is always true
                    self.rhs = None # make it unconditional
                elif val is False: # condition is always false
                    self.destination = self.else_destination # Make the else block as the destination
                    self.destination_ins = self.else_destination_ins
                    self.rhs = None # make it unconditional

    def propagate_copy(self, inset):
        if self.rhs is not None:
            self.rhs = self.rhs.propagate_copy(inset)