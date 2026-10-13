from .core.element import HTMLElement
from .core.fragment import Fragment
from .core.partial import Partial
from .core.parser import from_html
from .core.slot import Slot
from .core.component import Component
from .forms import Field
from .tags.form import (
    Textarea,
    Select,
    Option,
    Button,
    Fieldset,
    Form,
    Input,
    Label,
    Optgroup,
    Legend,
    Output,
    Progress,
    Meter,
    Datalist,
)
from .tags.html import (
    HTML,
    Head,
    Body,
    Title,
    Meta,
    Link,
    Script,
    Style,
    IFrame,
    Base,
    Noscript,
    Template,
    Svg,
    Math,
)
from .tags.layout import (
    Div,
    Section,
    Header,
    Nav,
    Footer,
    HorizontalRule,
    Main,
    Article,
    Aside,
    Details,
    Summary,
    Dialog,
    Address,
    Hgroup,
    Search,
    Menu,
)
from .tags.lists import (
    UnorderedList,
    OrderedList,
    ListItem,
    DescriptionDetails,
    DescriptionList,
    DescriptionTerm,
)
from .tags.media import (
    Image,
    Video,
    Audio,
    Source,
    Picture,
    Figure,
    Figcaption,
    Canvas,
    Track,
    Embed,
    Object,
    Param,
    Map,
    Area,
)
from .tags.table import (
    Table,
    TableFooter,
    TableHeaderCell,
    TableHeader,
    TableBody,
    TableDataCell,
    TableRow,
    Caption,
    Col,
    Colgroup,
)
from .tags.text import (
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
    Paragraph,
    Blockquote,
    Pre,
    Quote,
    Cite,
    Em,
    Italic,
    Span,
    Strong,
    Abbr,
    Anchor,
    Href,
    Small,
    Superscript,
    Subscript,
    Time,
    Code,
    Bold,
    Del,
    Ins,
    Strikethrough,
    Underline,
    Kbd,
    Samp,
    Var,
    Mark,
    Dfn,
    Br,
    Wbr,
    Bdi,
    Bdo,
    Ruby,
    Rt,
    Rp,
    Data,
)
from .styles import (
    CSSStyle,
    StyleSheet,
    Theme,
)

# layout
Division = Div
Navigation = Nav

# lists
Ul = UnorderedList
Ol = OrderedList
Li = ListItem

Dd = DescriptionDetails
Dl = DescriptionList
Dt = DescriptionTerm

# media
Img = Image

# table
TFoot = TableFooter
Th = TableHeaderCell
THead = TableHeader
TBody = TableBody
Td = TableDataCell
Tr = TableRow

Column = Col
ColumnGroup = Colgroup

# text
Head1 = H1
Head2 = H2
Head3 = H3
Head4 = H4
Head5 = H5
Head6 = H6

P = Paragraph
p = P
Preformatted = Pre
Q = Quote
Emphasis = Em
I = Italic
Abbreviation = Abbr
A = Anchor
Sub = Subscript
Sup = Superscript
B = Bold
Deleted = Del
Inserted = Ins
S = Strikethrough
U = Underline
KeyboardInput = Kbd
SampleOutput = Samp
Variable = Var
Definition = Dfn
Break = Br
WordBreak = Wbr
BiDirectionalIndependent = Bdi
BiDirectionalOverride = Bdo
RubyText = Rt
RubyParenthesis = Rp

__all__ = [
    "HTMLElement",
    "Fragment",
    "Partial",
    "from_html",
    "Slot",
    "Component",
    "Field",
    # styles
    "CSSStyle",
    "StyleSheet",
    "Theme",
    # form
    "Textarea",
    "Select",
    "Option",
    "Button",
    "Fieldset",
    "Form",
    "Input",
    "Label",
    "Optgroup",
    "Legend",
    "Output",
    "Progress",
    "Meter",
    "Datalist",
    # html
    "HTML",
    "Head",
    "Body",
    "Title",
    "Meta",
    "Link",
    "Script",
    "Style",
    "IFrame",
    "Base",
    "Noscript",
    "Template",
    "Svg",
    "Math",
    # layout
    "Div",
    "Section",
    "Header",
    "Nav",
    "Footer",
    "HorizontalRule",
    "Main",
    "Article",
    "Aside",
    "Details",
    "Summary",
    "Dialog",
    "Address",
    "Hgroup",
    "Search",
    "Menu",
    # lists
    "UnorderedList",
    "OrderedList",
    "ListItem",
    "DescriptionDetails",
    "DescriptionList",
    "DescriptionTerm",
    # media
    "Image",
    "Video",
    "Audio",
    "Source",
    "Picture",
    "Figure",
    "Figcaption",
    "Canvas",
    "Track",
    "Embed",
    "Object",
    "Param",
    "Map",
    "Area",
    # table
    "Table",
    "TableFooter",
    "TableHeaderCell",
    "TableHeader",
    "TableBody",
    "TableDataCell",
    "TableRow",
    "Caption",
    "Col",
    "Colgroup",
    # text
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "Paragraph",
    "Blockquote",
    "Pre",
    "Quote",
    "Cite",
    "Em",
    "Italic",
    "Span",
    "Strong",
    "Abbr",
    "Anchor",
    "Href",
    "Small",
    "Superscript",
    "Subscript",
    "Time",
    "Code",
    "Bold",
    "Del",
    "Ins",
    "Strikethrough",
    "Underline",
    "Kbd",
    "Samp",
    "Var",
    "Mark",
    "Dfn",
    "Br",
    "Wbr",
    "Bdi",
    "Bdo",
    "Ruby",
    "Rt",
    "Rp",
    "Data",
    # aliases
    ## layout
    "Division",
    "Navigation",
    ## lists
    "Ul",
    "Ol",
    "Li",
    "Dd",
    "Dl",
    "Dt",
    ## media
    "Img",
    ## table
    "TFoot",
    "Th",
    "THead",
    "TBody",
    "Td",
    "Tr",
    "Column",
    "ColumnGroup",
    ## text
    "Head1",
    "Head2",
    "Head3",
    "Head4",
    "Head5",
    "Head6",
    "P",
    "p",
    "Q",
    "Emphasis",
    "I",
    "Abbreviation",
    "A",
    "Sub",
    "Sup",
    "B",
    "Deleted",
    "Inserted",
    "S",
    "U",
    "KeyboardInput",
    "SampleOutput",
    "Variable",
    "Definition",
    "Break",
    "WordBreak",
    "BiDirectionalIndependent",
    "BiDirectionalOverride",
    "RubyText",
    "RubyParenthesis"
]
