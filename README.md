# NitroUI

**Build HTML with Python, not strings.**

NitroUI is a zero-dependency Python library that lets you construct HTML documents using a clean, composable class-based API. No template files, no string concatenation, no runtime dependencies.

```python
from nitro_ui import *

page = HTML(
    Head(Title("Dashboard")),
    Body(
        Nav(
            Anchor("Home", href="/"),
            Anchor("Settings", href="/settings", cls="active")
        ),
        Main(
            H1("Welcome back!"),
            Div(
                Paragraph("You have ", Strong("3"), " new notifications."),
                Button("View All", type="button", cls="btn-primary")
            )
        )
    )
)

print(page.render(pretty=True))
```

## Why NitroUI?

- **Type-safe**: IDE autocomplete and type hints for every element
- **Composable**: Build reusable components as Python classes
- **Zero dependencies**: Just Python 3.8+, nothing else
- **Framework agnostic**: Works with FastAPI, Django, Flask, or standalone
- **Serializable**: Convert to/from JSON for drag-and-drop builders
- **Secure by default**: Automatic HTML escaping, CSS injection prevention, tag/attribute validation
- **SVG-aware**: Correct camelCase attribute handling for SVG elements
- **LLM-friendly**: Perfect for AI-generated interfaces

## Installation

```bash
pip install nitro-ui
```

### Claude Code Skill

Add NitroUI as a skill in [Claude Code](https://claude.ai/code) for AI-assisted HTML generation:

```bash
npx skills add nitrosh/nitro-ui
```

## Quick Examples

### Dynamic Content

```python
from nitro_ui import *

def render_user_card(user):
    return Div(
        Image(src=user["avatar"], alt=user["name"]),
        H3(user["name"]),
        Paragraph(user["bio"]),
        Anchor("View Profile", href=f"/users/{user['id']}"),
        cls="user-card"
    )

users = [
    {"id": 1, "name": "Alice", "bio": "Backend engineer", "avatar": "/avatars/alice.jpg"},
    {"id": 2, "name": "Bob", "bio": "Frontend developer", "avatar": "/avatars/bob.jpg"},
]

grid = Div(*[render_user_card(u) for u in users], cls="user-grid")
```

### Method Chaining

```python
from nitro_ui import *

card = (Div()
    .add_attribute("id", "hero")
    .add_styles({"background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "padding": "4rem"})
    .append(H1("Ship faster with NitroUI"))
    .append(Paragraph("Stop fighting with templates. Start building.")))
```

### Reusable Components

```python
from nitro_ui import *

class Card(Component):
    tag = "div"
    class_name = "card"

    def template(self, title: str):
        return [
            H3(title, cls="card-title"),
            Slot()  # children go here
        ]

class Alert(Component):
    tag = "div"
    class_name = "alert"

    def template(self, message: str, variant: str = "info"):
        self.add_attribute("class", f"alert-{variant}")
        self.add_attribute("role", "alert")
        return [Paragraph(message), Slot()]

# Usage
page = Div(
    Alert("Your changes have been saved.", variant="success"),
    Card("Statistics",
        Paragraph("Total users: 1,234"),
        Paragraph("Active today: 89")
    )
)
```

Components support named slots for complex layouts:

```python
class Modal(Component):
    tag = "div"
    class_name = "modal"

    def template(self, title: str):
        return [
            Div(H2(title), Slot("actions"), cls="modal-header"),
            Div(Slot(), cls="modal-body"),
            Div(Slot("footer"), cls="modal-footer")
        ]

# Named slots via kwargs
Modal("Confirm Delete",
    Paragraph("Are you sure?"),
    actions=Button("×", cls="close"),
    footer=[Button("Cancel"), Button("Delete", cls="danger")]
)
```

### External Stylesheets with Themes

```python
from nitro_ui import *
from nitro_ui.styles import CSSStyle, StyleSheet, Theme

# Use a preset theme
theme = Theme.modern()
stylesheet = StyleSheet(theme=theme)

# Register component styles
btn = stylesheet.register("btn", CSSStyle(
    background_color="var(--color-primary)",
    color="var(--color-white)",
    padding="var(--spacing-sm) var(--spacing-md)",
    border_radius="6px",
    border="none",
    cursor="pointer",
    _hover=CSSStyle(background_color="var(--color-primary-dark)")
))

# Use in your HTML
page = HTML(
    Head(
        Title("Styled Page"),
        Style(stylesheet.render())
    ),
    Body(
        Button("Click Me", cls=btn)
    )
)
```

### Framework Integration

**FastAPI**
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nitro_ui import *

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML(
        Head(Title("FastAPI + NitroUI")),
        Body(H1("Hello from FastAPI"))
    ).render()
```

**Flask**
```python
from flask import Flask
from nitro_ui import *

app = Flask(__name__)

@app.route("/")
def home():
    return HTML(
        Head(Title("Flask + NitroUI")),
        Body(H1("Hello from Flask"))
    ).render()
```

**Django**
```python
from django.http import HttpResponse
from nitro_ui import *

def home(request):
    return HttpResponse(HTML(
        Head(Title("Django + NitroUI")),
        Body(H1("Hello from Django"))
    ).render())
```

## Core Features

### Pretty Printing

```python
# Compact output (default) - ideal for production
page.render()

# Indented output - ideal for debugging
page.render(pretty=True)
```

### JSON Serialization

Perfect for drag-and-drop builders, undo/redo, or API communication:

```python
from nitro_ui import *
from nitro_ui.core.element import HTMLElement

# Serialize
json_data = page.to_json(indent=2)

# Deserialize
restored = HTMLElement.from_json(json_data)
```

### HTML Parsing

Import existing HTML into NitroUI for manipulation:

```python
from nitro_ui import from_html

element = from_html('<div class="card"><h1>Hello</h1></div>')
element.append(Paragraph("Added with NitroUI"))
```

### Fragments

Group elements without a wrapper tag:

```python
from nitro_ui import *

def table_rows(items):
    return Fragment(*[
        TableRow(TableDataCell(item["name"]), TableDataCell(item["price"]))
        for item in items
    ])
```

### Form Builder

Generate HTML5 forms with validation using the `Field` class:

```python
from nitro_ui import *

form = Form(
    Field.email("email", label="Email", required=True),
    Field.password("password", label="Password", min_length=8),
    Field.select("country", ["USA", "Canada", "Mexico"], label="Country"),
    Field.checkbox("terms", label="I agree to the Terms", required=True),
    Button("Sign Up", type="submit"),
    action="/register"
)
```

Field types: `text`, `email`, `password`, `url`, `tel`, `search`, `textarea`, `number`, `range`, `date`, `time`, `datetime_local`, `select`, `checkbox`, `radio`, `file`, `hidden`, `color`. See [SKILL.md](SKILL.md) for full API.

### HTMX Integration

Build interactive UIs without JavaScript. NitroUI converts `hx_*` kwargs to `hx-*` attributes automatically:

```python
from nitro_ui import *

# Live search
Input(
    type="text",
    hx_get="/search",
    hx_trigger="keyup changed delay:300ms",
    hx_target="#results"
)

# Delete with confirmation
Button(
    "Delete",
    hx_delete="/items/1",
    hx_confirm="Are you sure?",
    hx_swap="outerHTML"
)

# Load more
Button("Load More", hx_get="/items?page=2", hx_target="#list", hx_swap="beforeend")
```

All HTMX attributes are supported: `hx_get`, `hx_post`, `hx_put`, `hx_delete`, `hx_target`, `hx_swap`, `hx_trigger`, `hx_confirm`, `hx_indicator`, `hx_boost`, and more. See [SKILL.md](SKILL.md) for the complete reference.

### Raw HTML Partials

Embed raw HTML for trusted content like analytics tags:

```python
from nitro_ui import Head, Meta, Title, Partial

Head(
    Meta(charset="utf-8"),
    Partial("""
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'GA_ID');
        </script>
    """),
    Title("My Page")
)

# Or load from a file (lazy-loaded at render time)
Partial(file="partials/analytics.html")
```

**Warning:** `Partial` bypasses HTML escaping. Only use with trusted content.

### CSS Style Helpers

```python
div = Div("Content")
div.add_style("color", "blue")
div.add_styles({"padding": "20px", "margin": "10px"})
div.remove_style("margin")
color = div.get_style("color")  # "blue"
```

## Available Elements

Import all elements with `from nitro_ui import *`:

| Module                 | Elements                                                                                       |
|------------------------|-----------------------------------------------------------------------------------------------|
| `nitro_ui.tags.html`   | HTML, Head, Body, Title, Meta, Link, Script, Style, Base, Noscript, IFrame, Template, Svg, Math |
| `nitro_ui.tags.layout` | Div, Section, Article, Header, Nav, Footer, Main, Aside, Details, Summary, Dialog, Address, Hgroup, Search, Menu |
| `nitro_ui.tags.text`   | H1-H6, Paragraph, Span, Strong, Em, Bold, Italic, Anchor (alias: Href), Code, Pre, Blockquote, Br, Wbr, Bdi, Bdo, Ruby, Rt, Rp, Data, and more |
| `nitro_ui.tags.form`   | Form, Input, Button, Select, Option, Textarea, Label, Fieldset, Legend, Optgroup, Output, Progress, Meter, Datalist |
| `nitro_ui.tags.lists`  | UnorderedList, OrderedList, ListItem, DescriptionList, DescriptionTerm, DescriptionDetails     |
| `nitro_ui.tags.media`  | Image, Video, Audio, Source, Track, Picture, Figure, Figcaption, Canvas, Embed, Object, Param, Map, Area |
| `nitro_ui.tags.table`  | Table, TableRow, TableHeader, TableBody, TableFooter, TableHeaderCell, TableDataCell, Caption, Col, Colgroup |

## Element API

**Manipulation**
- `append(*children)` / `prepend(*children)` - Add children
- `clear()` - Remove all children
- `clone()` - Deep copy element
- `find_by_attribute(attr, value)` - Find child by attribute

**Attributes**
- `add_attribute(key, value)` / `add_attributes(list)`
- `get_attribute(key)` / `has_attribute(key)`
- `remove_attribute(key)`
- HTML5 boolean attributes (`disabled`, `checked`, `required`, etc.) render correctly: `True` renders as a bare attribute, `False` omits it, `None` omits it
- SVG camelCase attributes are supported via snake_case kwargs: `view_box` renders as `viewBox`, `preserve_aspect_ratio` as `preserveAspectRatio`, etc.

**Styles**
- `add_style(prop, value)` / `add_styles(dict)`
- `get_style(prop)` / `remove_style(prop)`

**Output**
- `render(pretty=False)` - Generate HTML string
- `to_json()` / `from_json()` - JSON serialization
- `to_dict()` / `from_dict()` - Dictionary conversion

All manipulation methods return `self` for chaining.

## For AI/LLM Integration

NitroUI is designed to work seamlessly with AI code generation. See [SKILL.md](SKILL.md) for a complete technical reference including method signatures, all tags, and common patterns.

## Development

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Format
black src/ tests/
```

## Ecosystem

- **[nitro-cli](https://github.com/nitrosh/nitro-cli)** - Static site generator
- **[nitro-ui](https://github.com/nitrosh/nitro-ui)** - Programmatic HTML generation
- **[nitro-datastore](https://github.com/nitrosh/nitro-datastore)** - Data loading with dot notation access
- **[nitro-dispatch](https://github.com/nitrosh/nitro-dispatch)** - Plugin system
- **[nitro-validate](https://github.com/nitrosh/nitro-validate)** - Data validation

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.