"""
Created on Tue Oct  9 20:56:33 2018

@author: vsanni
"""

import jumble.units as us
import numpy as np

print("Order of Magnitude:")

for om in range(-6,6):
    x = 3.21*10**om
    print("    %10.3e, %3d" % (x, us.order_of_magnitude(x)))

x = 0
print("    %10.3e, %3d" % (x, us.order_of_magnitude(x)))

#%%
x = 10000
units_prefix, ifactor= us.prefix(x)
print("\nunits.prefix(%g) => x = %g %s" %(x, x*ifactor, units_prefix))

#%%
f = np.logspace(0,6,3)

print("\nunits with prefix (units.prefixed):")
print("    mode: max   =>", us.prefixed(f,"Hz", mode="max"))
print("    mode: min   =>", us.prefixed(f,"Hz", mode="min"))
print("    mode: range =>", us.prefixed(f,"Hz", mode="range"))
print("    mode: M     =>", us.prefixed(f,"Hz", mode="M"))

#%%
print("\nconvert to new units:")

print("   1 W->dBm", us.convert(1, old_units="W" , new_units="dBm"))
print("   1 dB->W" , us.convert(1, old_units="dB", new_units="W"))
print("   1 nm->m" , us.convert(1, old_units="nm", new_units="m"))

#%%

print("\nmeasurement:")

print("    prefixed units                      :", us.measure("P_0", 12.4e3 ,.012e3  ,"W"))
print("    scientific notation units           :", us.measure("P_0", 12.4e3 ,.012e3  ,"W", prefix_units=False))
print("    prefixed units latex translated     :", us.measure("P_0", 12.4e-6,.012e-6,"W", latex=True))
print("    scientific notation latex translated:", us.measure("P_0", 12.4e-6,.012e-6,"W", latex=True, prefix_units=False))
