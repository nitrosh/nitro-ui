"""Attributes and inline styles examples for NitroUI.

This module demonstrates how to work with HTML attributes and CSS styles:
- Adding attributes via constructor
- Adding/removing attributes after creation
- Working with inline CSS styles
- Special attribute handling (class_name, for_element)
"""

from nitro_ui import *


def constructor_attributes():
    """Adding attributes via the constructor."""
    print("=== Constructor Attributes ===\n")

    # Basic attributes
    div = Div(
        "Content here",
        id="main-content",
        class_name="container wrapper",
        data_page="home",
        data_user_id="123",
    )
    print("Basic attributes:")
    print(div.render())
    print()

    # Input with multiple attributes
    input_field = Input(
        type="email",
        name="user_email",
        placeholder="Enter your email",
        required="true",
        autocomplete="email",
    )
    print("Input with attributes:")
    print(input_field.render())
    print()

    # Link with target and rel
    link = Link(
        "External Link",
        href="https://example.com",
        target="_blank",
        rel="noopener noreferrer",
    )
    print("Link with security attributes:")
    print(link.render())


def add_attributes_after_creation():
    """Adding attributes after element creation."""
    print("\n=== Add Attributes After Creation ===\n")

    div = Div("Content")

    # Add single attribute
    div.add_attribute("id", "my-div")
    div.add_attribute("class", "container")
    div.add_attribute("data-testid", "main-container")

    print("After add_attribute():")
    print(div.render())
    print()

    # Add multiple attributes at once
    span = Span("Text")
    span.add_attributes(
        [
            ("id", "my-span"),
            ("class", "highlight"),
            ("role", "alert"),
            ("aria-live", "polite"),
        ]
    )

    print("After add_attributes():")
    print(span.render())


def attribute_operations():
    """Getting, checking, and removing attributes."""
    print("\n=== Attribute Operations ===\n")

    element = Div("Content", id="test", class_name="container", data_value="123")

    # Check if attribute exists
    print(f"Has 'id' attribute: {element.has_attribute('id')}")
    print(f"Has 'title' attribute: {element.has_attribute('title')}")

    # Get attribute value
    print(f"id value: {element.get_attribute('id')}")
    print(f"class value: {element.get_attribute('class_name')}")

    # Get multiple attributes
    attrs = element.get_attributes("id", "class_name")
    print(f"Multiple attributes: {attrs}")

    # Remove attribute
    element.remove_attribute("data-value")
    print(f"\nAfter removing data-value:")
    print(element.render())


def inline_styles():
    """Working with inline CSS styles."""
    print("\n=== Inline Styles ===\n")

    div = Div("Styled content")

    # Add single style
    div.add_style("color", "blue")
    div.add_style("font-size", "16px")

    print("After add_style():")
    print(div.render())
    print()

    # Add multiple styles at once
    div.add_styles(
        {
            "background-color": "#f0f0f0",
            "padding": "20px",
            "margin": "10px",
            "border-radius": "5px",
        }
    )

    print("After add_styles():")
    print(div.render())
    print()

    # Get a specific style value
    color = div.get_style("color")
    print(f"Color value: {color}")

    # Remove a style
    div.remove_style("margin")
    print(f"\nAfter removing margin:")
    print(div.render())


def styled_components():
    """Building styled components."""
    print("\n=== Styled Components ===\n")

    # Card component with styles
    card = Div(
        H3("Card Title"), Paragraph("Card content goes here."), class_name="card"
    ).add_styles(
        {
            "background": "white",
            "border-radius": "8px",
            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "padding": "20px",
            "margin": "16px",
        }
    )

    print("Styled card:")
    print(card.render(pretty=True))

    # Alert component
    alert = Div(
        Strong("Warning!"),
        " This action cannot be undone.",
        class_name="alert alert-warning",
    ).add_styles(
        {
            "background-color": "#fff3cd",
            "border": "1px solid #ffc107",
            "border-radius": "4px",
            "padding": "12px 16px",
            "color": "#856404",
        }
    )

    print("Styled alert:")
    print(alert.render())


def special_attributes():
    """Special attribute handling (class_name, for_element)."""
    print("\n=== Special Attributes ===\n")

    # class_name becomes class in HTML (Python keyword workaround)
    div = Div("Content", class_name="my-class another-class")
    print("class_name -> class:")
    print(div.render())
    print()

    # for_element becomes for in HTML (Python keyword workaround)
    label = Label("Email:", for_element="email-input")
    input_el = Input(type="email", id="email-input", name="email")
    form_group = Div(label, input_el, class_name="form-group")

    print("for_element -> for:")
    print(form_group.render(pretty=True))


def aria_attributes():
    """Working with ARIA accessibility attributes."""
    print("\n=== ARIA Attributes ===\n")

    # Button with ARIA attributes
    button = Button(
        "Open Menu",
        aria_expanded="false",
        aria_controls="dropdown-menu",
        aria_haspopup="true",
    )
    print("Button with ARIA:")
    print(button.render())
    print()

    # Navigation with ARIA landmark
    nav = Nav(
        Link("Home", href="/"),
        Link("About", href="/about"),
        aria_label="Main navigation",
        role="navigation",
    )
    print("Navigation with ARIA:")
    print(nav.render())
    print()

    # Alert with live region
    alert = Div(
        "Form submitted successfully!",
        role="alert",
        aria_live="polite",
        aria_atomic="true",
    )
    print("Alert with live region:")
    print(alert.render())


def data_attributes():
    """Working with data-* attributes."""
    print("\n=== Data Attributes ===\n")

    # Element with data attributes (underscores become hyphens)
    element = Div(
        "Interactive element",
        data_action="toggle",
        data_target="#modal",
        data_user_id="12345",
        data_config='{"theme": "dark", "size": "large"}',
    )

    print("Element with data-* attributes:")
    print(element.render())
    print()

    # Product card with data for JavaScript
    product = Div(
        Image(src="/products/widget.jpg", alt="Widget"),
        H3("Widget Pro"),
        Paragraph("$99.99"),
        Button("Add to Cart", class_name="add-to-cart"),
        class_name="product-card",
        data_product_id="SKU-123",
        data_price="99.99",
        data_category="electronics",
    )

    print("Product card with data attributes:")
    print(product.render(pretty=True))


def boolean_attributes():
    """Working with boolean HTML attributes."""
    print("\n=== Boolean Attributes ===\n")

    # Form elements with boolean attributes
    form = Form(
        Div(
            Input(type="text", name="username", required="true", autofocus="true"),
            class_name="form-group",
        ),
        Div(
            Input(type="checkbox", name="remember", checked="true"),
            Label("Remember me", for_element="remember"),
            class_name="form-group",
        ),
        Div(
            Input(
                type="text", name="readonly_field", value="Cannot edit", readonly="true"
            ),
            class_name="form-group",
        ),
        Div(
            Input(
                type="text", name="disabled_field", value="Disabled", disabled="true"
            ),
            class_name="form-group",
        ),
        Button("Submit", type="submit"),
        action="/submit",
        method="post",
    )

    print("Form with boolean attributes:")
    print(form.render(pretty=True))


if __name__ == "__main__":
    constructor_attributes()
    add_attributes_after_creation()
    attribute_operations()
    inline_styles()
    styled_components()
    special_attributes()
    aria_attributes()
    data_attributes()
    boolean_attributes()
