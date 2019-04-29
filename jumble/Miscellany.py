"""
$HeadURL: file:///home/svn/python/lib/Miscellany.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""

_last_printed_char =""

def _check_last_printed_char(v):
    global _last_printed_char

    try:
        if isinstance(v[-1], str): _last_printed_char = v[-1][-1]
        else                     : _last_printed_char = ""
    except:
        _last_printed_char = ""



def vprint(verbose,verbosity_level,*v, on_newline=False, **kv):

    if verbose >= verbosity_level:
        if on_newline and _last_printed_char != "\n": print()
        print( *v, end="", **kv)
        _check_last_printed_char(v)



def eprint(*v, **kv):
    try:
        raise Exception()
    except:
        if _last_printed_char != "\n": print()
        print( *v, end="", **kv)
        _check_last_printed_char(v)


#def MinimalCompare(x, Par, MinLength=1, CaseSensitive=False):
#
#    if (x==None or Par == None):
#        return(False)
#
#    if (CaseSensitive):
#        return(x == Par[:max(MinLength, len(x))])
#
#    else:
#        return(x.lower() == Par.lower()[:max(MinLength, len(x))])



def wine(s):

    import subprocess

    return subprocess.call( 'wine ' + s)



def CheckFunctionsIO(V):

    def  CheckFunctionNoInput(Function, Output):

         FOut = Function()

         if (FOut==Output):
             return(FOut, True)
         else:
             return(FOut, False)

    def  CheckFunction(Input, Function, Output):


         if (type(Input) is tuple):
              FOut = Function(*Input)

         else:
           FOut = Function(Input)

         if (FOut==Output):
             return(FOut, True)
         else:
             return(FOut, False)

    N  = len(V)
    n  = 0
    for i in (list(range(N))):
        if ( len(V[i]) == 2):
            FOut, Result = CheckFunctionNoInput(*V[i])

        elif ( len(V[i]) == 3):
            FOut, Result = CheckFunction(*V[i])

        else:
            raise ValueError('list must be either [in, func, out] or [func, out] ')

        print(i, V[i], FOut, end=' ')
        if (Result == True):
            print('=> Ok')
            n += 1
        else:
            print('=> Error')

    print('Number I/O tested            :', N)
    print('Number I/O tested Ok         :', n)
    print('Number I/O tested with errors:', N-n)

    return n



def LocalHostIP():
    from netifaces import interfaces, ifaddresses, AF_INET

    LHIP = {}
    for ifName in interfaces():
        for k,v in ifaddresses(ifName).items() :
            if k == AF_INET:
                LHIP[str(ifName)] = str(v[0]['addr'])

    return LHIP



def Color(n):
    Palette = [ (  0,   0, 144),
               (  0, 144,   0),
               (255, 208,   0),
               (  0, 144, 144),
               (  0,   0,   0),
               (128, 48,    0),
               (0  , 0,   144),
               (0  , 176,   0),
               (192, 96,    0),
               (144, 144,  144)]

    n = min(n,9)

    return Palette[n][0]/255.0,Palette[n][1]/255.0,Palette[n][1]/255.0
