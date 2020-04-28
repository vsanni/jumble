"""
$HeadURL: file:///home/svn/python/lib/type_extra.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""


def number( x, frmt="%g"):

    s = frmt % x

    if   s.find("e") != -1: return s.replace("e", "\cdot 10^{")+"}"
    elif s.find("E") != -1: return s.replace("E", "\cdot 10^{")+"}"
    else                  : return s



def translate_measure(s):

    if "x" in s: s_close_parentesis_spacing = ""
    else       : s_close_parentesis_spacing = "\\,"

    s = s.replace("("  , "\\left(" )
    s = s.replace(")"  , "\\right)"+s_close_parentesis_spacing)
    s = s.replace("+-" , "\\pm"    )
    s = s.replace("x"  , "\\cdot"  )
    s = s.replace("10^", "10^{"    )
    s = s.replace(" u", " \\mu "   )
    s = s.replace("%%", " \\%"     )

    if "10^" in s:
        n = s.rfind(" ")
        s = s[:n]+"}\\,"+s[n:]

    return s
