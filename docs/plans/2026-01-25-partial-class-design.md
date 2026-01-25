# Partial Class Design

## Overview

`Partial` is an escape hatch for embedding raw HTML strings directly into the NitroUI element tree. It bypasses HTML escaping, making it suitable for trusted static content like analytics snippets, third-party embeds, or legacy HTML.

## Usage Examples

```python
from nitro_ui import Head, Meta, Title, Partial

# Inline HTML string
Head(
    Meta(charset="utf-8"),
    Partial("""
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'GA_ID');
        </script>
    """),
    Title("My Page")
)

# Load from file
Head(
    Meta(charset="utf-8"),
    Partial(file="partials/google-analytics.html"),
    Title("My Page")
)
```

## API

### Constructor

```python
class Partial(HTMLElement):
    def __init__(self, html: str = None, *, file: str = None):
        ...
```

**Parameters:**
- `html`: Raw HTML string to embed directly
- `file`: Path to file containing HTML to embed

**Constraints:**
- Must specify exactly one of `html` or `file`
- Specifying both raises `ValueError`
- Specifying neither raises `ValueError`

### Behavior

| Aspect | Decision |
|--------|----------|
| Input | Raw HTML string OR file path (mutually exclusive) |
| Inheritance | Extends `HTMLElement` |
| File loading | Lazy (at render time) |
| Escaping | None - raw output |
| Content validation | None - trusts developer |
| Children | Not supported (raw HTML only) |

## Implementation

### File Location

`src/nitro_ui/core/partial.py`

### Class Implementation

```python
from typing import Union
from nitro_ui.core.element import HTMLElement, DEFAULT_MAX_DEPTH


class Partial(HTMLElement):
    """Embeds raw HTML directly without escaping.

    Use for trusted static content like analytics snippets, third-party
    embeds, or legacy HTML that should not be escaped.

    Warning: Content is rendered without any HTML escaping. Only use
    with trusted content to avoid XSS vulnerabilities.

    Example:
        Partial("<script>console.log('hello')</script>")
        Partial(file="partials/analytics.html")
    """

    __slots__ = ["_html", "_file"]

    def __init__(self, html: str = None, *, file: str = None):
        if html and file:
            raise ValueError("Cannot specify both 'html' and 'file'")
        if not html and not file:
            raise ValueError("Must specify either 'html' or 'file'")

        super().__init__(tag="partial")
        self._html = html
        self._file = file

    def render(
        self,
        pretty: bool = False,
        _indent: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> str:
        """Renders the raw HTML content.

        Args:
            pretty: Ignored (raw HTML is returned as-is)
            _indent: Ignored (raw HTML is returned as-is)
            max_depth: Ignored (no recursion needed)

        Returns:
            The raw HTML string

        Raises:
            FileNotFoundError: If file path doesn't exist
            IOError: If file cannot be read
        """
        self.on_before_render()

        if self._file:
            with open(self._file, "r", encoding="utf-8") as f:
                result = f.read()
        else:
            result = self._html

        self.on_after_render()
        return result

    def to_dict(self) -> dict:
        """Serializes the Partial to a dictionary."""
        result = {"type": "partial"}
        if self._html:
            result["html"] = self._html
        if self._file:
            result["file"] = self._file
        return result

    def to_json(self, indent: int = None) -> str:
        """Serializes the Partial to a JSON string."""
        import json
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "Partial":
        """Reconstructs a Partial from a dictionary."""
        if data.get("type") != "partial":
            raise ValueError("Not a Partial element")
        return cls(html=data.get("html"), file=data.get("file"))

    @classmethod
    def from_json(cls, json_str: str) -> "Partial":
        """Reconstructs a Partial from a JSON string."""
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)
```

## Serialization

### to_dict() Output

```python
# For inline HTML
{"type": "partial", "html": "<script>...</script>"}

# For file-based
{"type": "partial", "file": "partials/analytics.html"}
```

Note: File-based partials serialize the path, not the content. On deserialization, the file must still exist for rendering to work.

## Files to Create/Modify

| File | Change |
|------|--------|
| `src/nitro_ui/core/partial.py` | New file - `Partial` class |
| `src/nitro_ui/core/__init__.py` | Export `Partial` |
| `src/nitro_ui/__init__.py` | Export `Partial` |
| `tests/test_partial.py` | New file - test cases |

## Test Cases

1. **Basic rendering** - inline HTML renders without escaping
2. **File loading** - reads file content at render time
3. **Validation errors** - both/neither params raises `ValueError`
4. **Integration** - works as child of other elements (`Div(Partial(...))`)
5. **Serialization round-trip** - `to_dict()` → `from_dict()` works for both modes
6. **File not found** - raises `FileNotFoundError` at render time
7. **Pretty printing** - indentation param is accepted but doesn't affect output
8. **Empty string** - `Partial("")` should work (empty but valid)
