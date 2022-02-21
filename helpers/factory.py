"""Factory for creating a game character."""

from typing import Any, Callable

from .base import SourceManager


# Callable[..., BaseScenario]  # requires no arguments, returns BaseScenario object
character_creation_funcs: dict[str, Callable[..., SourceManager]] = {}


def register(character_type: str, creator_fn: Callable[..., SourceManager]) -> None:
    """Register a new game character type."""
    character_creation_funcs[character_type] = creator_fn


def unregister(character_type: str) -> None:
    """Unregister a game character type."""
    character_creation_funcs.pop(character_type, None)


def create(arguments: dict[str, Any]) -> SourceManager:
    """Create a game character of a specific type, given JSON data."""
    args_copy = arguments.copy()
    character_type = args_copy.pop("type")
    try:
        creator_func = character_creation_funcs[character_type]
    except KeyError:
        raise ValueError(f"unknown character type {character_type!r}") from None
    return creator_func(**args_copy)
