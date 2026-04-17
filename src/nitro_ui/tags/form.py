from nitro_ui.core.element import HTMLElement, register_tag
from nitro_ui.tags.tag_factory import simple_tag_class

Textarea = simple_tag_class("textarea")
BaseSelect = simple_tag_class("select")
Option = simple_tag_class("option")
Button = simple_tag_class("button")
Fieldset = simple_tag_class("fieldset")
Legend = simple_tag_class("legend")
Input = simple_tag_class("input", self_closing=True)
Optgroup = simple_tag_class("optgroup")
Output = simple_tag_class("output")
Progress = simple_tag_class("progress")
Meter = simple_tag_class("meter")
Datalist = simple_tag_class("datalist")


class Select(BaseSelect):
    """HTML ``<select>`` dropdown with a convenience option builder."""

    @classmethod
    def with_items(cls, *items, **kwargs) -> "Select":
        """Build a ``<select>`` and wrap plain items as ``<option>`` children.

        ``HTMLElement`` arguments (including ``Option`` / ``Optgroup``)
        are appended unchanged. Any other value is wrapped in an
        ``Option(item)``.

        Args:
            *items: Option elements or plain values.
            **kwargs: Attributes forwarded to the ``<select>``.

        Returns:
            A populated ``Select`` instance.

        Example:
            >>> Select.with_items("Red", "Green", "Blue", name="color").render()
            '<select name="color"><option>Red</option><option>Green</option><option>Blue</option></select>'
        """
        opt = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                opt.append(item)
            else:
                opt.append(Option(item))
        return opt


register_tag("select", Select)


def label_extra_init(self, kwargs):
    """Translate ``for_element`` to ``for`` when a ``Label`` is constructed.

    NitroUI normalizes Python-keyword-clashing attrs as ``for_element``;
    the ``<label>`` tag uses the HTML name directly.
    """
    if "for_element" in kwargs:
        kwargs["for"] = kwargs.pop("for_element")


Label = simple_tag_class("label", extra_init=label_extra_init)


class Form(HTMLElement):
    """HTML ``<form>`` element with a convenience field-appending builder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "form"})

    @classmethod
    def with_fields(cls, *items, **kwargs) -> "Form":
        """Build a ``<form>`` from a flat list of fields and text nodes.

        Equivalent to ``Form(*items, **kwargs)`` but with a type guard -
        anything that is not an ``HTMLElement`` or string raises
        ``TypeError`` rather than silently misbehaving.

        Args:
            *items: Elements or strings to place inside the form.
            **kwargs: Attributes forwarded to the ``<form>``.

        Returns:
            A populated ``Form`` instance.

        Raises:
            TypeError: If any item is not an ``HTMLElement`` or string.
        """
        form = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                form.append(item)
            elif isinstance(item, str):
                form.append(item)
            else:
                raise TypeError(
                    f"Invalid form field: {item!r} (type {type(item).__name__}). "
                    "Expected an HTMLElement or string."
                )
        return form


register_tag("form", Form)
