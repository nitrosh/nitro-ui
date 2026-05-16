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
_BOOLEAN_ATTRIBUTES = frozenset({
    "allowfullscreen", "async", "autofocus", "autoplay", "checked",
    "controls", "default", "defer", "disabled", "formnovalidate",
    "hidden", "inert", "ismap", "itemscope", "loop", "multiple",
    "muted", "nomodule", "novalidate", "open", "playsinline",
    "readonly", "required", "reversed", "selected",
})

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


def _validate_css_value(value: str) -> bool:
    """Validate that a CSS value doesn't contain injection attacks.

    Args:
        value: The CSS value to validate

    Returns:
        True if safe, False if potentially dangerous
    """
    if not isinstance(value, str):
        return True  # Non-strings will be converted safely
    return not _DANGEROUS_CSS_PATTERN.search(value)


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
        "_text",
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
            ValueError: If ``tag`` is empty, malformed, or a child has an
                unsupported type.
        """
        # Attributes that should keep underscores (not convert to hyphens)
        PRESERVE_UNDERSCORE = {"class_name", "for_element"}

        # Map trailing underscore convention to NitroUI convention
        # e.g., class_ -> class_name, for_ -> for_element
        # Also support cls as a short alias for class_name
        KEYWORD_MAPPINGS = {
            "class_": "class_name",
            "cls": "class_name",
            "for_": "for_element",
        }

        if not tag:
            raise ValueError("A valid HTML tag name is required")

        # Validate tag name to prevent injection
        if not _VALID_TAG_PATTERN.match(tag):
            raise ValueError(
                f"Invalid HTML tag name: {tag!r}. "
                "Tag names must start with a letter and contain only "
                "letters, digits, and hyphens."
            )

        def normalize_attr_key(k: str) -> str:
            # First, handle keyword mappings (class_ -> class_name, for_ -> for_element)
            if k in KEYWORD_MAPPINGS:
                return KEYWORD_MAPPINGS[k]
            # Preserve certain keys with underscores
            if k in PRESERVE_UNDERSCORE:
                return k
            # Check SVG camelCase map (view_box -> viewBox)
            if k in _SVG_SNAKE_TO_CAMEL:
                return _SVG_SNAKE_TO_CAMEL[k]
            # Convert remaining underscores to hyphens (data_value -> data-value)
            return k.replace("_", "-")

        fixed_attributes = {normalize_attr_key(k): v for k, v in attributes.items()}

        self._tag: str = tag
        self._children: List[HTMLElement] = []
        self._text: str = ""
        self._attributes: dict = fixed_attributes
        self._self_closing: bool = self_closing
        self._styles_cache: Union[dict, None] = None
        self._prefix: Union[str, None] = None

        if _GENERATE_IDS:
            self.generate_id()

        # Batch text children to avoid repeated string concatenation
        text_parts: List[str] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                self._children.append(child)
            elif isinstance(child, str):
                text_parts.append(child)
            elif child is not None:
                # Raise error for invalid types
                raise ValueError(
                    f"Invalid child type: {type(child).__name__}."
                    " Children must be HTMLElement instances"
                    " or strings."
                )
        if text_parts:
            self._text = "".join(text_parts)

        # Warn if children/text added to self-closing elements
        if self._self_closing and (self._children or self._text):
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

    def prepend(self, *children: Union["HTMLElement", str, List[Any]]) -> "HTMLElement":
        """Insert children at the front of this element.

        Mirrors ``append()`` but adds content at the start rather than the
        end. Strings are prefixed to the existing text content; elements
        are placed before existing children.

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
        new_children: List[HTMLElement] = []
        text_parts: List[str] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                new_children.append(child)
            elif isinstance(child, str):
                text_parts.append(child)
            elif child is not None:
                raise ValueError(
                    f"Invalid child type: {type(child).__name__}. "
                    "Children must be HTMLElement instances or strings."
                )
        if text_parts:
            self._text = "".join(text_parts) + self._text
        self._children = new_children + self._children
        return self

    def append(self, *children: Union["HTMLElement", str, List[Any]]) -> "HTMLElement":
        """Add children to the end of this element.

        Strings are concatenated to the existing text content; elements
        are placed after existing children. Nested lists/tuples are
        flattened so you can splice collections in directly.

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
        text_parts: List[str] = []
        for child in self._flatten(children):
            if isinstance(child, HTMLElement):
                self._children.append(child)
            elif isinstance(child, str):
                text_parts.append(child)
            elif child is not None:
                raise ValueError(
                    f"Invalid child type: {type(child).__name__}. "
                    "Children must be HTMLElement instances or strings."
                )
        if text_parts:
            self._text += "".join(text_parts)
        return self

    def filter(
        self,
        condition: Callable[[Any], bool],
        recursive: bool = False,
        max_depth: int = DEFAULT_MAX_DEPTH,
        _current_depth: int = 0,
    ) -> Iterator["HTMLElement"]:
        """Yield children (and optionally descendants) matching a predicate.

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
        for child in self._children:
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
        """Remove every direct child matching a predicate.

        Only the immediate children are considered (not descendants).

        Args:
            condition: Called with each child; return ``True`` to remove it.

        Returns:
            This element, for chaining.
        """
        to_remove = list(self.filter(condition))
        for child in to_remove:
            if child in self._children:
                self._children.remove(child)
        return self

    def clear(self) -> "HTMLElement":
        """Remove all children from this element.

        Text content is left untouched; use ``text = ""`` to clear it.

        Returns:
            This element, for chaining.
        """
        self._children.clear()
        return self

    def pop(self, index: int = 0) -> "HTMLElement":
        """Remove and return a child by position.

        Args:
            index: Position to remove from; defaults to the first child.

        Returns:
            The removed ``HTMLElement``.

        Raises:
            IndexError: If the element has no children or the index is
                out of range.
        """
        return self._children.pop(index)

    def first(self) -> Union["HTMLElement", None]:
        """Return the first child, or ``None`` if this element has none."""
        return self._children[0] if self._children else None

    def last(self) -> Union["HTMLElement", None]:
        """Return the last child, or ``None`` if this element has none."""
        return self._children[-1] if self._children else None

    def add_attribute(self, key: str, value: str) -> "HTMLElement":
        """Set a single HTML attribute on this element.

        Existing attributes with the same key are overwritten. Setting the
        ``style`` attribute invalidates the parsed-styles cache used by
        ``add_style`` / ``get_style``.

        Args:
            key: Attribute name (use ``class_name`` instead of ``class``).
            value: Attribute value. Will be HTML-escaped at render time.

        Returns:
            This element, for chaining.
        """
        # Prevent duplicate class attributes from mixed API usage
        if key == "class" and "class_name" in self._attributes:
            self._attributes["class_name"] = value
        elif key == "class_name" and "class" in self._attributes:
            del self._attributes["class"]
            self._attributes["class_name"] = value
        else:
            self._attributes[key] = value
        if key == "style":
            self._styles_cache = None
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
        has_style = False
        for key, value in attributes:
            self.add_attribute(key, value)
            if key == "style":
                has_style = True

        if has_style:
            self._styles_cache = None
        return self

    def remove_attribute(self, key: str) -> "HTMLElement":
        """Remove an attribute by key. Missing keys are silently ignored.

        Args:
            key: Attribute name to remove.

        Returns:
            This element, for chaining.
        """
        self._attributes.pop(key, None)
        if key == "style":
            self._styles_cache = None
        return self

    def get_attribute(self, key: str) -> Union[str, None]:
        """Return the value of a named attribute, or ``None`` if absent."""
        return self._attributes.get(key)

    def has_attribute(self, key: str) -> bool:
        """Return ``True`` if the given attribute is set on this element."""
        return key in self._attributes

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

    def add_style(self, key: str, value: str) -> "HTMLElement":
        """Add a single inline CSS declaration to this element.

        Values are checked for common injection patterns (``javascript:``,
        ``expression(...)``, etc.) before being stored.

        Args:
            key: CSS property name (e.g. ``"color"``, ``"font-size"``).
            value: CSS property value (e.g. ``"red"``, ``"14px"``).

        Returns:
            This element, for chaining.

        Raises:
            ValueError: If ``value`` contains potentially dangerous content.

        Example:
            >>> Div().add_style("color", "red").render()
            '<div style="color: red"></div>'
        """
        if not _validate_css_value(str(value)):
            raise ValueError(
                f"CSS value for '{key}' contains potentially "
                f"dangerous content: {value!r}. "
                "Values cannot contain javascript:, expression(),"
                " or other injection patterns."
            )
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
            ValueError: If any value contains potentially dangerous content.
        """
        for key, value in styles.items():
            if not _validate_css_value(str(value)):
                raise ValueError(
                    f"CSS value for '{key}' contains potentially"
                    f" dangerous content: {value!r}. "
                    "Values cannot contain javascript:, "
                    "expression(), or other injection patterns."
                )
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
        """Swap a child at the given index with a new element.

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
        self._children[old_index] = new_child

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
            for child in element._children:
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
            return {key: self._attributes.get(key) for key in keys}
        return self._attributes.copy()

    def count_children(self) -> int:
        """Return the number of direct children (not including text content)."""
        return len(self._children)

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
        """A shallow copy of the list of child elements.

        The returned list can be mutated without affecting this element.
        Assigning to this property replaces the internal child list.
        """
        return list(self._children)

    @children.setter
    def children(self, value: List["HTMLElement"]) -> None:
        self._children = value

    @property
    def text(self) -> str:
        """Text content of this element (already-joined, unescaped source)."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

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
        """Returns a string of HTML attributes for the tag."""
        # Map internal attribute names to HTML attribute names
        ATTR_RENDER_MAP = {
            "class_name": "class",
            "for_element": "for",
        }

        def render_key(k: str) -> str:
            return ATTR_RENDER_MAP.get(k, k)

        parts = []
        for k, v in self._attributes.items():
            render_k = render_key(k)

            # Validate attribute key to prevent injection
            if not _VALID_ATTR_PATTERN.match(render_k):
                warnings.warn(
                    f"Skipping invalid attribute name: {render_k!r}",
                    UserWarning,
                    stacklevel=3,
                )
                continue

            # Handle None values - skip the attribute
            if v is None:
                continue

            # Handle boolean attributes
            if render_k in _BOOLEAN_ATTRIBUTES:
                if v is True or v == "" or v == render_k:
                    parts.append(render_k)
                elif v is False:
                    continue  # Omit the attribute entirely
                else:
                    # Non-boolean value on a boolean attribute, render normally
                    parts.append(f'{render_k}="{html.escape(str(v), quote=True)}"')
            else:
                parts.append(f'{render_k}="{html.escape(str(v), quote=True)}"')

        attr_str = " ".join(parts)
        return f" {attr_str}" if attr_str else ""

    def render(
        self,
        pretty: bool = False,
        _indent: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> str:
        """Serialize this element and its subtree to an HTML string.

        Attribute values and text content are HTML-escaped. The opening
        tag, attributes, children, and closing tag are emitted in order;
        self-closing elements emit ``<tag />`` with no children.

        Args:
            pretty: If ``True``, insert indentation and newlines for
                human-readable output. Defaults to compact output.
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

        attributes = self._render_attributes()
        indent_str = "  " * _indent if pretty else ""
        tag_start = f"{indent_str}<{self._tag}{attributes}"

        if self._self_closing:
            parts = [tag_start, " />"]
            if pretty:
                parts.append("\n")
            result = "".join(parts)
        else:
            if pretty and self._children:
                children_html = "".join(
                    child.render(pretty=True, _indent=_indent + 1, max_depth=max_depth)
                    for child in self._children
                )
                escaped_text = html.escape(self._text)

                if self._children or self._text:
                    parts = [tag_start, ">"]
                    if escaped_text:
                        parts.append(escaped_text)
                    if self._children:
                        parts.extend(["\n", children_html, indent_str])
                    parts.append(f"</{self._tag}>\n")
                    result = "".join(parts)
                else:
                    result = f"{tag_start}></{self._tag}>\n"
            elif pretty:
                # Pretty mode but no children - still add newline
                escaped_text = html.escape(self._text)
                result = f"{tag_start}>{escaped_text}</{self._tag}>\n"
            else:
                children_html = "".join(
                    child.render(
                        pretty=pretty, _indent=_indent + 1, max_depth=max_depth
                    )
                    for child in self._children
                )
                escaped_text = html.escape(self._text)
                result = f"{tag_start}>{escaped_text}{children_html}</{self._tag}>"

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
        ``attributes``, ``text``, and ``children`` (recursively). It is
        JSON-safe and round-trips via ``from_dict()``.

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
        return {
            "tag": self._tag,
            "self_closing": self._self_closing,
            "attributes": self._attributes.copy(),
            "text": self._text,
            "children": [
                child.to_dict(_depth=_depth + 1, max_depth=max_depth)
                for child in self._children
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
    ) -> "HTMLElement":
        """Reconstruct an element tree from a ``to_dict()`` result.

        Uses the tag registry populated by the tag factory to instantiate
        the most specific subclass for each tag, so ``Fragment``,
        ``Table``, ``Form``, etc. round-trip as their real types.

        Args:
            data: Dict produced by ``to_dict()``.
            max_depth: Traversal cutoff (default 1000).

        Returns:
            Reconstructed ``HTMLElement`` (or subclass matching ``tag``).

        Raises:
            ValueError: If ``data`` is not a dict, is missing ``tag``, or
                has a field with the wrong type.
            RecursionError: If ``max_depth`` is exceeded.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        if "tag" not in data:
            raise ValueError("Dictionary must contain 'tag' key")

        if _depth > max_depth:
            raise RecursionError(
                f"Maximum recursion depth ({max_depth}) exceeded in from_dict(). "
                "This usually indicates deeply nested or circular data."
            )

        # Validate field types
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

        text = data.get("text", "")
        if text is not None and not isinstance(text, str):
            raise ValueError(f"'text' must be a string, got {type(text).__name__}")

        children_data = data.get("children", [])
        if not isinstance(children_data, list):
            raise ValueError(
                f"'children' must be a list, got {type(children_data).__name__}"
            )

        # Use the _TAG_REGISTRY for subclass reconstruction if available
        target_cls = _TAG_REGISTRY.get(tag, cls) if cls is HTMLElement else cls

        # Handle Fragment type specially
        if tag == "fragment":
            from nitro_ui.core.fragment import Fragment
            target_cls = Fragment

        # Fragment and other subclasses may set their own tag in __init__,
        # so only pass tag when using base HTMLElement
        if target_cls is HTMLElement:
            element = target_cls(tag=tag, self_closing=self_closing)
        else:
            try:
                element = target_cls()
            except TypeError:
                # Fallback for subclasses that require tag
                element = target_cls(tag=tag, self_closing=self_closing)
        element._attributes = dict(attributes)

        if text:
            element._text = text

        if children_data:
            for child_data in children_data:
                child = HTMLElement.from_dict(
                    child_data,
                    _depth=_depth + 1,
                    max_depth=max_depth,
                )
                element._children.append(child)

        return element

    @classmethod
    def from_json(cls, json_str: str) -> "HTMLElement":
        """Reconstruct an element tree from a ``to_json()`` result.

        Args:
            json_str: JSON previously produced by ``to_json()``.

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

        return cls.from_dict(data)


# Tag registry for subclass reconstruction in from_dict()
# Populated by tag_factory and tag modules at import time
_TAG_REGISTRY: dict = {}


def register_tag(tag_name: str, tag_class: type) -> None:
    """Register a tag class for from_dict() reconstruction."""
    _TAG_REGISTRY[tag_name] = tag_class
