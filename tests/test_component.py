import unittest

from nitro_ui.core.component import Component
from nitro_ui.core.slot import Slot
from nitro_ui.tags.layout import Div
from nitro_ui.tags.text import H1, H2, H3, Paragraph, Span
from nitro_ui.tags.form import Button


class TestComponentBasic(unittest.TestCase):

    def test_minimal_component(self):
        """Test a minimal component with just a tag."""
        class Simple(Component):
            tag = "section"

        result = Simple()
        self.assertEqual(str(result), "<section></section>")

    def test_component_with_class_name(self):
        """Test component with default class name."""
        class Card(Component):
            tag = "div"
            class_name = "card"

        result = Card()
        self.assertEqual(str(result), '<div class="card"></div>')

    def test_component_default_slot(self):
        """Test component renders children into default slot."""
        class Card(Component):
            tag = "div"
            class_name = "card"

            def template(self):
                return [Slot()]

        result = Card(Paragraph("Hello"), Paragraph("World"))
        self.assertEqual(
            str(result),
            '<div class="card"><p>Hello</p><p>World</p></div>'
        )

    def test_component_with_props(self):
        """Test component with props defined in template method."""
        class Card(Component):
            tag = "div"
            class_name = "card"

            def template(self, title: str):
                return [
                    H3(title, cls="card-title"),
                    Slot()
                ]

        result = Card("My Title", Paragraph("Content"))
        self.assertEqual(
            str(result),
            '<div class="card"><h3 class="card-title">My Title</h3><p>Content</p></div>'
        )

    def test_component_prop_with_default(self):
        """Test component with props that have default values."""
        class Alert(Component):
            tag = "div"
            class_name = "alert"

            def template(self, message: str, level: str = "info"):
                return [
                    Span(f"[{level.upper()}]", cls="level"),
                    Span(message)
                ]

        # Using default
        result = Alert("Hello")
        self.assertIn("[INFO]", str(result))

        # Overriding default
        result2 = Alert("Error!", level="error")
        self.assertIn("[ERROR]", str(result2))


class TestComponentSlots(unittest.TestCase):

    def test_named_slot(self):
        """Test component with named slot."""
        class Modal(Component):
            tag = "div"
            class_name = "modal"

            def template(self, title: str):
                return [
                    H2(title),
                    Div(Slot(), cls="body"),
                    Div(Slot("footer"), cls="footer")
                ]

        result = Modal(
            "My Modal",
            Paragraph("Body content"),
            footer=Button("Close")
        )
        rendered = str(result)
        self.assertIn('<h2>My Modal</h2>', rendered)
        self.assertIn('<div class="body"><p>Body content</p></div>', rendered)
        self.assertIn('<div class="footer"><button>Close</button></div>', rendered)

    def test_named_slot_with_list(self):
        """Test named slot receiving a list of elements."""
        class Modal(Component):
            tag = "div"

            def template(self):
                return [
                    Div(Slot(), cls="body"),
                    Div(Slot("actions"), cls="actions")
                ]

        result = Modal(
            Paragraph("Content"),
            actions=[Button("Cancel"), Button("OK")]
        )
        rendered = str(result)
        self.assertIn('<button>Cancel</button><button>OK</button>', rendered)

    def test_empty_slot(self):
        """Test that empty named slots render nothing."""
        class Card(Component):
            tag = "div"

            def template(self):
                return [
                    Div(Slot(), cls="body"),
                    Div(Slot("footer"), cls="footer")
                ]

        result = Card(Paragraph("Body"))
        rendered = str(result)
        self.assertIn('<div class="body"><p>Body</p></div>', rendered)
        self.assertIn('<div class="footer"></div>', rendered)

    def test_slot_with_default_content(self):
        """Test slot falls back to default content when not provided."""
        class Card(Component):
            tag = "div"

            def template(self):
                return [
                    Slot(),
                    Div(Slot("footer", default=Button("Close")), cls="footer")
                ]

        # Without footer
        result = Card(Paragraph("Body"))
        self.assertIn('<button>Close</button>', str(result))

        # With footer - should use provided content
        result2 = Card(Paragraph("Body"), footer=Button("Save"))
        self.assertIn('<button>Save</button>', str(result2))
        self.assertNotIn('Close', str(result2))

    def test_multiple_named_slots(self):
        """Test component with multiple named slots."""
        class Layout(Component):
            tag = "div"
            class_name = "layout"

            def template(self):
                return [
                    Div(Slot("header"), cls="header"),
                    Div(Slot(), cls="main"),
                    Div(Slot("sidebar"), cls="sidebar"),
                    Div(Slot("footer"), cls="footer")
                ]

        result = Layout(
            Paragraph("Main content"),
            header=H1("Title"),
            sidebar=Span("Side"),
            footer=Span("Footer")
        )
        rendered = str(result)
        self.assertIn('<div class="header"><h1>Title</h1></div>', rendered)
        self.assertIn('<div class="main"><p>Main content</p></div>', rendered)
        self.assertIn('<div class="sidebar"><span>Side</span></div>', rendered)
        self.assertIn('<div class="footer"><span>Footer</span></div>', rendered)


class TestComponentClassMerging(unittest.TestCase):

    def test_class_name_merging(self):
        """Test that user class_name merges with default."""
        class Card(Component):
            tag = "div"
            class_name = "card"

        result = Card(class_name="highlighted")
        self.assertEqual(str(result), '<div class="card highlighted"></div>')

    def test_class_name_merging_with_cls(self):
        """Test that cls alias also merges."""
        class Card(Component):
            tag = "div"
            class_name = "card"

        result = Card(cls="featured")
        self.assertEqual(str(result), '<div class="card featured"></div>')

    def test_no_default_class(self):
        """Test component without default class uses only user class."""
        class Simple(Component):
            tag = "div"

        result = Simple(class_name="custom")
        self.assertEqual(str(result), '<div class="custom"></div>')

    def test_no_class_at_all(self):
        """Test component without any class."""
        class Simple(Component):
            tag = "div"

        result = Simple()
        self.assertEqual(str(result), '<div></div>')


class TestComponentHTMLAttributes(unittest.TestCase):

    def test_html_attributes_passthrough(self):
        """Test that HTML attributes pass through to root element."""
        class Card(Component):
            tag = "div"
            class_name = "card"

        result = Card(id="card-1", data_testid="main-card")
        rendered = str(result)
        self.assertIn('id="card-1"', rendered)
        self.assertIn('data-testid="main-card"', rendered)

    def test_attributes_dont_conflict_with_props(self):
        """Test that HTML attrs and props are properly separated."""
        class Alert(Component):
            tag = "div"

            def template(self, message: str):
                return [Span(message)]

        result = Alert("Hello", id="alert-1", role="alert")
        rendered = str(result)
        self.assertIn('id="alert-1"', rendered)
        self.assertIn('role="alert"', rendered)
        self.assertIn('<span>Hello</span>', rendered)


class TestComponentEdgeCases(unittest.TestCase):

    def test_no_slot_appends_children(self):
        """Test that children append at end when no Slot defined."""
        class Simple(Component):
            tag = "div"

            def template(self, label: str):
                return [Span(label)]

        result = Simple("Hi", Paragraph("Extra"))
        self.assertEqual(
            str(result),
            '<div><span>Hi</span><p>Extra</p></div>'
        )

    def test_none_in_template_filtered(self):
        """Test that None values in template are filtered out."""
        class Conditional(Component):
            tag = "div"

            def template(self, show_icon: bool = False):
                return [
                    Span("*") if show_icon else None,
                    Slot()
                ]

        result_without = Conditional(Paragraph("Content"))
        self.assertEqual(str(result_without), '<div><p>Content</p></div>')

        result_with = Conditional(Paragraph("Content"), show_icon=True)
        self.assertIn('<span>*</span>', str(result_with))

    def test_missing_required_prop_raises(self):
        """Test that missing required prop raises TypeError."""
        class Card(Component):
            tag = "div"

            def template(self, title: str):
                return [H3(title)]

        with self.assertRaises(TypeError) as ctx:
            Card()
        self.assertIn("title", str(ctx.exception))

    def test_deeply_nested_slots(self):
        """Test slots work in deeply nested structures."""
        class Complex(Component):
            tag = "div"

            def template(self):
                return [
                    Div(
                        Div(
                            Div(Slot(), cls="inner"),
                            cls="middle"
                        ),
                        cls="outer"
                    )
                ]

        result = Complex(Paragraph("Deep"))
        self.assertIn(
            '<div class="inner"><p>Deep</p></div>',
            str(result)
        )

    def test_empty_children(self):
        """Test component with no children."""
        class Card(Component):
            tag = "div"
            class_name = "card"

            def template(self, title: str):
                return [
                    H3(title),
                    Slot()
                ]

        result = Card("Title")
        self.assertEqual(
            str(result),
            '<div class="card"><h3>Title</h3></div>'
        )

    def test_prop_via_kwarg(self):
        """Test that props can be passed via kwargs."""
        class Card(Component):
            tag = "div"

            def template(self, title: str):
                return [H3(title)]

        result = Card(title="Via Kwarg")
        self.assertIn('<h3>Via Kwarg</h3>', str(result))


class TestComponentInheritance(unittest.TestCase):

    def test_component_inherits_from_html_element(self):
        """Test that Component instances are HTMLElement instances."""
        class Card(Component):
            tag = "div"

        from nitro_ui.core.element import HTMLElement
        result = Card()
        self.assertIsInstance(result, HTMLElement)

    def test_component_can_use_element_methods(self):
        """Test that Component can use HTMLElement methods."""
        class Card(Component):
            tag = "div"
            class_name = "card"

        result = Card()
        result.add_attribute("data-extra", "value")
        self.assertIn('data-extra="value"', str(result))


if __name__ == "__main__":
    unittest.main()
