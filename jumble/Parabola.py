"""
$HeadURL: file:///home/svn/python/lib/Parabola.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""

def Parabola(x, a,b,c)                : return 1.0*a*x**2+b*x+c

def ParabolaVertexForm(x, a,h,k)      : return 1.0*a*(x-h)**2+k

def ParabolaVertexToStandard(a, h, k ): return  a, -2.0*a*h, 1.0*a*h**2+k

def ParabolaStandardToVertex(a, b, c ): return  a, -b/(2.0*a), c - b**2/(4.0*a)  
    
def ParabolaFromThreePoints(x, y):
    """
    Purpose: find parabolas coefficientsstarting from three points ona plane.

    Synopsis: a, b, c =ParabolaThreePoint(x, y)

    a, b, c     parabola coeff
    x, y       parabola points

              y = ax**2 + bx + c

    Example: a, b, c = ParabolaThreePoint([0, 1, 2], [-1, 0, 3])
    """

    Delta=(x[2]*x[0]**2-x[1]*x[0]**2+x[1]*x[2]**2-x[0]*x[2]**2+x[0]*x[1]**2-x[2]*x[1]**2)

    a=-(-x[2]*y[0]+x[0]*y[2]+x[1]*y[0]+x[2]*y[1]-x[1]*y[2]-x[0]*y[1])/Delta
    b=(-x[2]**2*y[0]+x[2]**2*y[1]+y[2]*x[0]**2-y[1]*x[0]**2+x[1]**2*y[0]-y[2]*x[1]**2)/Delta
    c=(-y[2]*x[1]*x[0]**2+x[1]**2*x[0]*y[2]+x[2]**2*x[1]*y[0]-x[2]**2*x[0]*y[1]+y[1]*x[2]*x[0]**2-x[1]**2*x[2]*y[0])/Delta

    return a, b, c


def ParabolaVertexCoord(a, b, c):

    x0 = -b/(2*a)
    
    return x0, Parabola(x0, a, b, c)
