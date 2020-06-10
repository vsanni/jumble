"""
$HeadURL: file:///home/svn/python/lib/vprint.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""

import numpy as np
import jumble.figures as figs

def _error(s): raise ValueError(s)

def interval_check(f, a, b):
    fa = f(a)
    fb = f(b)

    if fa*fb > 0:
        _error("roots.interval_check: error, intial function values from the interval extremities %g, and %g have same sign " % (a,b))

    return fa, fb


def secant(f, a, b, tol=1.e-6, N=100, verbose=False, axis= None):
    """
        Purpose: finds a root of a function using the bisection method

        Synopsis: x, n = roots_secant(f, a, b, tol, N)

        f        function
        a, b    range
        tol      maximum tolerated systematic error from function zero. tol=1.e-6
        N        maximum number of iteration befor exiting. Default N=100
        verbose  if True prints the x and f(x) during the search. Default verbose=False

        x        function zero found if n < N
        n       number of iteration done


        Example: x, n = roots_secant(sin, -1, 2, 1.e-8, 10)
    """

    a      = float(a)
    b      = float(b)

    fa, _ = interval_check(f, a, b)

    abs_fx = abs(fa)
    for n in range(1, N+1):

        Df     = f(b)-f(a)
        if   a == b:
            _error("roots.bisection: error, failed to converge, Df is zero, error %e , tolerance %e, iterations %d" % ( abs_fx, tol, n ) )
        else:
            x      = b-f(b)*(b-a)/Df
            a      = b
            b      = x
            abs_fx = abs(f(x))

            if verbose         : print("%3d, %21.14e, %21.14e" % (n, x, f(x)) )
            if axis is not None: _plot(axis, f,a,b, n)

        if abs_fx <= tol: break

    if abs_fx > tol: _error("roots.bisection: error, failed to converge, error %e , tolerance %e, iterations %d" % ( abs_fx, tol, n ) )

    return x, n



def bisection(f, a, b, tol=1.e-6, N=100, verbose=False, axis=None):
    """
    Purpose: finds a root of a function using the bisection method

    Synopsis: x, n = roots_bisection(f, a, b, tol, N)

    f        function object

    a, b      range

    tol      maximum tolerated systematic error from function zero. tol=1.e-6

    N        maximum number of iteration befor exiting. Default N=100

    verbose  if True prints the current zero estimation x, and f(x)
             during the search. Default verbose=False

    Returns
    -------

    x        function zero found if n < N

    n        number of iteration done

    Example: x, n = root_bisection(sin, -1, 2, 1.e-8, 100)
    """

    interval_check(f, a, b)

    for n in range(1, N+1):
        x  = (a+b)/2.0

        if verbose         : print("%3d, %21.14e, %21.14e" % (n, x, f(x)) )
        if axis is not None: _plot(axis, f,a,b, n)

        fx = f(x)
        t  = f(b)*fx
        if   t < 0: a = x
        elif t > 0: b = x
        else      : break

        if abs(fx) <= tol: break

    if abs(fx) > tol: _error("root.bisection: error, failed to converge, error %e , tolerance %e, iterations %d" % ( abs(fx), tol, n ) )

    return x, n



def newton(f, a, b, tol=1.e-6, N=100, df_dx=None, verbose=False, axis=None):
    """
    Purpose: finds a root of a function using the Newton's method

    Synopsis: x, n = roots_bisection(f, a, b, tol, N)

    f        function object

    a, b      range

    tol      maximum tolerated systematic error from function zero. tol=1.e-6

    N        maximum number of iteration befor exiting. Default N=100

    verbose  if True prints the current estimated zero and derivative estimation f(x)
             during the search. Default verbose=False

    x        function zero found if n < N

    n        number of iteration done

    Example: x, n = root_bisection_derivative(sin, -1, 2, 1.e-8, 100)
    """

    def central_difference_df_dx(f, x, Dx):
        """
        central difference based numerical derivative
        """
        return 0.5*( f(x+Dx)-f(x-Dx) )/Dx

    interval_check(f, a, b)

    if df_dx is None: df_dx = central_difference_df_dx
    try:
        x  = 0.5*(a+b)
        dx = x/100
        for n in range(1, N+1):
            Dx = f(x)/(df_dx(f, x, dx)+1e-6)
            if verbose         : print("%3d, %21.14e, %21.14e" % (n, x, f(x)) )
            if axis is not None: _plot(axis, f, x, x-Dx, n)
            x = x-Dx
            if abs(f(x)) <= tol: break
    except:
        _error("roots.newton: error, failed to converge, error %e , tolerance %e, iterations %d" % ( abs(f(x)), tol, n ) )

    n += 1
    if verbose         : print("%3d, %21.14e, %21.14e" % (n, x, f(x)) )
    if axis is not None: _plot(axis, f, a, b, n)

    if abs(f(x)) > tol: _error("roots.newton: error, failed to converge, error %e , tolerance %e, iterations %d" % ( abs(f(x)), tol, n ) )

    return x, n



def plot_set(f,a,b, N=1000, title=None):

    fig, axis = figs.axes()

    X = np.linspace(a, b, N)
    f = [f(x) for x in X]

    axis.plot(X,f)
    axis.grid(True)
    axis.set_xlabel("independent variable, x")
    axis.set_ylabel("dependent variable, y=f(x)")

    if title is not None: axis.set_title(title)

    return fig, axis, X, f



def _plot(axis, f,a,b, n):

    axis.plot([a,b], [f(a), f(b)], "o-", color="C1")
    axis.text(a, f(a), " %d" % n)
