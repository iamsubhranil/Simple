from tac import Tac

def find_index(instructions):
    def fi(ins):
        return instructions.index(ins)

def find_basic_blocks(instructions):

    # A 2D array of tacs which
    # form a basic block
    basic_blocks = []

    print instructions

    leaders = [instructions[0]]
    i = 1
    while i < len(instructions):
        if instructions[i].is_branch():
            if i < (len(instructions) - 1) and instructions[i + 1] not in leaders:
                leaders.append(instructions[i + 1])
            if instructions[i].destination_ins is not None and instructions[i].destination_ins not in leaders:
                leaders.append(instructions[i].destination_ins)
            if instructions[i].else_destination_ins is not None and instructions[i].else_destination_ins not in leaders:
                leaders.append(instructions[i].else_destination_ins)
        i = i + 1

    #global instrs
    #instrs = instructions
    leaders.sort(key=lambda x: instructions.index(x))

    print "\nLeaders"
    print "========\n"
    print leaders, "\n"

    worklist = list(leaders)
    worklist.reverse()
    x = 0
    i = 0
    while len(worklist) > 0:
        ins = worklist.pop()
        block = [ins]
        #i = x + 1
        #print instructions[i] not in leaders
        i = i + 1
        while i < len(instructions) and instructions[i] not in leaders:
            block.append(instructions[i])
            i = i + 1
        bb = BasicBlock()
        bb.labels = dict(ins.targetof)
        bb.instructions = block
        basic_blocks.append(bb)
        #x = x + 1
    return basic_blocks

def bb_to_cfg(basic_blocks):
    i = 0
    # A adjacency matrix for the
    # directed control flow graph
    cfg = [None] * len(basic_blocks)
    while i < len(basic_blocks):
        x = basic_blocks[i].instructions[-1]
        cfg[i] = ['None'] * len(basic_blocks)
        if x.is_branch():
            ins = x.destination_ins
            lbl = x.destination
            eins = x.else_destination_ins
            elbl = x.else_destination
            # Find the block which contains
            # the inst
            # We have to consider backward
            # blocks to in case it is a loop
            j = 0
            while j < len(basic_blocks):
                if ins in basic_blocks[j].instructions:
                    cfg[i][j] = lbl
                    basic_blocks[j].targetof[basic_blocks[i]] = lbl
                    basic_blocks[i].destinations.append(basic_blocks[j])
                    break
                j = j + 1
            # Same for else inst
            j = 0
            while j < len(basic_blocks):
                if eins in basic_blocks[j].instructions:
                    cfg[i][j] = elbl
                    basic_blocks[j].targetof[basic_blocks[i]] = elbl
                    basic_blocks[i].destinations.append(basic_blocks[j])
                    break
                j = j + 1
        if x.rhs is not None and x.lhs is not None: # it is an assignment
            if i < len(basic_blocks) - 1:
                lbl = ' '
                #if x.is_branch():
                #    lbl = 'else'
                cfg[i][i + 1] = lbl
                basic_blocks[i + 1].targetof[basic_blocks[i]] = lbl
                basic_blocks[i].destinations.append(basic_blocks[i + 1]) # Auto append the next block
        i = i + 1
    return cfg

def print_cfg(cfg, basic_blocks):
    print " " * 4,
    for i in range(len(basic_blocks)):
        print "%-4d" % i,
    print
    k = 0
    for i in cfg:
        print "%-4d" % k,
        for j in i:
            if j == 'None':
                j = '--'
            elif j == ' ' or j == 'else':
                j = '->'
            print "%-4s" % j,
        print "\n"
        k = k + 1

def view_cfg(cfg, basic_blocks):
    from dotviewer import graphclient
    import py
    content = ["digraph G{"]
    i = 0
    for blk in cfg:
        s = '"%s" [label="%s"];\n' % (i, basic_blocks[i].get_label())
        content.append(s)
        j = 0
        while j < len(blk):
            if blk[j] != 'None':
                s = '"%s" -> "%s" [label="%s"];\n' % (i, j, blk[j])
                content.append(s)
            j = j + 1
        i = i + 1
    """content.extend(basic_blocks[0].view())
    # Show all nonreachable blocks
    for block in basic_blocks:
        if block.viewed != 1:
            content.extend(block.view())
    """
    content.append("\n}")
    #print content
    try:
        p = py.test.ensuretemp("automaton").join("temp.dot")
        remove = False
    except AttributeError: # pytest lacks ensuretemp, make a normal one
        p = py.path.local.mkdtemp().join('automaton.dot')
        remove = True
        p.write("\n".join(content))
        graphclient.display_dot_file(str(p))
        if remove:
            p.dirpath().remove

def find_reaching_definitions(cfg, basic_blocks):
    out = {}
    for bb in basic_blocks:
        out[bb] = None

    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(basic_blocks):
            prevout = out[basic_blocks[i]]
            j = 0
            inbb = set()
            while j < len(basic_blocks):
                if cfg[j][i] != 'None':
                    #print "Out : ", basic_blocks[j].calculate_out()
                    inbb = inbb.union(basic_blocks[j].calculate_out())
                    #print "In : ", inbb
                j = j + 1
            basic_blocks[i].inset = inbb
            newout = basic_blocks[i].calculate_out()
            if newout != prevout:
                out[basic_blocks[i]] = newout
                changed = True
                break
            i = i + 1


class BasicBlock(object):

    def __init__(self):
        # List of all blocks whose
        # target is this block
        # mapped with the labels
        self.targetof = {}
        # List of tacs in this block
        self.instructions = []
        # The destination(s) of this block,
        # if any
        self.destinations = []
        # Flag to denote whether or not
        # this block was drawn
        self.viewed = 0
        # The set of input definitions
        # to the block, a set of tacs
        self.inset = None
        # The dict of set of input 
        # definitions of each 
        # instruction of the
        # block, to provide more
        # fine grained optimization
        # at instruction level
        self.ininsset = {}

    def __repr__(self):
        s = 'BasicBlock : {\n'
        for i in self.instructions:
            s = s + str(i)
            try:
                s = s + ' in' + str(self.ininsset[i])
            except KeyError:
                pass
            s = s + '\n'
        s = s + '\n}'
        return s

    def get_label(self):
        s = self.instructions[0].nocolor()
        i = 1
        while i < len(self.instructions):
            s = s + '\\n' + self.instructions[i].nocolor()
            i = i + 1
        return s.replace('"', '') #.replace("\\", "\\\\")

    def view(self):
        self.viewed = 1
        yield '"%s" [label="%s"];\n' % (id(self), self.get_label())
        for i in self.destinations:
            yield '"%s" -> "%s" [label="%s"];' % (id(self), id(i), i.targetof[self])
            if i.viewed == 0:
                for line in i.view():
                    yield line

    def calculate_out(self):
        if self.inset is None:
            return set()
        kill = set()
        gen = set()
        prevout = self.inset
        for i in self.instructions:
            if i.lhs is not None:
                var_def = i.lhs
                for j in self.inset:
                    if j.lhs.sid == var_def.sid:
                        kill.add(j)
                gen.add(i)
            self.ininsset[i] = prevout
            prevout = gen.union(self.inset.difference(kill))
        #print "Gen : ", gen
        out = gen.union(self.inset.difference(kill))
        #print "Out : ", out
        #print self.inset, gen, kill, out
        return out

    def fold_constants(self):
        for i in self.instructions:
            i.fold_constants(self.ininsset[i])

