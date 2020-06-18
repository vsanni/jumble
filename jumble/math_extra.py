"""
$HeadURL: file:vprint.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""

import numpy as np
from scipy.special import erf

def central_difference_df_dx(f, x, Dx):
    """
    central difference based numerical derivative
    """
    return 0.5*( f(x+Dx)-f(x-Dx) )/Dx


def lorentian(x, x0, Gamma, A=1.0, y0=0.0):
    return A*.5*Gamma/((x-x0)**2+.25*Gamma**2)/np.pi + y0


def gaussian(x, mu=0.0, sigma=1.0, y0=1.0, y1=0.0):
    return y0*np.exp(-0.5*(x-mu/sigma)**2 ) + y1



def normal_pdf(x, mu=0.0, sigma=1.0, y0=None):

    if y0 is None: y0 = 1.0/(np.sqrt(2.0*np.pi)*sigma)

    return y0*np.exp( -0.5*(x-mu/sigma)**2 )


_sqrt_2 = np.sqrt(2.0)

def normal_cdf(x, mu=0.0, sigma=1.0):

    z = ( x - mu )/(_sqrt_2*sigma)

    return 0.5*(1. + erf(z))
