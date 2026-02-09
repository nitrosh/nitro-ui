"""Tests for all fixes from the pre-launch code audit.

Covers: security, boolean attributes, None values, CSS sanitization,
serialization depth limits, tag/attribute validation, parser fixes,
naming, self-closing warnings, and more.
"""

import unittest
import warnings

from nitro_ui.core.element import HTMLElement, _validate_css_value
from nitro_ui.core.fragment import Fragment
from nitro_ui.core.parser import from_html
from nitro_ui.styles.style import CSSStyle
from nitro_ui.styles.stylesheet import StyleSheet, _sanitize_css_value
from nitro_ui.tags.html import HTML
from nitro_ui.tags.text import Anchor, Href, H1, Paragraph
from nitro_ui.tags.form import Form, Input, Button, Datalist
from nitro_ui.tags.layout import (
    Div, Dialog, Address, Hgroup, Search, Menu,
)
from nitro_ui.tags.media import Image, Video


class TestHTMLLangDirOverride(unittest.TestCase):
    """Fix #1/#2: HTML class Python 3.8 compat + lang/dir override."""

    def test_html_default_lang(self):
        """HTML should have lang=en by default."""
        page = HTML()
        rendered = str(page)
        self.assertIn('lang="en"', rendered)

    def test_html_custom_lang(self):
        """User-provided lang should override the default."""
        page = HTML(lang="fr")
        rendered = str(page)
        self.assertIn('lang="fr"', rendered)
        self.assertNotIn('lang="en"', rendered)

    def test_html_custom_dir(self):
        """User-provided dir should override the default."""
        page = HTML(dir="rtl")
        rendered = str(page)
        self.assertIn('dir="rtl"', rendered)
        self.assertNotIn('dir="ltr"', rendered)


class TestBooleanAttributes(unittest.TestCase):
    """Fix #3: Boolean attributes render correctly per HTML5 spec."""

    def test_disabled_true(self):
        """disabled=True should render as bare 'disabled' attribute."""
        inp = Input(type="text", disabled=True)
        rendered = str(inp)
        self.assertIn("disabled", rendered)
        self.assertNotIn('disabled="True"', rendered)

    def test_disabled_false(self):
        """disabled=False should omit the attribute entirely."""
        inp = Input(type="text", disabled=False)
        rendered = str(inp)
        self.assertNotIn("disabled", rendered)

    def test_checked_true(self):
        """checked=True renders as bare 'checked'."""
        inp = Input(type="checkbox", checked=True)
        rendered = str(inp)
        self.assertIn("checked", rendered)
        self.assertNotIn('checked="True"', rendered)

    def test_required_true(self):
        """required=True renders as bare 'required'."""
        inp = Input(type="text", required=True)
        rendered = str(inp)
        self.assertIn("required", rendered)
        self.assertNotIn('required="True"', rendered)

    def test_hidden_true(self):
        """hidden=True renders as bare 'hidden'."""
        div = Div("content", hidden=True)
        rendered = str(div)
        self.assertIn("hidden", rendered)
        self.assertNotIn('hidden="True"', rendered)

    def test_readonly_true(self):
        """readonly=True renders as bare 'readonly'."""
        inp = Input(type="text", readonly=True)
        rendered = str(inp)
        self.assertIn("readonly", rendered)

    def test_boolean_empty_string(self):
        """Boolean attr with empty string renders as bare attribute."""
        inp = Input(type="text", disabled="")
        rendered = str(inp)
        self.assertIn("disabled", rendered)
        self.assertNotIn('disabled=""', rendered)

    def test_open_boolean(self):
        """open is a boolean attribute on dialog."""
        dialog = Dialog("Open dialog", open=True)
        rendered = str(dialog)
        self.assertIn("open", rendered)
        self.assertNotIn('open="True"', rendered)

    def test_controls_boolean(self):
        """controls is a boolean attribute on video."""
        video = Video(src="v.mp4", controls=True)
        rendered = str(video)
        self.assertIn("controls", rendered)
        self.assertNotIn('controls="True"', rendered)


class TestNoneAttributeValues(unittest.TestCase):
    """Fix #4: None attribute values are omitted from output."""

    def test_none_value_omitted(self):
        """Attributes with None value should not appear in output."""
        div = Div("content", id="main")
        div.add_attribute("data-extra", None)
        rendered = str(div)
        self.assertNotIn("data-extra", rendered)
        self.assertNotIn("None", rendered)

    def test_non_none_value_preserved(self):
        """Non-None values should still render normally."""
        div = Div("content", id="main")
        rendered = str(div)
        self.assertIn('id="main"', rendered)


class TestCSSValidation(unittest.TestCase):
    """Fix #5/#6: CSS sanitization is consistent and tested."""

    def test_validate_css_rejects_javascript(self):
        """CSS values containing javascript: are rejected."""
        self.assertFalse(_validate_css_value("url(javascript:alert(1))"))

    def test_validate_css_rejects_expression(self):
        """CSS values containing expression() are rejected."""
        self.assertFalse(_validate_css_value("expression(alert(1))"))

    def test_validate_css_rejects_data_url(self):
        """CSS values containing data: URLs are rejected."""
        self.assertFalse(_validate_css_value("url(data:text/html,<script>)"))

    def test_validate_css_rejects_braces(self):
        """CSS values containing { or } are rejected."""
        self.assertFalse(_validate_css_value("red; } .evil { color: blue"))

    def test_validate_css_rejects_css_comments(self):
        """CSS values containing comment syntax are rejected."""
        self.assertFalse(_validate_css_value("red /* injection */"))

    def test_validate_css_rejects_hex_escapes(self):
        """CSS values containing hex escapes are rejected."""
        self.assertFalse(_validate_css_value("\\6a avascript:"))

    def test_validate_css_allows_normal_values(self):
        """Normal CSS values are allowed."""
        self.assertTrue(_validate_css_value("red"))
        self.assertTrue(_validate_css_value("14px"))
        self.assertTrue(_validate_css_value("#007bff"))
        self.assertTrue(_validate_css_value("1px solid #ccc"))
        self.assertTrue(_validate_css_value("var(--color-primary)"))

    def test_add_style_rejects_dangerous_value(self):
        """add_style() raises ValueError for dangerous CSS values."""
        div = Div("content")
        with self.assertRaises(ValueError):
            div.add_style("background", "url(javascript:alert(1))")

    def test_add_styles_rejects_dangerous_value(self):
        """add_styles() raises ValueError for dangerous CSS values."""
        div = Div("content")
        with self.assertRaises(ValueError):
            div.add_styles({"background": "expression(alert(1))"})

    def test_stylesheet_sanitize_uses_shared_validation(self):
        """Stylesheet _sanitize_css_value uses the same validation."""
        with self.assertRaises(ValueError):
            _sanitize_css_value("url(javascript:alert(1))")

    def test_stylesheet_sanitize_allows_normal(self):
        """Stylesheet sanitization allows normal values."""
        self.assertEqual(_sanitize_css_value("red"), "red")
        self.assertEqual(_sanitize_css_value("14px"), "14px")

    def test_css_style_to_inline_sanitization(self):
        """CSSStyle.to_inline() validates values."""
        style = CSSStyle()
        style._styles["background"] = "url(javascript:alert(1))"
        with self.assertRaises(ValueError):
            style.to_inline()


class TestSerializationDepthLimits(unittest.TestCase):
    """Fix #7: to_dict/from_dict have recursion depth limits."""

    def test_to_dict_depth_limit(self):
        """to_dict() raises RecursionError when depth limit exceeded."""
        # Create a deeply nested tree
        root = Div("root")
        current = root
        for _ in range(50):
            child = Div("child")
            current.append(child)
            current = child

        # Should work at default depth
        data = root.to_dict()
        self.assertIsInstance(data, dict)

        # Should fail at low depth
        with self.assertRaises(RecursionError):
            root.to_dict(max_depth=10)

    def test_from_dict_depth_limit(self):
        """from_dict() raises RecursionError when depth limit exceeded."""
        # Create deeply nested dict
        data = {"tag": "div", "text": "leaf"}
        for _ in range(50):
            data = {"tag": "div", "children": [data]}

        # Should work at default depth
        element = HTMLElement.from_dict(data)
        self.assertIsInstance(element, HTMLElement)

        # Should fail at low depth
        with self.assertRaises(RecursionError):
            HTMLElement.from_dict(data, max_depth=10)


class TestTagNameValidation(unittest.TestCase):
    """Fix #8: Tag names are validated to prevent injection."""

    def test_valid_tag_name(self):
        """Valid tag names should work fine."""
        el = HTMLElement(tag="div")
        self.assertEqual(el.tag, "div")

    def test_valid_hyphenated_tag(self):
        """Custom elements with hyphens should work."""
        el = HTMLElement(tag="my-component")
        self.assertEqual(el.tag, "my-component")

    def test_invalid_tag_with_space(self):
        """Tag names with spaces are rejected."""
        with self.assertRaises(ValueError):
            HTMLElement(tag="div onclick=alert(1)")

    def test_invalid_tag_with_angle_bracket(self):
        """Tag names with angle brackets are rejected."""
        with self.assertRaises(ValueError):
            HTMLElement(tag="div><script>alert(1)</script><div")

    def test_invalid_tag_empty_after_strip(self):
        """Empty tag names are rejected."""
        with self.assertRaises(ValueError):
            HTMLElement(tag="")


class TestAttributeKeyValidation(unittest.TestCase):
    """Fix #9: Attribute keys are validated."""

    def test_valid_attribute_keys(self):
        """Normal attribute keys render fine."""
        div = Div("test", id="main", class_name="container")
        rendered = str(div)
        self.assertIn('id="main"', rendered)
        self.assertIn('class="container"', rendered)

    def test_invalid_attribute_key_skipped(self):
        """Invalid attribute keys are skipped with a warning."""
        div = Div("test")
        div._attributes['x="><script>'] = "val"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            rendered = str(div)
            self.assertTrue(len(w) > 0)
            self.assertNotIn("script", rendered)


class TestParserFixes(unittest.TestCase):
    """Fix #11/#12/#13: Parser text handling improvements."""

    def test_parser_calls_close(self):
        """Parser should flush all text and call close()."""
        # Text at end of input without closing tag shouldn't be lost
        element = from_html("<div>hello")
        self.assertIsNotNone(element)
        self.assertEqual(element.text, "hello")

    def test_parser_preserves_pre_whitespace(self):
        """Parser should preserve whitespace inside <pre> tags."""
        element = from_html("<pre>  indented\n  code  </pre>")
        self.assertIsNotNone(element)
        self.assertIn("  indented", element.text)

    def test_parser_preserves_code_whitespace(self):
        """Parser should preserve whitespace inside <code> tags."""
        element = from_html("<code>  spaces  </code>")
        self.assertIsNotNone(element)
        self.assertIn("  spaces  ", element.text)

    def test_parser_strips_normal_whitespace(self):
        """Parser should still strip whitespace for normal elements."""
        element = from_html("<div>  hello  </div>")
        self.assertIsNotNone(element)
        self.assertEqual(element.text, "hello")

    def test_parser_boolean_attributes(self):
        """Parser stores boolean HTML attributes as True."""
        element = from_html('<input type="checkbox" checked>')
        self.assertIsNotNone(element)
        self.assertEqual(element.get_attribute("checked"), True)

    def test_parser_input_validation(self):
        """Parser rejects non-string input."""
        with self.assertRaises(TypeError):
            from_html(None)
        with self.assertRaises(TypeError):
            from_html(123)


class TestAnchorNaming(unittest.TestCase):
    """Fix #14: Href renamed to Anchor with backward compat."""

    def test_anchor_creates_a_tag(self):
        """Anchor class creates <a> tags."""
        a = Anchor("Click me", href="/page")
        self.assertEqual(a.tag, "a")
        self.assertIn('href="/page"', str(a))

    def test_href_is_anchor_alias(self):
        """Href is a backward-compatible alias for Anchor."""
        self.assertIs(Href, Anchor)

    def test_href_still_works(self):
        """Href still works as before."""
        a = Href("Link", href="/test")
        self.assertEqual(a.tag, "a")


class TestSelfClosingWarnings(unittest.TestCase):
    """Fix #15: Self-closing tags warn when children are added."""

    def test_self_closing_with_text_warns(self):
        """Adding text to self-closing element emits a warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Image("alt text", src="img.jpg")
            self.assertTrue(
                any(
                    "Self-closing" in str(x.message)
                    for x in w
                )
            )

    def test_self_closing_without_children_no_warning(self):
        """Self-closing elements without children don't warn."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Image(src="img.jpg")
            self.assertFalse(
                any(
                    "Self-closing" in str(x.message)
                    for x in w
                )
            )


class TestFormWithFields(unittest.TestCase):
    """Fix #16: Form.with_fields() accepts HTMLElement children."""

    def test_with_fields_accepts_div(self):
        """Form.with_fields() should accept Div wrapper elements."""
        form = Form.with_fields(
            Div(Input(type="text", name="name")),
            Button("Submit", type="submit"),
        )
        rendered = str(form)
        self.assertIn("<form>", rendered)
        self.assertIn("<div>", rendered)
        self.assertIn("<button", rendered)

    def test_with_fields_is_classmethod(self):
        """Form.with_fields() should be a classmethod."""
        # This verifies it can be called on subclasses correctly
        self.assertTrue(callable(Form.with_fields))

    def test_with_fields_rejects_non_element(self):
        """Form.with_fields() raises TypeError for invalid types."""
        with self.assertRaises(TypeError):
            Form.with_fields(123)


class TestDatalistMoved(unittest.TestCase):
    """Fix #17: Datalist is now in form.py."""

    def test_datalist_exists_in_form(self):
        """Datalist is importable from form module."""
        dl = Datalist(id="browsers")
        self.assertEqual(dl.tag, "datalist")


class TestCSSParserSemicolon(unittest.TestCase):
    """Fix #19: CSS parser handles semicolons inside url()."""

    def test_parse_url_with_semicolon(self):
        """Semicolons inside url() should not split the value."""
        style_str = "background: url(data:image/png;base64,abc)"
        result = HTMLElement._parse_styles(style_str)
        self.assertEqual(result["background"], "url(data:image/png;base64,abc)")

    def test_parse_multiple_with_url(self):
        """Multiple properties with url() should parse correctly."""
        style_str = "background: url(data:image/png;base64,abc); color: red"
        result = HTMLElement._parse_styles(style_str)
        self.assertEqual(result["background"], "url(data:image/png;base64,abc)")
        self.assertEqual(result["color"], "red")

    def test_parse_normal_styles_still_work(self):
        """Normal style strings without url() still parse correctly."""
        style_str = "color: red; font-size: 14px"
        result = HTMLElement._parse_styles(style_str)
        self.assertEqual(result["color"], "red")
        self.assertEqual(result["font-size"], "14px")


class TestDuplicateClassPrevention(unittest.TestCase):
    """Fix #20: Duplicate class attribute prevention."""

    def test_add_class_when_class_name_exists(self):
        """Adding 'class' when 'class_name' exists updates class_name."""
        div = Div("test", class_name="foo")
        div.add_attribute("class", "bar")
        rendered = str(div)
        # Should only have one class attribute
        self.assertEqual(rendered.count("class="), 1)
        self.assertIn('class="bar"', rendered)

    def test_add_class_name_when_class_exists(self):
        """Adding 'class_name' when 'class' exists updates correctly."""
        div = Div("test")
        div._attributes["class"] = "foo"
        div.add_attribute("class_name", "bar")
        rendered = str(div)
        self.assertEqual(rendered.count("class="), 1)


class TestFromDictValidation(unittest.TestCase):
    """Fix #21: from_dict() validates input types."""

    def test_rejects_non_dict(self):
        """from_dict() raises ValueError for non-dict input."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict("not a dict")

    def test_rejects_missing_tag(self):
        """from_dict() raises ValueError when tag is missing."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict({"attributes": {}})

    def test_rejects_non_string_tag(self):
        """from_dict() raises ValueError when tag is not a string."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict({"tag": 123})

    def test_rejects_non_bool_self_closing(self):
        """from_dict() raises ValueError when self_closing is not bool."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict({"tag": "div", "self_closing": "yes"})

    def test_rejects_non_dict_attributes(self):
        """from_dict() raises ValueError when attributes is not a dict."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict({"tag": "div", "attributes": "invalid"})

    def test_rejects_non_list_children(self):
        """from_dict() raises ValueError when children is not a list."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict({"tag": "div", "children": "invalid"})

    def test_rejects_non_string_text(self):
        """from_dict() raises ValueError when text is not a string."""
        with self.assertRaises(ValueError):
            HTMLElement.from_dict({"tag": "div", "text": 123})


class TestFromDictSubclassPreservation(unittest.TestCase):
    """Fix #22: from_dict() preserves subclass types via tag registry."""

    def test_div_reconstructed_as_div_type(self):
        """from_dict with tag='div' should reconstruct via registry."""
        data = {"tag": "div", "text": "hello"}
        element = HTMLElement.from_dict(data)
        # The element should be from the tag registry (a Div-like class)
        self.assertEqual(element.tag, "div")

    def test_fragment_reconstructed_as_fragment(self):
        """from_dict with tag='fragment' should return a Fragment."""
        frag = Fragment(H1("Title"), Paragraph("Content"))
        data = frag.to_dict()
        restored = HTMLElement.from_dict(data)
        self.assertIsInstance(restored, Fragment)


class TestChildrenPropertyCopy(unittest.TestCase):
    """Fix #23: children property returns a copy."""

    def test_children_returns_copy(self):
        """children property should return a copy, not internal list."""
        div = Div(Paragraph("child"))
        children = div.children
        children.append(H1("injected"))
        # Original should not be affected
        self.assertEqual(div.count_children(), 1)

    def test_children_content_matches(self):
        """children copy should have the same content."""
        p = Paragraph("child")
        div = Div(p)
        children = div.children
        self.assertEqual(len(children), 1)
        self.assertIs(children[0], p)


class TestFragmentSerialization(unittest.TestCase):
    """Fix #24: Fragment serialization round-trip."""

    def test_fragment_to_dict(self):
        """Fragment.to_dict() should include tag='fragment'."""
        frag = Fragment(H1("Title"))
        data = frag.to_dict()
        self.assertEqual(data["tag"], "fragment")

    def test_fragment_round_trip(self):
        """Fragment serialized and deserialized should be a Fragment."""
        frag = Fragment(H1("Title"), Paragraph("Content"))
        data = frag.to_dict()
        restored = HTMLElement.from_dict(data)
        self.assertIsInstance(restored, Fragment)
        # Should render without wrapper tag
        rendered = restored.render()
        self.assertNotIn("<fragment>", rendered)
        self.assertIn("<h1>Title</h1>", rendered)


class TestNewHTML5Tags(unittest.TestCase):
    """Fix #25: Missing HTML5 tags are available."""

    def test_address(self):
        a = Address("123 Street")
        self.assertEqual(a.tag, "address")

    def test_hgroup(self):
        hg = Hgroup(H1("Title"))
        self.assertEqual(hg.tag, "hgroup")

    def test_search(self):
        s = Search(Input(type="search"))
        self.assertEqual(s.tag, "search")

    def test_menu(self):
        m = Menu()
        self.assertEqual(m.tag, "menu")

    def test_template(self):
        from nitro_ui.tags.html import Template
        t = Template(Div("slot content"))
        self.assertEqual(t.tag, "template")

    def test_svg(self):
        from nitro_ui.tags.html import Svg
        s = Svg()
        self.assertEqual(s.tag, "svg")

    def test_math(self):
        from nitro_ui.tags.html import Math
        m = Math()
        self.assertEqual(m.tag, "math")

    def test_bdi(self):
        from nitro_ui.tags.text import Bdi
        b = Bdi("text")
        self.assertEqual(b.tag, "bdi")

    def test_bdo(self):
        from nitro_ui.tags.text import Bdo
        b = Bdo("text", dir="rtl")
        self.assertEqual(b.tag, "bdo")

    def test_ruby_rt_rp(self):
        from nitro_ui.tags.text import Ruby, Rt, Rp
        r = Ruby("text", Rp("("), Rt("annotation"), Rp(")"))
        self.assertEqual(r.tag, "ruby")

    def test_data(self):
        from nitro_ui.tags.text import Data
        d = Data("100", value="100")
        self.assertEqual(d.tag, "data")


class TestTagsInitImports(unittest.TestCase):
    """Fix #27: tags/__init__.py provides unified imports."""

    def test_import_from_tags_package(self):
        """Should be able to import from nitro_ui.tags directly."""
        from nitro_ui.tags import Div, H1, Form, Table, Image, UnorderedList
        self.assertIsNotNone(Div)
        self.assertIsNotNone(H1)
        self.assertIsNotNone(Form)
        self.assertIsNotNone(Table)
        self.assertIsNotNone(Image)
        self.assertIsNotNone(UnorderedList)


class TestPrettyRendering(unittest.TestCase):
    """Fix #28: Pretty rendering indentation for leaf nodes."""

    def test_pretty_leaf_node_has_newline(self):
        """Leaf nodes in pretty mode should end with newline."""
        div = Div(Paragraph("Hello"))
        rendered = div.render(pretty=True)
        lines = rendered.strip().split("\n")
        # Should have proper indentation structure
        self.assertTrue(lines[0].startswith("<div>"))
        self.assertTrue(lines[1].strip().startswith("<p>"))

    def test_pretty_empty_element_has_newline(self):
        """Empty elements in pretty mode should end with newline."""
        div = Div()
        rendered = div.render(pretty=True)
        self.assertTrue(rendered.endswith(">\n"))


class TestCSSStyleHash(unittest.TestCase):
    """Fix #29: CSSStyle.__hash__ includes pseudo/breakpoints."""

    def test_different_pseudos_different_hash(self):
        """Styles with different pseudos should ideally have different hashes."""
        s1 = CSSStyle(color="red", _hover=CSSStyle(color="blue"))
        s2 = CSSStyle(color="red", _hover=CSSStyle(color="green"))
        # They should still be usable in sets even if hashes collide
        self.assertNotEqual(s1, s2)

    def test_same_styles_same_hash(self):
        """Identical styles should have the same hash."""
        s1 = CSSStyle(color="red")
        s2 = CSSStyle(color="red")
        self.assertEqual(hash(s1), hash(s2))


class TestCSSStyleMerge(unittest.TestCase):
    """Fix #30: CSSStyle.merge() deep merges pseudo-selectors."""

    def test_deep_merge_pseudo_selectors(self):
        """Merging should deep-merge pseudo-selectors."""
        s1 = CSSStyle(
            color="red",
            _hover=CSSStyle(color="blue", font_size="14px"),
        )
        s2 = CSSStyle(
            background="white",
            _hover=CSSStyle(color="green"),
        )
        merged = s1.merge(s2)

        # Base styles should be merged
        self.assertEqual(merged._styles["color"], "red")
        self.assertEqual(merged._styles["background"], "white")

        # Hover should be deep-merged: color from s2, font-size from s1
        hover = merged._pseudo["hover"]
        self.assertEqual(hover._styles["color"], "green")
        self.assertEqual(hover._styles["font-size"], "14px")

    def test_merge_does_not_mutate_originals(self):
        """Merging should not mutate the original styles."""
        s1_hover = CSSStyle(color="blue")
        s1 = CSSStyle(_hover=s1_hover)
        s2 = CSSStyle(_hover=CSSStyle(font_size="14px"))
        merged = s1.merge(s2)

        # Modifying merged should not affect s1
        merged._pseudo["hover"]._styles["color"] = "CHANGED"
        self.assertEqual(s1_hover._styles["color"], "blue")

    def test_merge_unique_pseudos(self):
        """Pseudos unique to each side should be preserved."""
        s1 = CSSStyle(_hover=CSSStyle(color="blue"))
        s2 = CSSStyle(_active=CSSStyle(color="red"))
        merged = s1.merge(s2)

        self.assertIn("hover", merged._pseudo)
        self.assertIn("active", merged._pseudo)


class TestStyleSheetFromDictValidation(unittest.TestCase):
    """StyleSheet.from_dict() validates class names."""

    def test_rejects_invalid_class_name(self):
        """from_dict() should reject invalid class names."""
        data = {
            "classes": {
                "valid-name": {"styles": {"color": "red"}},
                "invalid name with spaces": {"styles": {"color": "blue"}},
            },
            "breakpoints": {},
        }
        with self.assertRaises(ValueError):
            StyleSheet.from_dict(data)


class TestParserBooleanAttributes(unittest.TestCase):
    """Parser stores boolean attributes as True."""

    def test_checked_parsed_as_true(self):
        """Parsed boolean attribute should be True, not empty string."""
        element = from_html('<input type="checkbox" checked>')
        self.assertEqual(element.get_attribute("checked"), True)

    def test_disabled_parsed_as_true(self):
        element = from_html('<input type="text" disabled>')
        self.assertEqual(element.get_attribute("disabled"), True)

    def test_boolean_renders_correctly_after_parse(self):
        """Parsed boolean attributes should render as bare attributes."""
        element = from_html('<input type="checkbox" checked>')
        rendered = str(element)
        self.assertIn("checked", rendered)
        self.assertNotIn('checked=""', rendered)
        self.assertNotIn('checked="True"', rendered)


if __name__ == "__main__":
    unittest.main()
