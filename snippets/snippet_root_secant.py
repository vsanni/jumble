"""
Created on Wed Oct 10 12:39:25 2018

@author: vsannibale
"""

import jumble.roots as roots

def f(x): return (x-2)*(x+7)

fig, axis, _,_ = roots.plot_set(f, 0, 5, title="Secant Finding Roots Method")

print("secant:")
print(roots.secant(f,  0, 5, verbose=True, axis =axis))
print(roots.secant(f,-10, 0))
print(roots.secant(f,-10, 5))
print(roots.secant(f,  5,15))
