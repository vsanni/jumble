"""
Created on Tue Oct  9 20:56:33 2018

@author: vsanni
"""


from jumble.circular_buffer import CircularBuffer

cb  = CircularBuffer(size= 3, mode="overlap_check")

cb.print()

print("----"*20)

for n in range(3+2):
    print("putting:",n+10)
    cb.put(n+10)
    cb.print()

print("----"*20)

for n in range(5):
    print("get          :", cb.get())
    cb.print()
