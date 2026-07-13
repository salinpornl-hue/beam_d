# beam_d

`beam_d` is a beam-only structural-engineering toolkit. The analysis core is intentionally based on a **2D planar frame element** so the same foundation can later support straight beams, stepped-top beams, stepped-bottom beams, vertical offsets, and sloped/Z-shaped beam axes.

## Open the program with one click on Windows

1. Download the `agent/frame-core-foundation` branch as a ZIP file.
2. Extract the ZIP file to a normal folder. Do not run it from inside the ZIP.
3. Double-click `OPEN_BEAM_D.bat`.
4. On the first run, wait while the launcher creates a private Python environment and installs the required packages.
5. The Streamlit program opens automatically in the default browser.
6. Keep the black launcher window open while using the program. Close it to stop beam_d.

Python 3.10 or newer is required. During Python installation, select **Add Python to PATH**. See `HOW_TO_OPEN.txt` for troubleshooting.

## Current engineering scope

This first increment provides the verified global-analysis foundation:

- three degrees of freedom per node: horizontal displacement `u`, vertical displacement `v`, and rotation `θ`
- axial and flexural stiffness (`EA` and `EI`)
- local-to-global coordinate transformation
- nodal forces and moments
- full-length uniform element loads in local axes
- prescribed translational and rotational restraints
- nodal displacements, support reactions, and local member-end forces
- global force and moment equilibrium residuals
- benchmark tests for simply supported, cantilever, and axial cases

## Important limitation

A successful global frame analysis does **not** verify an abrupt step, re-entrant corner, or Z-beam transition. Those regions are geometric discontinuities (D-regions) and require a separate local design process such as a code-compliant strut-and-tie assessment, anchorage checks, and local reinforcement detailing.

The software will keep these statuses separate:

1. global analysis
2. ordinary beam-region design
3. local discontinuity-region design

## Example

```python
from beam_d import FrameModel2D, Node, SectionProperties

model = FrameModel2D()
model.add_node(Node("A", x=0.0, y=0.0))
model.add_node(Node("B", x=6_000.0, y=0.0))

section = SectionProperties(
    elastic_modulus=30_000.0,  # N/mm²
    area=180_000.0,            # mm²
    second_moment=5.4e9,       # mm⁴
)

model.add_element("AB", "A", "B", section)
model.set_restraint("A", ux=True, uy=True, rz=False)
model.set_restraint("B", ux=False, uy=True, rz=False)
model.add_uniform_load("AB", qy=-20.0)  # N/mm = 20 kN/m downward

result = model.solve()
print(result.reaction("A"))
print(result.element_results["AB"].end_forces_local)
```

## Units

The solver is unit-consistent rather than unit-prescriptive. A recommended internal system is:

- length: mm
- force: N
- moment: N·mm
- stress / elastic modulus: N/mm² (MPa)
- distributed load: N/mm

All inputs in one model must use a single consistent system.

## Development sequence

1. 2D frame analysis core and verification
2. load cases, combinations, live-load patterning, and envelopes
3. ordinary rectangular RC beam flexure and shear design
4. serviceability and reinforcement fit checks
5. stepped geometry, centroid offsets, and rigid links
6. explicit D-region / strut-and-tie workflow
7. reviewed reinforcement detailing

See [`docs/engineering_basis.md`](docs/engineering_basis.md) for the governing engineering decisions and exclusions.
