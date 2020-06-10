"""
Created on Sun Sep 21 17:43:40 2014

@author: vsanni
"""


class CircularBuffer:


    def __init__(self, size= None, mode = "overlap_check", buffer=None):

        self.size   = size
        self.buffer = buffer
        self._mode  = {"simplex":(self._put_simplex, self._get_simplex), "count":(self._put_count, self._get_count),"overlap_check":(self._put_check, self._get_check)}

        self.reset()
        self.mode   = mode

    @property
    def buffer(self): return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        if buffer is None:
            self._buffer = [None]*self.size #no real need to allocate mem in python when you don't know what you are going to save in the circular bufffer
        else             :
            self._buffer = buffer
            self.size    = len(self._buffer)

        self.max = self.size-1


    @property
    def mode(self): return self._check_overlap

    @mode.setter
    def mode(self,k):
        if k not in self._mode.keys(): raise ValueError("CircularBuffer: error, mode must be any of those \"" +  str("\", \"".join(self._mode.keys()))+"\"")
        self.put, self.get = self._mode[k]

    def reset(self):

        self.tail     = 0
        self.head     = 0
        if self._mode != "simplex": self.elements = 0
        else                      : self.elements = None


    def is_empty(self):
        if self._mode == "simplex": return None
        else                      : return self.elements == 0



    def is_full(self): return self.elements == self.size



    def print(self):

        print("buffer       :", self._buffer)
        print("head, element:", self.head , self._buffer[self.head])
        print("tail, element:", self.tail , self._buffer[self.tail])
        print("elements     :", self.elements)
        print("is empty     :", self.is_empty())
        print("is full      :", self.is_full())
        print("")


    def _put_simplex(self, element):
        self._buffer[self.head] = element
        if self.head >= self.max: self.head  = 0
        else                    : self.head += 1
        return True


    def _get_simplex(self):
        element = self._buffer[self.tail]
        if   self.tail >= self.max: self.tail  = 0
        else                      : self.tail += 1
        return element


    def _put_count(self, element):
        self._put_simplex(element)
        self.elements += 1
        if self.elements <= self.size: return False
        else                         : return True


    def _get_count(self):
        if not self.elements:
            return None
        else:
            self.elements -= 1
            return self._get_simplex()



    def _put_check(self, element):
        if self.elements == self.size:
            return False
        else:
            self._put_simplex(element)
            self.elements += 1
            return True



    def _get_check(self):
        if not self.elements:
            return None
        else:
            self.elements -= 1
            return self._get_simplex()
