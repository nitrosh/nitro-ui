"""Basic usage examples for NitroUI.

This module demonstrates the fundamental concepts of building HTML with NitroUI:
- Creating elements with text content
- Nesting elements
- Adding attributes
- Rendering HTML (compact and pretty)
"""

from nitro_ui import *


def hello_world():
    """The simplest possible NitroUI example."""
    print("=== Hello World ===\n")

    page = HTML(
        Head(Title("Hello World")),
        Body(H1("Hello, World!"), Paragraph("Welcome to NitroUI.")),
    )

    print(page.render(pretty=True))


def document_structure():
    """Building a complete HTML document with head metadata."""
    print("\n=== Document Structure ===\n")

    page = HTML(
        Head(
            Title("My Website"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Meta(name="description", content="A website built with NitroUI"),
            HtmlLink(rel="stylesheet", href="/css/styles.css"),
            HtmlLink(rel="icon", href="/favicon.ico"),
            Script(src="/js/main.js", defer="true"),
        ),
        Body(
            Header(
                Nav(
                    Link("Home", href="/"),
                    Link("About", href="/about"),
                    Link("Contact", href="/contact"),
                )
            ),
            Main(H1("Welcome"), Paragraph("This is the main content area.")),
            Footer(Paragraph("Copyright 2025")),
        ),
    )

    print(page.render(pretty=True))


def text_elements():
    """Demonstrating various text elements."""
    print("\n=== Text Elements ===\n")

    content = Div(
        H1("Main Heading"),
        H2("Subheading"),
        H3("Section Title"),
        Paragraph(
            "This is a paragraph with ",
            Strong("bold text"),
            ", ",
            Em("italic text"),
            ", and ",
            Code("inline code"),
            ".",
        ),
        Paragraph(
            "You can also use ",
            Mark("highlighted text"),
            ", ",
            Del("deleted text"),
            ", ",
            Ins("inserted text"),
            ", and ",
            Link("hyperlinks", href="https://example.com"),
            ".",
        ),
        Blockquote(
            Paragraph("This is a blockquote. It's great for quotes and callouts."),
            cite="https://example.com",
        ),
        Pre(Code("def hello():\n    print('Hello, World!')")),
        Paragraph(
            "Keyboard shortcuts: Press ", Kbd("Ctrl"), " + ", Kbd("C"), " to copy."
        ),
        Paragraph("Mathematical: x", Superscript("2"), " + y", Subscript("1"), " = z"),
        Paragraph(
            Abbr("HTML", title="HyperText Markup Language"),
            " is the standard markup language for web pages.",
        ),
    )

    print(content.render(pretty=True))


def layout_elements():
    """Demonstrating layout and structural elements."""
    print("\n=== Layout Elements ===\n")

    page = Div(
        Header(
            H1("Site Title"),
            Nav(
                Link("Home", href="/"),
                Link("Products", href="/products"),
                Link("About", href="/about"),
            ),
        ),
        Main(
            Article(
                Header(H2("Article Title")),
                Section(
                    H3("Introduction"), Paragraph("This is the introduction section.")
                ),
                Section(
                    H3("Main Content"), Paragraph("This is the main content section.")
                ),
                Footer(
                    Paragraph(
                        "Published on ", Time("2025-01-15", datetime="2025-01-15")
                    )
                ),
            ),
            Aside(
                H3("Related Links"),
                UnorderedList(
                    ListItem(Link("Link 1", href="#")),
                    ListItem(Link("Link 2", href="#")),
                    ListItem(Link("Link 3", href="#")),
                ),
            ),
        ),
        Footer(Paragraph("Footer content"), HorizontalRule()),
    )

    print(page.render(pretty=True))


def list_elements():
    """Demonstrating list elements."""
    print("\n=== List Elements ===\n")

    content = Div(
        H2("Unordered List"),
        UnorderedList(
            ListItem("Apple"),
            ListItem("Banana"),
            ListItem("Cherry"),
            ListItem(
                "Nested list:",
                UnorderedList(ListItem("Sub-item 1"), ListItem("Sub-item 2")),
            ),
        ),
        H2("Ordered List"),
        OrderedList(
            ListItem("First step"), ListItem("Second step"), ListItem("Third step")
        ),
        H2("Description List"),
        DescriptionList(
            DescriptionTerm("HTML"),
            DescriptionDetails("HyperText Markup Language"),
            DescriptionTerm("CSS"),
            DescriptionDetails("Cascading Style Sheets"),
            DescriptionTerm("JS"),
            DescriptionDetails("JavaScript"),
        ),
    )

    print(content.render(pretty=True))


def compact_vs_pretty():
    """Showing the difference between compact and pretty output."""
    print("\n=== Compact vs Pretty Output ===\n")

    page = Div(H1("Hello"), Paragraph("World"), class_name="container")

    print("Compact output:")
    print(page.render())
    print()

    print("Pretty output:")
    print(page.render(pretty=True))


def dynamic_content():
    """Building HTML dynamically based on data."""
    print("\n=== Dynamic Content ===\n")

    # Sample data
    products = [
        {"name": "Laptop", "price": 999.99, "in_stock": True},
        {"name": "Mouse", "price": 29.99, "in_stock": True},
        {"name": "Keyboard", "price": 79.99, "in_stock": False},
    ]

    # Build product cards dynamically
    product_list = Div(class_name="products")

    for product in products:
        stock_status = "In Stock" if product["in_stock"] else "Out of Stock"
        stock_class = "stock-available" if product["in_stock"] else "stock-unavailable"

        card = Div(
            H3(product["name"]),
            Paragraph(f"${product['price']:.2f}"),
            Span(stock_status, class_name=stock_class),
            class_name="product-card",
        )
        product_list.append(card)

    print(product_list.render(pretty=True))


def conditional_rendering():
    """Conditional content based on variables."""
    print("\n=== Conditional Rendering ===\n")

    user = {"name": "Alice", "is_admin": True, "notifications": 3}

    # Build header based on user state
    header = Header()
    header.append(H1(f"Welcome, {user['name']}"))

    if user["is_admin"]:
        header.append(
            Nav(
                Link("Dashboard", href="/dashboard"),
                Link("Users", href="/users"),
                Link("Settings", href="/settings"),
                class_name="admin-nav",
            )
        )

    if user["notifications"] > 0:
        header.append(
            Div(
                Span(f"{user['notifications']} new notifications"),
                class_name="notification-badge",
            )
        )

    print(header.render(pretty=True))


if __name__ == "__main__":
    hello_world()
    document_structure()
    text_elements()
    layout_elements()
    list_elements()
    compact_vs_pretty()
    dynamic_content()
    conditional_rendering()
