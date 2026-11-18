# Topic map — a complete Multiple Integral chapter

Derived from the six source parts and the pre-built prompt set under
`Maths Chapters/NOTES_OUTPUT/MULTIPLE INTEGRAL`. A full-mode book on this
chapter should cover every item below. Values in the last column were checked
before printing; `verify_math.py` now asserts them.

## 1. Double integrals
- Definition as a limit of sums; Fubini's theorem for continuous functions.
- Constant limits on a rectangle: `∬_R f dx dy = ∫_c^d[∫_a^b f dx]dy`.
- Variable limits: integrate the variable pair first; match limits to the
  differential.
- Standard results: `4`, `π²/4`, `2π`, `3/35`, `9/8`, `πa³/6`.

## 2. Change of order
- Four-step algorithm: read the boundaries, sketch the region, reverse the
  strip direction, write new limits. Never swap symbols without the sketch.
- Vertical strips (`dy dx`) ↔ horizontal strips (`dx dy`).
- Region types: triangle, parabolic strip, quarter circle, circle through the
  origin.
- Results: `πa/4`, `16a²/3`, `1`, `(e−1)/2`, `32/3`.

## 3. Polar form
- `x = r cos θ`, `y = r sin θ`, `x² + y² = r²`, **`dA = r dr dθ`**.
- Circles `r = a`, `r = a cos θ`, cardioid `r = a(1 + cos θ)`, lemniscate
  `r² = a² cos 2θ`.
- Results: `3πa²/4`, `π/4`, `a²`, `3π`.

## 4. Applications: area, mass, centre of mass
- Area `A = ∬_R dA`; choose Cartesian or polar limits.
- Mass `M = ∬_R δ dA`; moments `M_x = ∬ yδ dA`, `M_y = ∬ xδ dA`.
- Centre of mass `(x̄, ȳ) = (M_y/M, M_x/M)`.
- Results: `1/6`, `πab/2`, `16a²/3`; triangular plate with `δ = 6x+6y+6` on
  `0≤x≤1, 0≤y≤2x` gives `M = 14`, `M_x = 11`, `M_y = 10`,
  `(x̄, ȳ) = (5/7, 11/14)`.

## 5. Triple integrals
- Cartesian order `dz dy dx`, one variable at a time.
- Cylindrical `dV = r dz dr dθ`.
- Spherical `dV = ρ² sin φ dρ dφ dθ`.
- Results: `1/48` over the unit octant with `xyz`, `1/6` over a tetrahedron,
  `4πa³/3` for a sphere, `5πa³/64` for the cylindrical solid.

## 6. Transformations and Jacobians
- `J = ∂(x,y)/∂(u,v)`; if given `J' = ∂(u,v)/∂(x,y)`, then `|J| = 1/|J'|`.
- `dx dy = |J| du dv`; polar is the special case `J = r`.
- Oblique regions such as `y−x = u`, `3y+x = v` become rectangles.
- Dirichlet over `x,y,z ≥ 0, x+y+z ≤ 1`, with Gamma ratios; Liouville's
  extension for `(x/a)^p + (y/b)^q + (z/c)^r ≤ 1`.
- Symmetry: an odd integrand over a region symmetric about that axis is zero.
- Result: `∬(y−x) dA = −2` over `−3≤u≤1, 5≤v≤7`.

## Common mistakes
1. Changing the order without sketching the region.
2. Forgetting the polar factor `r`, or `ρ² sin φ` in spherical form.
3. Using `y³` for `∫y² dy` instead of `y³/3`.
4. Inverted inner limits producing a negative "area".
5. Leaving the inner variable in the outer integrand.

## Exam-focus topics
Change of order; Cartesian-to-polar conversion; Jacobians; area, mass and
volume applications. These are curriculum topics, not tags printed in the PDF
— `GATE_TAGGING` stays off.
