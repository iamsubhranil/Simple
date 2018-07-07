from strtbl import get_string, register_string
from display import *

class Atom(object):

    def __init__(self):
        self.name = 'Atom'
        # A cache of the last
        # reached definition
        # to the object.
        # If it matches to the
        # given inreachset, then
        # the cached result
        # is returned
        self.last_reached_def = None
        # All the cache objects here
        # are initialized with unique
        # values which they can never
        # take in their lifetime
        # to denote that they
        # have not even been initialized

        # A dictionary mapping loop id
        # to variance
        # An expression which is
        # declared to be variant
        # in a loop cannot be invariant,
        # however the reverse is not
        # true
        self.last_loop_variancy = {}
        self.last_constant = None
        self.last_expression = 0

    def reset_cache(self, inreachset):
        self.last_reached_def = inreachset
        self.last_loop_variancy = {}
        self.last_constant = None
        self.last_expression = 0

    # The set of reaching definitions 
    # given as one argument, the 
    # return value will be either 
    # a constant value,
    # or None if the atom can not be
    # evaluated due to multiple
    # reaching definitions
    def fold_constants(self, inset):
        found = True
        if self.last_reached_def != inset or self.last_constant == None:
            found = False
            self.reset_cache(inset)
        return self.last_constant, found

    # The set of reaching definitions
    # given as the argument.
    # The return value will be the
    # replaced expression if possible,
    # otherwise the expression itself
    def propagate_copy(self, inreachset):
        found = True
        if self.last_reached_def != inreachset or self.last_expression == 0:
            found = False
            self.reset_cache(inreachset)
        return self.last_expression, found

    # Returns true if the expression
    # contains the variable
    def contains(self, sid):
        print "Override this"

    # inreachset is the set of reaching definitions
    # loop is the set of basic blocks comprising
    # the loop under consideration
    # Returns true if the variable or expression
    # is loop invariant
    def is_loop_invariant(self, inreachset, loop):
        found = True
        if id(loop) in self.last_loop_variancy:
            return self.last_loop_variancy[id(loop)], True
        else:
            print self, "[no variancy found for the", inreachset, "]"
            found = False
            self.reset_cache(inreachset)
            self.last_loop_variancy[id(loop)] = False
        return self.last_loop_variancy[id(loop)], found

    # Returns the set of used variables in the expression
    def get_used(self):
        print "Override this"

class Var(Atom):

    def __init__(self, sid):
        Atom.__init__(self)
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
        res, found = Atom.fold_constants(self, inset)
        if found:
            return res

        res = self.find_only_definition(inset)
        if res is not None and isinstance(res, Const):
            #print "Found only def of (", self, ") at (", res, ")"
            self.last_constant = res.value
            return res.value
        return None

    # The set of reaching definitions
    # given as the argument.
    # The return value will be the
    # replaced variable if possible,
    # otherwise the variable itself
    def propagate_copy(self, inset):
        res, found = Atom.propagate_copy(self, inset)
        if found:
            return res

        res = self.find_only_definition(inset)
        if res is not None:
            if isinstance(res, Var): # The only definition is of the form x = y
                v = res.find_only_definition(inset) # Try to find the only definition of y
                if v is not None: # y is only defined once, hence return directly
                    self.last_expression = res
                    return res
        self.last_expression = self
        return self

    def contains(self, sid):
        return self.sid == sid

    def __eq__(self, other):
        return isinstance(other, Var) and self.sid == other.sid

    def is_loop_invariant(self, inreachset, loop):
        res, found = Atom.is_loop_invariant(self, inreachset, loop)
        if found:
            return res

        self.last_loop_variancy[id(loop)] = False
        ret = True
        count = 0
        inloop = False
        print get_string(self.sid), "->", inreachset
        defs = []
        for vardef in inreachset: # For every reaching definition
            if vardef.lhs == self: # Definition of present variable
                defs.append(vardef)
                count = count + 1

        for vardef in defs:
            for block in loop: # Search for it in the loop block
                if vardef in block.instructions: # There is a definition of the variable inside the loop
                    inloop = True
                    print "Declared", get_string(self.sid), " in loop, count :", count
                    if count > 1: # There is more than one definition of it
                        self.last_loop_variancy[id(loop)] = False
                        return False
                    ret = ret and vardef.rhs.is_loop_invariant(inreachset, loop)
        if not inloop: # The variable was not defined inside the loop, it is invariant
            self.last_loop_variancy[id(loop)] = True
            return True
        elif inloop and count == 1: # It is defined in the loop and that is the only definition
            self.last_loop_variancy[id(loop)] = ret
            return ret
        self.last_loop_variancy[id(loop)] = False
        return False # None of them holds

    def get_used(self):
        return set([self.sid])

class Const(Atom):

    def __init__(self, value):
        Atom.__init__(self)
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

    def contains(self, sid):
        return False

    def __eq__(self, other):
        return isinstance(other, Const) and self.value == other.value

    def is_loop_invariant(self, inreachset, loop):
        return True

    def get_used(self):
        return set()

class AtomicOp(Atom):

    def __init__(self):
        Atom.__init__(self)
        self.name = 'AtomicOp'

def func_not(val):
    return not val

def func_neg(val):
    return -val

class UnOp(AtomicOp):

    def __init__(self, right, op):
        Atom.__init__(self)
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
        res, found = Atom.fold_constants(self, inset)
        if found:
            return res

        val = self.right.fold_constants()
        if val is not None:
            self.last_constant = self.function[self.op](val)
            return self.last_constant
        return None

    def propagate_copy(self, inset):
        res, found = Atom.propagate_copy(self, inset)
        if found:
            return res

        if isinstance(self.right, Var):
            self.right = self.right.propagate_copy(inset)
        self.last_expression = self
        return self

    def contains(self, sid):
        return self.right.contains(sid)

    def __eq__(self, other):
        if isinstance(other, UnOp):
            m = self.op == other.op
            r = self.right == other.right
            return m and r
        return False

    def get_replacement(self, inavailset):
        for i in inavailset:
            if i.rhs == self:
                return i.lhs
        return self

    def is_loop_invariant(self, inreachset, loop):
        res, found = Atom.is_loop_invariant(self, inreachset, loop)
        if found:
            return res

        self.last_loop_variancy[id(loop)] = self.right.is_loop_invariant(inreachset, loop)
        return self.last_loop_variancy[id(loop)]

    def get_used(self):
        return self.right.get_used()

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
        Atom.__init__(self)
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
        res, found = Atom.fold_constants(self, inset)
        if found:
            return res

        lval = self.left.fold_constants(inset)
        rval = self.right.fold_constants(inset)
        # Although we may not be able to calculate
        # the whole expression, we can replace
        # parts of it easily
        if lval is not None:
            self.left = Const(lval)
        if rval is not None:
            self.right = Const(rval)
        if lval is not None and rval is not None:
            self.last_constant = self.function[self.op](lval, rval)
            return self.last_constant
        return None

    def propagate_copy(self, inset):
        res, found = Atom.propagate_copy(self, inset)
        if found:
            return res

        if isinstance(self.left, Var):
            self.left = self.left.propagate_copy(inset)
        if isinstance(self.right, Var):
            self.right = self.right.propagate_copy(inset)
        self.last_expression = self
        return self

    def contains(self, sid):
        return self.right.contains(sid) or self.left.contains(sid)

    def __eq__(self, other):
        if isinstance(other, BinOp):
            l = self.left == other.left
            m = self.op == other.op
            r = self.right == other.right
            return l and m and r
        return False

    def get_replacement(self, inavailset):
        assert isinstance(inavailset, set)
        for i in inavailset:
            if i.rhs == self:
                return i.lhs
        return self

    def is_loop_invariant(self, inreachset, loop):
        res, found = Atom.is_loop_invariant(self, inreachset, loop)
        print res, found
        if found:
            return res

        self.last_loop_variancy[id(loop)] = self.left.is_loop_invariant(inreachset, loop) and self.right.is_loop_invariant(inreachset, loop)
        return self.last_loop_variancy[id(loop)]

    def get_used(self):
        return self.left.get_used().union(self.right.get_used())

# Derive it from Atom to provide cache features
# We'll see if any problem comes
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
        # The last set of reaching
        # definitions that reached
        # this statement. If that
        # remains same, then there
        # is no need to recalculate
        # the invariancy, just return
        # the cache
        self.last_reached_def = None
        # Whether this instruction was
        # loop in variant in context
        # with last_reached_def
        self.last_invariancy_status = False

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

    def eliminate_cse(self, inavailset):
        if self.rhs is not None:
            if isinstance(self.rhs, BinOp) \
                    or isinstance(self.rhs, UnOp):
                tmp = self.rhs.get_replacement(inavailset)
                if tmp != self.lhs:
                    self.rhs = tmp

    def is_loop_invariant(self, inreachset, loop):
        if self.lhs is not None and self.rhs is not None:
            print "From tac :", self, inreachset
            return self.rhs.is_loop_invariant(inreachset, loop) #and self.rhs.is_loop_invariant(inreachset, loop)
            #return self.last_invariancy_status
        return False
