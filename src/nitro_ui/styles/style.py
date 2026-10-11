"""CSS Style class for NitroUI."""

import copy
import re
from typing import Dict, Any, Optional, Tuple

from nitro_ui.core.element import _validate_css_property, _validate_css_value

BREAKPOINTS = ("xs", "sm", "md", "lg", "xl", "2xl")

FUNCTIONAL_PSEUDOS = frozenset(
    {
        "nth-child",
        "nth-last-child",
        "nth-of-type",
        "nth-last-of-type",
        "not",
        "is",
        "where",
        "has",
        "lang",
        "dir",
    }
)

_PSEUDO_NAME_PATTERN = re.compile(r"^[a-z][a-z-]*$")
_PSEUDO_ARG_PATTERN = re.compile(r"^[a-zA-Z0-9_+\-.,:#() ]+$")
_PSEUDO_KEY_PATTERN = re.compile(r"^([a-z][a-z-]*)(?:\((.*)\))?$")
_BREAKPOINT_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


def _balanced(text: str) -> bool:
    depth = 0
    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def _pseudo_key(name: str, arg: Optional[str] = None) -> str:
    """Build a validated pseudo-selector key like ``hover`` or ``nth-child(2n)``.

    Raises:
        ValueError: If the name or argument is unsafe, a functional
            pseudo-class has no argument, or a plain one is given one.
    """
    if not isinstance(name, str) or not _PSEUDO_NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid pseudo-selector name: {name!r}. Use lowercase letters "
            "and hyphens only (e.g. 'hover', 'focus-visible')."
        )
    if name in FUNCTIONAL_PSEUDOS:
        if arg is None or str(arg).strip() == "":
            raise ValueError(
                f"Pseudo-selector ':{name}()' needs an argument. Pass a tuple, "
                f"e.g. _{name.replace('-', '_')}=(\"2n+1\", CSSStyle(...))."
            )
        arg = str(arg).strip()
        if not _PSEUDO_ARG_PATTERN.match(arg) or not _balanced(arg):
            raise ValueError(f"Invalid argument for ':{name}()': {arg!r}.")
        return f"{name}({arg})"
    if arg is not None:
        raise ValueError(f"Pseudo-selector ':{name}' does not take an argument.")
    return name


def _parse_pseudo_key(key: str) -> Tuple[str, Optional[str]]:
    """Split a stored pseudo key back into ``(name, arg)`` and validate it."""
    match = _PSEUDO_KEY_PATTERN.match(key) if isinstance(key, str) else None
    if not match:
        raise ValueError(f"Invalid pseudo-selector: {key!r}.")
    name, arg = match.group(1), match.group(2)
    _pseudo_key(name, arg)
    return name, arg


def _validate_breakpoint_name(name: str) -> str:
    if not isinstance(name, str) or not _BREAKPOINT_NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid breakpoint name: {name!r}. Use letters, digits, "
            "underscores, or hyphens."
        )
    return name


def _check_property(name: str) -> str:
    if not _validate_css_property(name):
        raise ValueError(
            f"Invalid CSS property name: {name!r}. Property names must be "
            "a standard CSS identifier or a custom property starting with '--'."
        )
    return name


class CSSStyle:
    """Declarative CSS style with pseudo-selector and breakpoint support.

    Instances capture a set of base CSS declarations plus nested
    ``CSSStyle`` objects for pseudo-selectors (``:hover``, ``:active``,
    ...) and responsive breakpoints (``sm``, ``md``, ``lg``, ...).
    Property names are written in snake_case; they are converted to
    kebab-case at emit time.

    Example:
        >>> style = CSSStyle(
        ...     background_color="#007bff",
        ...     color="white",
        ...     _hover=CSSStyle(background_color="#0056b3"),
        ...     _md=CSSStyle(padding="20px"),
        ... )
        >>> style.to_inline()
        'background-color: #007bff; color: white'
    """

    _KNOWN_PSEUDOS = frozenset(
        {
            "hover",
            "active",
            "focus",
            "focus-visible",
            "focus-within",
            "visited",
            "link",
            "first-child",
            "last-child",
            "only-child",
            "first-of-type",
            "last-of-type",
            "checked",
            "disabled",
            "enabled",
            "empty",
            "placeholder",
            "before",
            "after",
        }
    )

    def __init__(self, **kwargs):
        """Create a CSSStyle from keyword arguments.

        Args:
            **kwargs: CSS declarations as ``property=value`` pairs.
                Underscores in names become hyphens
                (``background_color`` -> ``background-color``). Keys
                starting with an underscore and assigned a ``CSSStyle``
                become breakpoints (``_xs``, ``_sm``, ``_md``, ``_lg``,
                ``_xl``, ``_2xl``) or pseudo-selectors (``_hover``,
                ``_focus_visible``, ``_first_child``, ``_before``, ...).
                Functional pseudo-classes take an ``(argument, CSSStyle)``
                tuple, e.g. ``_nth_child=("2n+1", CSSStyle(...))``.
                ``None`` values are skipped.

        Raises:
            ValueError: If a property or pseudo-selector name is invalid,
                or a functional pseudo-class is missing its argument.
            TypeError: If a pseudo-selector or breakpoint key is given
                something other than a ``CSSStyle``.
        """
        self._styles: Dict[str, str] = {}
        self._pseudo: Dict[str, "CSSStyle"] = {}
        self._breakpoints: Dict[str, "CSSStyle"] = {}

        for key, value in kwargs.items():
            if value is None:
                continue
            name = key[1:].replace("_", "-") if key.startswith("_") else None

            if name and name[0].isdigit() and name not in BREAKPOINTS:
                raise ValueError(
                    f"Unknown breakpoint {key!r}. Use one of: "
                    + ", ".join(f"_{bp}" for bp in BREAKPOINTS)
                )
            if name in BREAKPOINTS:
                if not isinstance(value, CSSStyle):
                    raise TypeError(
                        f"Breakpoint {key!r} expects a CSSStyle, "
                        f"got {type(value).__name__}."
                    )
                self._breakpoints[name] = value
            elif isinstance(value, tuple) and name is not None:
                if len(value) != 2 or not isinstance(value[1], CSSStyle):
                    raise TypeError(
                        f"Pseudo-selector {key!r} expects (argument, CSSStyle)."
                    )
                self._pseudo[_pseudo_key(name, value[0])] = value[1]
            elif isinstance(value, CSSStyle):
                if name is None:
                    raise TypeError(
                        f"{key!r} holds a CSSStyle but isn't a pseudo-selector "
                        "or breakpoint. Prefix it with an underscore, e.g. _hover."
                    )
                self._pseudo[_pseudo_key(name)] = value
            elif name in self._KNOWN_PSEUDOS or name in FUNCTIONAL_PSEUDOS:
                raise TypeError(
                    f"Pseudo-selector {key!r} expects a CSSStyle, "
                    f"got {type(value).__name__}."
                )
            else:
                self._styles[_check_property(self._to_css_prop(key))] = str(value)

    def _to_css_prop(self, prop: str) -> str:
        """
        Convert Python snake_case to CSS kebab-case.

        Args:
            prop: Property name in snake_case

        Returns:
            Property name in kebab-case
        """
        return prop.replace("_", "-")

    def merge(self, other: "CSSStyle") -> "CSSStyle":
        """Combine another style into a new ``CSSStyle`` without mutating either.

        Values from ``other`` win on conflict. Pseudo-selectors and
        breakpoints are deep-merged recursively, so an ``_hover`` on
        either side survives.

        Args:
            other: Style whose declarations overlay this one.

        Returns:
            A new ``CSSStyle`` with the merged content.
        """
        merged = CSSStyle()
        merged._styles = {**self._styles, **other._styles}

        # Deep merge pseudo-selectors
        all_pseudo_keys = set(self._pseudo) | set(other._pseudo)
        for key in all_pseudo_keys:
            if key in self._pseudo and key in other._pseudo:
                # Both have this pseudo - merge their styles
                merged._pseudo[key] = self._pseudo[key].merge(other._pseudo[key])
            elif key in other._pseudo:
                merged._pseudo[key] = copy.deepcopy(other._pseudo[key])
            else:
                merged._pseudo[key] = copy.deepcopy(self._pseudo[key])

        # Deep merge breakpoints
        all_bp_keys = set(self._breakpoints) | set(other._breakpoints)
        for key in all_bp_keys:
            if key in self._breakpoints and key in other._breakpoints:
                merged._breakpoints[key] = self._breakpoints[key].merge(
                    other._breakpoints[key]
                )
            elif key in other._breakpoints:
                merged._breakpoints[key] = copy.deepcopy(other._breakpoints[key])
            else:
                merged._breakpoints[key] = copy.deepcopy(self._breakpoints[key])

        return merged

    def to_inline(self) -> str:
        """Render the base declarations as a single ``style`` attribute value.

        Only the base declarations are emitted - pseudo-selectors and
        breakpoints cannot be expressed inline and require a stylesheet.
        Values are validated against the same injection patterns
        enforced by ``HTMLElement.add_style``.

        Returns:
            A string like ``"color: red; padding: 10px"``, or an empty
            string if no base declarations are set.

        Raises:
            ValueError: If any value contains potentially dangerous content.
        """
        if not self._styles:
            return ""
        for key, value in self._styles.items():
            _check_property(key)
            if not _validate_css_value(str(value)):
                raise ValueError(
                    f"CSS value for '{key}' contains potentially dangerous content: "
                    f"{value!r}. Values cannot contain javascript:, expression(), "
                    "or other injection patterns."
                )
        return "; ".join(f"{k}: {v}" for k, v in self._styles.items())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this style (including nested pseudo/breakpoint maps) to a dict.

        The output is JSON-safe and round-trips via ``from_dict()``.

        Returns:
            A dict with keys ``styles``, optionally ``pseudo`` and
            ``breakpoints`` holding nested ``CSSStyle.to_dict()`` output.
        """
        result: Dict[str, Any] = {"styles": self._styles.copy()}

        if self._pseudo:
            result["pseudo"] = {k: v.to_dict() for k, v in self._pseudo.items()}

        if self._breakpoints:
            result["breakpoints"] = {
                k: v.to_dict() for k, v in self._breakpoints.items()
            }

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CSSStyle":
        """Reconstruct a ``CSSStyle`` from a ``to_dict()`` result.

        Args:
            data: Dict previously produced by ``to_dict()``.

        Returns:
            A new ``CSSStyle`` equivalent to the serialized one.

        Raises:
            ValueError: If any property name in ``data["styles"]`` is not
                a valid CSS identifier.
        """
        style = cls()
        for key, value in dict(data.get("styles", {})).items():
            if not _validate_css_property(key):
                raise ValueError(
                    f"Invalid CSS property name in serialized data: {key!r}."
                )
            if value is not None:
                style._styles[key] = value

        for key, value in data.get("pseudo", {}).items():
            _parse_pseudo_key(key)
            style._pseudo[key] = cls.from_dict(value)

        for key, value in data.get("breakpoints", {}).items():
            style._breakpoints[_validate_breakpoint_name(key)] = cls.from_dict(value)

        return style

    def has_pseudo_or_breakpoints(self) -> bool:
        """Return ``True`` if this style carries any pseudo-selector or breakpoint.

        Inline ``style="..."`` can't express pseudo-selectors or media
        queries, so this is a useful signal for deciding whether the
        style must be registered on a ``StyleSheet``.
        """
        return bool(self._pseudo or self._breakpoints)

    def is_complex(self, threshold: int = 3) -> bool:
        """Return ``True`` when the base declaration count exceeds a threshold.

        Useful alongside ``has_pseudo_or_breakpoints`` to decide whether
        a given style is better off in an external stylesheet.

        Args:
            threshold: Maximum number of declarations considered simple;
                the style is "complex" when it has strictly more.
        """
        return len(self._styles) > threshold

    def __repr__(self) -> str:
        """Return a debug representation showing the inline form."""
        inline = "; ".join(f"{k}: {v}" for k, v in self._styles.items())
        return f"CSSStyle({inline})"

    def __eq__(self, other: object) -> bool:
        """Return ``True`` if base, pseudo, and breakpoint maps all match."""
        if not isinstance(other, CSSStyle):
            return False
        return (
            self._styles == other._styles
            and self._pseudo == other._pseudo
            and self._breakpoints == other._breakpoints
        )

    def __hash__(self) -> int:
        """Return a stable hash based on declarations and pseudo/breakpoint keys."""
        styles_tuple = tuple(sorted(self._styles.items()))
        # Include pseudo and breakpoint keys in hash for better distribution
        pseudo_keys = tuple(sorted(self._pseudo.keys()))
        bp_keys = tuple(sorted(self._breakpoints.keys()))
        return hash((styles_tuple, pseudo_keys, bp_keys))
