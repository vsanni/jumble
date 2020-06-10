"""
Created on Wed Oct 10 12:39:25 2018

@author: vsannibale
"""

import jumble.roots as roots

def f(x): return (x-2)*(x+7)

roots.figs.close_all()

fig, axis, _,_ = roots.plot_set(f, 0, 5, title="Secant Finding Roots Method")

print("Secant:")
print(roots.secant(f,  0, 5, verbose=True, axis =axis))
print(roots.secant(f,-10, 0))
print(roots.secant(f,  4, 10)) # cannot work sign f(4) == sign f(8)
