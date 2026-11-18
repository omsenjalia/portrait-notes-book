"""math_values.py — one source of truth for every number printed in a book.

Build scripts format results through MX(key); verify_math.py recomputes the
same values numerically and asserts they match. A typo in a worked result,
answer key or practice item therefore fails before delivery.
"""
VALUES = {
    'four':        (r'4',                                              4.0),
    'pi2_4':       (r'\frac{\pi^2}{4}',                                0.0),  # computed below
    '3_35':        (r'\frac{3}{35}',                                   3 / 35),
    '9_8':         (r'\frac{9}{8}',                                    9 / 8),
    'pi_a3_6':     (r'\frac{\pi a^3}{6}',                              0.0),
    '3pi_a2_4':    (r'\frac{3\pi a^2}{4}',                             0.0),
    '2a3_3':       (r'\frac{2a^3}{3}',                                 0.0),
    '13_4':        (r'\frac{13}{4}',                                   13 / 4),
    '9_4':         (r'\frac{9}{4}',                                    9 / 4),
    'pi_a2_2':     (r'\frac{\pi a^2}{2}',                              0.0),
    '1_12':        (r'\frac{1}{12}',                                   1 / 12),
    '10_3':        (r'\frac{10}{3}',                                   10 / 3),
    '1_2':         (r'\frac{1}{2}',                                    1 / 2),
    '1_3':         (r'\frac{1}{3}',                                    1 / 3),
    'ln_ratio':    (r'\ln\!\left(\tfrac a2\right)\ln\!\left(\tfrac b2\right)', 0.0),
    'e_1_2':       (r'\frac{e-1}{2}',                                  0.0),
    'pi_4':        (r'\frac{\pi}{4}',                                  0.0),
    'one':         (r'1',                                              1.0),
    'e8_1_4':      (r'\frac{e^8-1}{4}',                                 0.0),
    'neg_1_24':    (r'-\frac{1}{24}',                                  -1 / 24),
    '26_3':        (r'\frac{26}{3}',                                   26 / 3),
    'sphere_vol':  (r'\frac{4\pi a^3}{3}',                             0.0),
}

# Fill the symbolic entries once, from the same constants the checker uses.
import math as _m
VALUES['pi2_4']    = (VALUES['pi2_4'][0], _m.pi ** 2 / 4)
VALUES['pi_a3_6']  = (VALUES['pi_a3_6'][0], _m.pi / 6)          # a = 1
VALUES['3pi_a2_4'] = (VALUES['3pi_a2_4'][0], 3 * _m.pi / 4)     # a = 1
VALUES['2a3_3']    = (VALUES['2a3_3'][0], 2 / 3)                # a = 1
VALUES['pi_a2_2']  = (VALUES['pi_a2_2'][0], _m.pi / 2)          # a = 1
VALUES['ln_ratio'] = (VALUES['ln_ratio'][0], _m.log(3 / 2) * _m.log(2))  # a=3,b=4
VALUES['e_1_2']    = (VALUES['e_1_2'][0], (_m.e - 1) / 2)
VALUES['pi_4']     = (VALUES['pi_4'][0], _m.pi / 4)
VALUES['e8_1_4']   = (VALUES['e8_1_4'][0], (_m.e ** 8 - 1) / 4)
VALUES['sphere_vol'] = (VALUES['sphere_vol'][0], 4 * _m.pi / 3)



# Full-chapter book values (a = 1 where a symbolic result is printed)
VALUES['area_para']   = (r'\frac{1}{6}', 1/6)
VALUES['ellipse_half'] = (r'\frac{\pi ab}{2}', _m.pi/2)
VALUES['octant_xyz']  = (r'\frac{1}{48}', 1/48)
VALUES['cyl_solid']   = (r'\frac{5\pi a^3}{64}', 5*_m.pi/64)


def MX(key):
    """Canonical LaTeX for a named result."""
    return VALUES[key][0]


def num(key):
    return VALUES[key][1]
