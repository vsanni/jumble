"""
Created on Tue Oct  9 20:56:33 2018

@author: vsanni
"""


from jumble.text_manipulation import Camel2snake,tag_find_chunks,read_text_file

s = read_text_file("../../jumble/jumble/figures.py")
N0, N1, StringFlag = tag_find_chunks(s)

for n0, n1, sFlag in zip(N0, N1,StringFlag):
    if sFlag:  print(s[n0:n1], end="")
    else    :  print(Camel2snake(s[n0:n1]), end="")

