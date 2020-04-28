"""
Created on Wed Oct 10 12:39:25 2018

@author: vsannibale
"""

from jumble.text_manipulation import tag_find_chunks

s = "This is not a string\"\"\"string between 3 double quotes\"\"\"'string between single quotes' not a string\"string between double quotes\""

N0,N1,string = tag_find_chunks(s)

for n0,n1,a in zip(N0,N1,string):
    print("<%s>" % s[n0:n1],a)

