"""
$HeadURL: file:///home/svn/python/lib/type_extra.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""

import numpy as np
import time
import datetime



def length(x):

    try:
        if (isinstance(x,int) or isinstance(x,float)):
            return 1

        elif isinstance(x, (np.ndarray, np.generic) ):
            if x.dtype.type == np.string_: return len(str(x))
            else                         : return len(x)

        else:
            return len(x)

    except:
        return 0



def is_numeric(x):
    try   :  x/1.0;  return True
    except:          return False



def is_numeric_string(x):
    try   :  float(x)/1.0;  return True
    except:                 return False



def is_complex(x): return np.iscomplexobj(x)

def is_even(x)   : return  x % 2 == 0

def is_odd(x)    : return x % 2 != 0



def convert_float(x):

    try   : return float(x), True
    except: return None    , False



def convert_int(x):

    try   : return int(x), True
    except: return None  , False




def as_list(v, n=1):

    if   type(v) is list : return v*n
    elif type(v) is tuple: return list(v)*n
    else                 : return [v]*n



def list_exact_find(list_, t, mode='all'):

     found = [i for i, s in enumerate(list_) if s == t]

     if   found        == []     : return None
     elif mode.lower() == 'first': return found[0]
     elif mode.lower() == 'last' : return found[-1]
     elif mode.lower() == 'all'  : return found
     else                        : raise Exception("list_exact_find: unknown search mode, valid modes are \"first\", \"all\", or \"last\"" )


def list_find(list_, t, mode='all'):

    found = [ [i, s.find(t)] for i, s in enumerate(list_) if t in s]

    if   found        == []     : return None
    elif mode.lower() == 'first': return found[0]
    elif mode.lower() == 'last' : return found[-1]
    elif mode.lower() == 'all'  : return found
    else                        : raise Exception("list_exact_find: unknown search mode, valid modes are \"first\", \"all\", or \"last\"" )



def range_distribute(n,p):

    if p>n: p = n

    Dn, dn = divmod(n,p)

    n = [Dn]*p
    for i in range(dn): n[i] +=1

    n = np.array([0]+n).cumsum()

    s, e = n[ :-1], n[1:  ]

    return s, e



def string_replace(s, BadChars="", Replacement=""):

    for c in BadChars: s=s.replace(c,Replacement)

    return s



def key_valid(Key, Replacement=""):

    s = string_replace(Key, BadChars=" #^*/|()[]{}<>'`~\":;,.?$%&!@=-\t\r\n", Replacement=Replacement)

    if s[0].isdecimal(): s = "_"+s

    return s


def string_to_value(s):
    s= s.strip()
    if is_numeric_string(s):
        vf = float(s)
        vi = int(s)
        if vf == vi: return vi
        else       : return vf
    else:
        return s


def string_abbreviate( s, n, where="Start", abbreviation_string="..."):

    n -= len(abbreviation_string)

    if len(s) > n:
        if   where.lower() == "start":
            s = "..."+ s[-n:]

        elif where.lower() == "middle":
            n0 = n>>1
            n1 = n - n0
            s = s[:n0]+"..."+ s[-n1:]

        elif where.lower() == "end":
            s = s[:n]+ "..."

        else:
            s = None

    return s



def keys_pascal_case(d): return { k.title().replace("_","") : v for k,v in d.items()}



def time_stamp_hour2seconds(HourTimeStamp):
    x = time.strptime(HourTimeStamp,'%H:%M:%S')
    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
