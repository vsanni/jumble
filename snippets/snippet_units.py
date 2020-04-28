"""
Created on Tue Oct  9 20:56:33 2018

@author: vsanni
"""

import jumble.units as units
import numpy as np

print("Order of Magnitude:")

for om in range(-6,6):
    x = 3.21*10**om
    print("%10.3e, %3d" % (x, units.order_of_magnitude(x)))

x = 0
print("%10.3e, %3d" % (x, units.order_of_magnitude(x)))

#%%
x = 10000

units_prefix, ifactor, om = units.prefix(x)
print("\nunits.prefix(10000) => x = %f %s" %(x*ifactor, units_prefix))

#%%
f = np.logspace(0,6,100)

print("\nunits with prefix:")
print("mode: max", units.prefixed(f,"Hz", mode="max"))
print("mode: min", units.prefixed(f,"Hz", mode="min"))
print("mode: avg", units.prefixed(f,"Hz", mode="avg"))
print("mode: G", units.prefixed(f,"Hz", mode="G"))

#%%
print("\nconvert to standard units:")

print("1 W->dBm", units.standard_convert(1, units="W", standard_units="dBm"))
print("1 dB->W", units.standard_convert(1, units="dB", standard_units="W"))
print("1 nm->m", units.standard_convert(1, units="nm", standard_units="m"))

#%%

print("measurement:")

print("prefixed units                      :", units.measure("P_0", 12.4e3,.012e3, 3, "W"))
print("scientific notation units           :", units.measure("P_0", 12.4e3,.012e3, 3, "W", prefix_units=False))
print("prefixed units latex translated     :", units.measure("P_0", 12.4e-6,.012e-6, 3, "W", latex=True))
print("scientific notation latex translated:", units.measure("P_0", 12.4e-6,.012e-6, 3, "W", latex=True, prefix_units=False))
