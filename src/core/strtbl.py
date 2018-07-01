from rpython.rlib.rmd5 import md5

class StringTable(object):

    def __init__(self):
        self.stringtable = {}
        self.stringhashlist = []

strtable = StringTable()
md5ins = md5()

def register_string(string):
    assert isinstance(string, str)
    global strtable
    md5ins.input = string
    hval = md5ins.hexdigest()
    if hval not in strtable.stringtable:
        strtable.stringtable[hval] = string
        s = len(strtable.stringhashlist)
        strtable.stringhashlist.append(hval)
        #stringhashlist.extend([hval])
        return s
    return strtable.stringhashlist.index(hval)

def get_string(idx):
    return strtable.stringtable[strtable.stringhashlist[idx]]
