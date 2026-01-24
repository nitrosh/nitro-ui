---
name: nitro-ui
description: Generate NitroUI code - a Python library for programmatic HTML generation using classes instead of templates
---

# NitroUI Skill Guide

**Quick reference for Claude to generate NitroUI code.**

## What is NitroUI?

A zero-dependency Python library for programmatic HTML generation. Build HTML with Python classes instead of string templates.

```python
from nitro_ui import Div, H1, Paragraph

page = Div(
    H1("Welcome"),
    Paragraph("Built with NitroUI"),
    class_name="container"
)
print(page.render())
# <div class="container"><h1>Welcome</h1><p>Built with NitroUI</p></div>
```

---

## Two Import Styles

### PascalCase (Traditional)
```python
from nitro_ui import Div, H1, Paragraph, UnorderedList, ListItem, Image
```

### Lowercase HTML-like (Looks like real HTML)
```python
from nitro_ui.html import div, h1, p, ul, li, img, a, table, tr, td

page = div(
    h1("Title"),
    p("This looks like HTML!"),
    ul(
        li(a("Home", href="/")),
        li(a("About", href="/about")),
    ),
    class_name="container"
)
```

### Python Keyword Conflicts (use trailing underscore)
```python
from nitro_ui.html import del_, input_, object_, map_

form_field = input_(type="text", name="username")  # <input>
deleted = del_("removed text")                      # <del>
```

---

## Element Constructor Pattern

All elements follow this pattern:

```python
Element(*children, **attributes)
```

- `*children`: HTMLElement instances, strings, or nested lists
- `**attributes`: HTML attributes as keyword arguments

**Special attribute mappings:**
- `class_name` → `class` (Python keyword workaround)
- `for_element` → `for` (Python keyword workaround)
- `data_*` → `data-*` (underscores become hyphens)

```python
div = Div(
    H1("Title"),
    "Some text",
    id="main",
    class_name="container",
    data_value="123"
)
# <div id="main" class="container" data-value="123"><h1>Title</h1>Some text</div>
```

---

## Quick Reference: All Tags

### Document Structure
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `HTML` | `html` | `<html>` (includes DOCTYPE) |
| `Head` | `head` | `<head>` |
| `Body` | `body` | `<body>` |
| `Title` | `title` | `<title>` |
| `Meta` | `meta` | `<meta>` |
| `Link` | `link` | `<link>` |
| `Script` | `script` | `<script>` |
| `Style` | `style` | `<style>` |

### Layout
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `Div` | `div` | `<div>` |
| `Section` | `section` | `<section>` |
| `Article` | `article` | `<article>` |
| `Header` | `header` | `<header>` |
| `Footer` | `footer` | `<footer>` |
| `Nav` | `nav` | `<nav>` |
| `Main` | `main` | `<main>` |
| `Aside` | `aside` | `<aside>` |
| `HorizontalRule` | `hr` | `<hr>` |

### Text
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `H1`-`H6` | `h1`-`h6` | `<h1>`-`<h6>` |
| `Paragraph` | `p` | `<p>` |
| `Span` | `span` | `<span>` |
| `Strong` | `strong` | `<strong>` |
| `Em` | `em` | `<em>` |
| `Bold` | `b` | `<b>` |
| `Italic` | `i` | `<i>` |
| `Underline` | `u` | `<u>` |
| `Strikethrough` | `s` | `<s>` |
| `Code` | `code` | `<code>` |
| `Pre` | `pre` | `<pre>` |
| `Href` | `a` | `<a>` |
| `Br` | `br` | `<br>` |
| `Del` | `del_` | `<del>` |

### Lists
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `UnorderedList` | `ul` | `<ul>` |
| `OrderedList` | `ol` | `<ol>` |
| `ListItem` | `li` | `<li>` |
| `DescriptionList` | `dl` | `<dl>` |
| `DescriptionTerm` | `dt` | `<dt>` |
| `DescriptionDetails` | `dd` | `<dd>` |

### Forms
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `Form` | `form` | `<form>` |
| `Input` | `input_` | `<input>` |
| `Button` | `button` | `<button>` |
| `Textarea` | `textarea` | `<textarea>` |
| `Select` | `select` | `<select>` |
| `Option` | `option` | `<option>` |
| `Label` | `label` | `<label>` |
| `Fieldset` | `fieldset` | `<fieldset>` |

### Tables
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `Table` | `table` | `<table>` |
| `TableRow` | `tr` | `<tr>` |
| `TableDataCell` | `td` | `<td>` |
| `TableHeaderCell` | `th` | `<th>` |
| `TableHeader` | `thead` | `<thead>` |
| `TableBody` | `tbody` | `<tbody>` |
| `TableFooter` | `tfoot` | `<tfoot>` |

### Media
| PascalCase | Lowercase | HTML Tag |
|------------|-----------|----------|
| `Image` | `img` | `<img>` |
| `Video` | `video` | `<video>` |
| `Audio` | `audio` | `<audio>` |
| `Figure` | `figure` | `<figure>` |
| `Figcaption` | `figcaption` | `<figcaption>` |
| `Canvas` | `canvas` | `<canvas>` |

---

## Key Methods (All Return `self` for Chaining)

### Adding/Removing Children
```python
element.append(child1, child2)      # Add to end
element.prepend(child1, child2)     # Add to start
element.clear()                      # Remove all children
element.pop(0)                       # Remove and return child at index
```

### Attributes
```python
element.add_attribute("id", "main")
element.add_attributes([("id", "main"), ("role", "button")])
element.get_attribute("id")          # Returns str or None
element.has_attribute("id")          # Returns bool
element.remove_attribute("id")
```

### Inline Styles
```python
element.add_style("color", "red")
element.add_styles({"color": "red", "padding": "10px"})
element.get_style("color")           # Returns str or None
element.remove_style("color")
```

### Querying
```python
element.count_children()             # Returns int
element.first()                      # First child or None
element.last()                       # Last child or None
element.find_by_attribute("id", "x") # Find descendant
element.filter(lambda e: e.tag == "p")  # Iterator of matching children
```

### Rendering
```python
element.render()                     # Compact HTML string
element.render(pretty=True)          # Indented HTML string
str(element)                         # Same as render()
```

### Serialization
```python
# To/from JSON
json_str = element.to_json(indent=2)
element = HTMLElement.from_json(json_str)

# To/from dict
data = element.to_dict()
element = HTMLElement.from_dict(data)

# Parse HTML string
element = from_html('<div class="x">Hello</div>')
elements = from_html('<p>One</p><p>Two</p>', fragment=True)  # List
```

### Utility
```python
element.clone()                      # Deep copy
element.generate_id()                # Add unique ID if none exists
```

---

## Fragment (No Wrapper Tag)

```python
from nitro_ui import Fragment, H1, Paragraph

# Renders children without wrapper
frag = Fragment(H1("Title"), Paragraph("Content"))
print(frag.render())
# <h1>Title</h1><p>Content</p>
```

---

## Styling System

### Inline Styles
```python
div = Div("Content")
div.add_style("color", "blue")
div.add_styles({"padding": "20px", "margin": "10px"})
```

### External StyleSheet
```python
from nitro_ui.styles import CSSStyle, StyleSheet, Theme

# Create stylesheet with theme
theme = Theme.modern()  # or Theme.classic(), Theme.minimal()
stylesheet = StyleSheet(theme=theme)

# Register CSS classes
btn = stylesheet.register("btn", CSSStyle(
    background_color="var(--color-primary)",
    color="white",
    padding="10px 20px",
    _hover=CSSStyle(background_color="var(--color-primary-dark)")
))

# Use in elements
button = Button("Click", class_name=btn)

# Generate CSS
css = stylesheet.render()
style_tag = stylesheet.to_style_tag()
```

### BEM Naming
```python
card = stylesheet.register_bem("card", style=CSSStyle(padding="20px"))
# Returns: "card"

header = stylesheet.register_bem("card", element="header", style=CSSStyle(font_weight="bold"))
# Returns: "card__header"

featured = stylesheet.register_bem("card", modifier="featured", style=CSSStyle(border="2px solid"))
# Returns: "card--featured"
```

### Responsive Breakpoints
```python
container = stylesheet.register("container", CSSStyle(
    padding="10px",
    _sm=CSSStyle(padding="15px"),  # 640px+
    _md=CSSStyle(padding="20px"),  # 768px+
    _lg=CSSStyle(padding="30px"),  # 1024px+
))
```

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
            class_name="container"
        )
    )
)
html = page.render(pretty=True)
```

### Navigation
```python
from nitro_ui.html import nav, ul, li, a

navbar = nav(
    ul(
        li(a("Home", href="/")),
        li(a("About", href="/about")),
        li(a("Contact", href="/contact")),
    ),
    class_name="navbar"
)
```

### Form
```python
from nitro_ui.html import form, label, input_, button, select, option

login_form = form(
    label("Email:", for_element="email"),
    input_(type="email", id="email", name="email", required=True),
    label("Password:", for_element="password"),
    input_(type="password", id="password", name="password", required=True),
    button("Log In", type="submit"),
    action="/login",
    method="post"
)
```

### Table from Data
```python
from nitro_ui.html import table, thead, tbody, tr, th, td

data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
]

t = table(
    thead(tr(th("Name"), th("Age"))),
    tbody(*[
        tr(td(row["name"]), td(str(row["age"])))
        for row in data
    ])
)
```

### Card Component
```python
from nitro_ui.html import div, h3, p, a

def card(title, content, link_url=None):
    children = [h3(title), p(content)]
    if link_url:
        children.append(a("Learn more", href=link_url))
    return div(*children, class_name="card")

# Usage
cards = div(
    card("Feature 1", "Description here", "/feature-1"),
    card("Feature 2", "Another description", "/feature-2"),
    class_name="card-grid"
)
```

### Dynamic List
```python
from nitro_ui.html import ul, li

items = ["Apple", "Banana", "Orange"]
list_element = ul(*[li(item) for item in items])
```

### Method Chaining
```python
container = (Div()
    .add_attribute("id", "hero")
    .add_styles({"background": "#f0f0f0", "padding": "2rem"})
    .append(H1("Welcome"))
    .append(Paragraph("Get started today.")))
```

### Custom Component Class
```python
from nitro_ui import HTMLElement, H2, Paragraph

class Card(HTMLElement):
    def __init__(self, title, content, **kwargs):
        super().__init__(tag="div", class_name="card", **kwargs)
        self.append(
            H2(title, class_name="card-title"),
            Paragraph(content, class_name="card-body")
        )

# Usage
card = Card("My Card", "Card content here", id="card-1")
```

---

## Security Notes

- **Automatic HTML escaping**: All text content and attribute values are escaped
- **CSS value validation**: Inline styles reject `javascript:`, `expression()`, etc.
- **CSS class validation**: StyleSheet rejects malicious class names
- **No raw HTML injection**: Cannot inject unescaped HTML (prevents XSS)

---

## Framework Integration

### FastAPI
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nitro_ui.html import html, head, body, title, h1

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return html(
        head(title("FastAPI + NitroUI")),
        body(h1("Hello!"))
    ).render()
```

### Flask
```python
from flask import Flask
from nitro_ui.html import html, head, body, title, h1

app = Flask(__name__)

@app.route("/")
def home():
    return html(
        head(title("Flask + NitroUI")),
        body(h1("Hello!"))
    ).render()
```

### Django
```python
from django.http import HttpResponse
from nitro_ui.html import html, head, body, title, h1

def home(request):
    page = html(
        head(title("Django + NitroUI")),
        body(h1("Hello!"))
    )
    return HttpResponse(page.render())
```

---

## Quick Checklist

When generating NitroUI code:

- [ ] Choose import style: PascalCase (`from nitro_ui import`) or lowercase (`from nitro_ui.html import`)
- [ ] Use `class_name` not `class` (Python keyword)
- [ ] Use `for_element` not `for` (Python keyword)
- [ ] Use `input_`, `del_`, `object_`, `map_` for Python conflicts
- [ ] Children go as positional args, attributes as keyword args
- [ ] Call `.render()` to get HTML string
- [ ] Use `pretty=True` for readable output during development
- [ ] All manipulation methods return `self` for chaining (except `replace_child`, `generate_id`)
- [ ] Use `Fragment` when you need multiple elements without a wrapper
