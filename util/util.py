def getExchange(code):
    first =  code[:1]
    return 'SZ' if first in ['0', '1', '2', '3'] else 'SH'
