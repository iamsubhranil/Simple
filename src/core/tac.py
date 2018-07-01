from strtbl import get_string, register_string
from display import *

class Atom(object):

    def __init__(self):
        self.name = 'Atom'

class Var(Atom):

    def __init__(self, sid):
        self.name = 'AtomVar'
        self.sid = sid

    def __repr__(self):
        return get_string(self.sid)

    def nocolor(self):
        return str(self)

class Const(Atom):

    def __init__(self, value):
        self.name = 'AtomConst'
        self.value = value

    def __repr__(self):
        return str(self.value)

    def nocolor(self):
        return str(self)

class AtomicOp(Atom):

    def __init__(self):
        self.name = 'AtomicOp'

class UnOp(AtomicOp):

    def __init__(self, right, op):
        self.name = 'AtomicOp' + str(op)
        self.right = right
        self.op = op

    def __repr__(self):
        return sbold(str(self.op)) + ' ' + str(self.right)

    def nocolor(self):
        return str(self.op) + ' ' + self.right.nocolor()

class BinOp(AtomicOp):

    def __init__(self, left, right, op):
        self.name = 'AtomicOp' + str(op)
        self.left = left
        self.right = right
        self.op = op

    def __repr__(self):
        return str(self.left) + ' ' + cmgn(str(self.op)) + ' ' + str(self.right)

    def nocolor(self):
        return self.left.nocolor() + ' ' + str(self.op) + ' ' + self.right.nocolor()

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
        # destination.
        # An unconditional jump
        # instruction has all
        # variables unset expcept
        # this one.
        self.destination = None
        # The instruction which represents
        # the destination.
        self.destination_ins = None
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
        else: # usual assignment
            s = s + self.lhs.nocolor() + ' = ' + self.rhs.nocolor()

        return s

    def is_branch(self):
        if self.rhs is None: # unconditional jump
            return True
        elif self.lhs is None: # conditional jump
            return True
        return False
