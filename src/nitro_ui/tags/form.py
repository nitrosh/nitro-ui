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
    @classmethod
    def with_items(cls, *items, **kwargs):
        opt = cls(**kwargs)
        for item in items:
            if isinstance(item, HTMLElement):
                opt.append(item)
            else:
                opt.append(Option(item))
        return opt


register_tag("select", Select)


def label_extra_init(self, kwargs):
    if "for_element" in kwargs:
        kwargs["for"] = kwargs.pop("for_element")


Label = simple_tag_class("label", extra_init=label_extra_init)


class Form(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "form"})

    @classmethod
    def with_fields(cls, *items, **kwargs):
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
