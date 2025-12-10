"""Custom components examples for NitroUI.

This module demonstrates how to create reusable custom components
by subclassing HTMLElement:
- Basic custom components
- Components with lifecycle hooks
- Parameterized components
- Component composition
- Building a component library
"""

from nitro_ui import *


class Card(HTMLElement):
    """A reusable card component."""

    def __init__(self, title, *children, **kwargs):
        super().__init__(*children, **{**kwargs, "tag": "div"})
        self.add_attribute("class", "card")
        self.add_styles(
            {
                "background": "white",
                "border-radius": "8px",
                "box-shadow": "0 2px 8px rgba(0,0,0,0.1)",
                "overflow": "hidden",
            }
        )

        # Add header with title
        self.prepend(
            Div(H3(title), class_name="card-header").add_styles(
                {"padding": "16px", "border-bottom": "1px solid #eee"}
            )
        )

        # Wrap existing children in body
        if children:
            body = Div(class_name="card-body").add_style("padding", "16px")
            for child in children:
                if isinstance(child, HTMLElement):
                    body.append(child)
            self.append(body)


class Alert(HTMLElement):
    """A configurable alert component."""

    VARIANTS = {
        "info": {"bg": "#cce5ff", "border": "#b8daff", "text": "#004085"},
        "success": {"bg": "#d4edda", "border": "#c3e6cb", "text": "#155724"},
        "warning": {"bg": "#fff3cd", "border": "#ffeeba", "text": "#856404"},
        "danger": {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24"},
    }

    def __init__(self, message, variant="info", dismissible=False, **kwargs):
        super().__init__(**{**kwargs, "tag": "div"})

        colors = self.VARIANTS.get(variant, self.VARIANTS["info"])

        self.add_attributes([("class", f"alert alert-{variant}"), ("role", "alert")])

        self.add_styles(
            {
                "background-color": colors["bg"],
                "border": f"1px solid {colors['border']}",
                "color": colors["text"],
                "padding": "12px 16px",
                "border-radius": "4px",
                "margin-bottom": "16px",
            }
        )

        self.append(Span(message))

        if dismissible:
            self.add_attribute("data-dismissible", "true")
            self.append(
                Button("x", type="button", class_name="alert-close").add_styles(
                    {
                        "float": "right",
                        "background": "none",
                        "border": "none",
                        "font-size": "20px",
                        "cursor": "pointer",
                        "color": colors["text"],
                    }
                )
            )


class Badge(HTMLElement):
    """A badge/tag component."""

    def __init__(self, text, variant="default", pill=False, **kwargs):
        super().__init__(text, **{**kwargs, "tag": "span"})

        colors = {
            "default": {"bg": "#6c757d", "text": "white"},
            "primary": {"bg": "#007bff", "text": "white"},
            "success": {"bg": "#28a745", "text": "white"},
            "danger": {"bg": "#dc3545", "text": "white"},
            "warning": {"bg": "#ffc107", "text": "#212529"},
        }

        color = colors.get(variant, colors["default"])

        self.add_attribute("class", f"badge badge-{variant}")
        self.add_styles(
            {
                "display": "inline-block",
                "padding": "4px 8px",
                "font-size": "12px",
                "font-weight": "600",
                "background-color": color["bg"],
                "color": color["text"],
                "border-radius": "999px" if pill else "4px",
            }
        )


class Button(HTMLElement):
    """An enhanced button component."""

    def __init__(self, text, variant="primary", size="md", outline=False, **kwargs):
        super().__init__(text, **{**kwargs, "tag": "button"})

        colors = {
            "primary": "#007bff",
            "secondary": "#6c757d",
            "success": "#28a745",
            "danger": "#dc3545",
        }

        sizes = {
            "sm": {"padding": "6px 12px", "font-size": "14px"},
            "md": {"padding": "10px 20px", "font-size": "16px"},
            "lg": {"padding": "14px 28px", "font-size": "18px"},
        }

        color = colors.get(variant, colors["primary"])
        size_styles = sizes.get(size, sizes["md"])

        self.add_attribute("class", f"btn btn-{variant}")

        if outline:
            self.add_styles(
                {
                    "background-color": "transparent",
                    "border": f"2px solid {color}",
                    "color": color,
                    **size_styles,
                    "border-radius": "4px",
                    "cursor": "pointer",
                    "font-weight": "600",
                }
            )
        else:
            self.add_styles(
                {
                    "background-color": color,
                    "border": "none",
                    "color": "white",
                    **size_styles,
                    "border-radius": "4px",
                    "cursor": "pointer",
                    "font-weight": "600",
                }
            )


class Modal(HTMLElement):
    """A modal dialog component."""

    def __init__(self, title, *children, modal_id="modal", **kwargs):
        super().__init__(**{**kwargs, "tag": "div"})

        self.add_attributes(
            [
                ("id", modal_id),
                ("class", "modal"),
                ("role", "dialog"),
                ("aria-labelledby", f"{modal_id}-title"),
                ("aria-modal", "true"),
            ]
        )

        self.add_styles(
            {
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "background-color": "rgba(0,0,0,0.5)",
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
            }
        )

        # Modal content container
        content = Div(class_name="modal-content").add_styles(
            {
                "background": "white",
                "border-radius": "8px",
                "max-width": "500px",
                "width": "100%",
                "max-height": "90vh",
                "overflow": "auto",
            }
        )

        # Header
        header = Div(
            H2(title, id=f"{modal_id}-title"), class_name="modal-header"
        ).add_styles(
            {
                "padding": "16px 20px",
                "border-bottom": "1px solid #eee",
                "display": "flex",
                "justify-content": "space-between",
                "align-items": "center",
            }
        )
        content.append(header)

        # Body
        body = Div(*children, class_name="modal-body").add_styles({"padding": "20px"})
        content.append(body)

        self.append(content)


class Avatar(HTMLElement):
    """An avatar component for user profiles."""

    def __init__(self, src=None, name=None, size=40, **kwargs):
        super().__init__(**{**kwargs, "tag": "div"})

        self.add_attribute("class", "avatar")
        self.add_styles(
            {
                "width": f"{size}px",
                "height": f"{size}px",
                "border-radius": "50%",
                "overflow": "hidden",
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "font-weight": "600",
                "font-size": f"{size // 2}px",
            }
        )

        if src:
            self.append(
                Image(src=src, alt=name or "Avatar").add_styles(
                    {"width": "100%", "height": "100%", "object-fit": "cover"}
                )
            )
        elif name:
            # Generate initials and background color
            initials = "".join(word[0].upper() for word in name.split()[:2])
            bg_color = self._generate_color(name)
            self.add_styles({"background-color": bg_color, "color": "white"})
            self.text = initials

    @staticmethod
    def _generate_color(name):
        """Generate a consistent color from a name."""
        colors = ["#007bff", "#28a745", "#dc3545", "#ffc107", "#17a2b8", "#6f42c1"]
        return colors[sum(ord(c) for c in name) % len(colors)]


class NavItem(HTMLElement):
    """A navigation item component."""

    def __init__(self, text, href="#", active=False, **kwargs):
        super().__init__(**{**kwargs, "tag": "li"})

        self.add_attribute("class", "nav-item")

        link = Link(text, href=href, class_name="nav-link")
        if active:
            link.add_attribute("class", "nav-link active")
            link.add_style("font-weight", "600")

        self.append(link)


class Navbar(HTMLElement):
    """A navigation bar component."""

    def __init__(self, brand, *items, **kwargs):
        super().__init__(**{**kwargs, "tag": "nav"})

        self.add_attribute("class", "navbar")
        self.add_styles(
            {
                "display": "flex",
                "align-items": "center",
                "padding": "10px 20px",
                "background": "#fff",
                "box-shadow": "0 1px 3px rgba(0,0,0,0.1)",
            }
        )

        # Brand
        self.append(
            Link(brand, href="/", class_name="navbar-brand").add_styles(
                {
                    "font-size": "20px",
                    "font-weight": "700",
                    "text-decoration": "none",
                    "color": "#333",
                    "margin-right": "auto",
                }
            )
        )

        # Navigation items
        nav_list = UnorderedList(class_name="navbar-nav").add_styles(
            {
                "display": "flex",
                "list-style": "none",
                "margin": "0",
                "padding": "0",
                "gap": "20px",
            }
        )

        for item in items:
            nav_list.append(item)

        self.append(nav_list)


class WithLifecycleHooks(HTMLElement):
    """Component demonstrating lifecycle hooks."""

    def __init__(self, name, **kwargs):
        self.component_name = name
        super().__init__(**{**kwargs, "tag": "div"})
        self.add_attribute("class", "lifecycle-component")

    def on_load(self):
        """Called when the component is instantiated."""
        print(f"[{self.component_name}] on_load: Component initialized")
        self.append(Paragraph("Component loaded"))

    def on_before_render(self):
        """Called before rendering."""
        print(f"[{self.component_name}] on_before_render: About to render")

    def on_after_render(self):
        """Called after rendering."""
        print(f"[{self.component_name}] on_after_render: Rendering complete")

    def on_unload(self):
        """Called when the component is garbage collected."""
        print(f"[{self.component_name}] on_unload: Component destroyed")


def basic_custom_components():
    """Using basic custom components."""
    print("=== Basic Custom Components ===\n")

    page = Div(
        Card(
            "Welcome",
            Paragraph("This is a card component."),
            Paragraph("Cards are great for grouping content."),
        ),
        Alert("This is an info alert.", variant="info"),
        Alert("Success! Your changes have been saved.", variant="success"),
        Alert(
            "Warning! Please review your input.", variant="warning", dismissible=True
        ),
        Div(
            Badge("New", variant="primary"),
            Badge("Sale", variant="danger"),
            Badge("Featured", variant="success", pill=True),
            class_name="badges",
        ).add_style("margin", "20px 0"),
        class_name="container",
    )

    print(page.render(pretty=True))


def button_variants():
    """Demonstrating button variants."""
    print("\n=== Button Variants ===\n")

    buttons = Div(
        H3("Solid Buttons"),
        Div(
            Button("Primary", variant="primary"),
            Button("Secondary", variant="secondary"),
            Button("Success", variant="success"),
            Button("Danger", variant="danger"),
            class_name="button-group",
        ).add_styles({"display": "flex", "gap": "10px", "margin": "10px 0"}),
        H3("Outline Buttons"),
        Div(
            Button("Primary", variant="primary", outline=True),
            Button("Secondary", variant="secondary", outline=True),
            Button("Success", variant="success", outline=True),
            Button("Danger", variant="danger", outline=True),
            class_name="button-group",
        ).add_styles({"display": "flex", "gap": "10px", "margin": "10px 0"}),
        H3("Button Sizes"),
        Div(
            Button("Small", size="sm"),
            Button("Medium", size="md"),
            Button("Large", size="lg"),
            class_name="button-group",
        ).add_styles(
            {
                "display": "flex",
                "gap": "10px",
                "align-items": "center",
                "margin": "10px 0",
            }
        ),
    )

    print(buttons.render(pretty=True))


def avatar_examples():
    """Demonstrating avatar components."""
    print("\n=== Avatar Examples ===\n")

    avatars = Div(
        H3("Avatars with Images"),
        Div(
            Avatar(src="/avatars/user1.jpg", name="John Doe", size=40),
            Avatar(src="/avatars/user2.jpg", name="Jane Smith", size=50),
            Avatar(src="/avatars/user3.jpg", name="Bob Wilson", size=60),
            class_name="avatar-group",
        ).add_styles({"display": "flex", "gap": "10px", "align-items": "center"}),
        H3("Avatars with Initials"),
        Div(
            Avatar(name="John Doe", size=40),
            Avatar(name="Jane Smith", size=50),
            Avatar(name="Bob Wilson", size=60),
            Avatar(name="Alice Johnson", size=70),
            class_name="avatar-group",
        ).add_styles({"display": "flex", "gap": "10px", "align-items": "center"}),
    )

    print(avatars.render(pretty=True))


def navbar_example():
    """Demonstrating navbar component."""
    print("\n=== Navbar Example ===\n")

    navbar = Navbar(
        "NitroUI",
        NavItem("Home", href="/", active=True),
        NavItem("Products", href="/products"),
        NavItem("About", href="/about"),
        NavItem("Contact", href="/contact"),
    )

    print(navbar.render(pretty=True))


def modal_example():
    """Demonstrating modal component."""
    print("\n=== Modal Example ===\n")

    modal = Modal(
        "Confirm Action",
        Paragraph("Are you sure you want to proceed with this action?"),
        Paragraph("This cannot be undone."),
        Div(
            Button("Cancel", variant="secondary"),
            Button("Confirm", variant="danger"),
            class_name="modal-footer",
        ).add_styles(
            {
                "display": "flex",
                "gap": "10px",
                "justify-content": "flex-end",
                "margin-top": "20px",
            }
        ),
        modal_id="confirm-modal",
    )

    print(modal.render(pretty=True))


def lifecycle_hooks_demo():
    """Demonstrating lifecycle hooks."""
    print("\n=== Lifecycle Hooks Demo ===\n")

    component = WithLifecycleHooks("MyComponent")
    print("\nRendering component:")
    html = component.render()
    print(f"\nOutput: {html}")


def component_composition():
    """Building a page from composed components."""
    print("\n=== Component Composition ===\n")

    # Build a complete page using custom components
    page = Div(
        Navbar(
            "MyApp",
            NavItem("Dashboard", href="/dashboard", active=True),
            NavItem("Users", href="/users"),
            NavItem("Settings", href="/settings"),
        ),
        Main(
            Div(
                H1("Dashboard"),
                Div(
                    Card(
                        "Statistics",
                        Div(
                            Div(H2("1,234"), Paragraph("Total Users")),
                            Div(H2("567"), Paragraph("Active Today")),
                            Div(H2("89%"), Paragraph("Satisfaction")),
                            class_name="stats-grid",
                        ).add_styles(
                            {
                                "display": "grid",
                                "grid-template-columns": "repeat(3, 1fr)",
                                "gap": "20px",
                                "text-align": "center",
                            }
                        ),
                    ),
                    Card(
                        "Recent Activity",
                        UnorderedList(
                            ListItem("User John signed up"),
                            ListItem("Order #123 completed"),
                            ListItem("New comment on post"),
                        ),
                    ),
                    class_name="dashboard-cards",
                ).add_styles(
                    {
                        "display": "grid",
                        "grid-template-columns": "2fr 1fr",
                        "gap": "20px",
                        "margin-top": "20px",
                    }
                ),
                Alert("Welcome to your dashboard!", variant="info"),
                class_name="container",
            ).add_styles({"max-width": "1200px", "margin": "0 auto", "padding": "20px"})
        ),
        class_name="page",
    )

    print(page.render(pretty=True))


if __name__ == "__main__":
    basic_custom_components()
    button_variants()
    avatar_examples()
    navbar_example()
    modal_example()
    lifecycle_hooks_demo()
    component_composition()
