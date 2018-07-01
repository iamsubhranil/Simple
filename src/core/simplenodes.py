from strtbl import get_string, register_string
from tac import AtomicOp, BinOp, UnOp, Tac, Var, Const

tempvarcount = 0
templabelcount = 0
instructions = []
# It is a two tuple
# list which contains
# pending labels along
# with the tacs who
# generated the label
pending_labels = []

def check_if_bool(expr):
    t = expr.return_type()
    return t == bool or t == VariableExpression

def ins_append(i):
    global pending_labels
    for label in pending_labels:
        print label
        i.targetof[label[1]] = label[0]
        label[1].destination_ins = i
    pending_labels = []
    instructions.append(i)

def get_temp_var():
    global tempvarcount
    s = 't' + str(tempvarcount)
    tempvarcount += 1
    return s

def get_temp_label():
    global templabelcount
    s = 'L' + str(templabelcount)
    templabelcount += 1
    return s

class ValidationException(Exception):

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message

class CompilationContext(object):

    def __init__(self, sc, name):
        self.name = name
        self.supercontext = sc
        # It is a dictionary mapping
        # an sid and the
        # source_pos where sid is
        # declared
        self.symbol_table = {}
        # It is a 3D list
        # containing the sid, the
        # value of the sid, and the
        # source_pos where the value
        # of the sid is set
        # the value of the sid will
        # necessarily be an expression
        self.assignments = []
        # It is a two tuple list
        # mapping a function sid to
        # a FunctionDeclaration object
        self.callables = []

    def declare(self, sid, source_pos):
        self.symbol_table[sid] = source_pos
        self.assignments.append([sid, None, source_pos])

    def declare_function(self, sid, source_pos, func):
        self.symbol_table[sid] = source_pos
        self.callables.append((sid, func))

    def update_assignment(self, sid, value, source_pos):
        for i in self.assignments:
            c = i[0]
            if c == sid:
                sp = i[2]
                if sp.i >= source_pos.i:
                    i[1] = value

    def is_declared_only_current(self, sid, source_pos):
        if sid in self.symbol_table:
            decpos = self.symbol_table[sid]
            if decpos.i <= source_pos.i:
                return True
        return False

    def is_declared(self, sid, source_pos):
        if self.is_declared_only_current(sid, source_pos):
            return True
        elif self.supercontext is not None:
            return self.supercontext.is_declared(sid, source_pos)
        return False

    def get_state(self, sid, source_pos):
        i = 0
        val = None
        while i < len(self.assignments):
            record = self.assignments[i]
            if record[0] == sid:
                if record[2].i <= source_pos.i:
                    val = record[1]
            i = i + 1
        if val is not None:
            return val
        if val is None and self.supercontext is not None:
            return self.supercontext.get_state(sid, source_pos)
        return val

class Statement(object):

    def __init__(self, name, context):
        self.name = name
        self.context = context
        self.source_pos = None

    # Should be overridden
    def optimize(self):
        raise

    # Should be overridden
    def compile(self):
        raise

    # Should be overridden
    def validate(self):
        raise

class Program(Statement):

    def __init__(self, context):
        self.name = 'Program'
        self.context = context
        self.statements = []

    def compile(self):
        for st in self.statements:
            st.compile()
        if len(pending_labels) > 0:
            ins_append(Tac())

    def optimize(self):
        for st in self.statements:
            st.optimize()

    def validate(self):
        for st in self.statements:
            st.validate()

    def __repr__(self):
        s = ''
        for st in self.statements:
            if st is not None:
                s = s + str(st) + ";\n"
        return s

class AssignmentStatement(Statement):

    def __init__(self, context, source_pos, assignee, assignment):
        self.name = 'AssignmentStatement'
        self.context = context
        self.assignee = assignee
        self.assignment = assignment
        self.source_pos = source_pos

    def optimize(self):
        self.assignment = self.assignment.optimize()
        self.context.update_assignment(self.assignee, self.assignment, self.source_pos)

    def compile(self):
        s = Var(self.assignee.sid)
        t = self.assignment.compile()
        tac = Tac()
        tac.lhs = s
        tac.rhs = t
        ins_append(tac)

    def validate(self):
        if isinstance(self.assignee, VariableExpression):
            self.assignment.validate()
        else:
            raise ValidationException("Assignee must be a variable!")

    def __repr__(self):
        s = str(self.assignee) + ' = ' + str(self.assignment)
        return s

class ExpressionStatement(Statement):

    def __init__(self, context):
        self.name = 'ExpressionStatement'
        self.context = context
        self.exprs = []

    def optimize(self):
        i = 0
        while i < len(self.exprs):
            self.exprs[i] = self.exprs[i].optimize()

    def validate(self):
        for expr in self.exprs:
            expr.validate()

    def compile(self):
        for expr in self.exprs:
            expr.compile()

    def __repr__(self):
        s = ''
        i = 0
        for e in self.exprs:
            if i > 0:
                s = s + ', '
            i = i + 1
            s = s + str(e)
        return s

class IfStatement(Statement):

    def __init__(self, context, cond, thenpart, elsepart):
        self.name = 'IfStatement'
        self.context = context
        self.cond = cond
        self.thenpart = thenpart
        self.elsepart = elsepart

    def optimize(self):
        self.cond = self.cond.optimize()
        self.thenpart.optimize()
        if elsepart is not None:
            self.elsepart.optimize()

    def validate(self):
        self.cond.validate()
        if check_if_bool(self.cond):
            self.thenpart.validate()
            if self.elsepart is not None:
                self.elsepart.validate()
        else:
            raise ValidationException("Condition must be boolean!")

    def compile(self):
        t = self.cond.compile()
        l = get_temp_label()
        countercond = UnOp(t, '!')
        tac = Tac()
        tac.destination = l
        tac.rhs = countercond
        ins_append(tac)
        self.thenpart.compile()
        if self.elsepart is not None:
            l1 = get_temp_label()
            tac1 = Tac()
            tac1.destination = l1
            ins_append(tac1)
            pending_labels.append((l, tac))
            self.elsepart.compile()
            pending_labels.append((l1, tac1))
        else:
            pending_labels.append((l, tac))

    def __repr__(self):
        s = 'if ' + str(self.cond) + '{\n' + str(self.thenpart) + '\n}'
        if self.elsepart is not None:
            s = s + 'else {\n' + str(self.elsepart) + '\n}'
        return s

class WhileStatement(Statement):

    def __init__(self, context, cond, truestatement):
        self.name = 'WhileStatement'
        self.context = context
        self.cond = cond
        self.truestatement = truestatement

    def optimize(self):
        self.cond = self.cond.optimize()
        self.truestatement.optimize()

    def validate(self):
        self.cond.validate()
        if check_if_bool(self.cond):
            self.truestatement.validate()
        else:
            raise ValidationException("Condition must be boolean")

    def compile(self):
        l = get_temp_label()
        ujmp = Tac()
        pending_labels.append((l, ujmp))
        t = self.cond.compile()
        l1 = get_temp_label()
        countercond = UnOp(t, '!')
        cjmp = Tac()
        cjmp.destination = l1
        cjmp.rhs = countercond
        ins_append(cjmp)
        self.truestatement.compile()
        ujmp.destination = l
        ins_append(ujmp)
        pending_labels.append((l1, cjmp))

    def __repr__(self):
        s = 'while ' + str(self.cond) + '{\n' + str(self.truestatement) + '\n}'
        return s


class BlockStatement(Statement):

    def __init__(self, context):
        self.name = 'BlockStatement'
        self.context = context
        self.statements = []
        self.owncontext = None

    def optimize(self):
        for statement in self.statements:
            statement.optimize()

    def validate(self):
        for statement in self.statements:
            statement.validate()

    def compile(self):
        for statement in self.statements:
            statement.compile()

    def __repr__(self):
        s = "{\n"
        for st in self.statements:
            s = s + str(st) + ";\n"
        return s + '\n}'

class Expression(object):

    def __init__(self, name, context):
        self.name = name
        self.context = context
        self.source_pos = None

    # Should be overridden
    def optimize(self):
        raise

    # Should be overridden
    def is_constant(self):
        raise

    # Should be overridden
    def compile(self):
        raise

    # Should be overridden
    def eval(self):
        raise

    # Should be overridden
    def validate(self):
        raise

    # Should be overridden
    def return_type(self):
        raise

class ConstantExpression(Expression):

    def __init__(self, context, value, vtype):
        self.name = 'ConstantExpression'
        self.context = context
        self.value = value
        self.vtype = vtype

    def optimize(self):
        return self

    def is_constant(self):
        return True

    def compile(self):
        return Const(self.value)

    def eval(self):
        return self.value

    def validate(self):
        assert isinstance(self.value, self.vtype)

    def return_type(self):
        return self.vtype

    def __repr__(self):
        return str(self.value)

class BinaryExpression(Expression):

    def __init__(self, context, left, right, return_type, validator, string):
        self.name = 'BinaryExpression'
        self.context = context
        self.left = left
        self.right = right
        # For binary expressions, return type
        # is a function of left type and right type
        self.rt = return_type
        self.validator = validator
        self.opstring = string

    def optimize(self):
        # Constant folding
        self.left = self.left.optimize()
        self.right = self.right.optimize()

        if self.left.is_constant() and self.right.is_constant():
            return ConstantExpression(self.context, self.eval())
        else:
            return self

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    # Can only be called when the expression is constant
    def eval(self):
        return self.function(self.left.eval(), self.right.eval())

    def compile(self):
        t1 = self.left.compile()
        t2 = self.right.compile()
        t3 = BinOp(t1, t2, self.opstring)
        t = Var(register_string(get_temp_var()))
        tac = Tac()
        tac.lhs = t
        tac.rhs = t3
        ins_append(tac)
        return t

    def validate(self):
        self.left.validate()
        self.right.validate()
        if self.validator(self.left):
            pass
        else:
            raise ValidationException("Unable to validate left expression!")
        if self.validator(self.right):
            pass
        else:
            raise ValidationException("Unable to validate right expression!")

    def return_type(self):
        return self.rt(self.left, self.right)

    def __repr__(self):
        return str(self.left) + ' ' + self.opstring + ' ' + str(self.right)

class UnaryExpression(Expression):

    def __init__(self, context, right, return_type, validator, string):
        self.name = 'UnaryExpression'
        self.context = context
        self.right = right
        self.validator = validator
        # rt is a function of string
        # and right
        # ! -> bool
        # - -> highest_type(right)
        self.rt = return_type
        self.opstring = string

    def optimize(self):
        self.right = self.right.optimize()
        if self.right.is_constant():
            return ConstantExpression(self.context, self.eval())
        else:
            return self

    def is_constant(self):
        return right.is_constant()

    def eval(self):
        return self.function(self.right.eval())

    def compile(self):
        t1 = self.right.compile()
        t = Var(register_string(get_temp_var()))
        u = UnOp(t1, self.opstring)
        tac = Tac()
        tac.lhs = t
        tac.rhs = u
        ins_append(tac)
        return t

    def validate(self):
        self.right.validate()
        if self.validator(self.right):
            pass
        else:
            raise ValidationException("Unable to validate right expression!")

    def return_type(self):
        return self.rt(self.opstring, self.right)

    def __repr__(self):
        return self.opstring + ' ' + str(self.right)

class VariableExpression(Expression):

    def __init__(self, context, sid, source_pos):
        self.name = 'VariableExpression'
        self.context = context
        self.sid = sid
        self.source_pos = source_pos

    def optimize(self):
        if self.is_constant():
            return ConstantExpression(self.context, self.eval())
        else:
            return self

    def is_constant(self):
        i = self.context.get_state(self.sid, self.source_pos)
        if i is None:
            raise ValidationException("Value used before assignment : " + get_string(self.sid))
        return i.is_constant()

    def eval(self):
        if self.is_constant():
            state = self.context.get_state(self.sid, self.source_pos)
            se = state.eval()
            if self.context.is_declared_only_current(self.sid, self.source_pos):
                ce = ConstantExpression(self.context, se, type(se))
                self.context.update_assignment(self.sid, ce, self.source_pos)
            return se
        else:
            return self

    def compile(self):
        return Var(self.sid)

    def validate(self):
        if not self.context.is_declared(self.sid, self.source_pos):
            raise ValidationException("Variable not declared : " + get_string(self.sid))
        # if not context.is_declared_only_current(sid, self.source_pos):
        #    c = context.get_assigned(sid, self.source_pos)
        #    context.declare(sid, self.source_pos)
        #    context.update_assignment(sid, c, self.source_pos)

    def return_type(self):
        #if self.is_constant():
        #    return type(self.eval())
        #else:
        return VariableExpression

    def __repr__(self):
        return get_string(self.sid)
