"""Domain-specific exceptions for beam_d."""


class BeamDError(Exception):
    """Base exception for beam_d."""


class ModelValidationError(BeamDError):
    """Raised when the structural model contains invalid input."""


class ModelInstabilityError(BeamDError):
    """Raised when the free-degree stiffness matrix is singular."""
