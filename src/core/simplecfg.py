from tac import Tac
from simplenodes import get_temp_label
from queue import *

def find_index(instructions):
    def fi(ins):
        return instructions.index(ins)

def find_basic_blocks(instructions):

    # A 2D array of tacs which
    # form a basic block
    basic_blocks = []

    print(instructions)

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

    print("\nLeaders")
    print("========\n")
    print(leaders, "\n")

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
        basic_blocks[i].destinations = []
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
        elif x.rhs is not None and x.lhs is not None: # it is an assignment
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
    print(" " * 4, end=' ')
    for i in range(len(basic_blocks)):
        print("%-4d" % i, end=' ')
    print()
    k = 0
    for i in cfg:
        print("%-4d" % k, end=' ')
        for j in i:
            if j == 'None':
                j = '--'
            elif j == ' ' or j == 'else':
                j = '->'
            print("%-4s" % j, end=' ')
        print("\n")
        k = k + 1

def view_cfg(cfg, basic_blocks, name = "CFG"):
    from dotviewer import graphclient
    import graphcontentpage
    content = ['digraph "'+ name + '" {']
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
    graphclient.display_page(graphcontentpage.GraphContentPage("\n".join(content)))

def find_reaching_definitions(cfg, basic_blocks):
    out = []
    for bb in basic_blocks:
        out.append(set())

    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(basic_blocks):
            prevout = out[i]
            j = 0
            inbb = set()
            while j < len(basic_blocks): # Also consider successors since loop is natural
                if cfg[j][i] != 'None':
                    #print "Out : ", basic_blocks[j].calculate_reaching_defs()
                    inbb = inbb.union(out[j])
                    #print "In : ", inbb
                j = j + 1
            basic_blocks[i].inreachset = inbb
            newout = basic_blocks[i].calculate_reaching_defs()
            if newout != prevout:
                out[i] = newout
                changed = True
                break
            i = i + 1

def find_available_expressions(cfg, basic_blocks):
    out = []
    for bb in basic_blocks:
        out.append(set())

    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(basic_blocks):
            prevout = out[i]
            j = 0
            inbb = set()
            while j < i: # Only consider predecessors
                if cfg[j][i] != 'None':
                    #print basic_blocks[i], basic_blocks[j]
                    #print "Out : ", basic_blocks[j].calculate_avail()
                    inbb = inbb.union(out[j])
                    #print "In : ", inbb
                j = j + 1
            basic_blocks[i].inavailset = inbb
            newout = basic_blocks[i].calculate_avail()
            if newout != prevout:
                out[i] = newout
                changed = True
                break
            i = i + 1


def find_live_variables(cfg, basic_blocks):
    inset = []

    for bb in basic_blocks:
        inset.append(set())

    changed = True
    while changed:
        changed = False
        i = len(basic_blocks) - 1
        while i >= 0:
            previn = inset[i]
            j = 0 # Only search for successors
            outset = set()
            while j < len(basic_blocks):
                if cfg[i][j] != 'None':
                    outset = outset.union(inset[j])
                j = j + 1
            basic_blocks[i].outliveset = outset
            nwin = basic_blocks[i].calculate_live_in()
            if nwin != previn:
                inset[i] = nwin
                changed = True
                #break
            i = i - 1

def find_dominators(cfg, basic_blocks):
    lenb = len(basic_blocks)
    dom = [None] * lenb
    dom[0] = set()
    dom[0].add(0)
    i = 1
    while i < lenb:
        dom[i] = set()
        i = i + 1
    changed = True
    while changed:
        changed = False
        i = 0
        while i < lenb:
            #prev = dom[i]
            nw = set()
            nw.add(i)
            intersect = None
            j = 0
            while j < i:
                if cfg[j][i] != 'None':
                    if intersect is None:
                        intersect = dom[j]
                    else:
                        intersect = intersect.intersection(dom[j])
                j = j + 1
            if intersect is not None:
                nw = nw.union(intersect)
            if dom[i] != nw:
                changed = True
                dom[i] = nw
            i = i + 1

    """
    domtree = [None] * lenb
    i = 0
    while i < lenb:
        domtree[i] = ['None'] * lenb
        dc = set(dom[i])
        if i == 0:
            i = i + 1
            continue
        dc.remove(i)
        if i != 0:
            dc.remove(0)
        if len(dc) == 0:
            domtree[0][i] = 1
        else:
            domtree[max(dc)][i] = 1
        i = i + 1

    print "Domtree :", domtree
    view_cfg(domtree, basic_blocks)
    """
    return dom

def find_back_edges(cfg, dom):
    # A list of tuples
    back_edges = []
    i = 0
    while i < len(cfg):
        j = 0
        while j < len(cfg):
            if cfg[i][j] != 'None':
                if j in dom[i]:
                    back_edges.append((j, i))
            j = j + 1
        i = i + 1
    return back_edges

def get_natural_loop(cfg, m, n):
    """
    loop = set()
    stack = []
    loop.add(m)
    loop.add(n)
    stack.append(n)
    while len(stack) > 0:
    x = stack.pop()
    i = 0
    while i < x:
    if cfg[i][x] != 'None':
    if i not in loop:
    loop.add(i)
    stack.append(i)
    i = i + 1
    #return loop
    """
    # The back edge is from n -> m
    print(m, n)
    loop = []
    lc = len(cfg)
    reachmat = [None] * lc # Reachability matrix
    i = 0
    while i < lc:
        reachmat[i] = [False] * lc
        if i == m:
            i = i + 1
            continue
        j = 0
        while j < lc:
            if cfg[i][j] != 'None' and j != m:
                reachmat[i][j] = True
            j = j + 1
        i = i + 1

    #print reachmat

    k = 0
    while k < lc:
        i = 0
        while i < lc:
            j = 0
            while j < lc:
                reachmat[i][j] = reachmat[i][j] or (reachmat[i][k] and reachmat[k][j])
                j = j + 1
            i = i + 1
        k = k + 1

    for row in reachmat:
        for i in row:
            if i:
                print(1, end=' ')
            else:
                print(0, end=' ')
        print()

    loop.append(m)
    i = 0
    while i < lc:
        if reachmat[i][n]:
            loop.append(i)
        i = i + 1
    loop.append(n)
    print(loop)
    return loop

def insert_preheader(cfg, basic_blocks, loops, idx):
    # loops is a list of set of indices
    # This is a very crude approximation,
    # but the first element is usually
    # the header
    hidx = loops[idx][0]
    header = basic_blocks[hidx]

    # Generate the preheader and an
    # unconditional goto to the header
    preheader = BasicBlock()
    goto = Tac()
    l1 = get_temp_label()
    goto.destination = l1
    goto.destination_ins = header.instructions[0]
    preheader.instructions.append(goto)
    #print header, header.instructions[0].targetof
    header.instructions[0].targetof[goto] = l1
    # Find all jump targets to the header,
    # and if the source is not in loop,
    # change it to the preheader
    i = 0
    while i < len(cfg):
        if cfg[i][hidx] != 'None':
            if i not in loops[idx]:
                #print "Target from", basic_blocks[i]
                parent = basic_blocks[i].instructions[-1]
                #print parent
                if parent in header.instructions[0].targetof:
                    #print "Popping"
                    header.instructions[0].targetof.pop(parent, None)
                if parent.destination_ins == header.instructions[0]:
                    parent.destination_ins = goto
                    if parent.destination is not None:
                        #print "Dest :", parent.destination
                        goto.targetof[parent] = parent.destination
                else:
                    #print "Else dest:", parent.else_destination
                    if parent.else_destination is not None:
                        goto.targetof[parent] = parent.else_destination
                    parent.else_destination_ins = goto
        i = i + 1

    #print "Goto.targetof :", goto.targetof

    # Insert the preheader in place of the header
    basic_blocks.insert(hidx, preheader)

    # Now all the cfg information is invalid
    # So lets rebuild them
    cfg = bb_to_cfg(basic_blocks)

    # Rebulid the dominator tree
    dom = find_dominators(cfg, basic_blocks)

    # Rebulid the back edges list
    back_edges = find_back_edges(cfg, dom)

    # Finally, rebuild the loops
    loops = []
    for be in back_edges:
        loops.append(get_natural_loop(cfg, be[0], be[1]))
    print("New loops :", loops)

    # Return everything
    return (basic_blocks, cfg, dom, back_edges, loops)

def eliminate_dead_code(basic_blocks, cfg, dom, back_edges, loops):
    removeblocks = []
    for block in basic_blocks:
        block.eliminate_dead_code()
        #block.remove_only_goto()
        if len(block.instructions) == 0:
            removeblocks.append(block)

    if len(removeblocks) > 0:
        basic_blocks, cfg, dom, back_edges, loops = remove_blocks(removeblocks, basic_blocks)

    return basic_blocks, cfg, dom, back_edges, loops

# Calculate reachable blocks
def calculate_reachbility(basic_blocks):
    for bb in basic_blocks:
        bb.reachable = False

    blocklist = []
    blocklist.append(basic_blocks[0])

    while len(blocklist) > 0:
        block = blocklist.pop()
        if not block.reachable:
            block.reachable = True
            for dest in block.destinations:
                if not dest.reachable:
                    blocklist.append(dest)

# Remove unreachable blocks
def eliminate_dead_blocks(basic_blocks, cfg, dom, back_edges, loops):
    calculate_reachbility(basic_blocks)
    removable = []
    for bb in basic_blocks:
        if not bb.reachable:
            print(bb, "is not reachable")
            removable.append(bb)
    if len(removable) > 0:
        return remove_blocks(removable, basic_blocks)
    else:
        return basic_blocks, cfg, dom, back_edges, loops

# After constant folding and dead code elimination,
# some blocks only have one unconditional jump
# instruction inside them. This pass removes
# those blocks and directly connects their
# predecessors and successors instead
def eliminate_only_goto(basic_blocks, cfg, dom, back_edges, loops):
    calculate_reachbility(basic_blocks)
    removable = []
    for bb in basic_blocks:
        if bb.eliminate_only_goto():
            removable.append(bb)
    if len(removable) > 0:
        return remove_blocks(removable, basic_blocks)
    else:
        return basic_blocks, cfg, dom, back_edges, loops

# Remove a block from the list
def remove_blocks(removeblocks, basic_blocks):
    for block in removeblocks:
        basic_blocks.remove(block)
    return rebuild_all(basic_blocks)

# Rebuild everything from basic blocks
def rebuild_all(basic_blocks):
    # Rebuild the cfg
    cfg = bb_to_cfg(basic_blocks)

    # Rebulid the dominator tree
    dom = find_dominators(cfg, basic_blocks)

    # Rebulid the back edges list
    back_edges = find_back_edges(cfg, dom)

    # Finally, rebuild the loops
    loops = []
    for be in back_edges:
        loops.append(get_natural_loop(cfg, be[0], be[1]))

    return basic_blocks, cfg, dom, back_edges, loops

def optimize_loop_invariants(cfg, basic_blocks, dom, back_edges, loops, idx):
    preheader = basic_blocks[loops[idx][0] - 1]
    loopset = []
    for m in loops[idx]:
        loopset.append(basic_blocks[m])

    loop_invariants = []
    for i in loops[idx]:
        inv = basic_blocks[i].find_loop_invariants(loopset)
        for iv in inv:
            loop_invariants.append((iv, i))

    print(loop_invariants)

    exit = loops[idx][-1]
    removeblocks = []
    changed = False
    for (inv, idx) in loop_invariants:
        canbemoved = False
        if inv.lhs.sid in basic_blocks[exit].outliveset: # variable is live at exit
            if idx in dom[exit]: # The block containing the variable dominates the exit,
                # hence it can be moved to the preheader
                # Mark to show the CFG
                changed = True
                canbemoved = True
        else: # Variable is not live at exit, probably dead code
            changed = True
            canbemoved = True
        if canbemoved:
            block = basic_blocks[idx]
            block.remove_ins(inv)
            if len(block.instructions) == 0:
                # Mark the block for removal
                removeblocks.append(block)
            preheader.append_ins(inv)
    if len(removeblocks) > 0:
        basic_blocks, cfg, dom, back_edges, loops = remove_blocks(removeblocks, basic_blocks)
        print("New loops :", loops)

    if changed:
        # Refind reaching definitions, available expressions
        # and liveness information
        print("Invariant statement(s) moved!")
        print("Recalculating reaching definitions")
        find_reaching_definitions(cfg, basic_blocks)
        print("Recalculating available expressions")
        find_available_expressions(cfg, basic_blocks)
        print("Recalculating live variables")
        find_live_variables(cfg, basic_blocks)
        print(basic_blocks)
        print_cfg(cfg, basic_blocks)
        view_cfg(cfg, basic_blocks)

    # Return everything
    return (basic_blocks, cfg, dom, back_edges, loops)

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
        self.inreachset = None
        # The dict of set of input 
        # definitions of each 
        # instruction of the
        # block, to provide more
        # fine grained optimization
        # at instruction level
        self.insreachset = {}
        # The set of expressions available
        # to the block as input
        self.inavailset = None
        # The dict of set of expressions
        # available to each instruction
        # of the block
        self.insavailset = {}
        # The set of live variables
        # at the end of the block
        self.outliveset = None
        # To mark the node as reachable
        self.reachable = False


    def __repr__(self):
        s = 'BasicBlock : {\n'
        for i in self.instructions:
            s = s + str(i)
            # try:
            #     s = s + ' in' + str(self.insreachset[i])
            # except KeyError:
            #     pass
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

    def calculate_reaching_defs(self):
        if self.inreachset is None:
            return set()
        kill = set()
        gen = set()
        prevout = self.inreachset
        for i in self.instructions:
            if i.lhs is not None: # An assignment expression
                var_def = i.lhs
                for j in self.inreachset:
                    if j.lhs.sid == var_def.sid:
                        kill.add(j)
                gen.add(i)
            self.insreachset[i] = prevout
            prevout = gen.union(prevout.difference(kill))
        #print "Gen : ", gen
        #out = gen.union(self.inset.difference(kill))
        #print "Out : ", out
        #print self.inset, gen, kill, out
        return prevout

    def fold_constants(self):
        for i in self.instructions:
            print(i)
            i.fold_constants(self.insreachset[i])

    def propagate_copy(self):
        for i in self.instructions:
            i.propagate_copy(self.insreachset[i])

    def calculate_avail(self):
        if self.inavailset is None:
            return set()
        kill = set()
        gen = set()
        prevavail = self.inavailset
        for i in self.instructions:
            if i.lhs is not None: # Assignment expression
                gen.add(i)
                defined = i.lhs
                for j in prevavail:
                    if j.rhs.contains(defined.sid):
                        kill.add(j)
            self.insavailset[i] = prevavail
            prevavail = gen.union(prevavail.difference(kill))

        return prevavail

    def eliminate_cse(self):
        for i in self.instructions:
            print(i, self.insavailset[i])
            i.eliminate_cse(self.insavailset[i])

    def find_loop_invariants(self, loop):
        loop_invariants = []
        for i in self.instructions:
            #print "From block :", self.insreachset[i]
            if i.is_loop_invariant(self.insreachset[i], loop):
                loop_invariants.append(i)
        return loop_invariants

    def calculate_live_in(self):
        if self.outliveset is None:
            return set()
        use = set()
        defn = set()

        for ins in self.instructions:
            if ins.lhs is not None:
                defn.add(ins.lhs.sid)
            if ins.rhs is not None:
                use = use.union(ins.rhs.get_used())

        return use.union(self.outliveset.difference(defn))

    # Removes an instruction from the block
    def remove_ins(self, inv):
        # Check whether it is the leader of the block
        if self.instructions[0] == inv:
            if len(self.instructions) > 1: # Move the targets to the next instruction
                self.instructions[1].targetof = inv.targetof
                # Reset the targets to point to the next instruction
                for target in self.instructions[1].targetof:
                    if target.destination_ins == inv: # It was an if or unconditional target
                        target.destination_ins = self.instructions[1]
                    else: # It was an else target
                        target.else_destination_ins = self.instructions[1]
            else: # There is no other instruction in the block.
                # So remove it, retargetting its parent(s) to the next block.
                # This can only happen when there is only one assignment in
                # a block, hence it can be safely assumed that it will have
                # only one target, that too, will be the next block in the graph.
                for target in self.targetof:
                    target.destinations.remove(self)
                    target.destinations.extend(self.destinations)
                    for dest in self.destinations:
                        dest.targetof.pop(self, None)
                        dest.targetof[target] = self.targetof[target]
        self.instructions.remove(inv)
        #print self.instructions

    # Append an instruction to the block
    # If there is only one instruction in the block,
    # it is assumed that the instruction is
    # some kind of jump (otherwise you wouldn't
    # use this), and in consequence
    # it makes the argument as its leader
    # Otherwise, it appends the instruction
    # to the last but one position
    def append_ins(self, inv):
        # Check whether it is going to be the leader of the
        # preheader
        inv.targetof = {}
        if len(self.instructions) == 1:
            inv.targetof = self.instructions[0].targetof
            # Reset the targets to point to the next instruction
            for target in inv.targetof:
                if target.destination_ins == self.instructions[0]: # It was an if or unconditional target
                    target.destination_ins = inv
                else: # It was an else target
                    target.else_destination_ins = inv
        # FINALLY, insert it to the last but one position of the preheader
        self.instructions.insert(len(self.instructions) - 1, inv)

    # Check whether a variable is active
    # in outliveset, otherwise remove
    # its definition
    def eliminate_dead_code(self):
        toremove = []
        isempty = self.outliveset == None or len(self.outliveset) == 0
        for ins in self.instructions:
            if ins.lhs != None:
                if isempty or ins.lhs.sid not in self.outliveset:
                    toremove.append(ins)
        for tr in toremove:
            self.remove_ins(tr)

    # If there is only one unconditional
    # jump in this block, remove that
    def eliminate_only_goto(self):
        if len(self.instructions) == 1:
            prob = self.instructions[0]
            if prob.lhs == None and prob.rhs == None and prob.destination_ins != None:
                self.remove_ins(prob)
                return True
        return False

    # Find all induction variables in the
    # block
    def find_induction_variables(self, loop):
        loop_invariants = self.find_loop_invariants(loop)
        iv = []
        for ins in self.instructions:
            if ins.lhs != None:
                if ins.lhs.is_induction_variable(self.insreachset[ins], loop):
                    iv.append((ins.lhs.sid, 1, 0)) # induction triplet, i = i*1 + <loop_invariant>
        return iv
