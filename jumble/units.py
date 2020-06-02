"""
Created on Fri May  3 14:48:05 2019

@author: sannibalev@gmail.com
"""

import re
import numpy as np

from math import log10, floor, isnan
from jumble.latex import translate_measure
import jumble.type_extra as tye

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


prefixes_keys            = ("y", "z", "a", "f", "p", "n", "u", "m", "_", "k", "M", "G", "T", "P", "E", "Z", "Y")
prefixes                 = {k:10.0**n for n,k in zip(range(-24,len(prefixes_keys)*3,3),prefixes_keys) }

symbols                  = ["g", "Hz", "W", "A", "V", "s", "m", "rad", "H", "F", "Ohms"]
symbols_exception        = ["cm-1", "dBm", "dBu", "dBc", "dB", "min.", "hrs.", "days", "weeks", "mo", "m." ]

prefixed_dict            = _prefixed_dict_create(symbols, prefixes)
prefixed_reciprocal_dict = _prefixed_dict_create(symbols, prefixes, reciprocal=True)

solar_year = 365*24*3600+5*3600+48*60+46.0 #Solar year: 65 days 5 hours 48 minutes46 seconds
time_dict = {"min"     : 60.,
            "hour"     : 3600.,
            "day"      : 86400.,
            "week"     : 604800.,
            "month"    : 2592000.,
            "year"     : solar_year,
            "decade"   : solar_year*10.,
            "century"  : solar_year*100.,
            "millenium": solar_year*1000.,
            "hrs"      : 3600.,
            "mo."      : 2592000.,
            "yr."      : solar_year,
            "c."       : solar_year*100.,
            "m."       : solar_year*1000.,
            }


rad_2_deg = 180.0/np.pi
deg_2_rad = np.pi/180.0

vars().update(prefixed_dict)
vars().update(prefixed_reciprocal_dict)



def order_of_magnitude(x):

    if   x == 0  : return 0
    elif isnan(x): return 0
    else         : return int(floor(log10(abs(x))))



#%%dB ALWAYS RATIO OF POWERS!

def dB(x) : return 10*np.log10(x)        # ref to 1 W
def dBm(x): return 10*np.log10(x) + 30.0 # ref to 1 mW
def dBu(x): return 10*np.log10(x) + 60.0 # ref to 1 uW


def idB(X) : return 10.0**(np.asarray(X)/10.0)   # ref to 1 W
def idBm(X): return 10.0**(np.asarray(X)/10.0-3) # ref to 1 mW
def idBu(X): return 10.0**(np.asarray(X)/10.0-6) # ref to 1 uW

#%% cm^-1 units
def m_to_cm_1(x): return .01/x

def cm_1_to_m(x): return .01/x
    

#%% find stuff
def find_base(s):
 
    n = len(s)
    for se in symbols_exception+symbols:
        m = len(se)        
        if s[max(0,n-m):] == se: return se

    return None



def find_prefix_factor(s):
    if   s in prefixes.keys(): return prefixes[s]
    else                     : return None



def find(s, pre_reg_expr=None, post_reg_expr=None):
    
    if pre_reg_expr  is not None and post_reg_expr is not None: reg_expr = pre_reg_expr+"%s"+post_reg_expr 
    elif pre_reg_expr  is not None                            : reg_expr = pre_reg_expr+"%s"
    elif post_reg_expr is not None                            : reg_expr = "%s"+post_reg_expr
    else                                                      : reg_expr = "%s"

    for k in prefixed_dict.keys():
        if re.findall(reg_expr % k, s ) != []: return k

    return None



def breakdown(s, pre_reg_expr=None, post_reg_expr=None):
    
    if pre_reg_expr  is not None or post_reg_expr is not None: 
       s= find(s, pre_reg_expr, post_reg_expr)
       if s is None: 
           raise ValueError("units.breakdown: error, cannot recognize units \""+str(s)+"\"")

    base_unit = find_base(s)
    if base_unit is None:
        raise ValueError("units.breakdown: error, cannot recognize units \""+str(s)+"\"")
    
    prefix    = s[:-len(base_unit)]
    if prefix == ""               : prefix_factor = 1 
    elif prefix in prefixes.keys(): prefix_factor = prefixes[prefix]
    
    return base_unit, prefix, prefix_factor    
    


#%% convert units

def convert(x, old_units="", new_units=""):

    o_bu, o_px, o_sf = breakdown(old_units)
    n_bu, n_px, n_sf = breakdown(new_units)
    
    sf = o_sf/n_sf
    
    if   o_bu == "dB"   and n_bu == "W"   : return  idB(x)*sf
    elif o_bu == "dBm"  and n_bu == "W"   : return idBm(x)*sf
    elif o_bu == "dBu"  and n_bu == "W"   : return idBu(x)*sf
    elif o_bu == "W"    and n_bu == "dB"  : return  dB(np.asarray(x)*sf)
    elif o_bu == "W"    and n_bu == "dBm" : return dBm(np.asarray(x)*sf)
    elif o_bu == "W"    and n_bu == "dBu" : return dBu(np.asarray(x)*sf)
    elif o_bu == "cm-1" and n_bu == "m"   : return cm_1_to_m(x)*sf
    elif o_bu == "m"    and n_bu == "cm-1": return m_to_cm_1(x*sf)
    elif o_bu == n_bu                     : return np.asarray(x)*sf
    else:
        raise ValueError("units.convert: error, cannot conver "+str(old_units)+" to "+str(new_units))



#%% prefix

def prefix(x):

    om = order_of_magnitude(x)

    n     = (om+24) // 3
    n_max = len(prefixes_keys)-1
    if    n < 0    : n = 0
    elif  n > n_max: n =n_max

    k = prefixes_keys[n]
    
    return k if k != "_" else "", 1/prefixes[k], om 



def _prefixed_base_value(x, mode="range"):

    def range_(x):
        if tye.is_iterable(x): return .5*(x[0]+x[-1])
        else                 : return x
        
    prefix_function = {"avg": np.mean, "min": np.min, "max": np.max, "range": range_}

    return prefix_function[mode](x)



def _prefixed_time(t, mode, standard_units):

    """
    Synopsis: units, scale_factor, order_of_mag = prefixed_time(t)

    Input:
            t   time value to be scaled to the approriate units

    Output:
            units  Time units string
                'ps'          picoseconds
                'ns'          nanoseconds
                'us'          microseconds
                'ms'          milliseconds
                's'           seconds
                'min'         minutes
                'hrs'         hours
                'days'        days
                'weeks'       weeks
                'mo.'         months
                'yr.'         years
                'c.'          centuries
                'm.'          millenia

            scale_factor       scale factor to multiply the time t to adjust for the new units
    """

    d = time_dict

    t0 = _prefixed_base_value(t, mode)
    
    if t0 < d["min"]*10 or  standard_units: 
        prefixed_units, prefix_factor, om = prefix(t0)
        prefixed_units += "s"

    else:
        if   t0 >= d["min"    ]*10 and t0 < d["hour"     ]*6 : prefixed_units = "min"
        elif t0 >= d["hour"   ]*6  and t0 < d["day"      ]*4 : prefixed_units = "hrs"
        elif t0 >= d["day"    ]*4  and t0 < d["week"     ]*4 : prefixed_units = "days"
        elif t0 >= d["week"   ]*4  and t0 < d["month"    ]*4 : prefixed_units = "weeks"
        elif t0 >= d["month"  ]*4  and t0 < d["year"     ]   : prefixed_units = "mo."
        elif t0 >= d["year"   ]    and t0 < d["century"  ]   : prefixed_units = "yr."
        elif t0 >= d["century"]    and t0 < d["millenium"]   : prefixed_units = "c."
        else                                                 : prefixed_units = "m."
        om            = order_of_magnitude(t0)
        prefix_factor = 1/d[prefixed_units]

    return np.asarray(t)*prefix_factor, prefixed_units, prefix_factor, om



def prefixed(x, units, mode="range", standard_units=True, latex=False):
    
    if units == "s":
        prefixed_x, prefixed_units, prefix_factor, om = _prefixed_time(x, mode, standard_units)

    else:
        s, prefix_factor, om = prefix(_prefixed_base_value(x, mode))
        prefixed_units       = s+units
        prefixed_x           = np.asarray(x)*prefix_factor
        
    if latex: 
        if prefixed_units[0] == "u": prefixed_units = "\\mu "+prefixed_units[1:]

    return prefixed_x, prefixed_units, prefix_factor, om



def measure(name, x, sx, significant_digits, units, scientific_notation_digits_threshold=3, prefix_units=True, latex=False):

    def _format(dec, scientific_notation=False): 
        s = "%." + str(dec) + "f" if dec >=0  else "%.f"    
        if scientific_notation: return "%s = ( "+s+" +- " +s+ ") x 10^%d %s"
        else                  : return "%s = ( "+s+" +- " +s+ ")"

    if sx is None:
        s = ("%g" % x).lower().replace("e", "x10^").replace("+", "")        
        s = "%s = %s %s" % (name, s, units)

    else:
        n   = order_of_magnitude(x)
        dec = significant_digits-order_of_magnitude(sx)-1

        x  = round( x, dec)
        sx = round(sx, dec)

        if prefix_units:
            c_prefix, sf, om = prefix(x)
            s                = _format(dec+om-1) % (name, x*sf, sx*sf, c_prefix+units)

        elif  -scientific_notation_digits_threshold < n < scientific_notation_digits_threshold:            
            s = _format(dec) % (name, x, sx, units)

        else:
            s = _format(dec+n, scientific_notation=True) % (name, x/10**n, sx/10**n, n, units)

    if latex: s = translate_measure(s)

    return s
