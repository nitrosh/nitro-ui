"""Theme class for NitroUI styling system."""

import re
from typing import Dict, Optional, Any

from nitro_ui.core.element import _validate_css_value
from .style import CSSStyle

# Token names (color/spacing/typography keys) become part of the CSS variable
# identifier, so they must be safe to splice between ``--<group>-`` and the
# next character. Letters, digits, underscores, and hyphens only.
_VALID_TOKEN_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


class Theme:
    """Named design tokens plus component style presets.

    A ``Theme`` groups colors, typography, spacing, and per-component
    ``CSSStyle`` objects into a single bundle. When attached to a
    ``StyleSheet``, the theme's tokens are emitted as CSS custom
    properties inside a ``:root`` block. Three presets are included:
    :meth:`modern`, :meth:`classic`, and :meth:`minimal`.

    Example:
        >>> theme = Theme.modern()
        >>> "primary" in theme.colors
        True
        >>> "--color-primary" in theme.get_css_variables()
        True
    """

    def __init__(
        self,
        name: str = "Default",
        colors: Optional[Dict[str, str]] = None,
        typography: Optional[Dict[str, Any]] = None,
        spacing: Optional[Dict[str, str]] = None,
        components: Optional[Dict[str, Any]] = None,
    ):
        """Create a theme from individual token maps.

        Args:
            name: Human-readable label (e.g. ``"Modern"``).
            colors: Map of semantic color names to values - emitted as
                ``--color-<name>`` variables.
            typography: Font and size map - emitted as ``--font-...``
                variables. Nested dicts (e.g. ``sizes``) produce
                ``--font-<group>-<key>`` variables.
            spacing: Spacing scale - emitted as ``--spacing-<name>``.
            components: Per-component ``CSSStyle`` presets. Each value
                may be a single ``CSSStyle`` or a dict of variant names
                to ``CSSStyle`` (e.g. ``{"button": {"primary": ...}}``).
        """
        self.name = name
        self.colors = colors or {}
        self.typography = typography or {}
        self.spacing = spacing or {}
        self.components = components or {}

    def get_css_variables(self) -> Dict[str, str]:
        """Flatten colors, spacing, and typography into CSS custom properties.

        Called by ``StyleSheet.render()`` when a theme is attached, so
        every variable lands in the ``:root {}`` block. Token names and
        values are validated to prevent breaking out of the ``:root``
        declaration via braces, semicolons, or at-rules.

        Returns:
            A dict mapping variable names (``--color-primary``,
            ``--spacing-md``, ``--font-body``, ...) to their values.

        Raises:
            ValueError: If a token name contains characters that aren't
                safe in a CSS identifier, or a value contains injection
                patterns (``javascript:``, ``expression()``, braces, etc.).
        """

        def safe_key(group: str, key: str) -> str:
            if not isinstance(key, str) or not _VALID_TOKEN_NAME_PATTERN.match(key):
                raise ValueError(
                    f"Invalid theme {group} token name: {key!r}. Token names "
                    "must contain only letters, digits, underscores, or hyphens."
                )
            return key

        def safe_value(var_name: str, value: Any) -> str:
            text = str(value)
            if not _validate_css_value(text):
                raise ValueError(
                    f"Theme variable {var_name!r} contains potentially "
                    f"dangerous content: {text!r}. Values cannot contain "
                    "javascript:, expression(), braces, or other injection "
                    "patterns."
                )
            return text

        variables: Dict[str, str] = {}

        for key, value in self.colors.items():
            name = f"--color-{safe_key('color', key)}"
            variables[name] = safe_value(name, value)

        for key, value in self.spacing.items():
            name = f"--spacing-{safe_key('spacing', key)}"
            variables[name] = safe_value(name, value)

        if isinstance(self.typography, dict):
            for key, value in self.typography.items():
                if isinstance(value, str):
                    name = f"--font-{safe_key('typography', key)}"
                    variables[name] = safe_value(name, value)
                elif isinstance(value, dict):
                    group_key = safe_key("typography", key)
                    for sub_key, sub_value in value.items():
                        name = (
                            f"--font-{group_key}-"
                            f"{safe_key('typography', sub_key)}"
                        )
                        variables[name] = safe_value(name, sub_value)

        return variables

    def get_component_style(
        self, component: str, variant: str = "default"
    ) -> Optional[CSSStyle]:
        """Look up a preset ``CSSStyle`` for a component, optionally by variant.

        Components may be stored as a single style or as a map of
        variant names; this method handles both shapes.

        Args:
            component: Component key (e.g. ``"button"``, ``"card"``).
            variant: Variant to pull from a variant map (e.g.
                ``"primary"``). Ignored when the component is stored as
                a single style.

        Returns:
            The matching ``CSSStyle``, or ``None`` if the component or
            variant is not defined on this theme.
        """
        if component not in self.components:
            return None

        comp_styles = self.components[component]

        if isinstance(comp_styles, CSSStyle):
            return comp_styles
        elif isinstance(comp_styles, dict) and variant in comp_styles:
            return comp_styles[variant]

        return None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the theme (including nested component styles) to a dict.

        Returns a JSON-safe dict that round-trips via ``from_dict()``.
        Component entries that are ``CSSStyle`` instances are converted
        to their dict form.
        """
        return {
            "name": self.name,
            "colors": self.colors.copy(),
            "typography": self.typography.copy(),
            "spacing": self.spacing.copy(),
            "components": {
                name: (
                    style.to_dict()
                    if isinstance(style, CSSStyle)
                    else {
                        k: v.to_dict() if isinstance(v, CSSStyle) else v
                        for k, v in style.items()
                    }
                )
                for name, style in self.components.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """Reconstruct a ``Theme`` from a ``to_dict()`` result.

        Args:
            data: Dict previously produced by ``to_dict()``.

        Returns:
            A new ``Theme`` with equivalent tokens and components.
        """
        # Reconstruct components
        components = {}
        if "components" in data:
            for name, comp_data in data["components"].items():
                if isinstance(comp_data, dict):
                    # Check if it's a style dict or variants dict
                    if "styles" in comp_data:
                        components[name] = CSSStyle.from_dict(comp_data)
                    else:
                        # It's variants
                        components[name] = {
                            k: CSSStyle.from_dict(v) if isinstance(v, dict) else v
                            for k, v in comp_data.items()
                        }

        return cls(
            name=data.get("name", "Default"),
            colors=data.get("colors", {}),
            typography=data.get("typography", {}),
            spacing=data.get("spacing", {}),
            components=components,
        )

    def __repr__(self) -> str:
        """Return a debug representation containing the theme name."""
        return f"Theme(name='{self.name}')"

    # Preset themes

    @classmethod
    def modern(cls) -> "Theme":
        """Return the built-in "Modern" preset.

        A blue/violet palette with Inter-family fonts and rounded
        buttons. Suitable for contemporary SaaS interfaces.
        """
        return cls(
            name="Modern",
            colors={
                "primary": "#3b82f6",
                "primary-dark": "#2563eb",
                "secondary": "#8b5cf6",
                "secondary-dark": "#7c3aed",
                "neutral": "#6b7280",
                "success": "#10b981",
                "danger": "#ef4444",
                "warning": "#f59e0b",
                "info": "#3b82f6",
                "light": "#f3f4f6",
                "dark": "#1f2937",
                "white": "#ffffff",
                "black": "#000000",
            },
            typography={
                "body": "Inter, system-ui, -apple-system, sans-serif",
                "heading": "Inter, system-ui, -apple-system, sans-serif",
                "mono": "Consolas, Monaco, 'Courier New', monospace",
                "sizes": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "20px",
                    "2xl": "24px",
                    "3xl": "30px",
                    "4xl": "36px",
                },
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
                "3xl": "64px",
            },
            components={
                "button": {
                    "primary": CSSStyle(
                        background_color="var(--color-primary)",
                        color="var(--color-white)",
                        padding="12px 24px",
                        border_radius="6px",
                        border="none",
                        font_weight="600",
                        cursor="pointer",
                        transition="background-color 0.2s ease",
                        _hover=CSSStyle(background_color="var(--color-primary-dark)"),
                    ),
                    "secondary": CSSStyle(
                        background_color="var(--color-secondary)",
                        color="var(--color-white)",
                        padding="12px 24px",
                        border_radius="6px",
                        border="none",
                        font_weight="600",
                        cursor="pointer",
                        transition="background-color 0.2s ease",
                        _hover=CSSStyle(background_color="var(--color-secondary-dark)"),
                    ),
                },
                "card": CSSStyle(
                    background_color="var(--color-white)",
                    padding="var(--spacing-lg)",
                    border_radius="8px",
                    box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
                ),
            },
        )

    @classmethod
    def classic(cls) -> "Theme":
        """Return the built-in "Classic" preset.

        A Bootstrap-style palette with serif typography and square-ish
        components. Suitable for editorial or corporate interfaces.
        """
        return cls(
            name="Classic",
            colors={
                "primary": "#0066cc",
                "primary-dark": "#004c99",
                "secondary": "#6c757d",
                "secondary-dark": "#5a6268",
                "neutral": "#6c757d",
                "success": "#28a745",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#17a2b8",
                "light": "#f8f9fa",
                "dark": "#343a40",
                "white": "#ffffff",
                "black": "#000000",
            },
            typography={
                "body": "Georgia, 'Times New Roman', Times, serif",
                "heading": "Georgia, 'Times New Roman', Times, serif",
                "mono": "Courier New, Courier, monospace",
                "sizes": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "21px",
                    "2xl": "24px",
                    "3xl": "32px",
                    "4xl": "40px",
                },
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
                "3xl": "64px",
            },
            components={
                "button": {
                    "primary": CSSStyle(
                        background_color="var(--color-primary)",
                        color="var(--color-white)",
                        padding="10px 20px",
                        border_radius="4px",
                        border="none",
                        font_weight="400",
                        cursor="pointer",
                        transition="background-color 0.3s ease",
                        _hover=CSSStyle(background_color="var(--color-primary-dark)"),
                    ),
                    "secondary": CSSStyle(
                        background_color="var(--color-white)",
                        color="var(--color-primary)",
                        padding="10px 20px",
                        border_radius="4px",
                        border="2px solid var(--color-primary)",
                        font_weight="400",
                        cursor="pointer",
                        transition="all 0.3s ease",
                        _hover=CSSStyle(
                            background_color="var(--color-primary)",
                            color="var(--color-white)",
                        ),
                    ),
                },
                "card": CSSStyle(
                    background_color="var(--color-white)",
                    padding="var(--spacing-lg)",
                    border_radius="4px",
                    border="1px solid var(--color-light)",
                    box_shadow="0 2px 4px rgba(0, 0, 0, 0.05)",
                ),
            },
        )

    @classmethod
    def minimal(cls) -> "Theme":
        """Return the built-in "Minimal" preset.

        Black-and-white palette with system fonts, flat buttons, and
        no rounding. Suitable for content-heavy, text-first interfaces.
        """
        return cls(
            name="Minimal",
            colors={
                "primary": "#000000",
                "primary-dark": "#333333",
                "secondary": "#666666",
                "secondary-dark": "#444444",
                "neutral": "#999999",
                "success": "#00cc00",
                "danger": "#cc0000",
                "warning": "#cc9900",
                "info": "#0099cc",
                "light": "#f5f5f5",
                "dark": "#1a1a1a",
                "white": "#ffffff",
                "black": "#000000",
            },
            typography={
                "body": (
                    "-apple-system, BlinkMacSystemFont, 'Segoe UI', "
                    "Helvetica, Arial, sans-serif"
                ),
                "heading": (
                    "-apple-system, BlinkMacSystemFont, 'Segoe UI', "
                    "Helvetica, Arial, sans-serif"
                ),
                "mono": "'SF Mono', Monaco, 'Cascadia Code', monospace",
                "sizes": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "20px",
                    "2xl": "24px",
                    "3xl": "32px",
                    "4xl": "40px",
                },
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
                "3xl": "64px",
            },
            components={
                "button": {
                    "primary": CSSStyle(
                        background_color="var(--color-primary)",
                        color="var(--color-white)",
                        padding="8px 16px",
                        border_radius="0px",
                        border="none",
                        font_weight="500",
                        cursor="pointer",
                        transition="opacity 0.2s ease",
                        _hover=CSSStyle(opacity="0.8"),
                    ),
                    "secondary": CSSStyle(
                        background_color="var(--color-white)",
                        color="var(--color-primary)",
                        padding="8px 16px",
                        border_radius="0px",
                        border="1px solid var(--color-primary)",
                        font_weight="500",
                        cursor="pointer",
                        transition="all 0.2s ease",
                        _hover=CSSStyle(
                            background_color="var(--color-primary)",
                            color="var(--color-white)",
                        ),
                    ),
                },
                "card": CSSStyle(
                    background_color="var(--color-white)",
                    padding="var(--spacing-md)",
                    border_radius="0px",
                    border="1px solid var(--color-light)",
                ),
            },
        )
