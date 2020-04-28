"""
Created on Wed Oct 10 12:39:25 2018

@author: vsannibale
"""

from jumble.text_manipulation import find_strings

s = "This is not a string\"\"\"string between 3 double quotes\"\"\"'string between single quotes' not a string\"string between double quotes\""

N0,N1 = find_strings(s)

for n0,n1 in zip(N0,N1):
    print("<%s>" % s[n0:n1])
