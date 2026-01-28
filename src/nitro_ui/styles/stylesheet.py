"""StyleSheet class for managing CSS classes in NitroUI."""

import re
from typing import Dict, Optional, List, TYPE_CHECKING

from .style import CSSStyle

if TYPE_CHECKING:
    from .theme import Theme


# Valid CSS class name pattern: must start with letter, underscore, or hyphen
# followed by letters, digits, underscores, or hyphens
_VALID_CLASS_NAME_PATTERN = re.compile(r"^-?[_a-zA-Z][_a-zA-Z0-9-]*$")

# Characters that could be used for CSS injection attacks
_DANGEROUS_CSS_CHARS = re.compile(r"[{}<>]|/\*|\*/|\\[0-9a-fA-F]")


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

    Args:
        value: The CSS value to sanitize

    Returns:
        Sanitized CSS value

    Raises:
        ValueError: If the value contains dangerous characters that cannot be sanitized
    """
    if not isinstance(value, str):
        value = str(value)

    # Check for dangerous patterns
    if _DANGEROUS_CSS_CHARS.search(value):
        raise ValueError(
            f"CSS value contains potentially dangerous characters: {value!r}"
        )

    # Check for url() with javascript: or data: protocols (potential XSS)
    lower_value = value.lower()
    if "url(" in lower_value:
        if "javascript:" in lower_value or "data:" in lower_value:
            raise ValueError(
                f"CSS value contains potentially dangerous URL protocol: {value!r}"
            )

    # Check for expression() (IE CSS expressions - XSS vector)
    if "expression(" in lower_value:
        raise ValueError(
            f"CSS value contains potentially dangerous expression(): {value!r}"
        )

    return value


class StyleSheet:
    """
    Manages CSS classes and generates <style> tag content.

    Usage:
        # Create stylesheet
        stylesheet = StyleSheet()

        # Register styles
        btn_class = stylesheet.register("btn-primary", CSSStyle(
            background_color="#007bff",
            color="white",
            padding="10px 20px",
            _hover=CSSStyle(background_color="#0056b3")
        ))

        # Use in HTML
        button = Button("Click", class_name=btn_class)

        # Render CSS
        css_output = stylesheet.render()
    """

    def __init__(self, theme: Optional["Theme"] = None):
        """
        Initialize StyleSheet.

        Args:
            theme: Optional Theme object to include CSS variables
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
        """
        Register a style as a CSS class.

        Args:
            name: Optional class name. If not provided, auto-generates one.
            style: CSSStyle object to register

        Returns:
            The class name (for use in class_name attribute)

        Raises:
            ValueError: If the class name is invalid (contains dangerous characters)
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
        """
        Register a style using BEM naming convention.

        Args:
            block: Block name (e.g., "button")
            element: Optional element name (e.g., "icon")
            modifier: Optional modifier name (e.g., "primary")
            style: CSSStyle object to register

        Returns:
            The BEM class name
        """
        # Build BEM class name
        class_name = block

        if element:
            class_name += f"__{element}"

        if modifier:
            class_name += f"--{modifier}"

        return self.register(class_name, style)

    def get_style(self, name: str) -> Optional[CSSStyle]:
        """
        Get a registered style by class name.

        Args:
            name: Class name

        Returns:
            CSSStyle object or None if not found
        """
        return self._classes.get(name)

    def has_class(self, name: str) -> bool:
        """
        Check if a class is registered.

        Args:
            name: Class name

        Returns:
            True if class exists
        """
        return name in self._classes

    def unregister(self, name: str) -> bool:
        """
        Remove a registered class.

        Args:
            name: Class name to remove

        Returns:
            True if class was removed, False if not found
        """
        if name in self._classes:
            del self._classes[name]
            return True
        return False

    def clear(self) -> None:
        """Remove all registered classes."""
        self._classes.clear()
        self._counter = 0

    def set_breakpoint(self, name: str, value: str) -> None:
        """
        Set or update a breakpoint value.

        Args:
            name: Breakpoint name (e.g., "sm", "md")
            value: CSS value (e.g., "640px")
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
                sanitized_value = _sanitize_css_value(value)
                css_lines.append(f"{indent_str}{prop}: {sanitized_value};")
            css_lines.append("}")

        # Pseudo-selectors
        for pseudo, pseudo_style in style._pseudo.items():
            if pseudo_style._styles:
                css_lines.append(f".{class_name}:{pseudo} {{")
                for prop, value in pseudo_style._styles.items():
                    sanitized_value = _sanitize_css_value(value)
                    css_lines.append(f"{indent_str}{prop}: {sanitized_value};")
                css_lines.append("}")

        # Responsive breakpoints
        for breakpoint, bp_style in style._breakpoints.items():
            if bp_style._styles:
                min_width = self._breakpoint_values.get(breakpoint, "0px")
                css_lines.append(f"@media (min-width: {min_width}) {{")
                css_lines.append(f"{indent_str}.{class_name} {{")
                for prop, value in bp_style._styles.items():
                    sanitized_value = _sanitize_css_value(value)
                    css_lines.append(
                        f"{indent_str}{indent_str}{prop}: {sanitized_value};"
                    )
                css_lines.append(f"{indent_str}}}")
                css_lines.append("}")

        return css_lines

    def render(self, pretty: bool = True) -> str:
        """
        Generate CSS output for all registered classes.

        Args:
            pretty: If True, format with newlines and indentation

        Returns:
            CSS string
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
        """
        Generate a complete <style> tag with all CSS.

        Args:
            pretty: If True, format with newlines and indentation

        Returns:
            HTML <style> tag with CSS
        """
        css = self.render(pretty=pretty)
        if pretty:
            return f"<style>\n{css}\n</style>"
        else:
            return f"<style>{css}</style>"

    def count_classes(self) -> int:
        """
        Get the number of registered classes.

        Returns:
            Number of classes
        """
        return len(self._classes)

    def get_all_class_names(self) -> List[str]:
        """
        Get a list of all registered class names.

        Returns:
            List of class names
        """
        return list(self._classes.keys())

    def to_dict(self) -> Dict:
        """
        Serialize stylesheet to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "classes": {name: style.to_dict() for name, style in self._classes.items()},
            "breakpoints": self._breakpoint_values.copy(),
        }

    @classmethod
    def from_dict(cls, data: Dict, theme: Optional["Theme"] = None) -> "StyleSheet":
        """
        Deserialize stylesheet from dictionary.

        Args:
            data: Dictionary representation
            theme: Optional theme to include

        Returns:
            New StyleSheet object
        """
        stylesheet = cls(theme=theme)

        # Restore breakpoints
        if "breakpoints" in data:
            stylesheet._breakpoint_values = data["breakpoints"].copy()

        # Restore classes
        if "classes" in data:
            for name, style_data in data["classes"].items():
                style = CSSStyle.from_dict(style_data)
                stylesheet._classes[name] = style

        return stylesheet

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"StyleSheet(classes={self.count_classes()})"
