"""
Created on Fri Jan 18 22:44:55 2013

@author: vsanni
"""
from __future__ import print_function


import numpy  as np
import pickle as pickle
import gzip

from copy import deepcopy

from jumble.ContainerBase import ContainerBase

_n               = 0
_unwanted_string = "!un@p#ic$k7l^ea_b20d6le$v=/"
_N               = len(_unwanted_string)+1
_wanted_type     = ( bool, int, float, complex, str, tuple, list, bytearray, np.ndarray, np.generic)


def haskeys(s):

    try:
        list(s.keys())
        return True
    except:
        return False


def _keylist(s): return list(s.keys()) if haskeys(s) else list(range(len(s)))



def _clean_up(s):

    global _unwanted_string

    for k in _keylist(s):
        if isinstance(s[k], tuple): s[k] = list(s[k])

        if haskeys(s[k]):
            _clean_up(s[k])

        elif isinstance(s[k], list):
            _clean_up(s[k])

        elif isinstance(s[k], str):
            if s[k][:len(_unwanted_string)] ==  _unwanted_string:
                s[k] = None

    return s


def _remove_unwanted(s, reset=True, Verbose = 1):

    global _n, _Unpickleable, _wanted_type

    if reset:
        _n            = 0
        _Unpickleable = []

    for k in _keylist(s):
        if isinstance(s[k], tuple): s[k] = list(s[k])

        if haskeys(s[k]):
            _remove_unwanted(s[k], reset=False)

        elif isinstance(s[k], list):
            _remove_unwanted(s[k], reset=False)

        elif isinstance(s[k], _wanted_type) or s[k] is None:
            pass

        else:
            if Verbose >= 2:
                print("warning: not saving field object", s[k])
            _Unpickleable.append(s[k])
            s[k] = "%s:%d" % (_unwanted_string, _n)
            _n += 1

    return _Unpickleable



def _restore_unwanted(s, reset=True):

    global _n, _Unpickleable, _N

    if reset:
        _n = 0

    for k in _keylist(s):
        if haskeys(s[k]):
            _restore_unwanted(s[k], reset=False)

        elif isinstance(s[k], list):
            _restore_unwanted(s[k], reset=False)

        elif type(s[k]) is str:
            n = min(_N, len(s[k]))
            if s[k][:n-1] == _unwanted_string:
                s[k] = _Unpickleable[_n]
                _n  += 1




class Container(ContainerBase):

    def merge(self, s, deepmerge=True):
        for k, v in s.items():
            if not hasattr(self, k):
                self.__dict__[k] = deepcopy(v)
            elif isinstance(self.__dict__[k], Container) and isinstance(s[k], Container) and deepmerge:
                self.__dict__[k].merge(s[k])

            return self



    def save(self, filename, dataonly=True):

        extension = filename.split(".")[-1].lower()

        if dataonly is True:
            _remove_unwanted(self, reset=True)

        if extension == "pickle":
            with open(filename, 'wb') as fh:
                pickle.dump(self.__dict__, fh, protocol=pickle.HIGHEST_PROTOCOL)

        elif extension == "pgz":
            with gzip.GzipFile( filename, 'wb') as fh:
                pickle.dump(self.__dict__, fh, protocol=pickle.HIGHEST_PROTOCOL)

        else:
            raise ValueError("%s.save: cannot recognize extension \"%s\"" % (self.__module__, extension))

        if dataonly is True:
            _restore_unwanted(self, reset=True)

        return self



    def load(self, filename):

        extension = filename.split(".")[-1].lower()

        if extension == "pickle":
            with open(filename, 'rb') as fh:
                self.__dict__ = dict(pickle.load(fh).items())

        elif extension == "pgz":
            with gzip.GzipFile(filename, 'rb') as fh:
                self.__dict__ = dict(pickle.load(fh).items())

        else:
            raise ValueError("%s.load: cannot recognize extension \"%s\"" % (self.__module__, extension))

        _clean_up(self)

        return self
