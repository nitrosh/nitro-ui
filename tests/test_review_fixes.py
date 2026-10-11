"""Regression tests for the October 2026 code review.

Covers: ordered text and element children, raw text in script/style,
Partial serialization, Table.from_json, boolean values on regular
attributes, inline style validation, attribute key handling, the parser
keeping text order, pretty printing whitespace-sensitive tags, and
Component's tag property.
"""

import json
import os
import tempfile
import unittest

from nitro_ui import (
    Code,
    Component,
    Div,
    Fragment,
    HTMLElement,
    Input,
    Label,
    Paragraph,
    Partial,
    Pre,
    Script,
    Slot,
    Span,
    Strong,
    Style,
    Table,
    TableDataCell,
    TableRow,
    Textarea,
    from_html,
)


class TestChildOrder(unittest.TestCase):
    def test_text_after_element_keeps_position(self):
        p = Paragraph("Hello ", Strong("world"), "!")
        self.assertEqual(p.render(), "<p>Hello <strong>world</strong>!</p>")

    def test_append_and_prepend_keep_order(self):
        d = Div(Span("b"))
        d.append(" c").prepend("a ")
        self.assertEqual(d.render(), "<div>a <span>b</span> c</div>")

    def test_text_property_joins_all_text(self):
        p = Paragraph("a", Strong("b"), "c")
        self.assertEqual(p.text, "ac")

    def test_text_setter_replaces_text_nodes(self):
        p = Paragraph("a", Strong("b"), "c")
        p.text = "x"
        self.assertEqual(p.render(), "<p>x<strong>b</strong></p>")

    def test_children_excludes_text(self):
        p = Paragraph("a", Strong("b"), "c")
        self.assertEqual([c.tag for c in p.children], ["strong"])
        self.assertEqual(p.count_children(), 1)

    def test_nodes_returns_everything_in_order(self):
        s = Strong("b")
        p = Paragraph("a", s, "c")
        self.assertEqual(p.nodes, ["a", s, "c"])

    def test_pop_and_replace_child_use_element_positions(self):
        first, second = Span("1"), Span("2")
        d = Div("text", first, "more", second)
        d.replace_child(1, Strong("x"))
        self.assertIs(d.pop(0), first)
        self.assertEqual(d.render(), "<div>textmore<strong>x</strong></div>")

    def test_clear_keeps_text(self):
        d = Div("a", Span("b"), "c")
        d.clear()
        self.assertEqual(d.render(), "<div>ac</div>")

    def test_children_setter_validates(self):
        d = Div()
        with self.assertRaises(ValueError):
            d.children = [42]

    def test_fragment_keeps_order(self):
        f = Fragment("a", Span("b"), "c")
        self.assertEqual(f.render(), "a<span>b</span>c")

    def test_round_trip_keeps_order(self):
        p = Paragraph("Hello ", Strong("world"), "!")
        data = p.to_dict()
        self.assertEqual(data["text"], "Hello ")
        self.assertEqual(data["children"][1], "!")
        restored = HTMLElement.from_json(p.to_json())
        self.assertEqual(restored.render(), p.render())

    def test_old_dict_format_still_loads(self):
        data = {
            "tag": "p",
            "text": "Hi",
            "children": [{"tag": "b", "text": "x", "children": []}],
        }
        self.assertEqual(HTMLElement.from_dict(data).render(), "<p>Hi<b>x</b></p>")

    def test_component_template_text_keeps_position(self):
        class Note(Component):
            def template(self):
                return [Paragraph("Before ", Slot(), " after")]

        self.assertEqual(
            Note(Strong("x")).render(),
            "<div><p>Before <strong>x</strong> after</p></div>",
        )


class TestRawTextElements(unittest.TestCase):
    def test_script_is_not_entity_escaped(self):
        self.assertEqual(
            Script("if (a < b && c) {}").render(),
            "<script>if (a < b && c) {}</script>",
        )

    def test_style_is_not_entity_escaped(self):
        css = "ul > li { font-family: 'Courier New', \"Inter\"; }"
        self.assertEqual(Style(css).render(), f"<style>{css}</style>")

    def test_script_cannot_be_closed_early(self):
        html = Script('var s = "</script><img src=x onerror=alert(1)>";').render()
        self.assertEqual(html.lower().count("</script"), 1)
        self.assertIn("<\\/script>", html)

    def test_style_cannot_be_closed_early(self):
        html = Style("a{} </STYLE><script>alert(1)</script>").render()
        self.assertEqual(html.lower().count("</style"), 1)

    def test_script_comment_opener_neutralised(self):
        self.assertNotIn("<!--", Script("x = '<!--';").render())

    def test_parsed_script_round_trips(self):
        src = "<script>if (a < b) x()</script>"
        self.assertEqual(from_html(src).render(), src)

    def test_other_tags_still_escaped(self):
        self.assertEqual(Textarea("<b>").render(), "<textarea>&lt;b&gt;</textarea>")


class TestPartialSerialization(unittest.TestCase):
    def test_partial_inside_tree_serializes(self):
        tree = Div(Partial("<b>x</b>"))
        restored = HTMLElement.from_json(tree.to_json())
        self.assertEqual(restored.render(), "<div><b>x</b></div>")

    def test_file_partial_blocked_by_default(self):
        data = {"tag": "div", "children": [{"type": "partial", "file": "/etc/hosts"}]}
        with self.assertRaises(ValueError):
            HTMLElement.from_dict(data)
        with self.assertRaises(ValueError):
            Partial.from_dict({"type": "partial", "file": "/etc/hosts"})

    def test_file_partial_allowed_with_opt_in(self):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write("<i>file</i>")
        try:
            data = {"tag": "div", "children": [{"type": "partial", "file": f.name}]}
            el = HTMLElement.from_dict(data, allow_partial_files=True)
            self.assertEqual(el.render(), "<div><i>file</i></div>")
        finally:
            os.unlink(f.name)

    def test_empty_file_path_rejected(self):
        with self.assertRaises(ValueError):
            Partial(file="")


class TestTableFromJson(unittest.TestCase):
    def test_round_trip(self):
        table = Table(TableRow(TableDataCell("a")))
        restored = Table.from_json(table.to_json())
        self.assertEqual(restored.render(), "<table><tr><td>a</td></tr></table>")

    def test_file_path_is_deprecated_but_works(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump([["a", "b"]], f)
        try:
            with self.assertWarns(DeprecationWarning):
                table = Table.from_json(f.name)
            self.assertEqual(
                table.render(), "<table><tr><td>a</td><td>b</td></tr></table>"
            )
        finally:
            os.unlink(f.name)


class TestAttributeValues(unittest.TestCase):
    def test_python_bools_on_regular_attributes(self):
        self.assertEqual(
            Div(draggable=True, aria_hidden=False).render(),
            '<div draggable="true" aria-hidden="false"></div>',
        )

    def test_boolean_attributes_unchanged(self):
        self.assertEqual(
            Input(disabled=True, required=False).render(), "<input disabled />"
        )

    def test_parser_bare_custom_attribute(self):
        self.assertEqual(
            from_html("<div x-cloak hidden></div>").render(),
            '<div x-cloak="" hidden></div>',
        )


class TestInlineStyleValidation(unittest.TestCase):
    def test_style_kwarg_validated(self):
        with self.assertRaises(ValueError):
            Div(style="background:url(javascript:alert(1))")

    def test_style_via_add_attribute_validated(self):
        with self.assertRaises(ValueError):
            Div().add_attribute("style", "x: expression(alert(1))")

    def test_style_in_from_dict_validated(self):
        data = {"tag": "div", "attributes": {"style": "a: url(javascript:x)"}}
        with self.assertRaises(ValueError):
            HTMLElement.from_dict(data)

    def test_safe_style_kwarg_allowed(self):
        self.assertEqual(
            Div(style="color: red; margin: 0").render(),
            '<div style="color: red; margin: 0"></div>',
        )

    def test_property_name_validated(self):
        with self.assertRaises(ValueError):
            Div().add_style("color:red;background:url(x);x", "1")
        with self.assertRaises(ValueError):
            Div().add_styles({"a b": "1"})

    def test_custom_property_allowed(self):
        self.assertEqual(
            Div().add_style("--gap", "4px").render(), '<div style="--gap: 4px"></div>'
        )

    def test_semicolon_in_value_rejected(self):
        with self.assertRaises(ValueError):
            Div().add_style("color", "red; position: fixed")

    def test_parser_keeps_data_uri_styles(self):
        src = '<div style="background: url(data:image/png;base64,AAA)"></div>'
        self.assertEqual(from_html(src).render(), src)


class TestAttributeKeys(unittest.TestCase):
    def test_add_attribute_normalizes_underscores(self):
        self.assertEqual(
            Div().add_attribute("data_value", "1").render(),
            '<div data-value="1"></div>',
        )

    def test_class_aliases(self):
        d = Div(class_name="a")
        self.assertEqual(d.get_attribute("class"), "a")
        self.assertTrue(d.has_attribute("class"))
        d.add_attribute("class", "b")
        self.assertEqual(d.render(), '<div class="b"></div>')
        d.remove_attribute("class")
        self.assertEqual(d.render(), "<div></div>")

    def test_label_for(self):
        label = Label("Name", for_element="name")
        self.assertEqual(label.render(), '<label for="name">Name</label>')
        self.assertEqual(label.get_attribute("for"), "name")


class TestFromDictSelfClosing(unittest.TestCase):
    def test_self_closing_flag_respected_for_registered_tags(self):
        el = HTMLElement.from_dict({"tag": "div", "self_closing": True})
        self.assertEqual(el.render(), "<div />")


class TestParserTextOrder(unittest.TestCase):
    def test_interleaved_text(self):
        src = "<p>Hello <b>world</b> again</p>"
        self.assertEqual(from_html(src).render(), src)

    def test_text_around_void_element(self):
        self.assertEqual(from_html("<div>a<br>b</div>").render(), "<div>a<br />b</div>")

    def test_space_between_inline_elements(self):
        src = "<p><b>a</b> <i>b</i></p>"
        self.assertEqual(from_html(src).render(), src)

    def test_indentation_dropped(self):
        src = "<div>\n  <p>\n    Hi there\n  </p>\n</div>"
        self.assertEqual(from_html(src).render(), "<div><p>Hi there</p></div>")

    def test_preformatted_whitespace_kept(self):
        src = "<pre>  a\n    b  </pre>"
        self.assertEqual(from_html(src).render(), src)


class TestPrettyWhitespaceSensitive(unittest.TestCase):
    def test_pre_not_reindented(self):
        self.assertEqual(
            Pre(Code("a\n  b")).render(pretty=True),
            "<pre><code>a\n  b</code></pre>\n",
        )

    def test_pretty_mixed_content(self):
        self.assertEqual(
            Div("a", Span("b"), "c").render(pretty=True),
            "<div>a\n  <span>b</span>\n  c\n</div>\n",
        )


class TestComponentTag(unittest.TestCase):
    def test_tag_setter_changes_render(self):
        class Box(Component):
            tag = "section"

        box = Box()
        self.assertEqual(box.tag, "section")
        self.assertEqual(box.render(), "<section></section>")
        box.tag = "aside"
        self.assertEqual(box.render(), "<aside></aside>")

    def test_default_tag_is_div(self):
        class Plain(Component):
            pass

        self.assertEqual(Plain().render(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
