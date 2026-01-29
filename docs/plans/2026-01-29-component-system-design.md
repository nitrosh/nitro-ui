# Component System Design

## Overview

A declarative, class-based system for building reusable components in NitroUI. Addresses four pain points with the current approach:

1. **Too much boilerplate** — No more `super().__init__(**{**kwargs, "tag": "div"})`
2. **Unclear structure** — Declarative template instead of imperative `append()` calls
3. **Props vs attributes confusion** — Clear separation between component props, slots, and HTML attributes
4. **No enforced pattern** — Consistent `Component` base class for all custom components

## Basic Structure

### Component Base Class

```python
class Component(HTMLElement):
    """Base class for reusable components."""

    tag: str = "div"              # Root element tag
    class_name: str = None        # Default CSS class(es)

    def template(self) -> list:
        """Override to define component structure. Return list of children."""
        return [Slot()]           # Default: just render children
```

### Simple Component Example

```python
class Card(Component):
    tag = "div"
    class_name = "card"

    def template(self, title: str):
        return [
            H3(title, cls="card-title"),
            Slot()  # children go here
        ]
```

### Usage

```python
Card("My Title",
    Paragraph("Some content"),
    Button("Click me"),
    id="card-1",
    class_name="highlighted"
)
```

### Rendered Output

```html
<div class="card highlighted" id="card-1">
    <h3 class="card-title">My Title</h3>
    <p>Some content</p>
    <button>Click me</button>
</div>
```

## Named Slots

### Defining Slots in Template

```python
class Modal(Component):
    tag = "div"
    class_name = "modal"

    def template(self, title: str):
        return [
            Div(
                H2(title),
                Slot("actions"),              # named slot
                cls="modal-header"
            ),
            Div(Slot(), cls="modal-body"),    # default slot (unnamed)
            Div(Slot("footer"), cls="modal-footer")
        ]
```

### Using Named Slots

Named slots are passed via kwargs:

```python
Modal("Confirm Delete",
    Paragraph("Are you sure?"),           # → default slot
    actions=CloseButton(),                # → "actions" slot
    footer=[Button("Cancel"), Button("Delete", cls="danger")]
)
```

### Rendered Output

```html
<div class="modal">
    <div class="modal-header">
        <h2>Confirm Delete</h2>
        <button class="close">×</button>
    </div>
    <div class="modal-body">
        <p>Are you sure?</p>
    </div>
    <div class="modal-footer">
        <button>Cancel</button>
        <button class="danger">Delete</button>
    </div>
</div>
```

### Slot Rules

- `Slot()` — default slot, receives unwrapped `*children`
- `Slot("name")` — named slot, receives `name=` kwarg
- Named slot kwargs accept single element or list
- Empty slots render nothing (slot marker disappears)
- Component can have zero or one default slot, unlimited named slots

## Props vs HTML Attributes

### Resolution Order for kwargs

1. **Slot names** — if kwarg matches a `Slot("name")` in template → slot content
2. **Template params** — if kwarg matches a `template()` parameter → prop
3. **Otherwise** — HTML attribute on root element

### Example with All Three

```python
class Alert(Component):
    tag = "div"
    class_name = "alert"

    def template(self, message: str, level: str = "info"):
        return [
            Slot("icon"),
            Span(message),
            Slot("actions")
        ]

Alert("Saved!",
    level="success",              # prop (template param)
    icon=CheckIcon(),             # slot
    actions=CloseButton(),        # slot
    role="alert",                 # HTML attr
    id="notif-1"                  # HTML attr
)
```

## Class Name Merging

Default classes merge with user-provided classes (append behavior):

```python
class Card(Component):
    class_name = "card"

Card("Title", class_name="highlighted")
# → <div class="card highlighted">...</div>
```

## The Slot Class

### Implementation

```python
class Slot(HTMLElement):
    """Marker for where content should be inserted."""

    def __init__(self, name: str = None, default=None):
        self.name = name      # None = default slot
        self.default = default  # fallback content if slot not provided
```

### Slot with Default Content

```python
Slot("footer", default=Button("Close"))
# Uses default if no footer= provided
```

### Edge Cases

```python
# No slot defined — children append at end
class Simple(Component):
    def template(self, label: str):
        return [Span(label)]

Simple("Hi", Paragraph("extra"))
# → <div><span>Hi</span><p>extra</p></div>

# Empty slot — renders nothing (empty container)
Modal("Title")  # no footer= provided
# → <div class="modal-footer"></div>

# None in template — filtered out
def template(self, title: str, show_close: bool = False):
    return [
        CloseButton() if show_close else None,  # filtered when False
        H2(title),
        Slot()
    ]
```

## File Structure

```
src/nitro_ui/
├── core/
│   ├── element.py      # existing
│   ├── fragment.py     # existing
│   ├── component.py    # NEW — Component base class
│   └── slot.py         # NEW — Slot class
```

## Public API

New exports from `nitro_ui`:

```python
from nitro_ui import Component, Slot
```

## Full API Summary

```python
class MyComponent(Component):
    # Class attributes (all optional)
    tag: str = "div"           # default root tag
    class_name: str = None     # default CSS class(es)

    # Override to define structure
    def template(self, prop1, prop2="default") -> list:
        return [
            H2(prop1),
            Slot("header"),                           # named slot
            Div(Slot(), cls="content"),               # default slot
            Slot("footer", default=Button("Close"))   # slot with default
        ]

    # Lifecycle hooks (inherited from HTMLElement)
    def on_load(self): ...
    def on_before_render(self): ...
    def on_after_render(self): ...
```

## Usage Patterns

```python
# Minimal
Card("Title", Paragraph("body"))

# With named slots
Modal("Title", Paragraph("body"), footer=Button("OK"))

# With HTML attributes
Card("Title", Paragraph("body"), id="main", class_name="featured")

# With props
Alert("Message", level="warning", dismissible=True)
```
