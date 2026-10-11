"""HTML Parser for NitroUI - Convert raw HTML to NitroUI elements."""

import warnings
from html.parser import HTMLParser
from typing import List, Optional, Union

import re

from nitro_ui.core.element import (
    HTMLElement,
    _BOOLEAN_ATTRIBUTES,
    _SVG_CAMEL_ATTRS,
)


class HTMLParseWarning(UserWarning):
    """Warning raised when parsing potentially problematic HTML."""

    pass


# Tags where whitespace is significant and should be preserved
_PREFORMATTED_TAGS = frozenset({"pre", "code", "textarea", "script", "style"})

_WHITESPACE_RUN = re.compile(r"\s+")


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
        for key, value in attrs:
            if key in _SVG_CAMEL_ATTRS:
                key = _SVG_CAMEL_ATTRS[key]
            elif key == "class":
                key = "class_name"

            if key in attributes:
                warnings.warn(
                    f"Duplicate attribute '{key}' in <{tag}>. "
                    "The later value will overwrite the earlier one.",
                    HTMLParseWarning,
                    stacklevel=4,
                )

            if value is None:
                attributes[key] = True if key in _BOOLEAN_ATTRIBUTES else ""
            else:
                attributes[key] = value

        is_self_closing = tag in self.VOID_ELEMENTS

        element = HTMLElement(tag=tag, self_closing=is_self_closing)
        element._attributes = attributes

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

        if self.stack and not self._in_preformatted():
            self._strip_trailing_whitespace(self.stack[-1])

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

    def _in_preformatted(self) -> bool:
        return any(el.tag in _PREFORMATTED_TAGS for el in self.stack)

    @staticmethod
    def _strip_trailing_whitespace(element: HTMLElement) -> None:
        nodes = element._children
        if nodes and isinstance(nodes[-1], str):
            stripped = nodes[-1].rstrip()
            if stripped:
                nodes[-1] = stripped
            else:
                nodes.pop()

    def handle_data(self, data: str):
        """Buffer text content between tags."""
        self.text_buffer.append(data)

    def _flush_text_buffer(self):
        """Flush accumulated text to the current element, keeping its position.

        Whitespace is kept verbatim inside preformatted elements (pre,
        code, textarea, script, style). Elsewhere, runs of whitespace
        collapse to a single space, whitespace-only text spanning a line
        break (indentation) is dropped, and text at the start or end of an
        element is trimmed.
        """
        if not self.text_buffer:
            return

        text = "".join(self.text_buffer)
        self.text_buffer.clear()

        if self.current is not None and self._in_preformatted():
            self.current.append(text)
            return

        if not text.strip() and ("\n" in text or self.current is None):
            return
        text = _WHITESPACE_RUN.sub(" ", text)

        if self.current is not None:
            if not self.current._children:
                text = text.lstrip()
            self.current.append(text)
        else:
            self.roots.append(HTMLElement(text.strip(), tag="span"))

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
    """Parse an HTML string into a NitroUI element tree.

    Uses the standard library's ``html.parser`` under the hood. Class
    attributes are mapped to ``class_name``; SVG camelCase attributes
    (``viewBox`` etc.) are preserved. Whitespace inside ``<pre>``,
    ``<code>``, ``<textarea>``, ``<script>``, and ``<style>`` is kept
    verbatim; elsewhere it is stripped.

    Args:
        html_string: Raw HTML source.
        fragment: If ``True``, return a list with every root-level
            element (useful for snippets). If ``False``, return only the
            first root element, or ``None`` for an empty input.

    Returns:
        A single ``HTMLElement`` when ``fragment=False`` (or ``None`` if
        nothing was parsed), otherwise a list of elements.

    Raises:
        TypeError: If ``html_string`` is not a string.

    Example:
        >>> from_html('<div class="container"><h1>Hello</h1></div>').render()
        '<div class="container"><h1>Hello</h1></div>'
        >>> [el.render() for el in from_html('<h1>A</h1><p>B</p>', fragment=True)]
        ['<h1>A</h1>', '<p>B</p>']
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
