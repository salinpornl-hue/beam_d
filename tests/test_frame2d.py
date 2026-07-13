from __future__ import annotations

import pytest

from beam_d import FrameModel2D, ModelInstabilityError, Node, SectionProperties


def section() -> SectionProperties:
    return SectionProperties(
        elastic_modulus=30_000.0,
        area=300.0 * 600.0,
        second_moment=300.0 * 600.0**3 / 12.0,
    )


def test_simply_supported_beam_under_uniform_load() -> None:
    length = 6_000.0
    downward_load = 20.0

    model = FrameModel2D()
    model.add_node(Node("A", 0.0, 0.0))
    model.add_node(Node("B", length, 0.0))
    model.add_element("AB", "A", "B", section())
    model.set_restraint("A", ux=True, uy=True, rz=False)
    model.set_restraint("B", ux=False, uy=True, rz=False)
    model.add_uniform_load("AB", qy=-downward_load)

    result = model.solve()
    expected_reaction = downward_load * length / 2.0

    assert result.reaction("A")[1] == pytest.approx(expected_reaction, rel=1e-12)
    assert result.reaction("B")[1] == pytest.approx(expected_reaction, rel=1e-12)
    assert result.reaction("A")[2] == pytest.approx(0.0, abs=1e-6)
    assert result.reaction("B")[2] == pytest.approx(0.0, abs=1e-6)
    assert result.element_results["AB"].end_forces_local[2] == pytest.approx(0.0, abs=1e-6)
    assert result.element_results["AB"].end_forces_local[5] == pytest.approx(0.0, abs=1e-6)
    assert result.max_equilibrium_residual < 1e-5


def test_cantilever_tip_load_displacement_and_reactions() -> None:
    length = 4_000.0
    point_load = 50_000.0
    properties = section()

    model = FrameModel2D()
    model.add_node(Node("A", 0.0, 0.0))
    model.add_node(Node("B", length, 0.0))
    model.add_element("AB", "A", "B", properties)
    model.set_restraint("A", ux=True, uy=True, rz=True)
    model.add_nodal_load("B", fy=-point_load)

    result = model.solve()
    _, tip_vertical, tip_rotation = result.displacement("B")
    _, reaction_vertical, reaction_moment = result.reaction("A")

    expected_vertical = -point_load * length**3 / (
        3.0 * properties.elastic_modulus * properties.second_moment
    )
    expected_rotation = -point_load * length**2 / (
        2.0 * properties.elastic_modulus * properties.second_moment
    )

    assert tip_vertical == pytest.approx(expected_vertical, rel=1e-12)
    assert tip_rotation == pytest.approx(expected_rotation, rel=1e-12)
    assert reaction_vertical == pytest.approx(point_load, rel=1e-12)
    assert reaction_moment == pytest.approx(point_load * length, rel=1e-12)
    assert result.max_equilibrium_residual < 1e-5


def test_axial_extension() -> None:
    length = 3_000.0
    axial_load = 100_000.0
    properties = section()

    model = FrameModel2D()
    model.add_node(Node("A", 0.0, 0.0))
    model.add_node(Node("B", length, 0.0))
    model.add_element("AB", "A", "B", properties)
    model.set_restraint("A", ux=True, uy=True, rz=True)
    model.set_restraint("B", ux=False, uy=True, rz=True)
    model.add_nodal_load("B", fx=axial_load)

    result = model.solve()
    extension, _, _ = result.displacement("B")
    expected = axial_load * length / (properties.elastic_modulus * properties.area)

    assert extension == pytest.approx(expected, rel=1e-12)
    assert result.reaction("A")[0] == pytest.approx(-axial_load, rel=1e-12)
    assert result.max_equilibrium_residual < 1e-5


def test_inclined_element_transformation_preserves_rigid_rotation_geometry() -> None:
    model = FrameModel2D()
    model.add_node(Node("A", 0.0, 0.0))
    model.add_node(Node("B", 3_000.0, 4_000.0))
    model.add_element("AB", "A", "B", section())
    model.set_restraint("A", ux=True, uy=True, rz=True)
    model.add_nodal_load("B", fx=30_000.0, fy=40_000.0)

    result = model.solve()
    local_end = result.element_results["AB"].end_forces_local

    assert local_end[0] == pytest.approx(-50_000.0, rel=1e-12)
    assert local_end[1] == pytest.approx(0.0, abs=1e-6)
    assert local_end[2] == pytest.approx(0.0, abs=1e-3)
    assert result.max_equilibrium_residual < 1e-5


def test_unstable_model_is_rejected() -> None:
    model = FrameModel2D()
    model.add_node(Node("A", 0.0, 0.0))
    model.add_node(Node("B", 1_000.0, 0.0))
    model.add_element("AB", "A", "B", section())
    model.add_nodal_load("B", fy=-1_000.0)

    with pytest.raises(ModelInstabilityError):
        model.solve()


def test_invalid_zero_length_element_is_rejected() -> None:
    model = FrameModel2D()
    model.add_node(Node("A", 0.0, 0.0))
    model.add_node(Node("B", 0.0, 0.0))

    with pytest.raises(Exception, match="zero length"):
        model.add_element("AB", "A", "B", section())
