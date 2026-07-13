"""Linear-elastic planar frame assembly and solution."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from beam_d.exceptions import ModelInstabilityError, ModelValidationError
from beam_d.model import FrameElement2D, Node, Restraint, SectionProperties, UniformElementLoad

FloatArray = NDArray[np.float64]
DOF_PER_NODE = 3


@dataclass(frozen=True, slots=True)
class ElementAnalysisResult:
    """Element displacement and end-force results in local coordinates."""

    displacement_global: FloatArray
    displacement_local: FloatArray
    equivalent_nodal_load_local: FloatArray
    end_forces_local: FloatArray

    @property
    def start_actions(self) -> tuple[float, float, float]:
        return tuple(float(value) for value in self.end_forces_local[:3])

    @property
    def end_actions(self) -> tuple[float, float, float]:
        return tuple(float(value) for value in self.end_forces_local[3:])


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Complete result of one linear load state."""

    node_order: tuple[str, ...]
    displacement_vector: FloatArray
    reaction_vector: FloatArray
    applied_load_vector: FloatArray
    element_results: dict[str, ElementAnalysisResult]
    equilibrium_residual: dict[str, float]

    def _node_slice(self, node_id: str) -> slice:
        try:
            index = self.node_order.index(node_id)
        except ValueError as exc:
            raise KeyError(f"Unknown node {node_id!r} in result.") from exc
        start = DOF_PER_NODE * index
        return slice(start, start + DOF_PER_NODE)

    def displacement(self, node_id: str) -> tuple[float, float, float]:
        values = self.displacement_vector[self._node_slice(node_id)]
        return tuple(float(value) for value in values)

    def reaction(self, node_id: str) -> tuple[float, float, float]:
        values = self.reaction_vector[self._node_slice(node_id)]
        return tuple(float(value) for value in values)

    @property
    def max_equilibrium_residual(self) -> float:
        return max(abs(value) for value in self.equilibrium_residual.values())


@dataclass(slots=True)
class FrameModel2D:
    """Mutable model builder for a planar frame load state."""

    nodes: dict[str, Node] = field(default_factory=dict)
    elements: dict[str, FrameElement2D] = field(default_factory=dict)
    restraints: dict[str, Restraint] = field(default_factory=dict)
    nodal_loads: dict[str, FloatArray] = field(default_factory=dict)
    uniform_loads: dict[str, list[UniformElementLoad]] = field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ModelValidationError(f"Duplicate node id {node.id!r}.")
        self.nodes[node.id] = node

    def add_element(
        self,
        element_id: str,
        start_node_id: str,
        end_node_id: str,
        section: SectionProperties,
    ) -> None:
        if element_id in self.elements:
            raise ModelValidationError(f"Duplicate element id {element_id!r}.")
        try:
            start = self.nodes[start_node_id]
            end = self.nodes[end_node_id]
        except KeyError as exc:
            raise ModelValidationError(
                f"Element {element_id!r} references a node that has not been added."
            ) from exc
        self.elements[element_id] = FrameElement2D(element_id, start, end, section)

    def set_restraint(self, node_id: str, *, ux: bool, uy: bool, rz: bool) -> None:
        self._require_node(node_id)
        self.restraints[node_id] = Restraint(ux=ux, uy=uy, rz=rz)

    def add_nodal_load(
        self,
        node_id: str,
        *,
        fx: float = 0.0,
        fy: float = 0.0,
        mz: float = 0.0,
    ) -> None:
        self._require_node(node_id)
        values = np.array([fx, fy, mz], dtype=float)
        if not np.all(np.isfinite(values)):
            raise ModelValidationError("Nodal load components must be finite.")
        self.nodal_loads[node_id] = self.nodal_loads.get(node_id, np.zeros(3)) + values

    def add_uniform_load(self, element_id: str, *, qx: float = 0.0, qy: float = 0.0) -> None:
        self._require_element(element_id)
        self.uniform_loads.setdefault(element_id, []).append(UniformElementLoad(qx=qx, qy=qy))

    def solve(self) -> AnalysisResult:
        self._validate_model()
        node_order = tuple(self.nodes)
        dof_map = self._build_dof_map(node_order)
        number_of_dofs = DOF_PER_NODE * len(node_order)

        stiffness = np.zeros((number_of_dofs, number_of_dofs), dtype=float)
        applied = np.zeros(number_of_dofs, dtype=float)

        for node_id, load in self.nodal_loads.items():
            applied[dof_map[node_id]] += load

        for element_id, element in self.elements.items():
            indices = self._element_dof_indices(element, dof_map)
            stiffness[np.ix_(indices, indices)] += element.global_stiffness_matrix()

            transform = element.transformation_matrix()
            for load in self.uniform_loads.get(element_id, []):
                local_equivalent = element.equivalent_local_load(load)
                applied[indices] += transform.T @ local_equivalent

        restrained = self._restrained_dof_indices(node_order, dof_map)
        all_dofs = np.arange(number_of_dofs, dtype=int)
        free = np.setdiff1d(all_dofs, restrained, assume_unique=True)
        displacement = np.zeros(number_of_dofs, dtype=float)

        if free.size:
            free_stiffness = stiffness[np.ix_(free, free)]
            free_load = applied[free]
            try:
                displacement[free] = np.linalg.solve(free_stiffness, free_load)
            except np.linalg.LinAlgError as exc:
                raise ModelInstabilityError(
                    "The free-degree stiffness matrix is singular. Check supports, "
                    "connectivity, releases, and element properties."
                ) from exc

        reactions = stiffness @ displacement - applied
        element_results = self._recover_elements(displacement, dof_map)
        residual = self._equilibrium_residual(node_order, applied, reactions)

        return AnalysisResult(
            node_order=node_order,
            displacement_vector=displacement,
            reaction_vector=reactions,
            applied_load_vector=applied,
            element_results=element_results,
            equilibrium_residual=residual,
        )

    def _recover_elements(
        self,
        displacement: FloatArray,
        dof_map: dict[str, NDArray[np.int64]],
    ) -> dict[str, ElementAnalysisResult]:
        results: dict[str, ElementAnalysisResult] = {}
        for element_id, element in self.elements.items():
            indices = self._element_dof_indices(element, dof_map)
            global_displacement = displacement[indices]
            transform = element.transformation_matrix()
            local_displacement = transform @ global_displacement

            equivalent_local = np.zeros(6, dtype=float)
            for load in self.uniform_loads.get(element_id, []):
                equivalent_local += element.equivalent_local_load(load)

            end_forces = element.local_stiffness_matrix() @ local_displacement - equivalent_local
            results[element_id] = ElementAnalysisResult(
                displacement_global=global_displacement.copy(),
                displacement_local=local_displacement,
                equivalent_nodal_load_local=equivalent_local,
                end_forces_local=end_forces,
            )
        return results

    def _equilibrium_residual(
        self,
        node_order: tuple[str, ...],
        applied: FloatArray,
        reactions: FloatArray,
    ) -> dict[str, float]:
        total = applied + reactions
        force_x = 0.0
        force_y = 0.0
        moment_z = 0.0

        for index, node_id in enumerate(node_order):
            node = self.nodes[node_id]
            fx, fy, mz = total[DOF_PER_NODE * index : DOF_PER_NODE * index + DOF_PER_NODE]
            force_x += fx
            force_y += fy
            moment_z += mz + node.x * fy - node.y * fx

        return {
            "force_x": float(force_x),
            "force_y": float(force_y),
            "moment_z": float(moment_z),
        }

    def _validate_model(self) -> None:
        if not self.nodes:
            raise ModelValidationError("The model has no nodes.")
        if not self.elements:
            raise ModelValidationError("The model has no elements.")
        connected_nodes = {
            node_id
            for element in self.elements.values()
            for node_id in (element.start.id, element.end.id)
        }
        unconnected = set(self.nodes) - connected_nodes
        if unconnected:
            joined = ", ".join(sorted(unconnected))
            raise ModelValidationError(f"Unconnected nodes are not allowed: {joined}.")

    def _require_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            raise ModelValidationError(f"Unknown node id {node_id!r}.")

    def _require_element(self, element_id: str) -> None:
        if element_id not in self.elements:
            raise ModelValidationError(f"Unknown element id {element_id!r}.")

    @staticmethod
    def _build_dof_map(node_order: tuple[str, ...]) -> dict[str, NDArray[np.int64]]:
        return {
            node_id: np.arange(
                DOF_PER_NODE * index,
                DOF_PER_NODE * index + DOF_PER_NODE,
                dtype=int,
            )
            for index, node_id in enumerate(node_order)
        }

    @staticmethod
    def _element_dof_indices(
        element: FrameElement2D,
        dof_map: dict[str, NDArray[np.int64]],
    ) -> NDArray[np.int64]:
        return np.concatenate((dof_map[element.start.id], dof_map[element.end.id]))

    def _restrained_dof_indices(
        self,
        node_order: tuple[str, ...],
        dof_map: dict[str, NDArray[np.int64]],
    ) -> NDArray[np.int64]:
        restrained: list[int] = []
        for node_id in node_order:
            flags = self.restraints.get(node_id, Restraint()).as_tuple()
            restrained.extend(
                int(dof)
                for dof, is_restrained in zip(dof_map[node_id], flags, strict=True)
                if is_restrained
            )
        return np.array(sorted(restrained), dtype=int)
