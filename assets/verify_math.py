"""verify_math.py — recompute every result the books print; exit 1 on any FAIL.

Pure Python (fractions where exact, composite Simpson otherwise). Keeps the
worked examples, answer key and practice items honest: values come from
math_values.py, the single source of truth, and are checked against fresh
numerical integration of the stated integrands and limits.
"""
import math, sys
from math_values import VALUES

def simpson(f, a, b, n=200):
    if n % 2: n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3

def dbl(f, x0, x1, ylo, yhi, n=120):
    """Integrate f(x,y) with y limits that may depend on x."""
    def outer(x):
        lo, hi = ylo(x), yhi(x)
        return (simpson(lambda y: f(x, y), lo, hi, n=160) if hi >= lo
                else -simpson(lambda y: f(x, y), hi, lo, n=160))
    return simpson(outer, x0, x1, max(n, 240))

# Each entry: key -> (freshly computed value, relative tolerance)
C = {}
C['four']       = (dbl(lambda y, x: 1 - 6*x*x*y, -1, 1, lambda y: 0, lambda y: 2), 1e-9)
C['pi2_4']      = (simpson(lambda u: 1.0, 0, math.pi/2) ** 2, 1e-9)  # x=sin u kills the singularity
C['3_35']       = (dbl(lambda x, y: x*x + y*y, 0, 1, lambda x: x, lambda x: math.sqrt(x)), 1e-5)
C['9_8']        = (dbl(lambda x, y: x*y, 1, 2, lambda y: y, lambda y: 2), 1e-9)
C['pi_a3_6']    = (dbl(lambda th, u: math.sin(u) * math.cos(u)**2, 0, math.pi/2,
                       lambda th: 0, lambda th: math.pi/2), 1e-7)  # r=sin u removes the endpoint singularity
C['3pi_a2_4']   = (dbl(lambda th, r: r, 0, math.pi,
                       lambda th: 0, lambda th: 1 + math.cos(th)), 1e-8)
C['2a3_3']      = (dbl(lambda th, r: r*r*math.sin(th), 0, math.pi/2,
                       lambda th: 0, lambda th: 2*math.cos(th)), 1e-7)
C['13_4']       = (dbl(lambda y, x: 1 + 3*x*y, 1, 2, lambda y: 0, lambda y: 1), 1e-9)
C['9_4']        = (dbl(lambda y, x: 3*x*y, 1, 2, lambda y: 0, lambda y: 1), 1e-9)
C['1_12']       = (dbl(lambda th, x: x*x*math.cos(th), 0, math.pi/2,
                       lambda th: 0, lambda th: 1 - math.sin(th)), 1e-7)
C['10_3']       = (dbl(lambda x, y: x*x + y*y, 0, 1, lambda x: 0, lambda x: 2), 1e-9)
C['1_2']        = (dbl(lambda x, y: 1.0, 0, 1, lambda x: 0, lambda x: x), 1e-9)
C['1_3']        = (dbl(lambda x, y: x*x + y*y, 0, 1, lambda x: 0, lambda x: x), 1e-9)
C['ln_ratio']   = (dbl(lambda y, x: 1/(x*y), 2, 3, lambda y: 2, lambda y: 4), 1e-8)
C['e_1_2']      = (dbl(lambda x, y: math.exp(y/x) if x > 0 else 0, 0, 1,
                       lambda x: 0, lambda x: x), 1e-4)
C['pi_4']       = (dbl(lambda th, r: r, 0, math.pi, lambda th: 0, lambda th: math.sin(th)), 1e-9)
C['one']        = (dbl(lambda x, y: x*y, 0, 1, lambda x: 0, lambda x: 2), 1e-9)
C['e8_1_4']     = (simpson(lambda y: math.exp(2*y) / 2, 0, 4, n=400), 1e-8)  # inner x integral cancels
C['neg_1_24']   = (dbl(lambda x, y: x*y, 0, 1, lambda x: x, lambda x: x*x), 1e-8)
C['26_3']       = (simpson(lambda x: 2*x*x + 8, 0, 1), 1e-12)  # y^3 (no /3) slip value
C['sphere_vol'] = (8 * C['pi_a3_6'][0], 2e-5)

fails = 0
print(f'{"KEY":12s} {"COMPUTED":>14s} {"EXPECTED":>14s} {"REL.ERR":>10s}  RESULT')
for key, (computed, tol) in C.items():
    expected = VALUES[key][1]
    err = abs(computed - expected) / (abs(expected) or 1)
    ok = err <= tol
    fails += not ok
    print(f'{key:12s} {computed:14.9g} {expected:14.9g} {err:10.2e}  {"PASS" if ok else "FAIL"}')
print(f'\n{len(C)} values checked, {fails} FAIL(S)')
sys.exit(1 if fails else 0)
