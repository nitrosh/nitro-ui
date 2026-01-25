import json
import os
import tempfile

import pytest

from nitro_ui import Partial, Div, Head, Meta


class TestPartialBasic:
    """Tests for basic Partial functionality."""

    def test_render_inline_html(self):
        """Inline HTML renders without escaping."""
        html = "<script>alert('hello')</script>"
        partial = Partial(html)
        assert partial.render() == html

    def test_render_html_with_special_chars(self):
        """Special HTML characters are NOT escaped."""
        html = '<div class="test">&amp; < > "</div>'
        partial = Partial(html)
        assert partial.render() == html

    def test_render_empty_string(self):
        """Empty string is valid."""
        partial = Partial("")
        assert partial.render() == ""

    def test_render_multiline_html(self):
        """Multiline HTML renders correctly."""
        html = """
        <!-- Google Analytics -->
        <script async src="https://example.com/analytics.js"></script>
        <script>
            console.log('test');
        </script>
        """
        partial = Partial(html)
        assert partial.render() == html


class TestPartialFile:
    """Tests for file-based Partial functionality."""

    def test_render_from_file(self):
        """File content is loaded and rendered."""
        html = "<div>Content from file</div>"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(html)
            f.flush()
            try:
                partial = Partial(file=f.name)
                assert partial.render() == html
            finally:
                os.unlink(f.name)

    def test_lazy_loading(self):
        """File is read at render time, not construction time."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("initial content")
            f.flush()
            try:
                partial = Partial(file=f.name)

                # Modify file after construction
                with open(f.name, "w") as f2:
                    f2.write("modified content")

                # Should read modified content
                assert partial.render() == "modified content"
            finally:
                os.unlink(f.name)

    def test_file_not_found(self):
        """FileNotFoundError raised at render time for missing files."""
        partial = Partial(file="/nonexistent/path/file.html")
        with pytest.raises(FileNotFoundError):
            partial.render()

    def test_file_encoding(self):
        """UTF-8 content is handled correctly."""
        html = "<div>Unicode: \u00e9\u00e0\u00fc \u4e2d\u6587</div>"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html)
            f.flush()
            try:
                partial = Partial(file=f.name)
                assert partial.render() == html
            finally:
                os.unlink(f.name)


class TestPartialValidation:
    """Tests for Partial validation."""

    def test_error_both_html_and_file(self):
        """ValueError raised when both html and file are specified."""
        with pytest.raises(ValueError, match="Cannot specify both"):
            Partial("<div>test</div>", file="test.html")

    def test_error_neither_html_nor_file(self):
        """ValueError raised when neither html nor file is specified."""
        with pytest.raises(ValueError, match="Must specify either"):
            Partial()

    def test_none_html_with_file(self):
        """Explicit None for html with file works."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<div>test</div>")
            f.flush()
            try:
                partial = Partial(html=None, file=f.name)
                assert partial.render() == "<div>test</div>"
            finally:
                os.unlink(f.name)


class TestPartialIntegration:
    """Tests for Partial integration with other elements."""

    def test_as_child_of_div(self):
        """Partial works as child of Div."""
        div = Div(Partial("<span>raw</span>"))
        assert div.render() == "<div><span>raw</span></div>"

    def test_as_child_of_head(self):
        """Partial works in Head for analytics use case."""
        head = Head(
            Meta(charset="utf-8"),
            Partial("<script>analytics()</script>"),
        )
        result = head.render()
        assert '<meta charset="utf-8" />' in result
        assert "<script>analytics()</script>" in result

    def test_multiple_partials(self):
        """Multiple Partials work together."""
        div = Div(
            Partial("<span>first</span>"),
            Partial("<span>second</span>"),
        )
        assert div.render() == "<div><span>first</span><span>second</span></div>"

    def test_mixed_with_regular_elements(self):
        """Partial mixes with regular escaped elements."""
        div = Div(
            "Text with <angle> brackets",
            Partial("<script>unescaped</script>"),
        )
        result = div.render()
        assert "Text with &lt;angle&gt; brackets" in result
        assert "<script>unescaped</script>" in result


class TestPartialSerialization:
    """Tests for Partial serialization."""

    def test_to_dict_inline(self):
        """to_dict with inline HTML."""
        partial = Partial("<div>test</div>")
        result = partial.to_dict()
        assert result == {"type": "partial", "html": "<div>test</div>"}

    def test_to_dict_file(self):
        """to_dict with file path."""
        partial = Partial(file="path/to/file.html")
        result = partial.to_dict()
        assert result == {"type": "partial", "file": "path/to/file.html"}

    def test_to_json_inline(self):
        """to_json with inline HTML."""
        partial = Partial("<div>test</div>")
        result = partial.to_json()
        data = json.loads(result)
        assert data == {"type": "partial", "html": "<div>test</div>"}

    def test_to_json_indented(self):
        """to_json with indentation."""
        partial = Partial("<div>test</div>")
        result = partial.to_json(indent=2)
        assert "\n" in result

    def test_from_dict_inline(self):
        """from_dict with inline HTML."""
        data = {"type": "partial", "html": "<div>test</div>"}
        partial = Partial.from_dict(data)
        assert partial.render() == "<div>test</div>"

    def test_from_dict_file(self):
        """from_dict with file path."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<div>from file</div>")
            f.flush()
            try:
                data = {"type": "partial", "file": f.name}
                partial = Partial.from_dict(data)
                assert partial.render() == "<div>from file</div>"
            finally:
                os.unlink(f.name)

    def test_from_dict_invalid_type(self):
        """from_dict raises error for wrong type."""
        with pytest.raises(ValueError, match="Not a Partial element"):
            Partial.from_dict({"type": "element", "html": "<div>test</div>"})

    def test_from_json_inline(self):
        """from_json with inline HTML."""
        json_str = '{"type": "partial", "html": "<div>test</div>"}'
        partial = Partial.from_json(json_str)
        assert partial.render() == "<div>test</div>"

    def test_roundtrip_inline(self):
        """Full round-trip serialization for inline HTML."""
        original = Partial("<script>test()</script>")
        json_str = original.to_json()
        restored = Partial.from_json(json_str)
        assert restored.render() == original.render()

    def test_roundtrip_file(self):
        """Full round-trip serialization for file-based Partial."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<div>file content</div>")
            f.flush()
            try:
                original = Partial(file=f.name)
                json_str = original.to_json()
                restored = Partial.from_json(json_str)
                assert restored.render() == original.render()
            finally:
                os.unlink(f.name)


class TestPartialPrettyPrint:
    """Tests for pretty printing behavior."""

    def test_pretty_ignored(self):
        """Pretty print parameter doesn't affect raw HTML output."""
        html = "<div><span>content</span></div>"
        partial = Partial(html)
        assert partial.render(pretty=True) == html
        assert partial.render(pretty=False) == html

    def test_indent_ignored(self):
        """Indent parameter doesn't affect raw HTML output."""
        html = "<div>content</div>"
        partial = Partial(html)
        assert partial.render(_indent=5) == html


class TestPartialStr:
    """Tests for string conversion."""

    def test_str_returns_rendered(self):
        """__str__ returns rendered HTML."""
        partial = Partial("<div>test</div>")
        assert str(partial) == "<div>test</div>"
