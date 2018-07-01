from simplenodes import instructions
from tac import Tac

# A 2D array of tacs which
# form a basic block
basic_blocks = []

def find_index(ins):
    return instructions.index(ins)

def find_basic_blocks():
    leaders = [instructions[0]]
    i = 1
    while i < len(instructions):
        if instructions[i].is_branch():
            if i < (len(instructions) - 1) and instructions[i + 1] not in leaders:
                leaders.append(instructions[i + 1])
            if instructions[i].destination_ins not in leaders and instructions[i].destination_ins is not None:
                leaders.append(instructions[i].destination_ins)
            i = i + 1
        i = i + 1

    leaders.sort(key=find_index)

    print leaders

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

def bb_to_cfg():
    global basic_blocks
    i = 0
    while i < len(basic_blocks):
        x = basic_blocks[i].instructions[-1]
        if x.is_branch():
            ins = x.destination_ins
            lbl = x.destination
            # Find the block which contains
            # the inst
            # We have to consider backward
            # blocks to in case it is a loop
            j = 0
            while j < len(basic_blocks):
                if ins in basic_blocks[j].instructions:
                    basic_blocks[j].targetof[basic_blocks[i]] = lbl
                    basic_blocks[i].destinations.append(basic_blocks[j])
                    break
                j = j + 1
        if x.rhs is not None: # it is a conditional branch or assignment
            if i < len(basic_blocks) - 1:
                lbl = ' '
                if x.is_branch():
                    lbl = 'else'
                basic_blocks[i + 1].targetof[basic_blocks[i]] = lbl
                basic_blocks[i].destinations.append(basic_blocks[i + 1])
        i = i + 1

def view_cfg():
    from dotviewer import graphclient
    import py
    content = ["digraph G{"]
    content.extend(basic_blocks[0].view())
    # Show all nonreachable blocks
    for block in basic_blocks:
        if block.viewed != 1:
            content.extend(block.view())
    content.append("}")
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

    def __repr__(self):
        s = 'BasicBlock : {\n'
        for i in self.instructions:
            s = s + str(i) + '\n'
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

