"""
Created on Sun Sep 21 17:43:40 2014

@author: vsanni
"""


class CircularBuffer:

    def __init__(self, size= 8192, book_keeping= False):

        self._buffer      = [None]*size # no real need to allocate mem in pyhon when you don't know what you are going to save in the circular bufffer
        self.element_size = 1
        self.size         = size
        self.max          = size-1
        self.book_keeping = book_keeping

        self.reset()

    @property
    def book_keeping(self): return self._book_keeping

    @book_keeping.setter
    def book_keeping(self,v):
        if not type(v) is bool: raise ValueError("CircularBuffer(): error, book_keeping value must be boolean.")

        self._book_keeping = True if v else False

        if self._book_keeping: self.put, self.get = self._put_complex, self._get_complex
        else                 : self.put, self.get = self._put_simplex, self._get_simplex



    def reset(self):

        self.tail     = 0
        self.head     = 0
        self.elements = 0


    def is_empty(self): return self.elements == 0


    def print(self, s= None):

        print("_buffer       :", self._buffer)
        print("head, element:", self.head , self._buffer[self.head])
        print("tail, element:", self.tail , self._buffer[self.tail])
        print("elements     :", self.elements)



    def _put_simplex(self, element):
        self._buffer[self.head] = element
        if self.head >= self.max: self.head  = 0
        else:                     self.head += 1
        return True


    def _get_simplex(self):
        element = self._buffer[self.tail]
        if   self.tail >= self.max: self.tail  = 0
        else                      : self.tail += 1
        return element


    def _put_complex(self, element):
        self._put_simplex(element)
        self.elements += 1
        if self.elements <= self.size: return False
        else                         : return True


    def _get_complex(self):

        if not self.elements:
            return None
        else:
            self.elements -= 1
            return self._get_simplex()
