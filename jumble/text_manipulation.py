"""
Created on Tue Oct  9 20:56:33 2018

@author: vsanni
"""


def find_string_separator(s, quotes):

    q1 = "'"
    q2 = '"'
    q3 = '"""'

    k1 = s.find(q1)
    k2 = s.find(q2)
    k3 = s.find(q3)

    if quotes == "":
        if   k1==k2==k3       : k, n, quotes, open_string = -1, 1, "", False
        elif k1==-1 and k2==-1: k, n, quotes, open_string = k3, 3, q3, True
        elif k1==-1 and k3==-1: k, n, quotes, open_string = k2, 1, q2, True
        elif k2==-1 and k3==-1: k, n, quotes, open_string = k1, 1, q1, True
        elif k1==-1 and k2<k3 : k, n, quotes, open_string = k2, 1, q2, True
        elif k1==-1 and k3<=k2: k, n, quotes, open_string = k3, 3, q3, True
        elif k2==-1 and k1<k3 : k, n, quotes, open_string = k1, 1, q1, True
        elif k2==-1 and k3<k1 : k, n, quotes, open_string = k3, 3, q3, True
        elif k3==-1 and k1<k2 : k, n, quotes, open_string = k1, 1, q1, True
        elif k3==-1 and k2<k1 : k, n, quotes, open_string = k2, 1, q2, True
        elif k3< k1 and k3<=k2: k, n, quotes, open_string = k3, 3, q3, True
        elif k2< k1 and k2<=k3: k, n, quotes, open_string = k2, 1, q2, True
        elif k1< k2 and k1<k3 : k, n, quotes, open_string = k1, 1, q1, True

    elif quotes == q1  : k, n, quotes, open_string = k1, 1, "", False
    elif quotes == q2  : k, n, quotes, open_string = k2, 1, "", False
    elif quotes == q3  : k, n, quotes, open_string = k3, 3, "", False

    return k, quotes, open_string, n



def find_strings(s):

    n0         = []
    n1         = []
    quotes     = ""
    n          = 0
    while True:
        k, quotes, open_string, dn = find_string_separator(s[n:], quotes)
        if k == -1: break

        if open_string: n0.append(n+k)
        else         : n1.append(n+k+dn)

        n +=dn+k

    return n0, n1



def tag_find_chunks(s):

    dN     = []
    N      = []
    t      = []
    quotes = ""
    n      = 0

    while True:
        k, quotes, open_string, dn = find_string_separator(s[n:], quotes)
        if k == -1: break

        if open_string: t.append(True )
        else          : t.append(False)

        N.append(n+k)
        dN.append(dn)

        n += dn+k


    if N == []:
        N0, N1 = [0], [len(s)]
        t      = [False]

    else:
        if N[0] != 0:
            N = [-1]+N
            t = [False]+t

        if N[-1] != len(s)-1: N = N +[len(s)]

        N0 = [ n if s else n+dn for n, dn, s in zip(N[:-1], dN, t)]
        N1 = [ n+dn if s else n for n, dn, s in zip(N[1: ], dN, t)]

    return N0, N1, t[:len(N0)]



def Camel2snake(s):

    s += "  "

    t = s[0].lower()

    for n in range(len(s)-3):
        c, d, e, f = s[n:n+4]

        if c.islower() and d.isupper() and e != "_": t += "_"

        t += d.lower()

        if c.isupper() and d.isupper() and e.islower() and f != "_": t += "_"

    return t



def read_text_file(file_location):
    with open(file_location, mode='r') as fin:
        return fin.read()



def write_text_file(file_location):
    with open(file_location, mode='w') as fout:
        return fout.read()


def tokens(cmd, separator=" ", string_char="\"", comment_char="#"):
    open_  = False
    space  = False
    l      = []
    s      = ""

    for c in cmd:
       if c == comment_char and not open_:
           break

       elif space and not open_ and c == separator:
           pass

       else:
           if c == string_char: open_ ^= True
           space = True if c == separator  else False

           if open_ and space         : s+=c
           if open_ and not space     : s+=c
           if not open_ and space     : s, l = "", l+[s]
           if not open_ and not space : s += c

    return l+[s]
