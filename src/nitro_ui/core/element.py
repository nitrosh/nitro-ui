import copy
import html
import json
import os
import re
import uuid
import warnings
from typing import Callable, Any, Iterator, Union, List, Tuple

# Default maximum recursion depth for tree traversal operations
DEFAULT_MAX_DEPTH = 1000

# Pattern for detecting potentially dangerous CSS values
_DANGEROUS_CSS_PATTERN = re.compile(
    r'javascript:|expression\s*\(|url\s*\(\s*["\']?\s*data:|'
    r'url\s*\(\s*["\']?\s*javascript:|'
    r"[{}<>]|/\*|\*/|\\[0-9a-fA-F]",
    re.IGNORECASE,
)

# Valid HTML tag name pattern
_VALID_TAG_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]*$")

# Valid HTML attribute name pattern
_VALID_ATTR_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_:.@-]*$")

# HTML5 boolean attributes that should render as bare attributes
_BOOLEAN_ATTRIBUTES = frozenset(
    {
        "allowfullscreen",
        "async",
        "autofocus",
        "autoplay",
        "checked",
        "controls",
        "default",
        "defer",
        "disabled",
        "formnovalidate",
        "hidden",
        "inert",
        "ismap",
        "itemscope",
        "loop",
        "multiple",
        "muted",
        "nomodule",
        "novalidate",
        "open",
        "playsinline",
        "readonly",
        "required",
        "reversed",
        "selected",
    }
)

# Cache the environment variable check at module load time
_GENERATE_IDS = bool(os.environ.get("NITRO_UI_GENERATE_IDS"))

# SVG attributes that require camelCase.
# Maps lowercase -> correct camelCase form (per the SVG spec).
# Used by the parser to restore casing after html.parser lowercases,
# and by element rendering to output the correct attribute name.
_SVG_CAMEL_ATTRS = {
    "viewbox": "viewBox",
    "basefrequency": "baseFrequency",
    "calcmode": "calcMode",
    "clippathunits": "clipPathUnits",
    "diffuseconstant": "diffuseConstant",
    "edgemode": "edgeMode",
    "filterunits": "filterUnits",
    "glyphref": "glyphRef",
    "gradienttransform": "gradientTransform",
    "gradientunits": "gradientUnits",
    "kernelmatrix": "kernelMatrix",
    "kernelunitlength": "kernelUnitLength",
    "keypoints": "keyPoints",
    "keysplines": "keySplines",
    "keytimes": "keyTimes",
    "lengthadjust": "lengthAdjust",
    "limitingconeangle": "limitingConeAngle",
    "markerheight": "markerHeight",
    "markerunits": "markerUnits",
    "markerwidth": "markerWidth",
    "maskcontentunits": "maskContentUnits",
    "maskunits": "maskUnits",
    "numoctaves": "numOctaves",
    "pathlength": "pathLength",
    "patterncontentunits": "patternContentUnits",
    "patterntransform": "patternTransform",
    "patternunits": "patternUnits",
    "pointsatx": "pointsAtX",
    "pointsaty": "pointsAtY",
    "pointsatz": "pointsAtZ",
    "preserveaspectratio": "preserveAspectRatio",
    "primitiveunits": "primitiveUnits",
    "refx": "refX",
    "refy": "refY",
    "repeatcount": "repeatCount",
    "repeatdur": "repeatDur",
    "requiredextensions": "requiredExtensions",
    "requiredfeatures": "requiredFeatures",
    "specularconstant": "specularConstant",
    "specularexponent": "specularExponent",
    "spreadmethod": "spreadMethod",
    "startoffset": "startOffset",
    "stddeviation": "stdDeviation",
    "stitchtiles": "stitchTiles",
    "surfacescale": "surfaceScale",
    "systemlanguage": "systemLanguage",
    "tablevalues": "tableValues",
    "targetx": "targetX",
    "targety": "targetY",
    "textlength": "textLength",
    "xchannelselector": "xChannelSelector",
    "ychannelselector": "yChannelSelector",
    "zoomandpan": "zoomAndPan",
}

# Reverse map: snake_case kwarg -> camelCase SVG attribute name.
# e.g. "view_box" -> "viewBox", "gradient_units" -> "gradientUnits"
# Built from _SVG_CAMEL_ATTRS by converting each camelCase name to
# its snake_case equivalent.


def _build_svg_snake_map():
    """Build snake_case -> camelCase map for SVG attrs."""
    result = {}
    for camel in _SVG_CAMEL_ATTRS.values():
        # Convert camelCase to snake_case: viewBox -> view_box
        snake = re.sub(r"([a-z])([A-Z])", r"\1_\2", camel).lower()
        result[snake] = camel
    return result


_SVG_SNAKE_TO_CAMEL = _build_svg_snake_map()

_PRESERVE_UNDERSCORE = frozenset({"class_name", "for_element"})

_KEYWORD_MAPPINGS = {
    "class_": "class_name",
    "cls": "class_name",
    "for_": "for_element",
}

_ATTR_ALIASES = {
    "class": "class_name",
    "class_name": "class",
    "for": "for_element",
    "for_element": "for",
}

_ATTR_RENDER_MAP = {
    "class_name": "class",
    "for_element": "for",
}

# Raw text elements: browsers do not decode entities inside these, so their
# text must not be HTML-escaped.
_RAW_TEXT_TAGS = frozenset({"script", "style"})

_WHITESPACE_SENSITIVE_TAGS = frozenset({"pre", "textarea", "script", "style"})

_RAW_TEXT_CLOSE_PATTERN = re.compile(r"</(script|style)", re.IGNORECASE)


def _normalize_attr_key(key: str) -> str:
    """Convert a Python kwarg name to the stored attribute name.

    ``class_``/``cls`` -> ``class_name``, ``for_`` -> ``for_element``,
    ``view_box`` -> ``viewBox``, and remaining underscores become hyphens
    (``data_value`` -> ``data-value``).
    """
    if key in _KEYWORD_MAPPINGS:
        return _KEYWORD_MAPPINGS[key]
    if key in _PRESERVE_UNDERSCORE:
        return key
    if key in _SVG_SNAKE_TO_CAMEL:
        return _SVG_SNAKE_TO_CAMEL[key]
    return key.replace("_", "-")


def _escape_raw_text(tag: str, text: str) -> str:
    """Make text safe inside ``<script>``/``<style>`` without entity-escaping it.

    Neutralises any sequence that would end the element early.
    """
    text = _RAW_TEXT_CLOSE_PATTERN.sub(lambda m: "<\\/" + m.group(1), text)
    if tag == "script":
        text = text.replace("<!--", "<\\!--")
    return text


def _render_attr_value(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return html.escape(str(value), quote=True)


_VALID_CSS_PROPERTY_PATTERN = re.compile(
    r"^(--[a-zA-Z0-9_-]+|-?[a-zA-Z][a-zA-Z0-9-]*)$"
)


def _validate_css_value(value: str) -> bool:
    """Validate that a single CSS value doesn't contain injection attacks.

    Rejects ``;`` as well, since a single value must not be able to start
    a new declaration.

    Args:
        value: The CSS value to validate

    Returns:
        True if safe, False if potentially dangerous
    """
    if not isinstance(value, str):
        return True
    return ";" not in value and not _DANGEROUS_CSS_PATTERN.search(value)


def _validate_css_declarations(value: str) -> bool:
    """Validate a full inline style string such as ``"color: red; margin: 0"``."""
    if not isinstance(value, str):
        return True
    return not _DANGEROUS_CSS_PATTERN.search(value)


def _validate_css_property(name: str) -> bool:
    """Return True if ``name`` is a plausible CSS property or custom property."""
    return isinstance(name, str) and bool(_VALID_CSS_PROPERTY_PATTERN.match(name))


class HTMLElement:
    """Foundation class for every HTML element in NitroUI.

    Owns the tag name, attributes, inline styles, and a list of children
    (other ``HTMLElement`` instances or plain strings). All mutating methods
    return ``self`` so calls chain. Instances are also context managers and
    are serializable to JSON or HTML.

    Children may be passed positionally; keyword arguments become HTML
    attributes. Python keywords are handled via ``class_name`` / ``for_element``
    (``class_`` and ``for_`` are also accepted). Underscores in other kwargs
    are converted to hyphens (``data_value`` -> ``data-value``); SVG
    camelCase attributes (``view_box`` -> ``viewBox``) are preserved.

    Text content and attribute values are HTML-escaped automatically; only
    ``render()`` output is unescaped.

    Example:
        >>> el = HTMLElement("Hello", tag="div", class_name="greeting")
        >>> el.append(HTMLElement("world", tag="span")).render()
        '<div class="greeting">Hello<span>world</span></div>'
    """

    __slots__ = [
        "_tag",
        "_children",
        "_attributes",
        "_self_closing",
        "_styles_cache",
        "_prefix",
    ]

    def __init__(
        self,
        *children: Union["HTMLElement", str, List[Any]],
        tag: str,
        self_closing: bool = False,
        **attributes: str,
    ):
        """Create an HTML element with the given tag, children, and attributes.

        Args:
            *children: Positional children. Each may be an ``HTMLElement``,
                a string (appended to text content), a list/tuple of either
                (flattened recursively), or ``None`` (skipped).
            tag: HTML tag name (e.g. ``"div"``). Must match
                ``^[a-zA-Z][a-zA-Z0-9-]*$``.
            self_closing: If ``True``, renders as ``<tag />`` with no
                closing tag. Adding children emits a warning.
            **attributes: HTML attributes. See class docstring for the
                naming conventions applied to keys.

        Raises:
            ValueError: If ``tag`` is empty, malformed, a child has an
                unsupported type, or ``style`` contains dangerous CSS.
        """
        if not tag:
            raise ValueError("A valid HTML tag name is required")

        # Validate tag name to prevent injection
        if not _VALID_TAG_PATTERN.match(tag):
            raise ValueError(
                f"Invalid HTML tag name: {tag!r}. "
                "Tag names must start with a letter and contain only "
                "letters, digits, and hyphens."
            )

        fixed_attributes = {_normalize_attr_key(k): v for k, v in attributes.items()}
        self._check_style_attribute(fixed_attributes.get("style"))

        self._tag: str = tag
        self._children: List[Union[HTMLElement, str]] = self._coerce_children(children)
        self._attributes: dict = fixed_attributes
        self._self_closing: bool = self_closing
        self._styles_cache: Union[dict, None] = None
        self._prefix: Union[str, None] = None

        if _GENERATE_IDS:
            self.generate_id()

        if self._self_closing and self._children:
            warnings.warn(
                f"Self-closing element <{self._tag} /> cannot "
                "have children or text. Content will be "
                "discarded during rendering.",
                UserWarning,
                stacklevel=2,
            )

        self.on_load()

    def __str__(self) -> str:
        return self.render()

    def __del__(self) -> None:
        # Note: __del__ may not be called for objects with circular references.
        # Do not rely on on_unload() for critical cleanup operations.
        # Consider using context managers or explicit cleanup methods instead.
        try:
            self.on_unload()
        except Exception:
            # Suppress exceptions during garbage collection to avoid
            # confusing error messages during interpreter shutdown
            pass

    def __enter__(self) -> "HTMLElement":
        """Enter a ``with`` block, returning this element for further mutation."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit a ``with`` block. No cleanup is required."""
        pass

    @staticmethod
    def _flatten(items: Union[List[Any], tuple]) -> Iterator[Any]:
        """Recursively flattens nested iterables of children."""
        for item in items:
            if isinstance(item, (list, tuple)):
                yield from HTMLElement._flatten(item)
            else:
                yield item

    @staticmethod
    def _coerce_children(items: Any) -> List[Union["HTMLElement", str]]:
        """Flatten and validate children, keeping elements and text in order."""
        nodes: List[Union[HTMLElement, str]] = []
        for child in HTMLElement._flatten(items):
            if isinstance(child, HTMLElement):
                nodes.append(child)
            elif isinstance(child, str):
                if child:
                    nodes.append(child)
            elif child is not None:
                raise ValueError(
                    f"Invalid child type: {type(child).__name__}. "
                    "Children must be HTMLElement instances or strings."
                )
        return nodes

    def _element_children(self) -> List["HTMLElement"]:
        return [c for c in self._children if isinstance(c, HTMLElement)]

    def _node_index(self, index: int) -> int:
        """Map an index into the element-only child list to a node index."""
        positions = [
            i for i, c in enumerate(self._children) if isinstance(c, HTMLElement)
        ]
        return positions[index]

    def prepend(self, *children: Union["HTMLElement", str, List[Any]]) -> "HTMLElement":
        """Insert children at the front of this element.

        Mirrors ``append()`` but adds content at the start rather than the
        end. Text and elements keep the order they were given in.

        Args:
            *children: Elements, strings, or nested lists/tuples. ``None``
                values are skipped.

        Returns:
            This element, for chaining.

        Raises:
            ValueError: If any child is not an ``HTMLElement`` or string.

        Example:
            >>> Div(H2("Body")).prepend(H1("Title")).render()
            '<div><h1>Title</h1><h2>Body</h2></div>'
        """
        self._children = self._coerce_children(children) + self._children
        return self

    def append(self, *children: Union["HTMLElement", str, List[Any]]) -> "HTMLElement":
        """Add children to the end of this element.

        Text and elements render in the order they were added, so
        ``Paragraph("Hello ", Strong("world"), "!")`` keeps the ``!`` after
        the ``<strong>``. Nested lists/tuples are flattened so you can
        splice collections in directly.

        Args:
            *children: Elements, strings, or nested lists/tuples. ``None``
                values are skipped.

        Returns:
            This element, for chaining.

        Raises:
            ValueError: If any child is not an ``HTMLElement`` or string.

        Example:
            >>> Div().append(H1("Title"), Paragraph("Body")).render()
            '<div><h1>Title</h1><p>Body</p></div>'
        """
        self._children.extend(self._coerce_children(children))
        return self

    def filter(
        self,
        condition: Callable[[Any], bool],
        recursive: bool = False,
        max_depth: int = DEFAULT_MAX_DEPTH,
        _current_depth: int = 0,
    ) -> Iterator["HTMLElement"]:
        """Yield child elements (and optionally descendants) matching a predicate.

        Text nodes are never passed to ``condition``.

        Args:
            condition: Called with each child; return ``True`` to yield it.
            recursive: If ``True``, walk the full subtree; otherwise only
                direct children are considered.
            max_depth: Traversal cutoff (default 1000) guarding against
                circular references.

        Yields:
            Matching ``HTMLElement`` instances.

        Raises:
            RecursionError: If ``max_depth`` is exceeded.

        Example:
            >>> list(page.filter(lambda c: c.tag == "img", recursive=True))
            [<Image ...>, <Image ...>]
        """
        if _current_depth > max_depth:
            raise RecursionError(
                f"Maximum recursion depth ({max_depth}) exceeded in filter(). "
                "Consider increasing max_depth or checking for circular references."
            )
        for child in self._element_children():
            if condition(child):
                yield child
            if recursive:
                yield from child.filter(
                    condition,
                    recursive=True,
                    max_depth=max_depth,
                    _current_depth=_current_depth + 1,
                )

    def remove_all(self, condition: Callable[[Any], bool]) -> "HTMLElement":
        """Remove every direct child element matching a predicate.

        Only the immediate children are considered (not descendants), and
        text nodes are left alone.

        Args:
            condition: Called with each child; return ``True`` to remove it.

        Returns:
            This element, for chaining.
        """
        self._children = [
            c
            for c in self._children
            if not (isinstance(c, HTMLElement) and condition(c))
        ]
        return self

    def clear(self) -> "HTMLElement":
        """Remove all child elements from this element.

        Text content is left untouched; use ``text = ""`` to clear it.

        Returns:
            This element, for chaining.
        """
        self._children = [c for c in self._children if isinstance(c, str)]
        return self

    def pop(self, index: int = 0) -> "HTMLElement":
        """Remove and return a child element by position.

        Positions count elements only; text nodes are skipped.

        Args:
            index: Position to remove from; defaults to the first child.

        Returns:
            The removed ``HTMLElement``.

        Raises:
            IndexError: If the element has no children or the index is
                out of range.
        """
        try:
            node_index = self._node_index(index)
        except IndexError:
            raise IndexError("pop index out of range") from None
        return self._children.pop(node_index)

    def first(self) -> Union["HTMLElement", None]:
        """Return the first child element, or ``None`` if there are none."""
        elements = self._element_children()
        return elements[0] if elements else None

    def last(self) -> Union["HTMLElement", None]:
        """Return the last child element, or ``None`` if there are none."""
        elements = self._element_children()
        return elements[-1] if elements else None

    def _resolve_attr_key(self, key: str) -> str:
        """Normalize ``key`` and map it onto an existing alias if present.

        ``class``/``class_name`` and ``for``/``for_element`` refer to the
        same attribute, whichever spelling was used to set it.
        """
        key = _normalize_attr_key(key)
        alias = _ATTR_ALIASES.get(key)
        if key not in self._attributes and alias in self._attributes:
            return alias
        return key

    @staticmethod
    def _check_style_attribute(value: Any) -> None:
        if isinstance(value, str) and not _validate_css_declarations(value):
            raise ValueError(
                f"Inline style contains potentially dangerous content: {value!r}. "
                "Styles cannot contain javascript:, expression(), or other "
                "injection patterns."
            )

    def add_attribute(self, key: str, value: str) -> "HTMLElement":
        """Set a single HTML attribute on this element.

        Keys are normalized the same way as constructor kwargs
        (``data_value`` -> ``data-value``), and ``class``/``class_name`` or
        ``for``/``for_element`` update the same attribute. Setting the
        ``style`` attribute invalidates the parsed-styles cache used by
        ``add_style`` / ``get_style``.

        Args:
            key: Attribute name.
            value: Attribute value. Will be HTML-escaped at render time.

        Returns:
            This element, for chaining.

        Raises:
            ValueError: If ``key`` is ``style`` and the value contains
                dangerous CSS.
        """
        key = self._resolve_attr_key(key)
        if key == "style":
            self._check_style_attribute(value)
            self._styles_cache = None
        self._attributes[key] = value
        return self

    def add_attributes(self, attributes: List[Tuple[str, str]]) -> "HTMLElement":
        """Set multiple HTML attributes in one call.

        Args:
            attributes: Iterable of ``(key, value)`` pairs.

        Returns:
            This element, for chaining.

        Example:
            >>> el.add_attributes([("id", "main"), ("data-role", "card")])
        """
        for key, value in attributes:
            self.add_attribute(key, value)
        return self

    def remove_attribute(self, key: str) -> "HTMLElement":
        """Remove an attribute by key. Missing keys are silently ignored.

        Args:
            key: Attribute name to remove.

        Returns:
            This element, for chaining.
        """
        key = self._resolve_attr_key(key)
        self._attributes.pop(key, None)
        if key == "style":
            self._styles_cache = None
        return self

    def get_attribute(self, key: str) -> Union[str, None]:
        """Return the value of a named attribute, or ``None`` if absent."""
        return self._attributes.get(self._resolve_attr_key(key))

    def has_attribute(self, key: str) -> bool:
        """Return ``True`` if the given attribute is set on this element."""
        return self._resolve_attr_key(key) in self._attributes

    def _get_styles_dict(self) -> dict:
        """Gets the cached styles dictionary, parsing if necessary.

        Returns:
            Dictionary of CSS properties and values
        """
        if self._styles_cache is None:
            current_style = self._attributes.get("style", "")
            self._styles_cache = self._parse_styles(current_style)
        return self._styles_cache

    def _flush_styles_cache(self) -> None:
        """Flushes the styles cache back to the style attribute."""
        if self._styles_cache is not None:
            if self._styles_cache:
                self._attributes["style"] = self._format_styles(self._styles_cache)
            else:
                self._attributes.pop("style", None)

    @staticmethod
    def _check_style_declaration(key: str, value: Any) -> None:
        if not _validate_css_property(key):
            raise ValueError(f"Invalid CSS property name: {key!r}")
        if not _validate_css_value(str(value)):
            raise ValueError(
                f"CSS value for '{key}' contains potentially "
                f"dangerous content: {value!r}. "
                "Values cannot contain ';', javascript:, expression(),"
                " or other injection patterns."
            )

    def add_style(self, key: str, value: str) -> "HTMLElement":
        """Add a single inline CSS declaration to this element.

        The property name must be a valid CSS identifier, and values are
        checked for ``;`` and common injection patterns (``javascript:``,
        ``expression(...)``, etc.) before being stored.

        Args:
            key: CSS property name (e.g. ``"color"``, ``"font-size"``).
            value: CSS property value (e.g. ``"red"``, ``"14px"``).

        Returns:
            This element, for chaining.

        Raises:
            ValueError: If ``key`` is not a valid CSS property name or
                ``value`` contains potentially dangerous content.

        Example:
            >>> Div().add_style("color", "red").render()
            '<div style="color: red"></div>'
        """
        self._check_style_declaration(key, value)
        styles_dict = self._get_styles_dict()
        styles_dict[key] = value
        self._flush_styles_cache()
        return self

    def add_styles(self, styles: dict) -> "HTMLElement":
        """Merge a dict of inline CSS declarations into this element.

        Later keys overwrite earlier ones on the element. All values are
        validated before any are stored.

        Args:
            styles: Mapping of CSS property names to values, e.g.
                ``{"color": "red", "font-size": "14px"}``.

        Returns:
            This element, for chaining.

        Raises:
            ValueError: If any key is not a valid CSS property name or any
                value contains potentially dangerous content.
        """
        for key, value in styles.items():
            self._check_style_declaration(key, value)
        styles_dict = self._get_styles_dict()
        styles_dict.update(styles)
        self._flush_styles_cache()
        return self

    def get_style(self, key: str) -> Union[str, None]:
        """Return the inline CSS value for a property, or ``None`` if unset.

        Args:
            key: CSS property name (e.g. ``"color"``).

        Returns:
            The stored value, or ``None`` if this element has no such
            inline declaration.
        """
        styles_dict = self._get_styles_dict()
        return styles_dict.get(key)

    def remove_style(self, key: str) -> "HTMLElement":
        """Remove an inline CSS declaration by property name.

        Missing keys are silently ignored. If this removes the last
        declaration, the ``style`` attribute is dropped entirely.

        Args:
            key: CSS property name to remove.

        Returns:
            This element, for chaining.
        """
        styles_dict = self._get_styles_dict()
        styles_dict.pop(key, None)
        self._flush_styles_cache()
        return self

    @staticmethod
    def _parse_styles(style_str: str) -> dict:
        """
        Parses a CSS style string into a dictionary.
        Handles semicolons inside url() and other functional notation.

        Args:
            style_str: CSS style string (e.g., "color: red; font-size: 14px")

        Returns:
            Dictionary of CSS properties and values
        """
        if not style_str:
            return {}

        styles = {}
        # Split respecting parentheses (don't split on ; inside parens)
        depth = 0
        current = []
        for char in style_str:
            if char == "(":
                depth += 1
                current.append(char)
            elif char == ")":
                depth -= 1
                current.append(char)
            elif char == ";" and depth == 0:
                part = "".join(current).strip()
                if ":" in part:
                    key, value = part.split(":", 1)
                    styles[key.strip()] = value.strip()
                current = []
            else:
                current.append(char)
        # Handle the last segment
        part = "".join(current).strip()
        if ":" in part:
            key, value = part.split(":", 1)
            styles[key.strip()] = value.strip()

        return styles

    @staticmethod
    def _format_styles(styles_dict: dict) -> str:
        """
        Formats a dictionary of styles into a CSS style string.

        Args:
            styles_dict: Dictionary of CSS properties and values

        Returns:
            CSS style string (e.g., "color: red; font-size: 14px")
        """
        return "; ".join(f"{k}: {v}" for k, v in styles_dict.items())

    def generate_id(self) -> None:
        """Assign an auto-generated ``id`` attribute if one is not already set.

        The id is ``"el-"`` followed by the first 6 hex characters of a
        UUID4. Called automatically on construction when the
        ``NITRO_UI_GENERATE_IDS`` environment variable is set.
        """
        if "id" not in self._attributes:
            self._attributes["id"] = f"el-{str(uuid.uuid4())[:6]}"

    def clone(self) -> "HTMLElement":
        """Return a deep copy of this element and its entire subtree."""
        return copy.deepcopy(self)

    def replace_child(self, old_index: int, new_child: "HTMLElement") -> None:
        """Swap a child element at the given index with a new element.

        Positions count elements only; text nodes are skipped.

        Args:
            old_index: Position of the child to replace.
            new_child: Replacement element.

        Raises:
            ValueError: If ``new_child`` is not an ``HTMLElement``.
            IndexError: If ``old_index`` is out of range.
        """
        if not isinstance(new_child, HTMLElement):
            raise ValueError(
                f"new_child must be an HTMLElement, got {type(new_child).__name__}"
            )
        self._children[self._node_index(old_index)] = new_child

    def find_by_attribute(
        self,
        attr_name: str,
        attr_value: Any,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> Union["HTMLElement", None]:
        """Return the first descendant (or self) whose attribute matches.

        Performs a depth-first search through the subtree; the current
        element itself is checked before its children.

        Args:
            attr_name: Attribute name to look up on each visited element.
            attr_value: Value to compare against; must match exactly.
            max_depth: Traversal cutoff (default 1000) guarding against
                circular references.

        Returns:
            The first matching element, or ``None`` if no match is found.

        Raises:
            RecursionError: If ``max_depth`` is exceeded.
        """

        def _find(
            element: "HTMLElement", current_depth: int = 0
        ) -> Union["HTMLElement", None]:
            if current_depth > max_depth:
                raise RecursionError(
                    f"Maximum recursion depth ({max_depth}) "
                    "exceeded in find_by_attribute(). "
                    "Consider increasing max_depth or "
                    "checking for circular references."
                )
            if element.get_attribute(attr_name) == attr_value:
                return element
            for child in element._element_children():
                result = _find(child, current_depth + 1)
                if result:
                    return result
            return None

        return _find(self)

    def get_attributes(self, *keys: str) -> dict:
        """Return a copy of attributes, optionally restricted to given keys.

        Args:
            *keys: If provided, the returned dict is limited to these keys;
                missing keys map to ``None``. If omitted, all attributes
                are returned.

        Returns:
            A new dict; mutating it does not affect the element.
        """
        if keys:
            return {key: self.get_attribute(key) for key in keys}
        return self._attributes.copy()

    def count_children(self) -> int:
        """Return the number of direct child elements (not including text)."""
        return len(self._element_children())

    def on_load(self) -> None:
        """Hook called at the end of ``__init__``. Override for custom setup."""
        pass

    def on_before_render(self) -> None:
        """Hook called immediately before this element renders itself.

        Override to mutate the tree right before serialization. Called by
        ``render()`` on each invocation, including nested child renders.
        """
        pass

    def on_after_render(self) -> None:
        """Hook called immediately after this element finishes rendering."""
        pass

    def on_unload(self) -> None:
        """Hook called from ``__del__``. Do not rely on this for cleanup.

        Python's garbage collector may skip ``__del__`` for objects
        participating in reference cycles. Use explicit cleanup or context
        managers for anything load-bearing.
        """
        pass

    @property
    def tag(self) -> str:
        """The HTML tag name (e.g. ``"div"``, ``"span"``)."""
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        if not value:
            raise ValueError("A valid HTML tag name is required")
        if not _VALID_TAG_PATTERN.match(value):
            raise ValueError(
                f"Invalid HTML tag name: {value!r}. "
                "Tag names must start with a letter and contain only "
                "letters, digits, and hyphens."
            )
        self._tag = value

    @property
    def children(self) -> List["HTMLElement"]:
        """A shallow copy of the list of child elements (text excluded).

        The returned list can be mutated without affecting this element.
        Assigning to this property replaces the child elements; existing
        text is kept and placed before them. Use ``nodes`` to get or set
        text and elements together in order.
        """
        return self._element_children()

    @children.setter
    def children(self, value: List["HTMLElement"]) -> None:
        nodes = self._coerce_children(value)
        text = [c for c in self._children if isinstance(c, str)]
        self._children = text + nodes

    @property
    def nodes(self) -> List[Union["HTMLElement", str]]:
        """A shallow copy of all children, text and elements, in render order."""
        return list(self._children)

    @nodes.setter
    def nodes(self, value: List[Union["HTMLElement", str]]) -> None:
        self._children = self._coerce_children(value)

    @property
    def text(self) -> str:
        """All text content of this element joined together (unescaped)."""
        return "".join(c for c in self._children if isinstance(c, str))

    @text.setter
    def text(self, value: str) -> None:
        """Replace all text nodes with ``value``, placed before any elements."""
        elements = self._element_children()
        self._children = ([value] if value else []) + elements

    @property
    def attributes(self) -> dict:
        """Live dict of attributes. Mutation invalidates the styles cache on assign."""
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict) -> None:
        self._attributes = value
        self._styles_cache = None

    @property
    def self_closing(self) -> bool:
        """Whether this element renders as a void/self-closing tag."""
        return self._self_closing

    @self_closing.setter
    def self_closing(self, value: bool) -> None:
        self._self_closing = value

    def _render_attributes(self) -> str:
        """Returns a string of HTML attributes for the tag.

        Python ``True``/``False`` on boolean HTML attributes (``disabled``,
        ``checked``, ...) add or omit the bare attribute. On any other
        attribute they render as ``"true"``/``"false"``.
        """
        parts = []
        for k, v in self._attributes.items():
            render_k = _ATTR_RENDER_MAP.get(k, k)

            if not _VALID_ATTR_PATTERN.match(render_k):
                warnings.warn(
                    f"Skipping invalid attribute name: {render_k!r}",
                    UserWarning,
                    stacklevel=3,
                )
                continue

            if v is None:
                continue

            if render_k.lower() in _BOOLEAN_ATTRIBUTES:
                if v is True or v == "" or v == render_k:
                    parts.append(render_k)
                elif v is not False:
                    parts.append(f'{render_k}="{_render_attr_value(v)}"')
            else:
                parts.append(f'{render_k}="{_render_attr_value(v)}"')

        attr_str = " ".join(parts)
        return f" {attr_str}" if attr_str else ""

    def _render_text(self, text: str) -> str:
        tag = self._tag.lower()
        if tag in _RAW_TEXT_TAGS:
            return _escape_raw_text(tag, text)
        return html.escape(text)

    def _render_nodes(self, pretty: bool, _indent: int, max_depth: int) -> str:
        """Render this element's children (text and elements) in order."""
        if not pretty or self._tag.lower() in _WHITESPACE_SENSITIVE_TAGS:
            return "".join(
                (
                    self._render_text(node)
                    if isinstance(node, str)
                    else node.render(
                        pretty=False, _indent=_indent + 1, max_depth=max_depth
                    )
                )
                for node in self._children
            )

        child_indent = "  " * (_indent + 1)
        parts = []
        at_line_start = False
        for node in self._children:
            if isinstance(node, str):
                text = self._render_text(node)
                if at_line_start:
                    parts.append(f"{child_indent}{text}\n")
                else:
                    parts.append(text)
            else:
                if not at_line_start:
                    parts.append("\n")
                    at_line_start = True
                parts.append(
                    node.render(pretty=True, _indent=_indent + 1, max_depth=max_depth)
                )
        if at_line_start:
            parts.append("  " * _indent)
        return "".join(parts)

    def render(
        self,
        pretty: bool = False,
        _indent: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> str:
        """Serialize this element and its subtree to an HTML string.

        Attribute values and text content are HTML-escaped, except inside
        ``<script>`` and ``<style>``, where text is emitted as-is (browsers
        do not decode entities there) with any closing ``</script`` or
        ``</style`` sequence neutralised. Text and child elements render
        in the order they were added. Self-closing elements emit
        ``<tag />`` with no children.

        Args:
            pretty: If ``True``, insert indentation and newlines for
                human-readable output. Content of ``<pre>``, ``<textarea>``,
                ``<script>`` and ``<style>`` is never reformatted.
            max_depth: Traversal cutoff (default 1000) guarding against
                circular references in the tree.

        Returns:
            HTML representation of this element.

        Raises:
            RecursionError: If ``max_depth`` is exceeded - usually a sign
                of a circular reference rather than legitimate depth.

        Example:
            >>> Div(Paragraph("Hi"), class_name="card").render()
            '<div class="card"><p>Hi</p></div>'
        """
        if _indent > max_depth:
            raise RecursionError(
                f"Maximum recursion depth ({max_depth}) exceeded in render(). "
                "This usually indicates a circular reference in the element tree. "
                "Consider increasing max_depth if you have deeply nested HTML."
            )

        self.on_before_render()

        indent_str = "  " * _indent if pretty else ""
        newline = "\n" if pretty else ""
        tag_start = f"{indent_str}<{self._tag}{self._render_attributes()}"

        if self._self_closing:
            result = f"{tag_start} />{newline}"
        else:
            inner = self._render_nodes(pretty, _indent, max_depth)
            result = f"{tag_start}>{inner}</{self._tag}>{newline}"

        if self._prefix:
            result = f"{self._prefix}{result}"

        self.on_after_render()
        return result

    def to_dict(
        self,
        _depth: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> dict:
        """Serialize this element and its subtree to a plain dict.

        The returned dict has keys ``tag``, ``self_closing``,
        ``attributes``, ``text``, and ``children`` (recursively). ``text``
        holds any text that comes before the first child element. Text that
        follows an element is kept in ``children`` as a plain string so the
        original order survives. It is JSON-safe and round-trips via
        ``from_dict()``.

        Args:
            max_depth: Traversal cutoff (default 1000) guarding against
                circular references.

        Returns:
            Dict representation of the element.

        Raises:
            RecursionError: If ``max_depth`` is exceeded.
        """
        if _depth > max_depth:
            raise RecursionError(
                f"Maximum recursion depth ({max_depth}) exceeded in to_dict(). "
                "This usually indicates a circular reference in the element tree."
            )
        leading = 0
        while leading < len(self._children) and isinstance(
            self._children[leading], str
        ):
            leading += 1
        return {
            "tag": self._tag,
            "self_closing": self._self_closing,
            "attributes": self._attributes.copy(),
            "text": "".join(self._children[:leading]),
            "children": [
                (
                    child
                    if isinstance(child, str)
                    else child.to_dict(_depth=_depth + 1, max_depth=max_depth)
                )
                for child in self._children[leading:]
            ],
        }

    def to_json(self, indent: Union[int, None] = None) -> str:
        """Serialize this element and its subtree to a JSON string.

        Args:
            indent: Spaces for pretty-printed JSON, or ``None`` for compact
                single-line output.

        Returns:
            JSON representation; pair with ``from_json()`` to round-trip.
        """
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(
        cls,
        data: dict,
        _depth: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
        allow_partial_files: bool = False,
    ) -> "HTMLElement":
        """Reconstruct an element tree from a ``to_dict()`` result.

        Uses the tag registry populated by the tag factory to instantiate
        the most specific subclass for each tag, so ``Fragment``,
        ``Table``, ``Form``, etc. round-trip as their real types.
        Serialized ``Partial`` nodes are restored too.

        Args:
            data: Dict produced by ``to_dict()``.
            max_depth: Traversal cutoff (default 1000).
            allow_partial_files: Allow ``Partial`` nodes that read from a
                file path. Off by default, because a crafted payload could
                otherwise make ``render()`` read any file on disk.

        Returns:
            Reconstructed ``HTMLElement`` (or subclass matching ``tag``).

        Raises:
            ValueError: If ``data`` is not a dict, is missing ``tag``, has
                a field with the wrong type, has a dangerous inline style,
                or contains a file-backed ``Partial`` without
                ``allow_partial_files``.
            RecursionError: If ``max_depth`` is exceeded.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        if _depth > max_depth:
            raise RecursionError(
                f"Maximum recursion depth ({max_depth}) exceeded in from_dict(). "
                "This usually indicates deeply nested or circular data."
            )

        if data.get("type") == "partial":
            from nitro_ui.core.partial import Partial

            return Partial.from_dict(data, allow_files=allow_partial_files)

        if "tag" not in data:
            raise ValueError("Dictionary must contain 'tag' key")

        tag = data["tag"]
        if not isinstance(tag, str):
            raise ValueError(f"'tag' must be a string, got {type(tag).__name__}")

        self_closing = data.get("self_closing", False)
        if not isinstance(self_closing, bool):
            raise ValueError(
                f"'self_closing' must be a bool, got {type(self_closing).__name__}"
            )

        attributes = data.get("attributes", {})
        if not isinstance(attributes, dict):
            raise ValueError(
                f"'attributes' must be a dict, got {type(attributes).__name__}"
            )
        cls._check_style_attribute(attributes.get("style"))

        text = data.get("text", "")
        if text is not None and not isinstance(text, str):
            raise ValueError(f"'text' must be a string, got {type(text).__name__}")

        children_data = data.get("children", [])
        if not isinstance(children_data, list):
            raise ValueError(
                f"'children' must be a list, got {type(children_data).__name__}"
            )

        if tag == "fragment":
            from nitro_ui.core.fragment import Fragment

            target_cls = Fragment
        elif cls is HTMLElement:
            target_cls = _TAG_REGISTRY.get(tag, cls)
        else:
            target_cls = cls

        if target_cls is HTMLElement:
            element = target_cls(tag=tag, self_closing=self_closing)
        else:
            try:
                element = target_cls()
            except TypeError:
                element = target_cls(tag=tag, self_closing=self_closing)
            if "self_closing" in data:
                element._self_closing = self_closing
        element._attributes = dict(attributes)

        nodes: List[Union[HTMLElement, str]] = [text] if text else []
        for child_data in children_data:
            if isinstance(child_data, str):
                if child_data:
                    nodes.append(child_data)
                continue
            nodes.append(
                HTMLElement.from_dict(
                    child_data,
                    _depth=_depth + 1,
                    max_depth=max_depth,
                    allow_partial_files=allow_partial_files,
                )
            )
        element._children = nodes

        return element

    @classmethod
    def from_json(
        cls, json_str: str, allow_partial_files: bool = False
    ) -> "HTMLElement":
        """Reconstruct an element tree from a ``to_json()`` result.

        Args:
            json_str: JSON previously produced by ``to_json()``.
            allow_partial_files: See ``from_dict()``.

        Returns:
            Reconstructed ``HTMLElement`` (or registered subclass).

        Raises:
            ValueError: If the string is not valid JSON or the decoded
                payload is not a valid element dict.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        return cls.from_dict(data, allow_partial_files=allow_partial_files)


# Tag registry for subclass reconstruction in from_dict()
# Populated by tag_factory and tag modules at import time
_TAG_REGISTRY: dict = {}


def register_tag(tag_name: str, tag_class: type) -> None:
    """Register a tag class for from_dict() reconstruction."""
    _TAG_REGISTRY[tag_name] = tag_class
