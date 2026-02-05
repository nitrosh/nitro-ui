import unittest

from nitro_ui.core.slot import Slot
from nitro_ui.core.element import HTMLElement
from nitro_ui.tags.text import Paragraph
from nitro_ui.tags.form import Button


class TestSlot(unittest.TestCase):

    def test_default_slot_creation(self):
        """Test creating a default (unnamed) slot."""
        slot = Slot()
        self.assertIsNone(slot.slot_name)
        self.assertIsNone(slot.slot_default)

    def test_named_slot_creation(self):
        """Test creating a named slot."""
        slot = Slot("footer")
        self.assertEqual(slot.slot_name, "footer")
        self.assertIsNone(slot.slot_default)

    def test_slot_with_default_content_single(self):
        """Test creating a slot with default content (single element)."""
        default_btn = Button("Close")
        slot = Slot("footer", default=default_btn)
        self.assertEqual(slot.slot_name, "footer")
        self.assertEqual(slot.slot_default, default_btn)

    def test_slot_with_default_content_list(self):
        """Test creating a slot with default content (list of elements)."""
        defaults = [Button("Cancel"), Button("OK")]
        slot = Slot("actions", default=defaults)
        self.assertEqual(slot.slot_name, "actions")
        self.assertEqual(slot.slot_default, defaults)

    def test_default_slot_with_default_content(self):
        """Test default slot can have default content too."""
        default_content = Paragraph("No content provided")
        slot = Slot(default=default_content)
        self.assertIsNone(slot.slot_name)
        self.assertEqual(slot.slot_default, default_content)

    def test_slot_repr_default(self):
        """Test string representation of default slot."""
        slot = Slot()
        self.assertEqual(repr(slot), "Slot()")

    def test_slot_repr_named(self):
        """Test string representation of named slot."""
        slot = Slot("header")
        self.assertEqual(repr(slot), "Slot('header')")

    def test_slot_is_html_element(self):
        """Test that Slot inherits from HTMLElement."""
        slot = Slot()
        self.assertIsInstance(slot, HTMLElement)

    def test_slot_renders_empty(self):
        """Test that Slot renders to empty string when rendered directly."""
        slot = Slot()
        self.assertEqual(str(slot), "")
        self.assertEqual(slot.render(), "")

    def test_slot_can_be_child(self):
        """Test that Slot can be used as a child of other elements."""
        from nitro_ui.tags.layout import Div

        # This should not raise
        div = Div(Slot(), cls="container")
        # Slot should be in children
        self.assertEqual(len(div.children), 1)
        self.assertIsInstance(div.children[0], Slot)


if __name__ == "__main__":
    unittest.main()
