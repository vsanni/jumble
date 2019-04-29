"""
$HeadURL: file:///home/svn/python/lib/type_extra.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""
from math import log10, floor, isnan

def number( x, frmt="%g"):

    s = frmt % x

    if   s.find("e") != -1: return s.replace("e","\cdot 10^{")+"}"
    elif s.find("E") != -1: return s.replace("E","\cdot 10^{")+"}"
    else                  : return s


def order_of_magnitude(x):

    if   x == 0  : return 0
    elif isnan(x): return 0
    else         : return int(floor(log10(abs(x))))



def measure(name, x, sx, significant_digits, units):

    if sx is None:
       return "%s=%s\,%s" %(name, number(x), units)

    n   = order_of_magnitude(x)
    dec = -order_of_magnitude(sx)-1+significant_digits

    x  = round( x*10**dec)/10**dec
    sx = round(sx*10**dec)/10**dec

    if  -3 < n < 3:
      s    = "%." + str(dec) + "f" if dec >=0  else "%.f"
      frmt = "%s = \\left( "+s+" \\pm " +s+ "\\right) \\,%s"
      return frmt % (name, x, sx , units)

    else:
      dec += n
      s    = "%." + str(dec) + "f" if dec >=0  else "%.f"
      frmt = "%s = \\left( "+s+" \\pm " +s+ "\\right) \\cdot 10^{%d} \\,%s"

      return frmt % (name, x/10**n, sx/10**n, n,  units)


