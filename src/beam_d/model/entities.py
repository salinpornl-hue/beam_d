"""Core immutable entities for planar frame analysis."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

import numpy as np
from numpy.typing import NDArray

from beam_d.exceptions import ModelValidationError

FloatArray = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class Node:
    """A planar frame node in global Cartesian coordinates."""

    id: str
    x: float
    y: float

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ModelValidationError("Node id must not be blank.")
        if not np.isfinite(self.x) or not np.isfinite(self.y):
            raise ModelValidationError(f"Node {self.id!r} coordinates must be finite.")


@dataclass(frozen=True, slots=True)
class SectionProperties:
    """Elastic and geometric properties of a prismatic frame element."""

    elastic_modulus: float
    area: float
    second_moment: float

    def __post_init__(self) -> None:
        values = {
            "elastic_modulus": self.elastic_modulus,
            "area": self.area,
            "second_moment": self.second_moment,
        }
        for name, value in values.items():
            if not np.isfinite(value) or value <= 0.0:
                raise ModelValidationError(f"{name} must be finite and greater than zero.")


@dataclass(frozen=True, slots=True)
class Restraint:
    """Boolean restraints for global UX, UY, and RZ degrees of freedom."""

    ux: bool = False
    uy: bool = False
    rz: bool = False

    def as_tuple(self) -> tuple[bool, bool, bool]:
        return self.ux, self.uy, self.rz


@dataclass(frozen=True, slots=True)
class UniformElementLoad:
    """Full-length uniform load expressed in an element's local axes."""

    qx: float = 0.0
    qy: float = 0.0

    def __post_init__(self) -> None:
        if not np.isfinite(self.qx) or not np.isfinite(self.qy):
            raise ModelValidationError("Uniform load components must be finite.")


@dataclass(frozen=True, slots=True)
class FrameElement2D:
    """Two-node Euler-Bernoulli planar frame element."""

    id: str
    start: Node
    end: Node
    section: SectionProperties

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ModelValidationError("Element id must not be blank.")
        if self.length <= 0.0:
            raise ModelValidationError(f"Element {self.id!r} has zero length.")

    @property
    def length(self) -> float:
        return hypot(self.end.x - self.start.x, self.end.y - self.start.y)

    @property
    def direction_cosines(self) -> tuple[float, float]:
        length = self.length
        return (self.end.x - self.start.x) / length, (self.end.y - self.start.y) / length

    def transformation_matrix(self) -> FloatArray:
        """Return T such that local displacement = T @ global displacement."""

        c, s = self.direction_cosines
        return np.array(
            [
                [c, s, 0.0, 0.0, 0.0, 0.0],
                [-s, c, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, c, s, 0.0],
                [0.0, 0.0, 0.0, -s, c, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            ],
            dtype=float,
        )

    def local_stiffness_matrix(self) -> FloatArray:
        """Return the standard 6x6 local planar-frame stiffness matrix."""

        e = self.section.elastic_modulus
        a = self.section.area
        i = self.section.second_moment
        length = self.length

        ea_l = e * a / length
        ei = e * i
        l2 = length * length
        l3 = l2 * length

        return np.array(
            [
                [ea_l, 0.0, 0.0, -ea_l, 0.0, 0.0],
                [0.0, 12.0 * ei / l3, 6.0 * ei / l2, 0.0, -12.0 * ei / l3, 6.0 * ei / l2],
                [0.0, 6.0 * ei / l2, 4.0 * ei / length, 0.0, -6.0 * ei / l2, 2.0 * ei / length],
                [-ea_l, 0.0, 0.0, ea_l, 0.0, 0.0],
                [0.0, -12.0 * ei / l3, -6.0 * ei / l2, 0.0, 12.0 * ei / l3, -6.0 * ei / l2],
                [0.0, 6.0 * ei / l2, 2.0 * ei / length, 0.0, -6.0 * ei / l2, 4.0 * ei / length],
            ],
            dtype=float,
        )

    def global_stiffness_matrix(self) -> FloatArray:
        transform = self.transformation_matrix()
        return transform.T @ self.local_stiffness_matrix() @ transform

    def equivalent_local_load(self, load: UniformElementLoad) -> FloatArray:
        """Return the consistent nodal-load vector for a full uniform load.

        ``qx`` and ``qy`` are positive in the element local +x and +y axes.
        """

        length = self.length
        return np.array(
            [
                load.qx * length / 2.0,
                load.qy * length / 2.0,
                load.qy * length**2 / 12.0,
                load.qx * length / 2.0,
                load.qy * length / 2.0,
                -load.qy * length**2 / 12.0,
            ],
            dtype=float,
        )
