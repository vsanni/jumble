"""
Created on Tue Oct  9 20:56:33 2018

@author: vsanni
"""


from jumble.circular_buffer import CircularBuffer

cb  = CircularBuffer(size= 3, book_keeping=False)

for n in range(10):
    cb.put(n)
    cb.print()

print("-"*10)

for n in range(10):
    print(cb.get())
    cb.print()
