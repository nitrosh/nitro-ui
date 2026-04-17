from nitro_ui.core.element import HTMLElement, register_tag
from nitro_ui.tags.tag_factory import simple_tag_class

ListItem = simple_tag_class("li")
DescriptionDetails = simple_tag_class("dd")
DescriptionList = simple_tag_class("dl")
DescriptionTerm = simple_tag_class("dt")


class UnorderedList(HTMLElement):
    """HTML ``<ul>`` element with a convenience item-wrapping builder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "ul"})

    @classmethod
    def with_items(cls, *items, **kwargs) -> "UnorderedList":
        """Build a ``<ul>`` and wrap plain items as ``<li>`` children.

        ``HTMLElement`` arguments are appended unchanged; anything else
        (strings, numbers, ...) is wrapped in a ``ListItem``.

        Args:
            *items: Child elements or plain values.
            **kwargs: Attributes forwarded to the ``<ul>``.

        Returns:
            A populated ``UnorderedList`` instance.

        Example:
            >>> UnorderedList.with_items("Apples", "Oranges").render()
            '<ul><li>Apples</li><li>Oranges</li></ul>'
        """
        ul = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                ul.append(item)
            else:
                ul.append(ListItem(item))
        return ul


register_tag("ul", UnorderedList)


class OrderedList(HTMLElement):
    """HTML ``<ol>`` element with a convenience item-wrapping builder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "ol"})

    @classmethod
    def with_items(cls, *items, **kwargs) -> "OrderedList":
        """Build an ``<ol>`` and wrap plain items as ``<li>`` children.

        ``HTMLElement`` arguments are appended unchanged; anything else
        is wrapped in a ``ListItem``.

        Args:
            *items: Child elements or plain values.
            **kwargs: Attributes forwarded to the ``<ol>``.

        Returns:
            A populated ``OrderedList`` instance.
        """
        ol = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                ol.append(item)
            else:
                ol.append(ListItem(item))
        return ol


register_tag("ol", OrderedList)
