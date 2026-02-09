from nitro_ui.core.element import HTMLElement, register_tag
from nitro_ui.tags.tag_factory import simple_tag_class


class HTML(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **{
                "lang": "en",
                "dir": "ltr",
                **kwargs,
                "tag": "html",
                "self_closing": False,
            },
        )
        self._prefix = "<!DOCTYPE html>"


register_tag("html", HTML)

Head = simple_tag_class("head")
Body = simple_tag_class("body")
Title = simple_tag_class("title")
Meta = simple_tag_class("meta", self_closing=True)
Base = simple_tag_class("base", self_closing=True)
Link = simple_tag_class("link", self_closing=True)
Script = simple_tag_class("script")
Style = simple_tag_class("style")
Noscript = simple_tag_class("noscript")
IFrame = simple_tag_class("iframe")
Template = simple_tag_class("template")
Svg = simple_tag_class("svg")
Math = simple_tag_class("math")
