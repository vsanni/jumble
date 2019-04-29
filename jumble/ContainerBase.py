"""
Created on Tue Mar 20 20:38:10 2018

@author: vsanni
"""

from copy import deepcopy

class ContainerBase():

    def _haskeys(self, s):
        try:
            list(s.keys())
            return True
        except:
            return False

    def __init__(self, *v, **kv): self.arguments(*v, **kv)

    def __str__(self):
        s = ""
        if self.__dict__:
            n = len(max(list(self.keys()), key=len))
            Format = "%-"+str(n)+"s: "
            for k, v in sorted(self.items()):
                s += Format % k
                s += v.__repr__()+"\n" if isinstance(v, ContainerBase) else str(v) + "\n"
        return s

    def __setitem__(self, k, v): self.__dict__[k] = v

    def __getitem__(self, k)   : return self.__dict__[k]

    def __contains__(self, k)  : return k in self.__dict__

    def __repr__(self)         : return "<Container with %d fields at 0x%x>" % ( len(self.__dict__), id(self))

    def __eq__(self, t)        : return self.__dict__ == t

    def keys(self)             : return self.__dict__.keys()

    def values(self)           : return self.__dict__.values()

    def items(self)            : return self.__dict__.items()

    def clear(self)            : return self.__dict__.clear()

    def copy(self)             : return deepcopy(self)

    def delete(self, k)        : del self.__dict__[k]

    def update(self, *v, **kv) : self.__dict__.update(*v, **kv)

    def pop(self, key, default): return self.__dict__.pop( key, default)

    def popitem(self, *v, **kv): return self.__dict__.popitem()

    def arguments(self, *v, **kv):
        for s in v:
            if self._haskeys(s):
                self.update(s)
            else:
                raise ValueError("arguments without keywords must have keys and values")

        self.update(kv)


