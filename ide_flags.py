def isTransperentFlag(flag):
    if flag == 0: return False
    if flag % 4 == 0: return True
    return False