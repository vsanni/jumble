"""
$HeadURL: file:///home/svn/python/lib/SP.py $
$Date: 2014-06-06 19:15:23 -0700 (Fri, 06 Jun 2014) $
$Revision: 13 $
$Author: vsanni $
Testing Class : none
Remarks       :
Author        : Virginio Sannibale, Copyright 2011, vsanni@sbcglobal.net
"""


import jumble.vprint as my
from jumble.type_extra import length, is_whole

import numpy as np

from scipy import signal as signal
from math import factorial

#---------------------------------------------------------
def partition(a, b, dx):

    N = (b-a)/ float(dx)

    if  np.floor(N) != N: return np.arange(a, b, dx)
    else                : return np.arange(a, b+dx, dx)

#---------------------------------------------------------
def savitzky_golay(y, window=31, order=1, deriv=0, rate=1):
    """
    Savitzky-Golay filter to smooth (and optionally differentiate) data.
    The Savitzky-Golay is a type of low-pass filter particularly suited for
    smoothing noisy data. The main idea behind the approach is to make for
    each point a least-square fit with a polynomial of high order over an
    odd-sized window centered at the point [1]_.
    It has the advantage of preserving the original shape and features of the
    signal better than other types of filtering approaches, such as moving
    average techniques.

    Parameters
    ----------
    y : array_like, shape (N, )
        The values of the signal.
    window : int
        The length of the window. Must be an odd integer.
    order : int
        The order of the polynomial used in the filtering.
        Must be less than `window` - 1.
    deriv : int
        The order of the derivative to compute (default = 0 means only
        smoothing)
    rate : int
        Default = 1

    Returns
    -------
    ys : ndarray, shape (N, )
        The smoothed signal (or it's nth derivative).

    Examples
    --------
    t = np.linspace(-4, 4, 500)

    y = np.exp(-t ** 2) + np.random.normal(0, 0.05, t.shape)

    ys = savitzky_golay(y, window=31, order=5)

    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of Data
       by Simplified Least Squares Procedures. Analytical Chemistry, 1964,
       36 (8), 167-1693.

    """
    try:
        window = np.abs(np.int(window))
        order  = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window and order have to be of type int.")

    if window < 1:
        raise ValueError("window must be greater than zero.")

    if window < order + 2:
        raise ValueError("window is too small for the polynomial order.")

    if window % 2 == 0:
        window += 1

    hw = (window - 1) // 2

    # precompute coefficients
    b = np.mat([ [n ** k for k in range(order + 1)] for n in range(-hw, hw + 1)])

    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)

    # Pad the signal at the ends with values taken from the signal itself

    first_vals = y[ 0] - np.abs(y[1:hw + 1  ][::-1] - y[ 0])
    last_vals  = y[-1] + np.abs(y[-hw - 1:-1][::-1] - y[-1])

    y          = np.concatenate((first_vals, y, last_vals))

    return np.convolve(m[::-1], y, mode='valid')



def moving_average(x, n=3):

    if n<=0 : raise ValueError('error, average number must be greater than 1')

    N    = len(x)
    y    = np.empty(N-n+1, np.dtype(x.dtype))
    y[0] = np.sum(x[0:n])

    for i in range(0, N-n): y[i+1] = y[i] - x[i] + x[i+n]

    return y/n



def max_power_of_two(n): return int(np.log2(n))

#---------------------------------------------------------
def window_calc(N, Type='hanning'):
    # windows dictionary
    Window = {
               'hamming'         : signal.hamming,
               'hanning'         : signal.hanning,
               'bartlett'        : signal.bartlett,
               'blackman'        : signal.blackman,
               'blackmanharris'  : signal.blackmanharris
              }

    return Window[Type](N)


#---------------------------------------------------------
def window_norm_factor(w):
    #normalization factor per each fft of with a window of lenght N
    N          = len(w)
    W          = np.fft.fft(w)/N
    return 1/(N/2*np.real(W[0]))


#---------------------------------------------------------
def _window_set_stuff(x, w, a, Type='hanning'):

    N = len(x)

    if w is None:
        window_len = 2**max_power_of_two(N)
        w	       = window_calc(window_len, Type)

    elif isinstance(w, str):
        window_len = 2**max_power_of_two(N)
        w	       = window_calc(window_len, w)

    else:
        window_len = max(w.shape)


    window_half_len = int(window_len/2)
    NFFT            = window_half_len+1
    window_step     = int(np.floor(window_len*(1-a)))

    if N < window_len:
       raise Exception('SP._window_set_stuff: error not enough data points for the window and therefore for the required frequency bin')

    return N, NFFT, window_len, window_half_len, window_step, w



#---------------------------------------------------------
def _PS_DC_Value(x):
    # P[0] /= 4 #adjust DC value without considering the detrending
    return  np.mean(x)**2 # to avoid wrong DC value when data are detrended


#---------------------------------------------------------
def PS(x, w=None, a=0.5, sf=1.0, detrend=1, P=None, windows=0):

    N, NFFT, window_len, window_half_len, window_step, w = _window_set_stuff(x, w, a)

    sf   = float(sf)

    if P == None: P  = 0.0
    else        : P *= windows

    if   detrend==3: x = signal.detrend(x, type='constant')
    elif detrend==4: x = signal.detrend(x, type='linear'  )

    s = 0
    e = window_len
    while e <= N:
        if   detrend==1: X = np.fft.fft(signal.detrend(x[s:e], type='constant')*w)
        elif detrend==2: X = np.fft.fft(signal.detrend(x[s:e], type='linear'  )*w)
        else           : X = np.fft.fft(               x[s:e]                 *w)

        P       += X[:NFFT]*np.conj(X[:NFFT])
        s       += window_step
        e       += window_step
        windows += 1

    norm_factor =  window_norm_factor(w)**2

    P     = np.real(P)*norm_factor/windows #drop the imaginary part which should be zero and make a real vector
    P[0] /= 4 #adjust DC value
    df    = sf/window_len
    f     = np.linspace(0, NFFT, NFFT)*df

    return f, P, windows, norm_factor


#---------------------------------------------------------
def PSD(x, w=None, a=0.5, sf=1, detrend=1, P=None, windows=0):

    f, P, windows, norm_factor = PS(x, w, a, sf, detrend, P, windows)

    P = P/f[1]

    return f, P, windows, norm_factor


#---------------------------------------------------------
def FR(xi, xo, sf=1.0, w=None, a=0.5 , detrend=1):

    N, NFFT, window_len, window_half_len, window_step, w = _window_set_stuff(xi, w, a)

    if   detrend==3: xi, xo = signal.detrend(xi, type='constant'), signal.detrend(xo, type='constant')
    elif detrend==4: xi, xo = signal.detrend(xi, type='linear'  ), signal.detrend(xo, type='linear'  )

    sf   = float(sf)

    A    = np.zeros(NFFT)
    C    = np.zeros(NFFT)
    PIn  = np.zeros(NFFT)
    POut = np.zeros(NFFT)

    windows = 0
    s       = 0
    e       = window_len

    while e <= N:
        if   detrend == 1: In, Out = np.fft.fft(signal.detrend(xi[s:e], 'constant')*w), np.fft.fft(signal.detrend(xo[s:e], 'constant')*w)
        elif detrend == 2: In, Out = np.fft.fft(signal.detrend(xi[s:e], 'linear'  )*w), np.fft.fft(signal.detrend(xo[s:e], 'linear'  )*w)
        else             : In, Out = np.fft.fft(               xi[s:e]             *w), np.fft.fft(               xo[s:e]             *w)

        C       += Out[:NFFT]*np.conj(In[:NFFT])
        A       += np.abs(Out[:NFFT])/np.abs(In[:NFFT])
        PIn     += In *np.conj(In[:NFFT] )
        POut    += Out*np.conj(Out[:NFFT])

        s       += window_step
        e       += window_step
        windows += 1


    norm_factor =  window_norm_factor(w)**2

    PIn     = PIn/windows*norm_factor
    PIn[0] /= 4 #adjust DC value

    POut     = POut/windows*norm_factor
    POut[0] /= 4 #adjust DC value

    P      = np.angle(C)
    A      = np.abs  (A)/windows

    CC     = np.conj(C)*C/windows**2
    CF     = CC/(PIn*POut)

    df     = sf/window_len
    f      = np.linspace(0, NFFT, NFFT+1)*df

    return f, A, P, PIn, POut, CC, CF, windows, norm_factor



def SR( f0, xi, xo, sf=1, w=None, a=0.5 , detrend=1):

    F, A, P, PIn, POut, CC, CF, windows, norm_factor = FR( xi, xo, sf, w, a, detrend)

    if  f0 is None:
        f    = my.ThreePointsMax(F, A, 0)
        _, i = np.max(A)

    else:
        n = np.where((f0-F[1]*2 < F) & (F < f0+F[1]*2 ))[0]
        f = my.ThreePointsMax(F[n], A[n], 0, -1)

        if f != -1:
            _, i = np.max(A[n])
            i   += n[0]-1
        else:
            i = np.floor(np.mean( np.where((f0-F[1]*2 < F) & (F < f0+F[1]*2 ))[0] ))
            f = f0

    if i >0:
        a    = A[i]
        p    = P[i]
        cf   = CF[i]
        cc   = CC[i]
        pin  = PIn[i]
        pout = POut[i]
    else:
        a    = np.NaN
        p    = np.NaN
        cf   = np.NaN
        cc   = np.NaN
        pin  = np.NaN
        pout = np.NaN

    return f, a, p, pin, pout, cc, cf, F, A, P, PIn, POut, CC, CF, windows, norm_factor



def mixer(t, x, f0 =1.0, phi0=0.0):
    """
    synopsis: xx = mixer(t, x, f0 =1.0, phi0=0.0)

       t           time vector
       x           signal
       f0          LO frequency
       phi0        LO phase shift

     Examples:
              X = mixer( 0.001, sin( 2*np.pi*12.5*np.arange(0,10,.001)+pi/2) , 12.5, 0.0)
    """

    if length(t) == 1: t = np.arange(len(x))*t

    return x*np.exp(1j*2.0*np.pi*f0*t+phi0)



def lock_in(t, x, f0 =1.0, phi0=0.0, order=2, fc=None, zero_phase=True):
    """
    synopsis: lock_in(t, x, f0 =1.0, phi0=0.0, order=2, fc=None, zero_phase=True)

       t           time vector
       x           signal
       f0          lock in frequency
       phi0        lock in phase shift

     Examples:
              X = lock_in( 0.001, sin( 2*np.pi*12.5*np.arange(0,10,.001)+pi/2) , 12.5, 0.0)
    """

    if not is_whole(order): raise ValueError("lock_in: error, parameter order must whole number.")

    if fc is None    : fc = f0*1.3
    if length(t) == 1: t = np.arange(len(x))*t

    xx   = x*np.exp(1j*2.0*np.pi*f0*t+phi0)

    b, a = signal.butter(order//2 if zero_phase else order, 2*np.pi*fc, 'lowpass', analog=True)

    if   zero_phase: return 2*signal.filtfilt(b, a, xx)
    else           : return 2*signal.lfilter (b, a, xx)


#---------------------------------------------------------
def envelope(x, y, Dy=0.0, max_min=0):
    """
    synopsis: envelope(x, y, Dy=0.0, max_min=0)

       Y
       max_min
    """

    y0           = y[0]
    look_for_max = y[1] > y0

    X, Y, N = [], [], []

    for n, _y in enumerate(y):
         if look_for_max:
             if Dy < y0 - _y:
               look_for_max = False
               if max_min != 2:
                    N.append(n-1)
                    X.append(x[n-1])
                    Y.append(y0)
         else:
             if Dy < _y - y0:
                look_for_max = True
                if max_min != 1:
                    N.append(n-1)
                    X.append(x[n-1])
                    Y.append(y0)

         y0 = _y

    return X, Y, N


#---------------------------------------------------------
def MaxSkim(x, y, Dx=0.0):

    N   = []
    X   = []
    Y   = []

    n0 = 0
    n1 = 1
    for n in range(1, len(x)):
        if (Dx > x[n]-x[n0]):
            n1 = n
        else:
            _n = np.argmax(y[n0:n1])
            _y = y[_n]
            N.append(n0+_n)
            X.append(x[n0+_n])
            Y.append(_y)
            n0 = n
            n1 = n+1

    return X, Y, N



def PeakFind(x, y, Dx=0.0, Dy=0.0, Filter = ("moving_average", 5)):

    if (Filter[0] == "moving_average"):
       y0 = moving_average(y, Filter[1])
       x0 = x[0:len(y0)]+(x[1]-x[0])*Filter[1]

    elif (Filter[0] == "savitzky_golay"):
       y0 = savitzky_golay(y, *Filter[1:])
       x0 = x

    else:
       y0 = y
       x0 = x

    x1, y1, n1 = envelope(x0, y0, Dy, max_min=1)
    x2, y2, n2 = MaxSkim(x1, y1, Dx)

    return x2, y2, n2, x1, y1, n1, x0, y0



def zero_crossing(t,x):

    sign = np.sign(x-np.mean(x)).astype(int)
    ds   = np.abs(sign[:-1]-sign[1:])
    n    = np.where(ds > 0)[0]

    return ( x[n+1]*t[n]-x[n]*t[n+1] ) / (x[n+1]-x[n])



def period(t,x):

    t0 = zero_crossing(t,x)

    return 2*(t0[-1]-t0[0])/( t0.size-1), t0
