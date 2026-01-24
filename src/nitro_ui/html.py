"""Lowercase HTML-like aliases for NitroUI elements.

This module provides lowercase function-style aliases that mirror actual HTML tag names,
making NitroUI code look more like HTML.

Usage:
    from nitro_ui.html import div, h1, p, a, ul, li

    page = div(
        h1("Welcome"),
        p("This looks like HTML!"),
        ul(
            li("Item 1"),
            li("Item 2"),
        ),
        class_name="container"
    )

Note: Python keywords and builtins are suffixed with underscore:
    - del_ (for <del>)
    - input_ (for <input>)
    - object_ (for <object>)
    - map_ (for <map>)
"""

# Core
from .core.element import HTMLElement
from .core.fragment import Fragment
from .core.parser import from_html

# Form elements
from .tags.form import (
    Textarea as textarea,
    Select as select,
    Option as option,
    Button as button,
    Fieldset as fieldset,
    Form as form,
    Input as input_,  # 'input' is a Python builtin
    Label as label,
    Optgroup as optgroup,
    Legend as legend,
    Output as output,
    Progress as progress,
    Meter as meter,
)

# Document structure
from .tags.html import (
    HTML as html,
    Head as head,
    Body as body,
    Title as title,
    Meta as meta,
    Link as link,
    Script as script,
    Style as style,
    IFrame as iframe,
    Base as base,
    Noscript as noscript,
)

# Layout elements
from .tags.layout import (
    Div as div,
    Section as section,
    Header as header,
    Nav as nav,
    Footer as footer,
    HorizontalRule as hr,
    Main as main,
    Article as article,
    Aside as aside,
    Details as details,
    Summary as summary,
    Dialog as dialog,
)

# List elements
from .tags.lists import (
    UnorderedList as ul,
    OrderedList as ol,
    ListItem as li,
    Datalist as datalist,
    DescriptionDetails as dd,
    DescriptionList as dl,
    DescriptionTerm as dt,
)

# Media elements
from .tags.media import (
    Image as img,
    Video as video,
    Audio as audio,
    Source as source,
    Picture as picture,
    Figure as figure,
    Figcaption as figcaption,
    Canvas as canvas,
    Track as track,
    Embed as embed,
    Object as object_,  # 'object' is a Python builtin
    Param as param,
    Map as map_,  # 'map' is a Python builtin
    Area as area,
)

# Table elements
from .tags.table import (
    Table as table,
    TableFooter as tfoot,
    TableHeaderCell as th,
    TableHeader as thead,
    TableBody as tbody,
    TableDataCell as td,
    TableRow as tr,
    Caption as caption,
    Col as col,
    Colgroup as colgroup,
)

# Text elements
from .tags.text import (
    H1 as h1,
    H2 as h2,
    H3 as h3,
    H4 as h4,
    H5 as h5,
    H6 as h6,
    Paragraph as p,
    Blockquote as blockquote,
    Pre as pre,
    Quote as q,
    Cite as cite,
    Em as em,
    Italic as i,
    Span as span,
    Strong as strong,
    Abbr as abbr,
    Href as a,  # <a> tag
    Small as small,
    Superscript as sup,
    Subscript as sub,
    Time as time,
    Code as code,
    Bold as b,
    Del as del_,  # 'del' is a Python keyword
    Ins as ins,
    Strikethrough as s,
    Underline as u,
    Kbd as kbd,
    Samp as samp,
    Var as var,
    Mark as mark,
    Dfn as dfn,
    Br as br,
    Wbr as wbr,
)

# Styles (unchanged, not HTML tags)
from .styles import CSSStyle, StyleSheet, Theme

__all__ = [
    # Core
    "HTMLElement",
    "Fragment",
    "from_html",
    # Styles
    "CSSStyle",
    "StyleSheet",
    "Theme",
    # Form elements
    "textarea",
    "select",
    "option",
    "button",
    "fieldset",
    "form",
    "input_",
    "label",
    "optgroup",
    "legend",
    "output",
    "progress",
    "meter",
    # Document structure
    "html",
    "head",
    "body",
    "title",
    "meta",
    "link",
    "script",
    "style",
    "iframe",
    "base",
    "noscript",
    # Layout elements
    "div",
    "section",
    "header",
    "nav",
    "footer",
    "hr",
    "main",
    "article",
    "aside",
    "details",
    "summary",
    "dialog",
    # List elements
    "ul",
    "ol",
    "li",
    "datalist",
    "dd",
    "dl",
    "dt",
    # Media elements
    "img",
    "video",
    "audio",
    "source",
    "picture",
    "figure",
    "figcaption",
    "canvas",
    "track",
    "embed",
    "object_",
    "param",
    "map_",
    "area",
    # Table elements
    "table",
    "tfoot",
    "th",
    "thead",
    "tbody",
    "td",
    "tr",
    "caption",
    "col",
    "colgroup",
    # Text elements
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "blockquote",
    "pre",
    "q",
    "cite",
    "em",
    "i",
    "span",
    "strong",
    "abbr",
    "a",
    "small",
    "sup",
    "sub",
    "time",
    "code",
    "b",
    "del_",
    "ins",
    "s",
    "u",
    "kbd",
    "samp",
    "var",
    "mark",
    "dfn",
    "br",
    "wbr",
]
