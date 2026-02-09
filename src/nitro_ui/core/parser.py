"""HTML Parser for NitroUI - Convert raw HTML to NitroUI elements."""

import warnings
from html.parser import HTMLParser
from typing import List, Optional, Union

from nitro_ui.core.element import HTMLElement, _SVG_CAMEL_ATTRS


class HTMLParseWarning(UserWarning):
    """Warning raised when parsing potentially problematic HTML."""

    pass


# Tags where whitespace is significant and should be preserved
_PREFORMATTED_TAGS = frozenset({"pre", "code", "textarea", "script", "style"})


class NitroUIHTMLParser(HTMLParser):
    """Parse HTML and convert to NitroUI element tree."""

    VOID_ELEMENTS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self):
        super().__init__()
        self.roots: List[HTMLElement] = []
        self.stack: List[HTMLElement] = []
        self.current: Optional[HTMLElement] = None
        self.text_buffer: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        """Handle opening tags."""
        self._flush_text_buffer()

        attributes = {}
        seen_normalized = {}  # Track normalized attribute names to detect collisions

        for key, value in attrs:
            # Restore SVG camelCase attrs that HTMLParser lowercased
            # (e.g. "viewbox" -> "viewBox")
            if key in _SVG_CAMEL_ATTRS:
                normalized_key = _SVG_CAMEL_ATTRS[key]
            elif key == "class":
                normalized_key = "class_name"
            else:
                normalized_key = key.replace("-", "_")

            # Check for attribute collision
            if normalized_key in seen_normalized:
                original_key = seen_normalized[normalized_key]
                warnings.warn(
                    f"Attribute collision in <{tag}>: '{key}' normalizes to "
                    f"'{normalized_key}' which collides with '{original_key}'. "
                    f"The later value will overwrite the earlier one.",
                    HTMLParseWarning,
                    stacklevel=4,
                )
            else:
                seen_normalized[normalized_key] = key

            # Store boolean attributes as True instead of empty string
            if value is None:
                attributes[normalized_key] = True
            else:
                attributes[normalized_key] = value

        is_self_closing = tag in self.VOID_ELEMENTS

        element = HTMLElement(tag=tag, self_closing=is_self_closing, **attributes)

        if self.current is not None:
            self.current.append(element)
        else:
            self.roots.append(element)

        if not is_self_closing:
            self.stack.append(element)
            self.current = element

    def handle_endtag(self, tag: str):
        """Handle closing tags."""
        self._flush_text_buffer()

        # Ignore closing tags for void elements - these can appear when parsing
        # XHTML-style self-closing syntax like <br /> which some parsers interpret
        # as having a closing tag
        if tag in self.VOID_ELEMENTS:
            return

        if self.stack:
            if self.stack[-1].tag == tag:
                self.stack.pop()
                self.current = self.stack[-1] if self.stack else None
            else:
                # Mismatched closing tag
                expected = self.stack[-1].tag
                warnings.warn(
                    f"Mismatched HTML tags: expected </{expected}> but found </{tag}>. "
                    f"This may result in an incorrect element tree.",
                    HTMLParseWarning,
                    stacklevel=4,
                )
                # Try to find the matching opening tag in the stack
                for i in range(len(self.stack) - 1, -1, -1):
                    if self.stack[i].tag == tag:
                        # Found a match - close all tags up to and including this one
                        self.stack = self.stack[:i]
                        self.current = self.stack[-1] if self.stack else None
                        break
        else:
            # Closing tag with no opening tag (ignore void elements)
            warnings.warn(
                f"Unexpected closing tag </{tag}> with no matching opening tag.",
                HTMLParseWarning,
                stacklevel=4,
            )

    def handle_data(self, data: str):
        """Handle text content between tags.

        Preserves whitespace for preformatted elements (pre, code, textarea, etc.).
        Strips whitespace for other elements.
        """
        # Determine if we're inside a preformatted element
        in_preformatted = False
        if self.current is not None:
            for el in self.stack:
                if el.tag in _PREFORMATTED_TAGS:
                    in_preformatted = True
                    break

        if in_preformatted:
            text = data  # Preserve whitespace as-is
        else:
            text = data.strip()

        if text:
            if self.current is not None:
                self.text_buffer.append(text)
            else:
                # Text outside of any element - wrap in a root-level text node
                # by storing it temporarily and adding to next root element,
                # or creating a fragment-like root text element
                self.text_buffer.append(text)

    def _flush_text_buffer(self):
        """Flush accumulated text to the current element."""
        if not self.text_buffer:
            return

        text = "".join(self.text_buffer)
        self.text_buffer.clear()

        if self.current is not None:
            if self.current.text:
                self.current.text += text
            else:
                self.current.text = text
        elif text.strip():
            # Root-level text: create a span wrapper to preserve it
            wrapper = HTMLElement(text, tag="span")
            self.roots.append(wrapper)

    def parse_html(self, html_string: str) -> Optional[HTMLElement]:
        """Parse HTML string and return root element."""
        self.feed(html_string)
        self._flush_text_buffer()  # Flush any remaining text
        self.close()  # Process any remaining buffered data
        return self.roots[0] if self.roots else None

    def parse_fragment(self, html_string: str) -> List[HTMLElement]:
        """Parse HTML fragment and return list of elements."""
        self.feed(html_string)
        self._flush_text_buffer()  # Flush any remaining text
        self.close()  # Process any remaining buffered data
        return self.roots


def from_html(
    html_string: str, fragment: bool = False
) -> Union[HTMLElement, List[HTMLElement], None]:
    """Parse HTML string and convert to NitroUI element(s).

    Args:
        html_string: Raw HTML string to parse
        fragment: If True, returns list of elements (for HTML fragments)
                 If False, returns single root element (default)

    Returns:
        HTMLElement if fragment=False, List[HTMLElement] if fragment=True

    Example:
        >>> from nitro_ui.core.parser import from_html
        >>>
        >>> # Parse single element
        >>> element = from_html('<div class="container"><h1>Hello</h1></div>')
        >>> print(element.render())
        <div class="container"><h1>Hello</h1></div>
        >>>
        >>> # Parse fragment (multiple root elements)
        >>> elements = from_html('<h1>Title</h1><p>Content</p>', fragment=True)
        >>> for el in elements:
        ...     print(el.render())
    """
    if not isinstance(html_string, str):
        raise TypeError(
            f"html_string must be a string, got {type(html_string).__name__}"
        )

    parser = NitroUIHTMLParser()

    if fragment:
        return parser.parse_fragment(html_string)
    else:
        return parser.parse_html(html_string)


# Add convenience method to HTMLElement
def _from_html_classmethod(cls, html_string: str, fragment: bool = False):
    """Parse HTML string and convert to HTMLElement(s).

    This is a class method added to HTMLElement for convenience.

    Args:
        html_string: Raw HTML string to parse
        fragment: If True, returns list of elements

    Returns:
        HTMLElement or List[HTMLElement]
    """
    return from_html(html_string, fragment=fragment)


# Monkey-patch HTMLElement to add from_html class method
HTMLElement.from_html = classmethod(_from_html_classmethod)
