# Form Builder Design

## Overview

A declarative form field API that generates HTML5 form elements with validation attributes. Field functions return standard NitroUI elements, making them fully composable with the rest of the library.

**Goals:**
- Simple, NitroUI-like API using static methods on a `Field` class
- HTML5 validation only (no server-side validation in v1)
- Optional labels and wrappers for flexible layouts
- Full HTML5 input type coverage

## Basic API

```python
from nitro_ui import Form, Button
from nitro_ui.forms import Field

form = Form(
    Field.email("email", label="Email", required=True, placeholder="you@example.com"),
    Field.password("password", label="Password", min_length=8),
    Button("Log In", type="submit"),
    action="/login",
    method="post"
)
```

**Renders:**

```html
<form action="/login" method="post">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required placeholder="you@example.com">
    <label for="password">Password</label>
    <input type="password" id="password" name="password" minlength="8">
    <button type="submit">Log In</button>
</form>
```

## Field Types

### Text Inputs

```python
Field.text(name, label=None, required=False, min_length=None, max_length=None, pattern=None, placeholder=None, value=None, **attrs)
Field.email(name, label=None, required=False, placeholder=None, value=None, **attrs)
Field.password(name, label=None, required=False, min_length=None, max_length=None, placeholder=None, **attrs)
Field.url(name, label=None, required=False, placeholder=None, value=None, **attrs)
Field.tel(name, label=None, required=False, pattern=None, placeholder=None, value=None, **attrs)
Field.search(name, label=None, required=False, placeholder=None, value=None, **attrs)
Field.textarea(name, label=None, required=False, rows=None, cols=None, min_length=None, max_length=None, placeholder=None, value=None, **attrs)
```

### Numeric

```python
Field.number(name, label=None, required=False, min=None, max=None, step=None, value=None, **attrs)
Field.range(name, label=None, min=0, max=100, step=None, value=None, **attrs)
```

### Date/Time

```python
Field.date(name, label=None, required=False, min=None, max=None, value=None, **attrs)
Field.time(name, label=None, required=False, min=None, max=None, value=None, **attrs)
Field.datetime_local(name, label=None, required=False, min=None, max=None, value=None, **attrs)
```

### Selection

```python
Field.select(name, options, label=None, required=False, value=None, **attrs)
Field.checkbox(name, label=None, checked=False, value="on", **attrs)
Field.radio(name, options, label=None, required=False, value=None, **attrs)
```

### Other

```python
Field.file(name, label=None, required=False, accept=None, multiple=False, **attrs)
Field.hidden(name, value, **attrs)
Field.color(name, label=None, value=None, **attrs)
```

## Label Behavior

**Without label:**
```python
Field.email("email", required=True)
# <input type="email" id="email" name="email" required>
```

**With label:**
```python
Field.email("email", label="Email Address", required=True)
# <label for="email">Email Address</label>
# <input type="email" id="email" name="email" required>
```

**With wrapper:**
```python
Field.email("email", label="Email", required=True, wrapper="field")
# <div class="field">
#     <label for="email">Email</label>
#     <input type="email" id="email" name="email" required>
# </div>

Field.email("email", label="Email", wrapper={"cls": "form-group", "id": "email-field"})
# <div class="form-group" id="email-field">...</div>
```

**Custom ID:**
```python
Field.email("user_email", id="email-input", label="Email")
# <label for="email-input">Email</label>
# <input type="email" id="email-input" name="user_email">
```

## Select Options

Three formats supported:

```python
# Simple list
Field.select("country", ["USA", "Canada", "Mexico"])

# Tuples (value, label)
Field.select("status", [("active", "Active"), ("inactive", "Inactive")])

# Dicts (full control)
Field.select("priority", [
    {"value": "1", "label": "Low"},
    {"value": "2", "label": "Medium", "disabled": True}
])
```

## Radio Buttons

```python
Field.radio("plan", [
    ("free", "Free"),
    ("pro", "Pro - $10/mo")
], label="Plan", value="free")
```

**Renders:**
```html
<fieldset>
    <legend>Plan</legend>
    <label><input type="radio" name="plan" value="free" checked> Free</label>
    <label><input type="radio" name="plan" value="pro"> Pro - $10/mo</label>
</fieldset>
```

## Checkbox

```python
Field.checkbox("subscribe", label="Subscribe to newsletter", checked=True)
# <label><input type="checkbox" name="subscribe" value="on" checked> Subscribe to newsletter</label>
```

## File Structure

```
src/nitro_ui/
├── forms/
│   ├── __init__.py    # exports Field
│   └── field.py       # Field class with static methods
```

## Export

```python
from nitro_ui import Field
from nitro_ui.forms import Field  # alternative
```
