"""
$HeadURL: file:///home/svn/python/lib/vprint.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""


import sys
import jumble.vprint as vp
    

def eprint(type, value, traceback):
    if vp._last_printed_char != "\n": print()
    raise ValueError(value)

sys.excepthook = eprint

sys.tracebacklimit = 0
