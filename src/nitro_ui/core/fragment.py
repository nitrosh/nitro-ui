import html as html_module
from typing import Union, List, Any

from nitro_ui.core.element import HTMLElement, DEFAULT_MAX_DEPTH, register_tag


class Fragment(HTMLElement):
    """A container that renders only its children without wrapping tags.

    Useful for grouping elements without introducing extra DOM nodes.

    Example:
        fragment = Fragment(
            H1("Title"),
            Paragraph("Content")
        )
        # Renders: <h1>Title</h1><p>Content</p>
        # Instead of: <fragment><h1>Title</h1><p>Content</p></fragment>
    """

    def __init__(
        self, *children: Union["HTMLElement", str, List[Any]], **attributes: str
    ):
        # Initialize with a dummy tag name since we won't render it
        super().__init__(*children, tag="fragment", **attributes)

    def render(
        self,
        pretty: bool = False,
        _indent: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> str:
        """Renders only the children without the fragment wrapper.

        Args:
            pretty: If True, renders children with indentation
            _indent: Internal parameter for tracking indentation level
            max_depth: Maximum recursion depth (default 1000) to prevent stack overflow

        Returns:
            HTML string of all children concatenated

        Raises:
            RecursionError: If max_depth is exceeded
        """
        if _indent > max_depth:
            raise RecursionError(
                f"Maximum recursion depth ({max_depth}) exceeded in Fragment.render(). "
                "This usually indicates a circular reference in the element tree."
            )

        self.on_before_render()

        # Render only children, not the fragment tag itself
        if pretty:
            result = "".join(
                child.render(pretty=True, _indent=_indent, max_depth=max_depth)
                for child in self._children
            )
        else:
            result = "".join(
                child.render(pretty=False, _indent=_indent, max_depth=max_depth)
                for child in self._children
            )

        # Include text content if any
        if self._text:
            result = html_module.escape(self._text) + result

        self.on_after_render()
        return result


# Register fragment tag for from_dict() reconstruction
register_tag("fragment", Fragment)
