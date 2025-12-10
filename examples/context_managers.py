"""Context manager examples for NitroUI.

This module demonstrates using elements as context managers
for cleaner, more intuitive nesting:
- Basic context manager usage
- Nested context managers
- Building complex structures
- Comparison with regular nesting
"""

from nitro_ui import *


def basic_context_manager():
    """Basic context manager usage."""
    print("=== Basic Context Manager ===\n")

    # Using context manager
    with Div(id="container", class_name="main") as container:
        container.append(H1("Welcome"))
        container.append(Paragraph("This is the first paragraph."))
        container.append(Paragraph("This is the second paragraph."))

    print("Built with context manager:")
    print(container.render(pretty=True))


def nested_context_managers():
    """Nested context managers for complex structures."""
    print("\n=== Nested Context Managers ===\n")

    with Div(id="page", class_name="page-wrapper") as page:
        with Header(class_name="site-header") as header:
            header.append(H1("My Website"))
            with Nav(class_name="main-nav") as nav:
                nav.append(Link("Home", href="/"))
                nav.append(Link("About", href="/about"))
                nav.append(Link("Contact", href="/contact"))
            header.append(nav)
        page.append(header)

        with Main(class_name="content") as main:
            with Article(class_name="post") as article:
                article.append(H2("Article Title"))
                article.append(Paragraph("Article content goes here."))
            main.append(article)
        page.append(main)

        with Footer(class_name="site-footer") as footer:
            footer.append(Paragraph("Copyright 2025"))
        page.append(footer)

    print("Built with nested context managers:")
    print(page.render(pretty=True))


def comparison_with_regular():
    """Comparing context managers with regular nesting."""
    print("\n=== Comparison: Context Manager vs Regular ===\n")

    # Regular nesting (constructor-based)
    regular = Div(
        Header(H1("Title"), Nav(Link("Home", href="/"), Link("About", href="/about"))),
        Main(Article(H2("Article"), Paragraph("Content"))),
        Footer(Paragraph("Footer")),
        id="regular",
    )

    print("Regular nesting:")
    print(regular.render(pretty=True))

    # Context manager approach
    with Div(id="context") as context:
        with Header() as header:
            header.append(H1("Title"))
            with Nav() as nav:
                nav.append(Link("Home", href="/"))
                nav.append(Link("About", href="/about"))
            header.append(nav)
        context.append(header)

        with Main() as main:
            with Article() as article:
                article.append(H2("Article"))
                article.append(Paragraph("Content"))
            main.append(article)
        context.append(main)

        with Footer() as footer:
            footer.append(Paragraph("Footer"))
        context.append(footer)

    print("\nContext manager nesting:")
    print(context.render(pretty=True))

    print(
        "\n(Output is identical, but context managers can be clearer for dynamic content)"
    )


def dynamic_content_with_context():
    """Using context managers with dynamic content."""
    print("\n=== Dynamic Content with Context Managers ===\n")

    users = [
        {"name": "Alice", "role": "Admin"},
        {"name": "Bob", "role": "User"},
        {"name": "Charlie", "role": "User"},
    ]

    with Div(class_name="user-list") as user_list:
        user_list.append(H2("Users"))

        with UnorderedList() as ul:
            for user in users:
                with ListItem() as li:
                    li.append(Strong(user["name"]))
                    li.append(Span(f" - {user['role']}"))
                    if user["role"] == "Admin":
                        li.add_style("font-weight", "bold")
                ul.append(li)
        user_list.append(ul)

    print("Dynamic list with context managers:")
    print(user_list.render(pretty=True))


def conditional_with_context():
    """Conditional rendering with context managers."""
    print("\n=== Conditional Rendering ===\n")

    is_logged_in = True
    is_admin = True
    has_notifications = True
    notification_count = 5

    with Header(class_name="app-header") as header:
        header.append(H1("Dashboard"))

        with Nav(class_name="user-nav") as nav:
            if is_logged_in:
                nav.append(Link("Profile", href="/profile"))
                nav.append(Link("Settings", href="/settings"))

                if is_admin:
                    nav.append(Link("Admin Panel", href="/admin"))

                nav.append(Link("Logout", href="/logout"))
            else:
                nav.append(Link("Login", href="/login"))
                nav.append(Link("Sign Up", href="/signup"))

        header.append(nav)

        if is_logged_in and has_notifications:
            with Div(class_name="notifications") as notif:
                notif.append(Span(f"{notification_count} new notifications"))
            header.append(notif)

    print("Conditional header:")
    print(header.render(pretty=True))


def building_forms_with_context():
    """Building forms using context managers."""
    print("\n=== Building Forms ===\n")

    with Form(action="/submit", method="post") as form:
        with Fieldset() as personal:
            personal.append(Legend("Personal Information"))

            with Div(class_name="form-group") as group1:
                group1.append(Label("Name:", for_element="name"))
                group1.append(
                    Input(type="text", id="name", name="name", required="true")
                )
            personal.append(group1)

            with Div(class_name="form-group") as group2:
                group2.append(Label("Email:", for_element="email"))
                group2.append(
                    Input(type="email", id="email", name="email", required="true")
                )
            personal.append(group2)

        form.append(personal)

        with Fieldset() as preferences:
            preferences.append(Legend("Preferences"))

            with Div(class_name="form-group") as group3:
                group3.append(Label("Theme:", for_element="theme"))
                with Select(id="theme", name="theme") as theme_select:
                    theme_select.append(Option("Light", value="light"))
                    theme_select.append(Option("Dark", value="dark"))
                    theme_select.append(Option("System", value="system"))
                group3.append(theme_select)
            preferences.append(group3)

        form.append(preferences)

        with Div(class_name="form-actions") as actions:
            actions.append(Button("Submit", type="submit"))
            actions.append(Button("Reset", type="reset"))
        form.append(actions)

    print("Form built with context managers:")
    print(form.render(pretty=True))


def building_tables_with_context():
    """Building tables using context managers."""
    print("\n=== Building Tables ===\n")

    data = [
        {"product": "Widget", "price": 9.99, "qty": 5},
        {"product": "Gadget", "price": 19.99, "qty": 3},
        {"product": "Gizmo", "price": 14.99, "qty": 2},
    ]

    with Table(class_name="product-table") as table:
        with TableHeader() as thead:
            with TableRow() as header_row:
                header_row.append(TableHeaderCell("Product"))
                header_row.append(TableHeaderCell("Price"))
                header_row.append(TableHeaderCell("Quantity"))
                header_row.append(TableHeaderCell("Total"))
            thead.append(header_row)
        table.append(thead)

        with TableBody() as tbody:
            total_sum = 0
            for item in data:
                total = item["price"] * item["qty"]
                total_sum += total
                with TableRow() as row:
                    row.append(TableDataCell(item["product"]))
                    row.append(TableDataCell(f"${item['price']:.2f}"))
                    row.append(TableDataCell(str(item["qty"])))
                    row.append(TableDataCell(f"${total:.2f}"))
                tbody.append(row)
        table.append(tbody)

        with TableFooter() as tfoot:
            with TableRow() as footer_row:
                footer_row.append(TableDataCell(""))
                footer_row.append(TableDataCell(""))
                footer_row.append(TableHeaderCell("Total:"))
                footer_row.append(TableHeaderCell(f"${total_sum:.2f}"))
            tfoot.append(footer_row)
        table.append(tfoot)

    print("Table built with context managers:")
    print(table.render(pretty=True))


def complex_layout_with_context():
    """Building a complex page layout."""
    print("\n=== Complex Layout ===\n")

    sidebar_items = ["Dashboard", "Analytics", "Reports", "Settings"]
    cards_data = [
        {"title": "Users", "value": "1,234", "change": "+5%"},
        {"title": "Revenue", "value": "$56,789", "change": "+12%"},
        {"title": "Orders", "value": "456", "change": "-2%"},
    ]

    with Div(class_name="app-layout") as app:
        # Sidebar
        with Aside(class_name="sidebar") as sidebar:
            sidebar.append(H2("Menu"))
            with Nav() as nav:
                with UnorderedList() as menu:
                    for item in sidebar_items:
                        with ListItem() as li:
                            li.append(Link(item, href=f"/{item.lower()}"))
                        menu.append(li)
                nav.append(menu)
            sidebar.append(nav)
        app.append(sidebar)

        # Main content area
        with Main(class_name="main-content") as main:
            main.append(H1("Dashboard"))

            # Stats cards
            with Div(class_name="stats-grid") as stats:
                for card_data in cards_data:
                    with Div(class_name="stat-card") as card:
                        card.append(H3(card_data["title"]))
                        card.append(
                            Paragraph(card_data["value"], class_name="stat-value")
                        )
                        change_class = (
                            "positive" if "+" in card_data["change"] else "negative"
                        )
                        card.append(
                            Span(
                                card_data["change"], class_name=f"change {change_class}"
                            )
                        )
                    stats.append(card)
            main.append(stats)

            # Recent activity
            with Section(class_name="recent-activity") as activity:
                activity.append(H2("Recent Activity"))
                with UnorderedList() as activity_list:
                    activities = [
                        "User John signed up",
                        "New order #123 received",
                        "Payment processed",
                    ]
                    for act in activities:
                        activity_list.append(ListItem(act))
                activity.append(activity_list)
            main.append(activity)

        app.append(main)

    print("Complex layout:")
    print(app.render(pretty=True))


def mixing_styles_in_context():
    """Mixing context manager with regular nesting."""
    print("\n=== Mixed Styles ===\n")

    # You can mix context managers with regular constructor nesting
    with Div(class_name="container") as container:
        # Regular nesting for simple structures
        container.append(
            Header(
                H1("Title"), Nav(Link("Link 1", href="#1"), Link("Link 2", href="#2"))
            )
        )

        # Context manager for dynamic/conditional content
        with Main() as main:
            items = ["Item A", "Item B", "Item C"]
            with UnorderedList() as ul:
                for item in items:
                    ul.append(ListItem(item))
            main.append(ul)
        container.append(main)

        # Back to regular nesting
        container.append(Footer(Paragraph("Footer content")))

    print("Mixed nesting styles:")
    print(container.render(pretty=True))


def context_with_styling():
    """Using context managers with inline styling."""
    print("\n=== Context with Styling ===\n")

    with Div(class_name="styled-container") as container:
        container.add_styles(
            {"max-width": "800px", "margin": "0 auto", "padding": "20px"}
        )

        with Section(class_name="hero") as hero:
            hero.add_styles(
                {
                    "background": "linear-gradient(135deg, #667eea, #764ba2)",
                    "color": "white",
                    "padding": "60px 40px",
                    "border-radius": "12px",
                    "text-align": "center",
                }
            )
            hero.append(H1("Welcome to Our Site"))
            hero.append(Paragraph("Building beautiful interfaces with NitroUI"))

            with Div(class_name="cta-buttons") as buttons:
                buttons.add_style("margin-top", "20px")
                buttons.append(
                    Button("Get Started", type="button").add_styles(
                        {
                            "background": "white",
                            "color": "#667eea",
                            "padding": "12px 24px",
                            "border": "none",
                            "border-radius": "6px",
                            "margin": "0 8px",
                            "cursor": "pointer",
                        }
                    )
                )
                buttons.append(
                    Button("Learn More", type="button").add_styles(
                        {
                            "background": "transparent",
                            "color": "white",
                            "padding": "12px 24px",
                            "border": "2px solid white",
                            "border-radius": "6px",
                            "margin": "0 8px",
                            "cursor": "pointer",
                        }
                    )
                )
            hero.append(buttons)

        container.append(hero)

    print("Styled content with context managers:")
    print(container.render(pretty=True))


if __name__ == "__main__":
    basic_context_manager()
    nested_context_managers()
    comparison_with_regular()
    dynamic_content_with_context()
    conditional_with_context()
    building_forms_with_context()
    building_tables_with_context()
    complex_layout_with_context()
    mixing_styles_in_context()
    context_with_styling()
