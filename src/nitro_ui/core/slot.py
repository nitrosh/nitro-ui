from typing import Union, List, Any

from nitro_ui.core.element import HTMLElement


class Slot(HTMLElement):
    """Marker for where content should be inserted in a Component template.

    Slots act as placeholders that get replaced with actual content when
    the component renders. They support both default (unnamed) slots and
    named slots.

    Slot inherits from HTMLElement so it can be used as a child in templates,
    but it gets replaced during Component rendering and never actually renders.

    Example:
        class Card(Component):
            def template(self, title: str):
                return [
                    H3(title),
                    Slot(),  # default slot - receives *children
                    Slot("footer", default=Button("Close"))  # named slot
                ]

        # Usage
        Card("Title",
            Paragraph("body content"),  # goes to default Slot()
            footer=Button("Save")       # goes to Slot("footer")
        )
    """

    def __init__(
        self,
        name: str = None,
        default: Union["HTMLElement", List[Any], None] = None,
    ):
        """Create a slot marker.

        Args:
            name: Slot name. None for default slot, string for named slot.
            default: Default content if no content is provided for this slot.
                     Can be a single element or a list of elements.
        """
        # Initialize as a placeholder element that won't render
        super().__init__(tag="slot")
        self.slot_name = name  # Use slot_name to avoid conflict with any HTML attr
        self.slot_default = default

    def __repr__(self) -> str:
        if self.slot_name:
            return f"Slot({self.slot_name!r})"
        return "Slot()"

    def render(self, pretty: bool = False, _indent: int = 0, max_depth: int = 1000) -> str:
        """Slots should never render directly - they get replaced by Component."""
        # Return empty string if somehow rendered directly
        return ""
