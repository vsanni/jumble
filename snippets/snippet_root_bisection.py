"""
Created on Wed Oct 10 12:39:25 2018

@author: vsannibale
"""

import jumble.roots as roots

def f(x): return (x-2)*(x+7)

fig, axis, _,_ = roots.plot_set(f, 0, 5, title="Bisection Finding Roots Method")

print("bisection:")
print(roots.bisection(f,  0, 5, verbose=True, axis =axis))
print(roots.bisection(f,-10, 0))
print(roots.bisection(f,-10, 5))
print(roots.bisection(f,  5,15))
