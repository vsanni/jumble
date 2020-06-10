"""
$HeadURL: file:///home/svn/python/lib/vprint.py $
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
        print( *v, flush= True, end="", **kv)
        _check_last_printed_char(v)
