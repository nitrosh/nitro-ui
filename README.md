# NitroUI

**Build HTML with Python, not strings.**

NitroUI is a zero-dependency Python library that lets you construct HTML documents using a clean, composable class-based API. No template files, no string concatenation, no runtime dependencies.

```python
from nitro_ui import *

page = HTML(
    Head(Title("Dashboard")),
    Body(
        Nav(
            Link("Home", href="/"),
            Link("Settings", href="/settings", cls="active")
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

### HTML-like Syntax

Prefer lowercase tag names that look like real HTML? Use `nitro_ui.html`:

```python
from nitro_ui.html import div, h1, p, ul, li, a, img

page = div(
    h1("Welcome"),
    p("This looks just like HTML!"),
    ul(
        li(a("Home", href="/")),
        li(a("About", href="/about")),
    ),
    img(src="hero.jpg", alt="Hero image"),
    cls="container"
)
```

All standard HTML tags are available as lowercase functions. Python keywords use a trailing underscore: `del_`, `input_`, `object_`, `map_`.

### Dynamic Content

```python
from nitro_ui import *

def render_user_card(user):
    return Div(
        Image(src=user["avatar"], alt=user["name"]),
        H3(user["name"]),
        Paragraph(user["bio"]),
        Link("View Profile", href=f"/users/{user['id']}"),
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

class Card(HTMLElement):
    def __init__(self, title, *children, **kwargs):
        super().__init__(**{**kwargs, "tag": "div"})
        self.add_attribute("class", "card")
        self.append(H3(title, cls="card-title"))
        for child in children:
            self.append(child)

class Alert(HTMLElement):
    def __init__(self, message, variant="info", **kwargs):
        super().__init__(**{**kwargs, "tag": "div"})
        self.add_attributes([("class", f"alert alert-{variant}"), ("role", "alert")])
        self.append(Paragraph(message))

# Usage
page = Div(
    Alert("Your changes have been saved.", variant="success"),
    Card("Statistics",
        Paragraph("Total users: 1,234"),
        Paragraph("Active today: 89")
    )
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

**PascalCase imports** (`from nitro_ui import *`):

| Module                 | Elements                                                                |
|------------------------|-------------------------------------------------------------------------|
| `nitro_ui.tags.html`   | HTML, Head, Body, Title, Meta, Script, Style, HtmlLink, IFrame          |
| `nitro_ui.tags.layout` | Div, Section, Article, Header, Nav, Footer, Main, Aside, Dialog         |
| `nitro_ui.tags.text`   | H1-H6, Paragraph, Span, Strong, Em, Link, Code, Pre, Blockquote         |
| `nitro_ui.tags.form`   | Form, Input, Button, Select, Option, Textarea, Label, Fieldset          |
| `nitro_ui.tags.lists`  | UnorderedList, OrderedList, ListItem, DescriptionList                   |
| `nitro_ui.tags.media`  | Image, Video, Audio, Figure, Canvas, Picture, Source                    |
| `nitro_ui.tags.table`  | Table, TableRow, TableHeader, TableBody, TableHeaderCell, TableDataCell |

**Lowercase HTML-like imports** (`from nitro_ui.html import *`):

| Category | Aliases                                                              |
|----------|----------------------------------------------------------------------|
| Document | `html`, `head`, `body`, `title`, `meta`, `script`, `style`, `link`   |
| Layout   | `div`, `section`, `article`, `header`, `nav`, `footer`, `main`, `hr` |
| Text     | `h1`-`h6`, `p`, `span`, `strong`, `em`, `a`, `code`, `pre`, `b`, `i` |
| Form     | `form`, `input_`, `button`, `select`, `option`, `textarea`, `label`  |
| Lists    | `ul`, `ol`, `li`, `dl`, `dt`, `dd`                                   |
| Media    | `img`, `video`, `audio`, `figure`, `canvas`, `picture`, `source`     |
| Table    | `table`, `tr`, `td`, `th`, `thead`, `tbody`, `tfoot`                 |

*Note: `input_`, `del_`, `object_`, `map_` use trailing underscore to avoid Python keyword/builtin conflicts.*

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

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Links

- [Author](https://github.com/sn)
- [PyPI](https://pypi.org/project/nitro-ui/)
- [GitHub](https://github.com/sn/nitro-ui)
- [Skill Guide](SKILL.md)