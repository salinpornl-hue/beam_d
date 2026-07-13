# Engineering basis

## 1. Purpose

`beam_d` is limited to beam analysis and beam design. It is not intended to become a general building-analysis package.

The long-term geometric scope is:

- ordinary straight beams
- stepped-bottom beams
- stepped-top beams
- vertical-offset beams
- sloped-offset / Z-shaped beams

## 2. Analysis idealisation

The global solver uses planar frame elements with the nodal degrees of freedom

\[
\{d\}=\begin{bmatrix}u & v & \theta\end{bmatrix}^{T}
\]

and member actions

\[
\{f\}=\begin{bmatrix}N & V & M\end{bmatrix}^{T}.
\]

This preserves axial effects caused by centroid offsets, restraint, frame action, or changes in member direction.

## 3. Geometry layers

The implementation must keep the following concepts separate:

1. concrete outer profile
2. section centroidal axis
3. analytical reference axis

They may coincide for an ordinary prismatic beam but generally do not coincide at stepped or offset regions. Future rigid-link and rigid-offset objects will connect these layers explicitly.

## 4. B-regions and D-regions

### B-region

An ordinary beam region in which plane-sections behaviour and standard flexural/shear member design are considered applicable under the selected design standard.

### D-region

A disturbed region caused by a geometric or load discontinuity, including:

- abrupt depth changes
- re-entrant corners
- concentrated loads near a transition
- support regions
- openings
- sharp changes in member direction

Global frame forces are boundary actions for a D-region; they are not by themselves a complete local design.

## 5. Separate verification statuses

Every future design report must show independent statuses for:

- global model stability and equilibrium
- ordinary beam-region strength
- serviceability
- local D-region verification
- anchorage and detailing

A pass in one category must not imply a pass in another.

## 6. Current assumptions

The current solver uses linear-elastic Euler-Bernoulli planar frame elements:

- small displacement theory
- linear material response
- no shear deformation
- no geometric stiffness / second-order effects
- no torsion
- no out-of-plane bending
- prismatic properties within each element
- rigid joints unless releases are added in a later version

Short/deep transition pieces may require Timoshenko elements or a more refined local model, but neither replaces D-region design.

## 7. Sign convention

Global axes are right-handed:

- positive `X`: right
- positive `Y`: up
- positive `MZ` / rotation: counter-clockwise

Each element local `x` axis runs from its start node to its end node. Local `y` is 90° counter-clockwise from local `x`.

A uniform load `qy < 0` is therefore downward on a horizontal left-to-right element.

Internal member-end forces are returned in the element local sign convention. A later reporting layer will convert them into an explicitly documented sagging-positive beam convention for diagrams and RC design.

## 8. Design standards

No RC code equations are included in this increment. Code-specific values must later be provided through a design-code adapter rather than embedded in the analysis engine.

## 9. Professional-use limitation

The software is an engineering calculation aid. Project-specific modelling decisions, design-code interpretation, load paths, discontinuity-region models, and final reinforcement details require review and approval by the responsible qualified structural engineer.
