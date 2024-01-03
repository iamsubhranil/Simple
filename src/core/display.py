
COLOR_MAGENTA = '\033[95m'
COLOR_BLUE = '\033[94m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
STYLE_RESET = '\033[0m'
STYLE_BOLD = '\033[1m'
STYLE_UNDERLINE = '\033[4m'

def sbold(s):
    return STYLE_BOLD + s + STYLE_RESET

def sund(s):
    return STYLE_UNDERLINE + s + STYLE_RESET

def cred(s):
    return COLOR_RED + s + STYLE_RESET

def cblue(s):
    return COLOR_BLUE + s + STYLE_RESET

def cgrn(s):
    return COLOR_GREEN + s + STYLE_RESET

def cylw(s):
    return COLOR_YELLOW + s + STYLE_RESET

def cmgn(s):
    return COLOR_MAGENTA + s + STYLE_RESET

def perr(s):
    print(sbold(cred("[Error] ")) + s)

def pinfo(s):
    print(sbold(cblue("[Info] ")) + s)

def pwarn(s):
    print(sbold(cylw("[Warning] ")) + s)

def pok(s):
    print(sbold(cgrn("[Success] ")) + s)
