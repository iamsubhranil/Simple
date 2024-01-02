from hashlib import md5

class StringTable(object):

    def __init__(self):
        self.stringtable = {}
        self.stringhashlist = []

strtable = StringTable()

def register_string(string):
    assert isinstance(string, str)
    global strtable
    hval = md5(string).hexdigest()
    if hval not in strtable.stringtable:
        strtable.stringtable[hval] = string
        s = len(strtable.stringhashlist)
        strtable.stringhashlist.append(hval)
        #stringhashlist.extend([hval])
        return s
    return strtable.stringhashlist.index(hval)

def get_string(idx):
    return strtable.stringtable[strtable.stringhashlist[idx]]
