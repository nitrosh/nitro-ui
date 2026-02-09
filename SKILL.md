---
name: nitro-ui
description: Generate NitroUI code - a Python library for programmatic HTML generation using classes instead of templates
---

# NitroUI Skill Guide

A zero-dependency Python 3.8+ library for programmatic HTML generation. Build HTML with Python classes instead of string templates.

```python
from nitro_ui import Div, H1, Paragraph

page = Div(
    H1("Welcome"),
    Paragraph("Built with NitroUI"),
    cls="container"
)
print(page.render())
# <div class="container"><h1>Welcome</h1><p>Built with NitroUI</p></div>
```

---

## Imports

### Standard Import
```python
from nitro_ui import Div, H1, Paragraph, UnorderedList, ListItem, Image
```

### Core Classes
```python
from nitro_ui import HTMLElement, Fragment, Component, Slot, Partial, from_html
```

### Styling System
```python
from nitro_ui.styles import CSSStyle, StyleSheet, Theme
```

---

## All Tags

### Document Structure
| PascalCase | HTML | Notes |
|------------|------|-------|
| `HTML` | `<html>` | Includes `<!DOCTYPE html>`. Default `lang="en"`, `dir="ltr"` (overridable) |
| `Head` | `<head>` | |
| `Body` | `<body>` | |
| `Title` | `<title>` | |
| `Meta` | `<meta>` | Self-closing |
| `Link` | `<link>` | Self-closing |
| `Script` | `<script>` | |
| `Style` | `<style>` | |
| `Base` | `<base>` | Self-closing |
| `Noscript` | `<noscript>` | |
| `IFrame` | `<iframe>` | |
| `Template` | `<template>` | |
| `Svg` | `<svg>` | SVG camelCase attrs supported (see below) |
| `Math` | `<math>` | |

### Layout
| PascalCase | HTML |
|------------|------|
| `Div` | `<div>` |
| `Section` | `<section>` |
| `Article` | `<article>` |
| `Header` | `<header>` |
| `Footer` | `<footer>` |
| `Nav` | `<nav>` |
| `Main` | `<main>` |
| `Aside` | `<aside>` |
| `HorizontalRule` | `<hr>` (self-closing) |
| `Details` | `<details>` |
| `Summary` | `<summary>` |
| `Dialog` | `<dialog>` |
| `Address` | `<address>` |
| `Hgroup` | `<hgroup>` |
| `Search` | `<search>` |
| `Menu` | `<menu>` |

### Text
| PascalCase | HTML | Notes |
|------------|------|-------|
| `H1`-`H6` | `<h1>`-`<h6>` | |
| `Paragraph` | `<p>` | |
| `Span` | `<span>` | |
| `Strong` | `<strong>` | |
| `Em` | `<em>` | |
| `Bold` | `<b>` | |
| `Italic` | `<i>` | |
| `Underline` | `<u>` | |
| `Strikethrough` | `<s>` | |
| `Small` | `<small>` | |
| `Mark` | `<mark>` | |
| `Del` | `<del>` | |
| `Ins` | `<ins>` | |
| `Subscript` | `<sub>` | |
| `Superscript` | `<sup>` | |
| `Code` | `<code>` | |
| `Pre` | `<pre>` | |
| `Kbd` | `<kbd>` | |
| `Samp` | `<samp>` | |
| `Var` | `<var>` | |
| `Blockquote` | `<blockquote>` | |
| `Quote` | `<q>` | |
| `Cite` | `<cite>` | |
| `Abbr` | `<abbr>` | |
| `Dfn` | `<dfn>` | |
| `Time` | `<time>` | |
| `Anchor` | `<a>` | Preferred name for anchor links |
| `Href` | `<a>` | Backward-compatible alias for `Anchor` |
| `Br` | `<br>` | Self-closing |
| `Wbr` | `<wbr>` | Self-closing |
| `Bdi` | `<bdi>` | Bidirectional isolation |
| `Bdo` | `<bdo>` | Bidirectional override |
| `Ruby` | `<ruby>` | Ruby annotation |
| `Rt` | `<rt>` | Ruby text |
| `Rp` | `<rp>` | Ruby fallback parenthesis |
| `Data` | `<data>` | Machine-readable value |

### Lists
| PascalCase | HTML |
|------------|------|
| `UnorderedList` | `<ul>` |
| `OrderedList` | `<ol>` |
| `ListItem` | `<li>` |
| `DescriptionList` | `<dl>` |
| `DescriptionTerm` | `<dt>` |
| `DescriptionDetails` | `<dd>` |

### Forms
| PascalCase | HTML | Notes |
|------------|------|-------|
| `Form` | `<form>` | Also has `Form.with_fields()` classmethod |
| `Input` | `<input>` | Self-closing |
| `Button` | `<button>` | |
| `Textarea` | `<textarea>` | |
| `Select` | `<select>` | Also has `Select.with_items()` classmethod |
| `Option` | `<option>` | |
| `Optgroup` | `<optgroup>` | |
| `Label` | `<label>` | |
| `Fieldset` | `<fieldset>` | |
| `Legend` | `<legend>` | |
| `Output` | `<output>` | |
| `Progress` | `<progress>` | |
| `Meter` | `<meter>` | |
| `Datalist` | `<datalist>` | |

### Tables
| PascalCase | HTML |
|------------|------|
| `Table` | `<table>` |
| `TableHeader` | `<thead>` |
| `TableBody` | `<tbody>` |
| `TableFooter` | `<tfoot>` |
| `TableRow` | `<tr>` |
| `TableHeaderCell` | `<th>` |
| `TableDataCell` | `<td>` |
| `Caption` | `<caption>` |
| `Colgroup` | `<colgroup>` |
| `Col` | `<col>` (self-closing) |

`Table.from_json(path)` and `Table.from_csv(path)` create tables from files (first row = headers in `<thead>`, rest in `<tbody>`).

### Media
| PascalCase | HTML |
|------------|------|
| `Image` | `<img>` (self-closing) |
| `Video` | `<video>` |
| `Audio` | `<audio>` |
| `Source` | `<source>` (self-closing) |
| `Track` | `<track>` (self-closing) |
| `Picture` | `<picture>` |
| `Figure` | `<figure>` |
| `Figcaption` | `<figcaption>` |
| `Canvas` | `<canvas>` |
| `Embed` | `<embed>` (self-closing) |
| `Object` | `<object>` |
| `Param` | `<param>` (self-closing) |
| `Map` | `<map>` |
| `Area` | `<area>` (self-closing) |

---

## HTMLElement Constructor

```python
HTMLElement(
    *children,                  # HTMLElement, str, or nested lists (auto-flattened)
    tag: str,                   # Required HTML tag name
    self_closing: bool = False,
    **attributes                # HTML attributes as keyword arguments
)
```

**Special attribute mappings:**
- `cls` or `class_name` → renders as `class`
- `class_` → also maps to `class_name`
- `for_element` or `for_` → renders as `for`
- `data_*` → `data-*` (other underscores become hyphens)
- SVG camelCase attrs via snake_case: `view_box` → `viewBox`, `preserve_aspect_ratio` → `preserveAspectRatio`, etc. (52 SVG attributes supported)

**Boolean attributes** (`disabled`, `checked`, `required`, `hidden`, `readonly`, `autofocus`, `autoplay`, `controls`, `loop`, `muted`, `multiple`, `open`, `selected`, `defer`, `async`, `novalidate`, `formnovalidate`, `reversed`, `allowfullscreen`, `inert`, `playsinline`, `nomodule`, `default`, `ismap`, `itemscope`):
- `True` → bare attribute (e.g. `<input disabled>`)
- `False` → attribute omitted entirely
- `None` → attribute omitted entirely

```python
div = Div(
    H1("Title"),
    "Some text",
    id="main",
    cls="container",
    data_value="123"
)
# <div id="main" class="container" data-value="123"><h1>Title</h1>Some text</div>

# Boolean attributes
Input(type="checkbox", checked=True, disabled=False)
# <input type="checkbox" checked />

# SVG camelCase attributes
HTMLElement(tag="svg", view_box="0 0 100 100", preserve_aspect_ratio="xMidYMid")
# <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid"></svg>
```

### Properties

| Property | Type | Mutable | Notes |
|----------|------|---------|-------|
| `tag` | `str` | Yes | HTML tag name |
| `children` | `List[HTMLElement]` | Yes | Use methods preferred |
| `text` | `str` | Yes | Text content |
| `attributes` | `dict` | Yes | Setting invalidates style cache |
| `self_closing` | `bool` | Yes | |

---

## All Methods

### Children

| Method | Returns | Description |
|--------|---------|-------------|
| `append(*children)` | `self` | Add children to end |
| `prepend(*children)` | `self` | Add children to start |
| `clear()` | `self` | Remove all children |
| `pop(index=0)` | `HTMLElement` | Remove and return child |
| `remove_all(condition)` | `self` | Remove matching children |
| `replace_child(index, new)` | `None` | Replace child at index (not chainable) |
| `count_children()` | `int` | Number of direct children |
| `first()` | `HTMLElement\|None` | First child |
| `last()` | `HTMLElement\|None` | Last child |
| `filter(cond, recursive=False, max_depth=1000)` | `Iterator` | Matching children/descendants |
| `find_by_attribute(key, value, max_depth=1000)` | `HTMLElement\|None` | First descendant with matching attr |

Children can be `HTMLElement`, `str`, or nested lists. `None` is silently ignored. Other types raise `ValueError`.

### Attributes

| Method | Returns | Description |
|--------|---------|-------------|
| `add_attribute(key, value)` | `self` | Set single attribute |
| `add_attributes([(k,v),...])` | `self` | Set multiple attributes |
| `remove_attribute(key)` | `self` | Remove attribute |
| `get_attribute(key)` | `str\|None` | Get attribute value |
| `has_attribute(key)` | `bool` | Check existence |
| `get_attributes(*keys)` | `dict` | Get all (or specified) attributes. Returns a copy. |
| `generate_id()` | `None` | Add unique ID if none exists (not chainable) |

### Inline Styles

| Method | Returns | Description |
|--------|---------|-------------|
| `add_style(key, value)` | `self` | Set CSS property. Raises `ValueError` on dangerous values. |
| `add_styles(dict)` | `self` | Set multiple CSS properties |
| `get_style(key)` | `str\|None` | Get CSS property value |
| `remove_style(key)` | `self` | Remove CSS property |

CSS values are validated against injection patterns (`javascript:`, `expression()`, `url(data:)`, etc.).

### Rendering

| Method | Returns | Description |
|--------|---------|-------------|
| `render(pretty=False, max_depth=1000)` | `str` | HTML string. Raises `RecursionError` if depth exceeded. |
| `str(element)` | `str` | Same as `render()` |

### Serialization

| Method | Returns | Description |
|--------|---------|-------------|
| `to_dict(max_depth=1000)` | `dict` | `{tag, self_closing, attributes, text, children}` |
| `to_json(indent=None)` | `str` | JSON string |
| `HTMLElement.from_dict(data, max_depth=1000)` | `HTMLElement` | Reconstruct from dict. Validates input types. Restores subclass types via tag registry. |
| `HTMLElement.from_json(json_str)` | `HTMLElement` | Reconstruct from JSON |
| `from_html(html_str, fragment=False)` | `HTMLElement\|List\|None` | Parse HTML string. Preserves SVG camelCase attrs. |

`from_html` is also available as a standalone function: `from nitro_ui import from_html`

When `fragment=True`, returns `List[HTMLElement]`. When `False`, returns single element or `None`.

`from_dict()` reconstructs `Fragment` instances correctly and uses a tag registry to preserve subclass types where possible.

### Event Callbacks (Override in Subclasses)

| Method | Called When |
|--------|------------|
| `on_load()` | Element constructed |
| `on_before_render()` | Before `render()` |
| `on_after_render()` | After `render()` |
| `on_unload()` | Element garbage collected |

### Utility

| Method | Returns | Description |
|--------|---------|-------------|
| `clone()` | `HTMLElement` | Deep copy |
| `__enter__`/`__exit__` | `self` | Context manager support |

---

## Fragment (No Wrapper Tag)

Renders children without a wrapper element.

```python
from nitro_ui import Fragment, H1, Paragraph

frag = Fragment(H1("Title"), Paragraph("Content"))
print(frag.render())
# <h1>Title</h1><p>Content</p>
```

Use cases: conditional rendering without wrapper divs, returning multiple elements from functions, list composition.

---

## Partial (Raw HTML)

Embed raw HTML for trusted content. Bypasses escaping.

```python
from nitro_ui import Head, Meta, Title, Partial

# Inline raw HTML
Head(
    Meta(charset="utf-8"),
    Partial("""
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
        <script>gtag('config', 'GA_ID');</script>
    """),
    Title("My Page")
)

# Or load from file (lazy-loaded at render time)
Partial(file="partials/analytics.html")
```

**Warning:** Only use with trusted content - bypasses XSS protections.

---

## Component (Reusable Components)

Build reusable components with declarative templates and named slots.

```python
from nitro_ui import Component, Slot, H3, Paragraph, Div, Button

class Card(Component):
    tag = "div"
    class_name = "card"

    def template(self, title: str):
        return [
            H3(title, cls="card-title"),
            Slot()  # children go here
        ]

# Usage
card = Card("My Title",
    Paragraph("Content goes here"),
    id="card-1",
    cls="featured"
)
# <div class="card featured" id="card-1">
#     <h3 class="card-title">My Title</h3>
#     <p>Content goes here</p>
# </div>
```

### Class Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `tag` | `str` | `"div"` | Root element tag |
| `class_name` | `str` | `None` | Default CSS class(es) |

### Template Method

Override `template()` to define the component structure. Parameters become props.

```python
def template(self, title: str, level: str = "info"):
    return [
        Span(f"[{level.upper()}]"),
        Span(title),
        Slot()
    ]
```

### Slots

Use `Slot()` for the default slot (receives `*children`), `Slot("name")` for named slots.

```python
class Modal(Component):
    tag = "div"
    class_name = "modal"

    def template(self, title: str):
        return [
            Div(H2(title), Slot("actions"), cls="header"),
            Div(Slot(), cls="body"),
            Div(Slot("footer", default=Button("Close")), cls="footer")
        ]

# Usage - named slots via kwargs
Modal("Confirm",
    Paragraph("Are you sure?"),              # default slot
    actions=Button("X"),                     # named slot
    footer=[Button("Cancel"), Button("OK")]  # named slot (list)
)
```

**Slot rules:**
- `Slot()` — default slot, receives positional `*children`
- `Slot("name")` — named slot, receives `name=` kwarg
- `Slot("name", default=element)` — fallback content if slot not provided
- Named slot kwargs accept single element or list
- Empty slots render nothing

### Props vs Attributes

Arguments are separated automatically:

1. **HTMLElement args** → default slot children
2. **Non-HTMLElement positional args** → props (matched to `template()` params)
3. **Kwargs matching template params** → props
4. **Kwargs matching slot names** → slot content
5. **Other kwargs** → HTML attributes on root element

```python
class Alert(Component):
    def template(self, message: str, level: str = "info"):
        return [Slot("icon"), Span(message)]

Alert("Hello",                    # prop: message
    level="warning",              # prop (template param)
    icon=Icon("warning"),         # slot
    id="alert-1",                 # HTML attr
    role="alert"                  # HTML attr
)
```

### Class Name Merging

User-provided `cls` merges with the Component's default `class_name` (appends):

```python
class Card(Component):
    class_name = "card"

Card("Title", cls="featured")
# → <div class="card featured">...</div>
```

### Lifecycle Hooks

Components inherit HTMLElement lifecycle hooks:

```python
class MyComponent(Component):
    def on_load(self): ...           # After construction
    def on_before_render(self): ...  # Before render()
    def on_after_render(self): ...   # After render()
```

---

## Styling System

### CSSStyle

Represents CSS styles with pseudo-selectors and responsive breakpoints.

```python
from nitro_ui.styles import CSSStyle

style = CSSStyle(
    background_color="#007bff",    # snake_case -> kebab-case
    color="white",
    padding="10px 20px",
    border_radius="5px",
    _hover=CSSStyle(background_color="#0056b3"),   # pseudo-selector
    _md=CSSStyle(padding="15px 30px")              # breakpoint
)
```

**Pseudo-selectors** (prefix `_`): `_hover`, `_active`, `_focus`, `_visited`, `_link`, `_first_child`, `_last_child`, `_nth_child`, `_before`, `_after`

**Breakpoints** (prefix `_`): `_xs` (0px), `_sm` (640px), `_md` (768px), `_lg` (1024px), `_xl` (1280px), `_2xl` (1536px)

| Method | Returns | Description |
|--------|---------|-------------|
| `to_inline()` | `str` | CSS string for `style="..."` (base styles only) |
| `merge(other)` | `CSSStyle` | New merged style (other overrides) |
| `has_pseudo_or_breakpoints()` | `bool` | Has pseudo/responsive styles |
| `is_complex(threshold=3)` | `bool` | Has many properties |
| `to_dict()` / `CSSStyle.from_dict(data)` | | Serialization |

### StyleSheet

Manages CSS classes and generates `<style>` tag content.

```python
from nitro_ui.styles import StyleSheet, CSSStyle, Theme

# Optional theme for CSS variables
stylesheet = StyleSheet(theme=Theme.modern())

# Register classes
btn = stylesheet.register("btn-primary", CSSStyle(
    background_color="#007bff",
    color="white",
    _hover=CSSStyle(background_color="#0056b3")
))

# BEM naming
card = stylesheet.register_bem("card", style=CSSStyle(padding="20px"))
# "card"
card_header = stylesheet.register_bem("card", element="header",
    style=CSSStyle(font_weight="bold"))
# "card__header"
card_featured = stylesheet.register_bem("card", modifier="featured",
    style=CSSStyle(border="2px solid blue"))
# "card--featured"

# Use in elements
Button("Click", cls=btn)
Div(cls=f"{card} {card_featured}")

# Generate output
css = stylesheet.render()                  # CSS string
tag = stylesheet.to_style_tag()            # <style>...</style>
```

| Method | Returns | Description |
|--------|---------|-------------|
| `register(name, style)` | `str` | Register style, returns class name |
| `register_bem(block, element=, modifier=, style=)` | `str` | BEM class name |
| `get_style(name)` | `CSSStyle\|None` | Get registered style |
| `has_class(name)` | `bool` | Check if registered |
| `unregister(name)` | `bool` | Remove class |
| `clear()` | `None` | Remove all classes |
| `set_breakpoint(name, value)` | `None` | Set breakpoint value |
| `render(pretty=True)` | `str` | CSS output |
| `to_style_tag(pretty=True)` | `str` | `<style>` tag |
| `count_classes()` | `int` | Number of classes |
| `get_all_class_names()` | `List[str]` | All class names |
| `to_dict()` / `StyleSheet.from_dict(data, theme=)` | | Serialization |

### Theme

Preset design systems with CSS variables.

```python
from nitro_ui.styles import Theme

theme = Theme.modern()    # Blue primary, Inter font, modern components
theme = Theme.classic()   # Traditional blue, Georgia serif
theme = Theme.minimal()   # Black/white, system fonts

# Custom
theme = Theme(
    name="Custom",
    colors={"primary": "#007bff", "secondary": "#6c757d"},
    typography={"font_family": "Inter, sans-serif"},
    spacing={"sm": "8px", "md": "16px", "lg": "24px"},
    components={"button": {"primary": CSSStyle(...)}}
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `get_css_variables()` | `dict` | `{"--color-primary": "#007bff", ...}` |
| `get_component_style(component, variant="default")` | `CSSStyle\|None` | Component style |
| `to_dict()` / `Theme.from_dict(data)` | | Serialization |

---

## Common Patterns

### Complete Page
```python
from nitro_ui import HTML, Head, Body, Title, Meta, Div, H1, Paragraph

page = HTML(
    Head(
        Title("My Page"),
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1")
    ),
    Body(
        Div(
            H1("Welcome"),
            Paragraph("Hello, world!"),
            cls="container"
        )
    )
)
html = page.render(pretty=True)
```

### Navigation
```python
from nitro_ui import Nav, UnorderedList, ListItem, Anchor

navbar = Nav(
    UnorderedList(
        ListItem(Anchor("Home", href="/")),
        ListItem(Anchor("About", href="/about")),
        ListItem(Anchor("Contact", href="/contact")),
    ),
    cls="navbar"
)
```

### Form
```python
from nitro_ui import Form, Label, Input, Button

login_form = Form(
    Label("Email:", for_element="email"),
    Input(type="email", id="email", name="email", required=True),
    Label("Password:", for_element="password"),
    Input(type="password", id="password", name="password", required=True),
    Button("Log In", type="submit"),
    action="/login",
    method="post"
)
```

### Table from Data
```python
from nitro_ui import Table, TableHeader, TableBody, TableRow, TableHeaderCell, TableDataCell

data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

t = Table(
    TableHeader(TableRow(TableHeaderCell("Name"), TableHeaderCell("Age"))),
    TableBody(*[
        TableRow(TableDataCell(row["name"]), TableDataCell(str(row["age"])))
        for row in data
    ])
)
```

### Dynamic List
```python
from nitro_ui import UnorderedList, ListItem

items = ["Apple", "Banana", "Orange"]
list_element = UnorderedList(*[ListItem(item) for item in items])
```

### Method Chaining
```python
container = (Div()
    .add_attribute("id", "hero")
    .add_styles({"background": "#f0f0f0", "padding": "2rem"})
    .append(H1("Welcome"))
    .append(Paragraph("Get started today.")))
```

### Custom Component (Recommended)
```python
from nitro_ui import Component, Slot, Div, H2, Paragraph

class Card(Component):
    tag = "div"
    class_name = "card"

    def template(self, title: str):
        return [
            H2(title, cls="card-title"),
            Div(Slot(), cls="card-body")
        ]

card = Card("My Card", Paragraph("Card content here"), id="card-1")
```

### Custom Component (Alternative - Direct Subclass)
```python
from nitro_ui import HTMLElement, H2, Paragraph

class Card(HTMLElement):
    def __init__(self, title, content, **kwargs):
        super().__init__(tag="div", cls="card", **kwargs)
        self.append(
            H2(title, cls="card-title"),
            Paragraph(content, cls="card-body")
        )

card = Card("My Card", "Card content here", id="card-1")
```

### SVG Elements
```python
from nitro_ui import Svg, HTMLElement

# Using the Svg tag class with snake_case kwargs
icon = Svg(
    HTMLElement(
        HTMLElement(tag="circle", cx="12", cy="12", r="10"),
        tag="g",
    ),
    view_box="0 0 24 24",
    preserve_aspect_ratio="xMidYMid meet",
    cls="icon"
)

# Parsing SVG HTML preserves camelCase attributes
from nitro_ui import from_html
svg = from_html('<svg viewBox="0 0 100 100"><circle r="50"/></svg>')
print(svg.render())
# <svg viewBox="0 0 100 100"><circle r="50" /></svg>
```

### Parsing and Modifying HTML
```python
from nitro_ui import from_html, Paragraph

element = from_html('<div class="old"><h1>Title</h1></div>')
element.add_attribute("class", "new")
element.add_style("padding", "20px")
element.append(Paragraph("New content"))
html = element.render()
```

### Serialization Round-Trip
```python
from nitro_ui import Div, H1, HTMLElement

page = Div(H1("Title"), id="page")
json_str = page.to_json(indent=2)
loaded = HTMLElement.from_json(json_str)
html = loaded.render()
```

### Page with StyleSheet
```python
from nitro_ui import HTML, Head, Body, Button, Style
from nitro_ui.styles import CSSStyle, StyleSheet, Theme

theme = Theme.modern()
stylesheet = StyleSheet(theme=theme)

btn = stylesheet.register("btn", CSSStyle(
    background_color="var(--color-primary)",
    color="white",
    padding="10px 20px",
    _hover=CSSStyle(background_color="var(--color-primary-dark)")
))

page = HTML(
    Head(Style(stylesheet.render())),
    Body(Button("Click Me", cls=btn))
)
```

---

## Framework Integration

### FastAPI
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nitro_ui import HTML, Head, Body, Title, H1

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML(
        Head(Title("FastAPI + NitroUI")),
        Body(H1("Hello!"))
    ).render()
```

### Flask
```python
from flask import Flask
from nitro_ui import HTML, Head, Body, Title, H1

app = Flask(__name__)

@app.route("/")
def home():
    return HTML(
        Head(Title("Flask + NitroUI")),
        Body(H1("Hello!"))
    ).render()
```

### Django
```python
from django.http import HttpResponse
from nitro_ui import HTML, Head, Body, Title, H1

def home(request):
    page = HTML(
        Head(Title("Django + NitroUI")),
        Body(H1("Hello!"))
    )
    return HttpResponse(page.render())
```

---

## Form Builder

Generate HTML5 form fields with validation attributes using the `Field` class.

```python
from nitro_ui import Form, Button, Field

form = Form(
    Field.email("email", label="Email", required=True, placeholder="you@example.com"),
    Field.password("password", label="Password", min_length=8),
    Field.checkbox("remember", label="Remember me"),
    Button("Log In", type="submit"),
    action="/login",
    method="post"
)
```

### Text Fields

```python
Field.text(name, label=None, required=False, min_length=None, max_length=None, pattern=None, placeholder=None, value=None, wrapper=None, **attrs)
Field.email(name, label=None, required=False, placeholder=None, value=None, wrapper=None, **attrs)
Field.password(name, label=None, required=False, min_length=None, max_length=None, placeholder=None, wrapper=None, **attrs)
Field.url(name, label=None, required=False, placeholder=None, value=None, wrapper=None, **attrs)
Field.tel(name, label=None, required=False, pattern=None, placeholder=None, value=None, wrapper=None, **attrs)
Field.search(name, label=None, required=False, placeholder=None, value=None, wrapper=None, **attrs)
Field.textarea(name, label=None, required=False, rows=None, cols=None, min_length=None, max_length=None, placeholder=None, value=None, wrapper=None, **attrs)
```

### Numeric & Date Fields

```python
Field.number(name, label=None, required=False, min=None, max=None, step=None, value=None, wrapper=None, **attrs)
Field.range(name, label=None, min=0, max=100, step=None, value=None, wrapper=None, **attrs)
Field.date(name, label=None, required=False, min=None, max=None, value=None, wrapper=None, **attrs)
Field.time(name, label=None, required=False, min=None, max=None, value=None, wrapper=None, **attrs)
Field.datetime_local(name, label=None, required=False, min=None, max=None, value=None, wrapper=None, **attrs)
```

### Selection Fields

```python
# Select with different option formats
Field.select("country", ["USA", "Canada", "Mexico"])  # strings
Field.select("status", [("active", "Active"), ("inactive", "Inactive")])  # tuples
Field.select("priority", [{"value": "1", "label": "Low", "disabled": True}])  # dicts

# Pre-selected value
Field.select("country", ["USA", "Canada"], value="Canada", label="Country")

# Checkbox (label wraps input)
Field.checkbox("terms", label="I agree to the Terms", required=True)

# Radio buttons (wrapped in fieldset)
Field.radio("plan", [("free", "Free"), ("pro", "Pro")], label="Select Plan", value="free")
```

### Other Fields

```python
Field.file(name, label=None, required=False, accept=None, multiple=False, wrapper=None, **attrs)
Field.hidden(name, value, **attrs)
Field.color(name, label=None, value=None, wrapper=None, **attrs)
```

### Labels and Wrappers

```python
# No label - just input
Field.text("username")

# With label
Field.text("username", label="Username")
# → <label for="username">Username</label><input ...>

# With wrapper div
Field.text("username", label="Username", wrapper="form-field")
# → <div class="form-field"><label>...</label><input ...></div>

# Wrapper with attributes
Field.text("username", label="Username", wrapper={"cls": "form-group", "id": "field-1"})
```

### With HTMX

```python
Field.text("search",
    placeholder="Search...",
    hx_get="/search",
    hx_trigger="keyup changed delay:300ms",
    hx_target="#results"
)
```

---

## HTMX Integration

NitroUI works seamlessly with [HTMX](https://htmx.org/). Use `hx_*` kwargs — underscores convert to hyphens automatically.

### Basic Usage

```python
from nitro_ui import Button, Div, Input, Script

# Include HTMX
Script(src="https://unpkg.com/htmx.org@2.0.4")

# hx_get → hx-get, hx_target → hx-target, etc.
Button("Load More", hx_get="/items", hx_target="#list", hx_swap="beforeend")
```

### Common Patterns

```python
# Click to load
Button("Load", hx_get="/content", hx_target="#result")

# Delete with confirmation
Button("Delete", hx_delete="/items/1", hx_confirm="Are you sure?", hx_swap="outerHTML")

# Live search
Input(
    type="text",
    name="q",
    hx_get="/search",
    hx_trigger="keyup changed delay:300ms",
    hx_target="#results"
)

# Form submission
Form(
    Input(type="text", name="email"),
    Button("Subscribe"),
    hx_post="/subscribe",
    hx_swap="outerHTML"
)

# Infinite scroll
Div(
    hx_get="/items?page=2",
    hx_trigger="revealed",
    hx_swap="afterend"
)

# Polling
Div(id="notifications", hx_get="/notifications", hx_trigger="every 30s")
```

### All HTMX Attributes

| Python kwarg | HTML attribute | Description |
|--------------|----------------|-------------|
| `hx_get` | `hx-get` | GET request |
| `hx_post` | `hx-post` | POST request |
| `hx_put` | `hx-put` | PUT request |
| `hx_patch` | `hx-patch` | PATCH request |
| `hx_delete` | `hx-delete` | DELETE request |
| `hx_target` | `hx-target` | Target element selector |
| `hx_swap` | `hx-swap` | How to swap content |
| `hx_trigger` | `hx-trigger` | Event that triggers request |
| `hx_confirm` | `hx-confirm` | Confirmation dialog |
| `hx_indicator` | `hx-indicator` | Loading indicator |
| `hx_push_url` | `hx-push-url` | Push URL to history |
| `hx_select` | `hx-select` | Select content from response |
| `hx_select_oob` | `hx-select-oob` | Out-of-band select |
| `hx_swap_oob` | `hx-swap-oob` | Out-of-band swap |
| `hx_vals` | `hx-vals` | Additional values (JSON) |
| `hx_boost` | `hx-boost` | Boost all links/forms |
| `hx_include` | `hx-include` | Include additional inputs |
| `hx_params` | `hx-params` | Filter parameters |
| `hx_preserve` | `hx-preserve` | Preserve element |
| `hx_ext` | `hx-ext` | Extensions |

### HTMX Extensions

```python
# Server-Sent Events
Div(hx_ext="sse", sse_connect="/events", sse_swap="message")

# WebSockets
Div(hx_ext="ws", ws_connect="/ws")

# JSON encoding
Form(hx_ext="json-enc", hx_post="/api/submit")
```

---

## Security

- **Automatic HTML escaping**: All text content and attribute values are escaped
- **CSS value validation**: `add_style`/`add_styles`/`CSSStyle.to_inline()` reject `javascript:`, `expression()`, `url(data:)`, CSS hex escapes, etc. (raises `ValueError`). Uses a single shared validation implementation.
- **CSS class name validation**: StyleSheet rejects class names containing injection patterns
- **Tag name validation**: Tag names must match `^[a-zA-Z][a-zA-Z0-9-]*$`. Invalid names raise `ValueError`.
- **Attribute key validation**: Invalid attribute keys are skipped with a warning during rendering.
- **Boolean attribute safety**: `disabled=False` correctly omits the attribute (browsers treat any present attribute as truthy).
- **None attribute safety**: Attributes set to `None` are omitted from output (not rendered as literal `"None"`).
- **No raw HTML injection**: Cannot inject unescaped HTML (use `Partial` for trusted raw HTML)
- **Recursion protection**: `render()`, `filter()`, `find_by_attribute()`, `to_dict()`, `from_dict()` all have `max_depth` parameter (default 1000) to prevent stack overflow from circular references
- **Serialization validation**: `from_dict()` validates all field types. `StyleSheet.from_dict()` validates class names.
- **Child type validation**: Only `HTMLElement` and `str` accepted as children. `None` silently ignored, other types raise `ValueError`.
- **Self-closing element warnings**: Adding children or text to self-closing elements (e.g. `<img>`, `<input>`) emits a `UserWarning`.

---

## Gotchas

- **Package name mismatch**: PyPI is `nitro-ui`, import is `nitro_ui`
- **Anchor vs Href**: `Anchor` is the preferred name for `<a>` tags. `Href` is a backward-compatible alias. Both work identically.
- **Link is for `<link>` tags**: `Link` renders `<link>` (stylesheet/meta). Use `Anchor` (or `Href`) for `<a>` links.
- **`children` property returns a copy**: Mutating the returned list does not affect the element. Use `append()`/`prepend()` to modify.
- **`get_attributes()` returns a copy**: Mutating the returned dict does not affect the element. Use `add_attribute()` to modify.
- **`replace_child()` and `generate_id()` return `None`**: Not chainable, unlike other methods.
- **`from_dict()` expects normalized keys**: Designed for round-tripping with `to_dict()`. Attribute keys should already be in their final form (e.g. `data-value`, not `data_value`).
- **SVG attributes require snake_case kwargs**: Use `view_box` not `viewBox` when constructing via kwargs. The camelCase form is used for storage and rendering. `get_attribute("viewBox")` to access.
- **Boolean attributes**: `disabled=True` renders as bare `disabled`, `disabled=False` omits it entirely. `disabled="False"` still renders (as a string value).

---

## Quick Checklist

When generating NitroUI code:

- [ ] Use PascalCase imports: `from nitro_ui import Div, H1, Paragraph`
- [ ] Use `cls` for CSS classes (e.g., `Div(cls="container")`)
- [ ] Use `for_element` not `for` (Python keyword)
- [ ] Use `Anchor` (or `Href`) for `<a>` tags, `Link` for `<link>` tags
- [ ] Children go as positional args, attributes as keyword args
- [ ] Call `.render()` to get HTML string
- [ ] Use `pretty=True` for readable output during development
- [ ] All manipulation methods return `self` for chaining (except `replace_child`, `generate_id`)
- [ ] Use `Fragment` when you need multiple elements without a wrapper
- [ ] Use `Partial` for raw HTML (analytics, embeds) - bypasses escaping
- [ ] Use `Component` + `Slot` for reusable components with declarative templates
- [ ] Use `Field.xyz()` for form fields with HTML5 validation attributes
- [ ] Boolean attrs: pass `True`/`False`, not strings, for `disabled`, `checked`, `required`, etc.
- [ ] SVG attrs: use snake_case kwargs (`view_box`, `preserve_aspect_ratio`) - auto-converted to camelCase
