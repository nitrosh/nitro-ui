"""StyleSheet class for managing CSS classes in NitroUI."""

import re
from typing import Dict, Optional, List, TYPE_CHECKING

from .style import CSSStyle
from nitro_ui.core.element import _validate_css_value

if TYPE_CHECKING:
    from .theme import Theme


# Valid CSS class name pattern: must start with letter, underscore, or hyphen
# followed by letters, digits, underscores, or hyphens
_VALID_CLASS_NAME_PATTERN = re.compile(r"^-?[_a-zA-Z][_a-zA-Z0-9-]*$")

# Valid CSS property name pattern: a standard ident, or a CSS custom property
# (``--name``). Blocks at-rules, braces, semicolons, and whitespace from being
# smuggled in via dict keys (e.g. ``"@import url(evil); color"``).
_VALID_CSS_PROPERTY_PATTERN = re.compile(r"^(--)?[a-zA-Z][a-zA-Z0-9-]*$")


def _validate_css_property(name: str) -> bool:
    """Validate that a CSS property name is safe for CSS output.

    Args:
        name: The CSS property name to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not name or not isinstance(name, str):
        return False
    return bool(_VALID_CSS_PROPERTY_PATTERN.match(name))


def _sanitize_css_property(name: str) -> str:
    """Return ``name`` if it is a valid CSS property, else raise.

    Args:
        name: The CSS property name to validate.

    Returns:
        The property name unchanged.

    Raises:
        ValueError: If ``name`` is not a valid CSS identifier.
    """
    if not _validate_css_property(name):
        raise ValueError(
            f"Invalid CSS property name: {name!r}. Property names must be "
            "a standard CSS identifier (letters, digits, hyphens) or a "
            "custom property starting with '--'."
        )
    return name


def _validate_class_name(name: str) -> bool:
    """Validate that a class name is safe for CSS output.

    Args:
        name: The class name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    # Check for BEM naming (allows __ and --)
    # Split by BEM separators and validate each part
    parts = re.split(r"__|--", name)
    return all(_VALID_CLASS_NAME_PATTERN.match(part) for part in parts if part)


def _sanitize_css_value(value: str) -> str:
    """Sanitize a CSS value to prevent injection attacks.

    Uses the shared validation from core.element for consistency.

    Args:
        value: The CSS value to sanitize

    Returns:
        Sanitized CSS value

    Raises:
        ValueError: If the value contains dangerous characters
    """
    if not isinstance(value, str):
        value = str(value)

    if not _validate_css_value(value):
        raise ValueError(
            f"CSS value contains potentially dangerous content: {value!r}. "
            "Values cannot contain javascript:, expression(), or other "
            "injection patterns."
        )

    return value


class StyleSheet:
    """Registry of named CSS classes that renders to a ``<style>`` block.

    Attach ``CSSStyle`` objects under class names (or let the registry
    auto-name them), then emit the full stylesheet - including any theme
    CSS variables - with ``render()`` or ``to_style_tag()``. Responsive
    breakpoints stored on styles are rendered as ``@media`` queries
    using this sheet's breakpoint values.

    Example:
        >>> sheet = StyleSheet()
        >>> btn = sheet.register("btn-primary", CSSStyle(color="white"))
        >>> Button("Click", class_name=btn)  # doctest: +SKIP
        >>> sheet.render()  # doctest: +SKIP
    """

    def __init__(self, theme: Optional["Theme"] = None):
        """Create a new, empty stylesheet optionally tied to a theme.

        Args:
            theme: Optional ``Theme`` whose CSS variables are emitted
                inside a ``:root`` block when this sheet is rendered.
        """
        self.theme = theme
        self._classes: Dict[str, CSSStyle] = {}
        self._counter = 0

        # Default breakpoint values (can be customized)
        self._breakpoint_values = {
            "xs": "0px",
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px",
        }

    def register(
        self, name: Optional[str] = None, style: Optional[CSSStyle] = None
    ) -> str:
        """Store a style under a class name and return the name for use in HTML.

        If ``name`` is omitted, an auto-name like ``"s-0"`` is generated.
        User-supplied names are validated - BEM notation (``__``, ``--``)
        is permitted but random punctuation is not.

        Args:
            name: Explicit class name, or ``None`` to auto-generate.
            style: Style to register. An empty ``CSSStyle`` is used if
                omitted - useful for reserving a name.

        Returns:
            The class name to pass to ``class_name=`` on an element.

        Raises:
            ValueError: If ``name`` fails class-name validation.

        Example:
            >>> sheet = StyleSheet()
            >>> sheet.register("btn", CSSStyle(color="white"))
            'btn'
        """
        if style is None:
            style = CSSStyle()

        # Generate class name if not provided
        if name is None:
            name = f"s-{self._counter}"
            self._counter += 1
        else:
            # Validate user-provided class names
            if not _validate_class_name(name):
                raise ValueError(
                    f"Invalid CSS class name: {name!r}. Class names must start with "
                    "a letter, underscore, or hyphen, followed by letters, digits, "
                    "underscores, or hyphens. BEM notation (__ and --) is allowed."
                )

        # Store the style
        self._classes[name] = style

        return name

    def register_bem(
        self,
        block: str,
        element: Optional[str] = None,
        modifier: Optional[str] = None,
        style: Optional[CSSStyle] = None,
    ) -> str:
        """Register a style with a BEM-formatted class name.

        Assembles ``block``, ``block__element``, or
        ``block__element--modifier`` and delegates to ``register()``.

        Args:
            block: Block name (e.g. ``"button"``).
            element: Element name within the block (e.g. ``"icon"``).
            modifier: Modifier applied to the block or element
                (e.g. ``"primary"``).
            style: Style to register against the generated name.

        Returns:
            The full BEM class name - e.g. ``"button__icon--primary"``.
        """
        # Build BEM class name
        class_name = block

        if element:
            class_name += f"__{element}"

        if modifier:
            class_name += f"--{modifier}"

        return self.register(class_name, style)

    def get_style(self, name: str) -> Optional[CSSStyle]:
        """Return the style registered for a class name, or ``None`` if absent."""
        return self._classes.get(name)

    def has_class(self, name: str) -> bool:
        """Return ``True`` if a style is registered under this class name."""
        return name in self._classes

    def unregister(self, name: str) -> bool:
        """Remove a registered class and return whether it existed.

        Args:
            name: Class name to remove.

        Returns:
            ``True`` if the class was present and removed, ``False``
            if it was never registered.
        """
        if name in self._classes:
            del self._classes[name]
            return True
        return False

    def clear(self) -> None:
        """Drop every registered class and reset the auto-name counter."""
        self._classes.clear()
        self._counter = 0

    def set_breakpoint(self, name: str, value: str) -> None:
        """Override the ``min-width`` value used for a named breakpoint.

        Affects the ``@media`` queries emitted by ``render()`` for any
        styles that define responsive overrides.

        Args:
            name: Breakpoint key (e.g. ``"sm"``, ``"md"``).
            value: CSS length string (e.g. ``"640px"``).
        """
        self._breakpoint_values[name] = value

    def _render_class_styles(
        self, class_name: str, style: CSSStyle, indent: int = 2
    ) -> List[str]:
        """
        Render styles for a single class.

        Args:
            class_name: The CSS class name
            style: The CSSStyle object
            indent: Number of spaces for indentation

        Returns:
            List of CSS strings

        Raises:
            ValueError: If any CSS value contains dangerous characters
        """
        css_lines = []
        indent_str = " " * indent

        # Base styles
        if style._styles:
            css_lines.append(f".{class_name} {{")
            for prop, value in style._styles.items():
                sanitized_prop = _sanitize_css_property(prop)
                sanitized_value = _sanitize_css_value(value)
                css_lines.append(f"{indent_str}{sanitized_prop}: {sanitized_value};")
            css_lines.append("}")

        # Pseudo-selectors
        for pseudo, pseudo_style in style._pseudo.items():
            if pseudo_style._styles:
                css_lines.append(f".{class_name}:{pseudo} {{")
                for prop, value in pseudo_style._styles.items():
                    sanitized_prop = _sanitize_css_property(prop)
                    sanitized_value = _sanitize_css_value(value)
                    css_lines.append(
                        f"{indent_str}{sanitized_prop}: {sanitized_value};"
                    )
                css_lines.append("}")

        # Responsive breakpoints
        for breakpoint, bp_style in style._breakpoints.items():
            if bp_style._styles:
                min_width = self._breakpoint_values.get(breakpoint, "0px")
                css_lines.append(f"@media (min-width: {min_width}) {{")
                css_lines.append(f"{indent_str}.{class_name} {{")
                for prop, value in bp_style._styles.items():
                    sanitized_prop = _sanitize_css_property(prop)
                    sanitized_value = _sanitize_css_value(value)
                    css_lines.append(
                        f"{indent_str}{indent_str}{sanitized_prop}: {sanitized_value};"
                    )
                css_lines.append(f"{indent_str}}}")
                css_lines.append("}")

        return css_lines

    def render(self, pretty: bool = True) -> str:
        """Emit the full CSS text for every registered class.

        Output order: ``:root`` block with theme variables (if a theme
        was provided), then each class in registration order with its
        base rules, pseudo-selectors, and breakpoint media queries.
        Values are re-validated against injection patterns on render.

        Args:
            pretty: If ``True``, format with line breaks and indentation.
                If ``False``, collapse into a single compact line -
                suitable for embedding in an inline ``<style>``.

        Returns:
            CSS source string.

        Raises:
            ValueError: If any registered value contains dangerous content.
        """
        css_lines = []

        # CSS variables from theme
        if self.theme:
            css_lines.append(":root {")
            for key, value in self.theme.get_css_variables().items():
                css_lines.append(f"  {key}: {value};")
            css_lines.append("}")
            if pretty:
                css_lines.append("")  # Empty line for spacing

        # Render all classes
        for class_name, style in self._classes.items():
            class_css = self._render_class_styles(class_name, style)
            css_lines.extend(class_css)
            if pretty:
                css_lines.append("")  # Empty line between classes

        # Join with newlines if pretty, otherwise compact
        if pretty:
            return "\n".join(css_lines).rstrip()
        else:
            # Compact format
            return "".join(line.strip() for line in css_lines)

    def to_style_tag(self, pretty: bool = True) -> str:
        """Return the rendered CSS wrapped in a ready-to-drop ``<style>`` tag.

        Args:
            pretty: Forwarded to ``render()``; controls whether the
                inner CSS is pretty-printed or compact.

        Returns:
            A string starting with ``<style>`` and ending with ``</style>``.
        """
        css = self.render(pretty=pretty)
        if pretty:
            return f"<style>\n{css}\n</style>"
        else:
            return f"<style>{css}</style>"

    def count_classes(self) -> int:
        """Return the number of classes currently registered on this sheet."""
        return len(self._classes)

    def get_all_class_names(self) -> List[str]:
        """Return a list of every registered class name, in insertion order."""
        return list(self._classes.keys())

    def to_dict(self) -> Dict:
        """Serialize registered classes and breakpoint overrides to a dict.

        The result is JSON-safe and round-trips via ``from_dict()``. The
        associated ``Theme`` (if any) is not serialized here - pass it
        back in when deserializing.
        """
        return {
            "classes": {name: style.to_dict() for name, style in self._classes.items()},
            "breakpoints": self._breakpoint_values.copy(),
        }

    @classmethod
    def from_dict(cls, data: Dict, theme: Optional["Theme"] = None) -> "StyleSheet":
        """Reconstruct a ``StyleSheet`` from a ``to_dict()`` result.

        Args:
            data: Dict produced by ``to_dict()``.
            theme: Optional theme to attach to the new stylesheet; themes
                are not serialized by ``to_dict()`` and must be supplied
                here if they are needed.

        Returns:
            A new ``StyleSheet`` with matching classes and breakpoints.

        Raises:
            ValueError: If a serialized class name fails validation.
        """
        stylesheet = cls(theme=theme)

        # Restore breakpoints
        if "breakpoints" in data:
            stylesheet._breakpoint_values = data["breakpoints"].copy()

        # Restore classes (validate class names on deserialization)
        if "classes" in data:
            for name, style_data in data["classes"].items():
                if not _validate_class_name(name):
                    raise ValueError(
                        f"Invalid CSS class name in serialized data: {name!r}"
                    )
                style = CSSStyle.from_dict(style_data)
                stylesheet._classes[name] = style

        return stylesheet

    def __repr__(self) -> str:
        """Return a debug representation listing the registered class count."""
        return f"StyleSheet(classes={self.count_classes()})"
