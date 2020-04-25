"""
Created on Fri May  3 14:48:05 2019

@author: sannibalev@gmail.com
"""

import re
import numpy as np
from math import log10, floor, isnan

def order_of_magnitude(x):

    if   x == 0  : return 0
    elif isnan(x): return 0
    else         : return int(floor(log10(abs(x))))



#dB ALWAYS RATIO OF POWERS!

def dB(x) : return 10*np.log10(x)        # ref to 1 W
def dBm(x): return 10*np.log10(x) + 30.0 # ref to 1 mW
def dBu(x): return 10*np.log10(x) + 60.0 # ref to 1 uW


def idB(X) : return 10.0**(np.asarray(X)/10.0)    # ref to 1 W
def idBm(X): return 10.0**(np.asarray(X)/10.0-3) # ref to 1 mW
def idBu(X): return 10.0**(np.asarray(X)/10.0-6) # ref to 1 uW


def _prefixed_dict_create(symbols, prefixes, standard_units = True, reciprocal=False):
    d = dict()
    for s in symbols:
        for k, v in prefixes.items():
            if k !="_":
                key = k+s
                if   reciprocal: d["i"+key] = 1/v
                else           : d[key    ] = v

            elif standard_units:
                if   reciprocal: d["i"+s] = 1/v
                else           : d[s    ] = v

    return d

prefixes                 = {"p": 1.0e-12, "n": 1.0e-9, "u": 1.0e-6, "m": 1.0e-3, "_": 1.0, "k": 1.0e+3, "M": 1.0e+6, "G": 1.0e+9, "T": 1.0e+12, "E": 1.0e+15}
symbols                  = ["Hz", "W", "A", "V", "s", "m", "rad", "H", "F", "Ohms"]
prefixed_dict            = _prefixed_dict_create(symbols, prefixes)
prefixed_reciprocal_dict = _prefixed_dict_create(symbols, prefixes, reciprocal=True)

vars().update(prefixed_dict)
vars().update(prefixed_reciprocal_dict)

rad_2_deg = 180.0/np.pi
deg_2_rad = np.pi/180.0

def conversion_factor(s, reciprocal=False):

    D = prefixed_reciprocal_dict if reciprocal else prefixed_dict
    for k,v in D.items():
        if k in s: return v

    raise ValueError("units.conversion_factor: cannot determine units conversion factor from "+str(s) )



def find(s, reg_expr_format = None):

    for k,v in prefixed_dict.items():
        if reg_expr_format is None:
            if k in s: return k, v
        else:
            if re.findall(reg_expr_format % k, s ) != []: return k, v

    raise ValueError("units.find: cannot find any known  basic units from \"%s\"" % s )



def prefix(x):

    om = order_of_magnitude(x)

    if           om < -12: k ="p"
    elif  -12 <= om <  -9: k ="p"
    elif  -9  <= om <  -6: k ="n"
    elif  -6  <= om <  -3: k ="u"
    elif  -3  <= om <   0: k ="m"
    elif   0  <= om <   3: k ="_"
    elif   3  <= om <   6: k ="k"
    elif   6  <= om <   9: k ="M"
    elif   9  <= om <  12: k ="G"
    elif  12  <= om <  15: k ="T"
    elif  15  <= om      : k ="E"

    return k if k != "_" else "", 1/prefixes[k], om



def time_convert(t, standard_prefix=False):

    """
    Synopsis: units, scale_factor = time_scaled(t)

    Input:
            t   time value to be scaled to the approriate units

    Output:
            units  Time units string
                'ps'          picoseconds
                'ns'          nanoseconds
                'us'          microseconds
                'ms'          milliseconds
                's'           seconds
                'minutes'     minutes
                'hours'       hours
                'days'        days
                'weeks'       weeks
                'years'       years
                'c.'          centuries
                'm.'          millenia

            scale_factor       scale factor to adjust the time t
    """

    min_      =        60.
    hour      =      3600.
    day       =     86400.
    week      =    604800.
    month     =   2592000.
    year      = 365*24*3600+5*3600+48*60+46.0  #Solar year: 65 days 5 hours 48 minutes	46 seconds
    decade    =    year*10.
    century   =  decade*10.
    millenium = century*10.

    if   t <  min_*10 or  standard_prefix: units, sf, om = prefix(t) ; units += "s"
    elif t >= min_*10 and t < hour*6     : units, sf     = 'minutes', 1/min_
    elif t >= hour*6  and t < day*4      : units, sf     = 'hours'  , 1/hour
    elif t >= day*4   and t < week*4     : units, sf     = 'days'   , 1/day
    elif t >= week*4  and t < month*4    : units, sf     = 'weeks'  , 1/week
    elif t >= month*4 and t < year       : units, sf     = 'months' , 1/month
    elif t >= year    and t < century    : units, sf     = 'years'  , 1/year
    elif t >= century and t < millenium  : units, sf     = 'c.'     , 1/century
    else                                 : units, sf     = 'm.'     , 1/millenium

    om = order_of_magnitude(t)

    return units, sf, om



def prefixed(x, units, mode="avg"):

    x = np.asarray(x)

    frequency_prefix_mode = {"avg": np.mean, "min": np.min, "max": np.max}

    if   mode in frequency_prefix_mode.keys():
        x  = frequency_prefix_mode[mode](x)
        if units == "s":
            prefixed_units, iprefix_factor, om = time_convert(x)

        else:
            s, iprefix_factor, om = prefix(x)
            prefixed_units        = s+units

    elif mode in ["_","none",""]:
        prefixed_units, iprefix_factor, om = units, 1.0, order_of_magnitude(np.mean(x))

    elif mode in prefixes.keys():
        prefixed_units, iprefix_factor, om = mode+units, 1/prefixes[mode], order_of_magnitude(np.mean(x))

    else:
        raise ValueError("units.prefixed: error, cannot recognize mode "+str(mode) )

    return prefixed_units, iprefix_factor, om



def standard_convert(x, units="", standard_units=""):

    if   units     == "dB"  and standard_units == "W"  : return idB(x)
    elif units     == "dBm" and standard_units == "W"  : return idBm(x)
    elif units     == "dBu" and standard_units == "W"  : return idBu(x)
    elif units     == "W"   and standard_units == "dB" : return dB(x)
    elif units     == "W"   and standard_units == "dBm": return dBm(x)
    elif units     == "W"   and standard_units == "dBu": return dBu(x)
    elif units     == standard_units                   : return x[:]
    elif units[1:] == standard_units                   : return x*prefixes[units[0]]
    else:
        raise ValueError("units.standard_units: error, cannot recognize units "+str(units)+" or standard units "+str(standard_units))



def measure(name, x, sx, significant_digits, units, scientific_notation_digits_threshold=3, prefix=True):

    def number_format(dec): return "%." + str(dec) + "f" if dec >=0  else "%.f"

    if sx is None:
        s = "%g" % x
        if   s.find("e") != -1: s = s.replace("e", "x10^").replace("+", "")
        elif s.find("E") != -1: s = s.replace("E", "x10^").replace("+", "")
        else                  : s = s

        return "%s = %s %s" % (name, s, units)

    else:
        n   =  order_of_magnitude(x)
        dec = -order_of_magnitude(sx)-1+significant_digits

        x  = round( x, dec)
        sx = round(sx, dec)

        if prefix:
            c_prefix, sf, om = prefix(x)
            x               *= sf
            sx              *= sf
            units            = c_prefix+units

            s    = number_format(dec+om-1)
            frmt = "%s = ( "+s+" +- " +s+ ") %s"
            return frmt % (name, x, sx , units)

        elif  -scientific_notation_digits_threshold < n < scientific_notation_digits_threshold:
            s    = number_format(dec)
            frmt = "%s = ( "+s+" +- " +s+ ") %s"
            return frmt % (name, x, sx , units)

        else:
            s    = number_format(dec+n)
            frmt = "%s = ( "+s+" +- " +s+ ") x 10^%d %s"
            return frmt % (name, x/10**n, sx/10**n, n, units)
