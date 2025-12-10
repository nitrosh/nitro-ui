"""Method chaining examples for NitroUI.

This module demonstrates the fluent API design of NitroUI where methods
return self, enabling elegant chained operations:
- Chaining attribute methods
- Chaining style methods
- Chaining child manipulation methods
- Combining multiple chain types
"""

from nitro_ui import *


def basic_chaining():
    """Basic method chaining example."""
    print("=== Basic Method Chaining ===\n")

    # Build an element with chained methods
    container = (
        Div()
        .add_attribute("id", "main-container")
        .add_attribute("class", "wrapper")
        .add_style("background", "#fff")
        .add_style("padding", "20px")
        .append(H1("Welcome"))
        .append(Paragraph("This element was built with method chaining."))
    )

    print(container.render(pretty=True))


def chaining_attributes():
    """Chaining attribute operations."""
    print("\n=== Chaining Attributes ===\n")

    button = (
        Button("Submit")
        .add_attribute("type", "submit")
        .add_attribute("id", "submit-btn")
        .add_attributes(
            [
                ("class", "btn btn-primary"),
                ("data-loading", "false"),
                ("aria-label", "Submit form"),
            ]
        )
    )

    print("Button with chained attributes:")
    print(button.render())


def chaining_styles():
    """Chaining style operations."""
    print("\n=== Chaining Styles ===\n")

    # Build a styled card with chained style methods
    card = (
        Div("Card content")
        .add_style("background", "white")
        .add_style("border-radius", "8px")
        .add_styles(
            {
                "box-shadow": "0 2px 8px rgba(0,0,0,0.1)",
                "padding": "24px",
                "margin": "16px",
            }
        )
        .add_attribute("class", "card")
    )

    print("Card with chained styles:")
    print(card.render())
    print()

    # Modify and check styles
    card.add_style("border", "1px solid #eee")
    print(f"Has border style: {card.get_style('border')}")

    card.remove_style("margin")
    print(f"After removing margin:")
    print(card.render())


def chaining_children():
    """Chaining child manipulation methods."""
    print("\n=== Chaining Children ===\n")

    # Build a list with chained appends
    nav = (
        Nav()
        .add_attribute("class", "main-nav")
        .append(Link("Home", href="/"))
        .append(Link("Products", href="/products"))
        .append(Link("Services", href="/services"))
        .append(Link("About", href="/about"))
        .append(Link("Contact", href="/contact"))
    )

    print("Navigation built with chained appends:")
    print(nav.render(pretty=True))

    # Using prepend
    header = (
        Header().append(Paragraph("Welcome message")).prepend(H1("Site Title"))
    )  # H1 goes first

    print("Header with prepend:")
    print(header.render(pretty=True))


def complex_chaining():
    """Complex example combining multiple chain types."""
    print("\n=== Complex Chaining ===\n")

    # Build a complete card component in one chain
    product_card = (
        Div()
        .add_attribute("id", "product-123")
        .add_attribute("class", "product-card")
        .add_attributes([("data-product-id", "123"), ("data-category", "electronics")])
        .add_styles(
            {
                "background": "white",
                "border-radius": "12px",
                "box-shadow": "0 4px 12px rgba(0,0,0,0.1)",
                "overflow": "hidden",
                "transition": "transform 0.2s ease",
            }
        )
        .append(
            Image(src="/products/laptop.jpg", alt="Laptop Pro X1").add_styles(
                {"width": "100%", "height": "200px", "object-fit": "cover"}
            )
        )
        .append(
            Div(
                H3("Laptop Pro X1"),
                Paragraph("High-performance laptop for professionals"),
                Span("$1,299.00", class_name="price"),
            ).add_styles({"padding": "16px"})
        )
        .append(
            Div(
                Button("Add to Cart", class_name="btn-primary"),
                Button("Wishlist", class_name="btn-secondary"),
            ).add_styles(
                {
                    "padding": "16px",
                    "border-top": "1px solid #eee",
                    "display": "flex",
                    "gap": "8px",
                }
            )
        )
    )

    print("Complex product card:")
    print(product_card.render(pretty=True))


def chaining_with_removal():
    """Chaining including removal operations."""
    print("\n=== Chaining with Removal ===\n")

    # Create element with some items, then modify
    container = (
        Div()
        .add_attribute("class", "container")
        .add_attribute("data-temp", "will-be-removed")
        .add_style("margin", "10px")
        .add_style("padding", "20px")
        .add_style("will-remove", "yes")
        .append(Paragraph("Keep this"))
        .append(Div("Remove this", class_name="remove-me"))
        .append(Paragraph("Keep this too"))
    )

    print("Before removal:")
    print(container.render())
    print()

    # Chain removal operations
    container = (
        container.remove_attribute("data-temp")
        .remove_style("will-remove")
        .remove_all(lambda child: child.get_attribute("class_name") == "remove-me")
    )

    print("After removal chain:")
    print(container.render())


def conditional_chaining():
    """Conditional operations in chains."""
    print("\n=== Conditional Chaining ===\n")

    is_admin = True
    is_dark_mode = False

    # Build based on conditions
    header = Header()
    header.add_attribute("class", "site-header")

    if is_dark_mode:
        header.add_styles({"background": "#1a1a1a", "color": "#fff"})
    else:
        header.add_styles({"background": "#fff", "color": "#333"})

    header.append(H1("Dashboard"))

    if is_admin:
        header.append(
            Nav(
                Link("Users", href="/admin/users"),
                Link("Settings", href="/admin/settings"),
                class_name="admin-nav",
            )
        )

    print(f"Header (admin={is_admin}, dark_mode={is_dark_mode}):")
    print(header.render(pretty=True))


def builder_pattern():
    """Using chaining as a builder pattern."""
    print("\n=== Builder Pattern ===\n")

    def build_alert(message, alert_type="info", dismissible=False):
        """Build an alert component with builder-style chaining."""
        colors = {
            "info": {"bg": "#cce5ff", "border": "#004085", "text": "#004085"},
            "success": {"bg": "#d4edda", "border": "#155724", "text": "#155724"},
            "warning": {"bg": "#fff3cd", "border": "#856404", "text": "#856404"},
            "danger": {"bg": "#f8d7da", "border": "#721c24", "text": "#721c24"},
        }

        color = colors.get(alert_type, colors["info"])

        alert = (
            Div()
            .add_attribute("class", f"alert alert-{alert_type}")
            .add_attribute("role", "alert")
            .add_styles(
                {
                    "background-color": color["bg"],
                    "border": f"1px solid {color['border']}",
                    "color": color["text"],
                    "padding": "12px 16px",
                    "border-radius": "4px",
                    "margin-bottom": "16px",
                }
            )
            .append(Span(message))
        )

        if dismissible:
            alert.add_attribute("data-dismissible", "true")
            alert.append(
                Button("x", class_name="close-btn").add_styles(
                    {
                        "float": "right",
                        "background": "none",
                        "border": "none",
                        "cursor": "pointer",
                    }
                )
            )

        return alert

    # Build different alerts
    print("Info alert:")
    print(build_alert("This is an informational message.").render())

    print("\nSuccess alert (dismissible):")
    print(build_alert("Operation completed!", "success", dismissible=True).render())

    print("\nDanger alert:")
    print(build_alert("Something went wrong!", "danger").render())


def chainable_methods_reference():
    """Reference of all chainable methods."""
    print("\n=== Chainable Methods Reference ===\n")

    print("All these methods return 'self' for chaining:\n")

    methods = [
        ("append(*children)", "Add children at the end"),
        ("prepend(*children)", "Add children at the beginning"),
        ("add_attribute(key, value)", "Add single attribute"),
        ("add_attributes(list)", "Add multiple attributes"),
        ("remove_attribute(key)", "Remove an attribute"),
        ("add_style(key, value)", "Add single CSS style"),
        ("add_styles(dict)", "Add multiple CSS styles"),
        ("remove_style(key)", "Remove a CSS style"),
        ("clear()", "Remove all children"),
        ("remove_all(condition)", "Remove children matching condition"),
    ]

    for method, description in methods:
        print(f"  {method:<30} - {description}")


if __name__ == "__main__":
    basic_chaining()
    chaining_attributes()
    chaining_styles()
    chaining_children()
    complex_chaining()
    chaining_with_removal()
    conditional_chaining()
    builder_pattern()
    chainable_methods_reference()
