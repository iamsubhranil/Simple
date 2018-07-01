import struct
import array

from rpython.rlib.objectmodel import we_are_translated

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['string_of'] = reverse
    return type('Enum', (), enums)
# The frame will contain a symbol table, and a string
# table. All strings in the bytecode will be referred 
# as an index in that string table

opcode = enum(
    # Load the constant value specified in the bytecode
    # to the top of the stack
    'LOAD_CONSTANT_INT', # 8 bytes
    'LOAD_CONSTANT_FLOAT', # 8 bytes
    'LOAD_CONSTANT_BOOL', # 1 byte
    'LOAD_THIS',
    # Load the value at the specific slot to the top of the stack
    # slotnum : bytecode.next_int()
    # frame[tos] : context[slotnum]
    'LOAD_SLOT',
    # Load a global value, depth tells the number of parent
    # in its scope chain where the value would be found, 1
    # for its original parent, 2 for grandparent ...
    # depth : bytecode.next_int()
    # slot : bytecode.next_int()
    # frame[tos] : supercontext[depth][slot]
    'LOAD_GLOBAL',
    # Load a value with reference to a instance
    # present at the top of the stack.
    # The top of the stack will be replaced by
    # the referenced member
    # The referenced member will be specified as
    # string, which will be retrieved from the
    # symbol table of that instance.
    # mem : bytecode.next_int()
    # ins : frame[tos], frame[tos] : ins.get(mem)
    'LOAD_REFERENCE',
    # Store the value at the top of the stack to the specified slot
    # value : frame[tos], slotnum : bytecode.next_byte()
    # context[slotnum] : value
    'STORE_SLOT',
    # Store a global value
    # depth tells the number of parent
    # in its scope chain where the value would be found, 1
    # for its original parent, 2 for grandparent ...
    # depth : bytecode.next_int()
    # slot : bytecode.next_int()
    # supercontext[depth][slot] = frame[tos]
    'STORE_GLOBAL',
    # Store the value at the  top of the stack to the specified member
    # of the instance present at tos - 1
    # mem = bytecode.next_int()
    # val : frame[tos], ins : frame[tos - 1], ins.set(mem, value)
    'STORE_REFERENCE',
    # Pop two values from the tos, second value first, and perform
    # the specific operation between them, storing the result back
    # to the top of the stack
    # value2 : frame[tos], value1 : frame[tos - 1], frame[tos] <= value1 op value2
    'ARITH_ADD',
    'ARITH_SUB',
    'ARITH_MUL',
    'ARITH_DIV',
    'ARITH_POW',
    'LOGIC_OR',
    'LOGIC_AND',
    'LOGIC_GT',
    'LOGIC_LT',
    'LOGIC_EQ',
    'LOGIC_NE',
    'LOGIC_GTE',
    'LOGIC_LTE',
    # Pop one value from the TOS, perform the specific operation, and push the
    # result back
    # value : frame[tos], frame[tos] : op value
    'LOGIC_NOT', # expects a boolean
    'ARITH_NEG', # expects a number
    # Jumps to the specific address unconditionally
    # ip = bytecode.next_byte()
    'JUMP',
    # Jumps to the specific address if the criteria is met, otherwise jumps to
    # another address
    # if criteria_is_met then ip = bytecode.next_int() else ip = ip + 8 // skip the int
    'JUMP_IF_TRUE',
    'JUMP_IF_FALSE',
    # Calls a specific subroutine.
    # bytecode.next_int() denotes the number of arguments,
    # For a CALL N opcode, at first the callee will be retrieved by
    # accessing frame[tos - N], which will contain the routine.
    # Argument will be popped by the callee, 
    # <not_implemented> and the validation
    # will be performed by the compiler, hence the opcode
    # performs no checks at all <not_implemented>
    'CALL',
    # Returns from a subroutine
    # The return address will be retrieved from the active
    # context, both the ip and the context will be reset,
    # and the execution will resume
    'RETURN',
    # Loads a sub scope from the active scope and sets it as the
    # active scope
    # scopenum : bytecode.next_int()
    # scope : activescope.subscope[scopenum]
    'LOAD_SCOPE'
)

def source_highlight(source, source_pos, print_newline):
    if source is not None and source_pos is not None:
        print source.split('\n')[source_pos.lineno]
        if source_pos.columnno == 0:
            if print_newline == 1:
                print "^"
            else:
                print "^",
        else:
            if print_newline == 1:
                print " " * (source_pos.columnno - 1), "^"
            else:
                print " " * (source_pos.columnno - 1), "^",

class Disassembler(object):

    def __init__(self, bo):
        assert isinstance(bo, Bytecode2)
        self.bo = bo
        self.source = bo.source

    def highlight(self, source_pos):
        if self.source is not None:
            source_highlight(self.source, source_pos, 0)
            print "-" * (48 - source_pos.columnno),

    def dis(self):
        bak = self.bo.pos
        self.bo.pos = 0
        while self.bo.pos < len(self.bo.code):
            try:
                self.highlight(self.bo.debug_info[self.bo.pos])
            except KeyError:
                print " " * 50,
            op = self.bo.next_byte()
            s = str(opcode.string_of[op])
            if not we_are_translated():
                print "%3d" % (self.bo.pos - 1), " : ", "%-20s" % s, " ",
            else:
                print self.bo.pos - 1, " : ", s, " ",
            if not s.startswith('ARITH') \
            and not s.startswith('RETURN') \
            and not s.startswith('LOGIC'):
                if not we_are_translated():
                    fn = getattr(self, "handle_" + s)
                    fn()
                else:
                    #fn = self.handler[s]()
                    if s == 'LOAD_CONSTANT_INT':
                        self.handle_LOAD_CONSTANT_INT()
                    elif s == 'LOAD_CONSTANT_BOOL':
                        self.handle_LOAD_CONSTANT_BOOL()
                    elif s == 'LOAD_CONSTANT_FLOAT':
                        self.handle_LOAD_CONSTANT_FLOAT()
                    elif s == 'LOAD_SLOT':
                        self.handle_LOAD_SLOT()
                    elif s == 'LOAD_GLOBAL':
                        self.handle_LOAD_GLOBAL()
                    elif s == 'LOAD_REFERENCE':
                        self.handle_LOAD_REFERENCE()
                    elif s == 'STORE_SLOT':
                        self.handle_STORE_SLOT()
                    elif s == 'STORE_GLOBAL':
                        self.handle_STORE_GLOBAL()
                    elif s == 'STORE_REFERENCE':
                        self.handle_STORE_REFERENCE()
                    elif s == 'JUMP':
                        self.handle_JUMP()
                    elif s == 'JUMP_IF_TRUE':
                        self.handle_JUMP_IF_TRUE()
                    elif s == 'JUMP_IF_FALSE':
                        self.handle_JUMP_IF_FALSE()
                    elif s == 'CALL':
                        self.handle_CALL()
                    elif s == 'LOAD_SCOPE':
                        self.handle_LOAD_SCOPE()
                print
            else:
                print
        self.bo.pos = bak

    def handle_LOAD_CONSTANT_INT(self):
        print self.bo.next_int(), ' ',

    def handle_LOAD_CONSTANT_FLOAT(self):
        print self.bo.next_float()

    def handle_LOAD_CONSTANT_BOOL(self):
        print self.bo.next_byte()

    def handle_LOAD_SLOT(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_LOAD_GLOBAL(self):
        self.handle_LOAD_CONSTANT_INT()
        self.handle_LOAD_CONSTANT_INT()

    def handle_LOAD_REFERENCE(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_STORE_SLOT(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_STORE_GLOBAL(self):
        self.handle_LOAD_GLOBAL()

    def handle_STORE_REFERENCE(self):
        self.handle_LOAD_REFERENCE()

    def handle_JUMP(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_JUMP_IF_TRUE(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_JUMP_IF_FALSE(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_CALL(self):
        self.handle_LOAD_CONSTANT_INT()

    def handle_LOAD_SCOPE(self):
        self.handle_LOAD_CONSTANT_INT()

class Bytecode2:

    def __init__(self, source = None):
        self.code = []
        self.pos = 0
        self.debug_info = {}
        self.source = source

    def append_value(self, b, source_pos = None):
        if source_pos is not None:
            self.debug_info[self.pos] = source_pos

        self.code.append(b)
        self.pos += 1
        return self.pos - 1

    def insert_value(self, val, pos):
        self.code[pos] = val
        return pos

    def append_byte(self, b, source_pos = None):
        assert b < 256 and b >= 0
        return self.append_value(b, source_pos)

    def insert_byte(self, b, pos):
        assert b < 256 and b >= 0
        return self.insert_value(b, pos)

    # LSB is in lower order byte
    def append_int(self, b, source_pos = None):
        assert isinstance(b, int)
        return self.append_value(b, source_pos)

    def insert_int(self, b, pos):
        assert isinstance(b, int)
        return self.insert_value(b, pos)

    def append_float(self, b, source_pos = None):
        assert isinstance(b, float)
        return self.append_value(b, source_pos)

    def insert_float(self, b, pos):
        assert isinstance(b, float)
        return self.insert_value(b, pos)

    def set_pointer(self, s):
        self.pos = s

    def get_value(self, pos):
        return self.code[pos]

    def next_value(self):
        v = self.code[self.pos]
        self.pos += 1
        return v

    def next_byte(self):
        v = self.next_value()
        assert v < 256 and v >= 0
        return int(v)

    def get_byte(self, pos):
        v = self.get_value(pos)
        assert v < 256 and v >= 0
        return v

    def next_int(self):
        v = self.next_value()
        # print v
        if not we_are_translated():
            assert isinstance(v, int)
            return v
        return int(v)

    def get_int(self, pos):
        v = self.get_value(pos)
        assert isinstance(v, int)
        return v

    def next_float(self):
        v = self.next_value()
        assert isinstance(v, float)
        return v

    def get_float(self, pos):
        v = self.get_value(pos)
        assert isinstance(v, float)
        return v

    def __repr__(self):
        return str(self.code)

    def at_end(self):
        return self.pos >= len(self.code) - 1

if __name__ == "__main__":
    b = Bytecode2()
    h = b.append_byte(opcode.LOAD_SLOT)
    g = b.append_int(-23)
    f = b.append_float(32.32)
    from strtbl import register_string, get_string
    i = b.append_int(register_string("Hello World!"))
    print b
    b.set_pointer(0)
    print b.get_int(g)
    print b.get_float(f)
    print b.next_byte()
    print b.next_int()
    print b.next_float()
    print get_string(b.get_int(i))
    print register_string("Hello Kool!"), i
    b.insert_int(1, i)
    print b
    print get_string(b.get_int(i))
