"""CSS Style class for NitroUI."""

import copy
from typing import Dict, Any

from nitro_ui.core.element import _validate_css_value


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

    def __init__(self, **kwargs):
        """Create a CSSStyle from keyword arguments.

        Args:
            **kwargs: CSS declarations as ``property=value`` pairs.
                Underscores in names become hyphens
                (``background_color`` -> ``background-color``). Values
                starting with an underscore and assigned a ``CSSStyle``
                are routed to the pseudo-selector or breakpoint maps:
                ``_hover``, ``_active``, ``_focus``, ``_visited``,
                ``_link``, ``_first_child``, ``_last_child``,
                ``_nth_child``, ``_before``, ``_after``, plus
                breakpoints ``_xs``, ``_sm``, ``_md``, ``_lg``, ``_xl``,
                ``_2xl``.
        """
        self._styles: Dict[str, str] = {}
        self._pseudo: Dict[str, "CSSStyle"] = {}
        self._breakpoints: Dict[str, "CSSStyle"] = {}

        # Known pseudo-selectors
        PSEUDO_SELECTORS = {
            "_hover",
            "_active",
            "_focus",
            "_visited",
            "_link",
            "_first_child",
            "_last_child",
            "_nth_child",
            "_before",
            "_after",
        }

        BREAKPOINTS = {"_xs", "_sm", "_md", "_lg", "_xl", "_2xl"}

        for key, value in kwargs.items():
            if isinstance(value, CSSStyle):
                if key in PSEUDO_SELECTORS:
                    self._pseudo[key[1:].replace("_", "-")] = value
                elif key in BREAKPOINTS:
                    self._breakpoints[key[1:]] = value
            else:
                self._styles[self._to_css_prop(key)] = str(value)

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
        """
        style = cls()
        style._styles = dict(data.get("styles", {}))

        if "pseudo" in data:
            for key, value in data["pseudo"].items():
                style._pseudo[key] = cls.from_dict(value)

        if "breakpoints" in data:
            for key, value in data["breakpoints"].items():
                style._breakpoints[key] = cls.from_dict(value)

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
        return f"CSSStyle({self.to_inline()})"

    def __eq__(self, other: object) -> bool:
        """Return ``True`` if both styles have identical base, pseudo, and breakpoint maps."""
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
