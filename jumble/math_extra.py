"""
$HeadURL: file:vprint.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""


def central_difference_df_dx(f, x, Dx):
    """
    central difference based numerical derivative
    """
    return 0.5*( f(x+Dx)-f(x-Dx) )/Dx
