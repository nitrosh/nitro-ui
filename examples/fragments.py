"""Fragment examples for NitroUI.

This module demonstrates using Fragment to group elements
without adding a wrapper tag:
- Basic fragment usage
- Conditional rendering with fragments
- Returning multiple elements from functions
- List composition
- Fragment vs Div comparison
"""

from nitro_ui import *


def basic_fragment():
    """Basic Fragment usage."""
    print("=== Basic Fragment ===\n")

    # Without Fragment - adds a wrapper div
    with_wrapper = Div(H1("Title"), Paragraph("Content"))
    print("With wrapper (Div):")
    print(with_wrapper.render())

    # With Fragment - no wrapper tag
    without_wrapper = Fragment(H1("Title"), Paragraph("Content"))
    print("\nWithout wrapper (Fragment):")
    print(without_wrapper.render())


def fragment_in_parent():
    """Using Fragment within a parent element."""
    print("\n=== Fragment in Parent ===\n")

    # Fragment contents merge into parent
    container = Div(
        H1("Welcome"),
        Fragment(
            Paragraph("First paragraph"),
            Paragraph("Second paragraph"),
            Paragraph("Third paragraph"),
        ),
        Footer(Paragraph("Footer content")),
        class_name="container",
    )

    print("Fragment merged into parent:")
    print(container.render(pretty=True))


def conditional_rendering():
    """Conditional rendering with Fragment."""
    print("\n=== Conditional Rendering ===\n")

    def render_user_info(user, show_details=False):
        """Render user info, optionally with details."""
        content = Fragment()
        content.append(H2(user["name"]))

        if show_details:
            content.append(Paragraph(f"Email: {user['email']}"))
            content.append(Paragraph(f"Role: {user['role']}"))
            content.append(Paragraph(f"Status: {user['status']}"))
        else:
            content.append(Paragraph("Click to view details"))

        return content

    user = {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "Administrator",
        "status": "Active",
    }

    # Without details
    print("Without details:")
    card_simple = Div(
        render_user_info(user, show_details=False), class_name="user-card"
    )
    print(card_simple.render(pretty=True))

    # With details
    print("With details:")
    card_detailed = Div(
        render_user_info(user, show_details=True), class_name="user-card"
    )
    print(card_detailed.render(pretty=True))


def return_multiple_elements():
    """Returning multiple elements from functions."""
    print("\n=== Return Multiple Elements ===\n")

    def render_form_field(name, label_text, input_type="text", required=False):
        """Render a form field with label and input."""
        field_id = f"field-{name}"
        return Fragment(
            Label(label_text, for_element=field_id),
            Input(
                type=input_type,
                id=field_id,
                name=name,
                required="true" if required else None,
            ),
            Br(),
        )

    form = Form(
        render_form_field("username", "Username:", required=True),
        render_form_field("email", "Email:", input_type="email", required=True),
        render_form_field(
            "password", "Password:", input_type="password", required=True
        ),
        render_form_field("phone", "Phone (optional):", input_type="tel"),
        Button("Submit", type="submit"),
        action="/register",
        method="post",
    )

    print("Form with fragment-based fields:")
    print(form.render(pretty=True))


def list_composition():
    """Composing lists with fragments."""
    print("\n=== List Composition ===\n")

    def render_items(items, show_count=False):
        """Render a list of items, optionally with count."""
        fragment = Fragment()

        if show_count:
            fragment.append(Paragraph(f"Total: {len(items)} items"))

        for item in items:
            fragment.append(ListItem(item))

        return fragment

    items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

    # Render in an unordered list
    ul = UnorderedList(render_items(items, show_count=True))

    print("List with items from fragment:")
    print(ul.render(pretty=True))


def table_rows_fragment():
    """Using fragments for table rows."""
    print("\n=== Table Rows Fragment ===\n")

    def render_product_rows(products):
        """Render table rows for products."""
        fragment = Fragment()
        for product in products:
            row = TableRow(
                TableDataCell(product["name"]),
                TableDataCell(f"${product['price']:.2f}"),
                TableDataCell(product["stock"]),
            )
            fragment.append(row)
        return fragment

    products = [
        {"name": "Widget", "price": 9.99, "stock": "In Stock"},
        {"name": "Gadget", "price": 24.99, "stock": "Low Stock"},
        {"name": "Gizmo", "price": 14.99, "stock": "Out of Stock"},
    ]

    table = Table(
        TableHeader(
            TableRow(
                TableHeaderCell("Product"),
                TableHeaderCell("Price"),
                TableHeaderCell("Availability"),
            )
        ),
        TableBody(render_product_rows(products)),
    )

    print("Table with fragment rows:")
    print(table.render(pretty=True))


def nested_fragments():
    """Nested fragments."""
    print("\n=== Nested Fragments ===\n")

    def render_section(title, items):
        return Fragment(H3(title), UnorderedList(*[ListItem(item) for item in items]))

    def render_page_sections():
        return Fragment(
            render_section("Section 1", ["Item A", "Item B"]),
            render_section("Section 2", ["Item C", "Item D"]),
            render_section("Section 3", ["Item E", "Item F"]),
        )

    page = Div(
        H1("My Page"),
        render_page_sections(),
        Footer(Paragraph("End of page")),
        class_name="page",
    )

    print("Page with nested fragments:")
    print(page.render(pretty=True))


def fragment_with_text():
    """Fragment containing text content."""
    print("\n=== Fragment with Text ===\n")

    # Fragment can hold text alongside elements
    content = Fragment(
        "Some introductory text. ",
        Strong("Important note: "),
        "This is followed by more text.",
    )

    paragraph = Paragraph(content)
    print("Paragraph with fragment content:")
    print(paragraph.render())


def fragment_manipulation():
    """Manipulating fragment contents."""
    print("\n=== Fragment Manipulation ===\n")

    # Create a fragment
    fragment = Fragment(Paragraph("First"), Paragraph("Second"), Paragraph("Third"))

    print(f"Initial fragment children count: {fragment.count_children()}")
    print("Initial:")
    print(fragment.render())

    # Append to fragment
    fragment.append(Paragraph("Fourth"))

    # Prepend to fragment
    fragment.prepend(Paragraph("Zero"))

    print("\nAfter append and prepend:")
    print(fragment.render())

    # Clear fragment
    fragment.clear()
    print(f"\nAfter clear, children count: {fragment.count_children()}")


def fragment_vs_div():
    """Comparing Fragment and Div behavior."""
    print("\n=== Fragment vs Div Comparison ===\n")

    items = [Paragraph("Item 1"), Paragraph("Item 2"), Paragraph("Item 3")]

    # Using Div - adds wrapper
    div_wrapper = Div(*items, class_name="wrapper")
    print("Using Div (adds wrapper):")
    print(div_wrapper.render())
    print()

    # Using Fragment - no wrapper
    fragment_wrapper = Fragment(*items)
    print("Using Fragment (no wrapper):")
    print(fragment_wrapper.render())
    print()

    # Fragments are perfect when you don't want extra DOM nodes
    parent = Section(
        H2("Parent Section"),
        Fragment(Article(Paragraph("Article 1")), Article(Paragraph("Article 2"))),
    )
    print("Fragment inside parent (no extra nesting):")
    print(parent.render(pretty=True))


def reusable_fragment_components():
    """Creating reusable components that return fragments."""
    print("\n=== Reusable Fragment Components ===\n")

    def icon_button(icon, text, **kwargs):
        """Button with icon and text, no wrapper needed."""
        return Fragment(Span(icon, class_name="icon"), Span(text, class_name="text"))

    def stat_display(label, value, change=None):
        """Display a statistic with optional change indicator."""
        fragment = Fragment(
            Span(label, class_name="stat-label"),
            Span(str(value), class_name="stat-value"),
        )
        if change:
            sign = "+" if change > 0 else ""
            fragment.append(Span(f"{sign}{change}%", class_name="stat-change"))
        return fragment

    # Use in buttons
    btn1 = Button(icon_button("[x]", "Delete"), class_name="btn-danger")
    btn2 = Button(icon_button("[+]", "Add New"), class_name="btn-primary")

    print("Buttons with fragment content:")
    print(btn1.render())
    print(btn2.render())

    # Use in stats
    stats = Div(
        Div(stat_display("Users", "1,234", change=5), class_name="stat"),
        Div(stat_display("Revenue", "$5,678", change=-2), class_name="stat"),
        Div(stat_display("Orders", "89"), class_name="stat"),
        class_name="stats-container",
    )

    print("\nStats with fragment components:")
    print(stats.render(pretty=True))


def fragment_use_cases():
    """Summary of common Fragment use cases."""
    print("\n=== Fragment Use Cases ===\n")

    use_cases = [
        (
            "Conditional rendering",
            "Return content without wrapper when conditions are met",
        ),
        (
            "Multiple returns",
            "Return multiple elements from a function without extra nesting",
        ),
        ("List composition", "Build up collections of elements dynamically"),
        ("Table rows", "Return multiple <tr> elements for table bodies"),
        ("Component parts", "Return icon + text or label + input without wrapping"),
        (
            "Layout helpers",
            "Inject content into parents without affecting DOM structure",
        ),
    ]

    print("Common use cases for Fragment:")
    for name, description in use_cases:
        print(f"  - {name}: {description}")


if __name__ == "__main__":
    basic_fragment()
    fragment_in_parent()
    conditional_rendering()
    return_multiple_elements()
    list_composition()
    table_rows_fragment()
    nested_fragments()
    fragment_with_text()
    fragment_manipulation()
    fragment_vs_div()
    reusable_fragment_components()
    fragment_use_cases()
