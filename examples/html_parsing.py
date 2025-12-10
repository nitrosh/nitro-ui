"""HTML parsing examples for NitroUI.

This module demonstrates parsing raw HTML into NitroUI elements:
- Parsing single elements
- Parsing HTML fragments (multiple root elements)
- Modifying parsed elements
- Use cases for HTML parsing
"""

from nitro_ui import *
from nitro_ui import from_html
from nitro_ui.core.element import HTMLElement


def basic_parsing():
    """Basic HTML parsing."""
    print("=== Basic HTML Parsing ===\n")

    # Parse a simple HTML string
    html_string = '<div class="container"><h1>Hello World</h1></div>'

    element = from_html(html_string)

    print(f"Original HTML: {html_string}")
    print(f"Parsed element tag: {element.tag}")
    print(f"Parsed element class: {element.get_attribute('class_name')}")
    print(f"Rendered: {element.render()}")


def parse_nested_structure():
    """Parsing nested HTML structures."""
    print("\n=== Parse Nested Structure ===\n")

    html_string = """
    <article class="blog-post">
        <header>
            <h1>Article Title</h1>
            <p class="meta">Published on January 15, 2025</p>
        </header>
        <div class="content">
            <p>First paragraph of the article.</p>
            <p>Second paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
        </div>
        <footer>
            <p>Author: John Doe</p>
        </footer>
    </article>
    """

    element = from_html(html_string)

    print("Parsed and re-rendered:")
    print(element.render(pretty=True))


def parse_fragment():
    """Parsing HTML fragments with multiple root elements."""
    print("\n=== Parse Fragment ===\n")

    html_fragment = """
    <h1>Welcome</h1>
    <p>First paragraph</p>
    <p>Second paragraph</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    """

    # Parse as fragment (returns list of elements)
    elements = from_html(html_fragment, fragment=True)

    print(f"Number of root elements: {len(elements)}")
    print("\nEach element:")
    for i, el in enumerate(elements):
        print(f"  {i + 1}. <{el.tag}>: {el.text[:30] if el.text else '(children)'}...")

    print("\nAll elements rendered:")
    for el in elements:
        print(el.render())


def modify_parsed_elements():
    """Modifying elements after parsing."""
    print("\n=== Modify Parsed Elements ===\n")

    html_string = '<div class="card"><h2>Title</h2><p>Content</p></div>'

    element = from_html(html_string)
    print("Before modification:")
    print(element.render())

    # Add styles
    element.add_styles(
        {"border": "1px solid #ddd", "border-radius": "8px", "padding": "16px"}
    )

    # Add new content
    element.append(Paragraph("Added with NitroUI"))
    element.append(Button("Click Me", class_name="btn"))

    # Modify attribute
    element.add_attribute("id", "my-card")

    print("\nAfter modification:")
    print(element.render(pretty=True))


def using_class_method():
    """Using the HTMLElement.from_html class method."""
    print("\n=== Using Class Method ===\n")

    html_string = '<span class="badge">New</span>'

    # Alternative way to parse using class method
    element = HTMLElement.from_html(html_string)

    print(f"Parsed: {element.render()}")

    # Also works for fragments
    fragment_html = "<span>One</span><span>Two</span>"
    elements = HTMLElement.from_html(fragment_html, fragment=True)
    print(f"Fragment elements: {[el.render() for el in elements]}")


def parse_self_closing_tags():
    """Parsing HTML with self-closing tags."""
    print("\n=== Self-Closing Tags ===\n")

    html_string = """
    <div class="content">
        <img src="/image.jpg" alt="An image">
        <br>
        <input type="text" name="email" placeholder="Enter email">
        <hr>
        <meta name="viewport" content="width=device-width">
    </div>
    """

    element = from_html(html_string)

    print("Parsed HTML with self-closing tags:")
    print(element.render(pretty=True))


def parse_data_attributes():
    """Parsing HTML with data-* attributes."""
    print("\n=== Data Attributes ===\n")

    html_string = """
    <div
        data-user-id="12345"
        data-role="admin"
        data-config='{"theme": "dark"}'
        class="user-card">
        <h3>John Doe</h3>
    </div>
    """

    element = from_html(html_string)

    print("Parsed with data attributes:")
    print(element.render())

    # Access the data attributes
    print(f"\ndata-user-id: {element.get_attribute('data-user-id')}")
    print(f"data-role: {element.get_attribute('data-role')}")


def migrate_existing_html():
    """Migrating existing HTML to NitroUI."""
    print("\n=== Migrate Existing HTML ===\n")

    # Existing HTML from an old template
    old_html = """
    <nav class="navbar">
        <a href="/" class="logo">MyBrand</a>
        <ul class="nav-links">
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
        </ul>
    </nav>
    """

    # Parse the old HTML
    navbar = from_html(old_html)

    print("Migrated HTML:")
    print(navbar.render(pretty=True))

    # Now you can enhance it with NitroUI features
    navbar.add_styles(
        {
            "display": "flex",
            "justify-content": "space-between",
            "padding": "10px 20px",
            "background": "#333",
        }
    )

    # Add new elements
    navbar.append(Button("Sign In", class_name="sign-in-btn"))

    print("\nEnhanced version:")
    print(navbar.render(pretty=True))


def combine_parsed_and_new():
    """Combining parsed HTML with new NitroUI elements."""
    print("\n=== Combine Parsed and New ===\n")

    # Parse some existing HTML
    header_html = '<header class="site-header"><h1>My Site</h1></header>'
    header = from_html(header_html)

    # Create new elements with NitroUI
    main_content = Main(
        Section(
            H2("Welcome"),
            Paragraph("This section was created with NitroUI."),
            class_name="welcome-section",
        ),
        Section(
            H2("Features"),
            UnorderedList(
                ListItem("Feature 1"), ListItem("Feature 2"), ListItem("Feature 3")
            ),
            class_name="features-section",
        ),
    )

    footer = Footer(Paragraph("Copyright 2025 My Site"))

    # Combine into a page
    page = Div(header, main_content, footer, class_name="page-container")

    print("Combined page:")
    print(page.render(pretty=True))


def parse_and_search():
    """Parsing HTML and searching within it."""
    print("\n=== Parse and Search ===\n")

    html_string = """
    <div class="page">
        <nav id="main-nav">
            <a href="/">Home</a>
        </nav>
        <main id="content">
            <article id="post-123" class="blog-post">
                <h1>Post Title</h1>
                <p>Post content...</p>
            </article>
        </main>
        <aside id="sidebar">
            <h3>Related</h3>
        </aside>
    </div>
    """

    page = from_html(html_string)

    # Find elements by attribute
    nav = page.find_by_attribute("id", "main-nav")
    if nav:
        print(f"Found nav: {nav.render()}")

    article = page.find_by_attribute("id", "post-123")
    if article:
        print(f"\nFound article: {article.render()}")

    sidebar = page.find_by_attribute("id", "sidebar")
    if sidebar:
        print(f"\nFound sidebar: {sidebar.render()}")


def convert_template_snippet():
    """Converting template snippets to NitroUI."""
    print("\n=== Convert Template Snippets ===\n")

    # HTML snippets from a design library
    bootstrap_card = """
    <div class="card" style="width: 18rem;">
        <img src="/image.jpg" class="card-img-top" alt="Card image">
        <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
    </div>
    """

    card = from_html(bootstrap_card)

    # Now modify it dynamically
    title = card.find_by_attribute("class_name", "card-title")
    if title:
        title.text = "Product Name"

    body = card.find_by_attribute("class_name", "card-text")
    if body:
        body.text = "Product description goes here."

    print("Modified Bootstrap card:")
    print(card.render(pretty=True))


def build_template_library():
    """Building a template library from HTML snippets."""
    print("\n=== Template Library ===\n")

    class TemplateLibrary:
        def __init__(self):
            self.templates = {}

        def register(self, name, html_string):
            """Register an HTML template."""
            self.templates[name] = html_string

        def get(self, name, **replacements):
            """Get a template instance with optional text replacements."""
            if name not in self.templates:
                raise ValueError(f"Template '{name}' not found")

            element = from_html(self.templates[name])

            # Simple text replacement
            for attr_value, new_text in replacements.items():
                el = element.find_by_attribute("data-replace", attr_value)
                if el:
                    el.text = new_text

            return element

    # Create library
    library = TemplateLibrary()

    # Register templates
    library.register(
        "alert",
        """
        <div class="alert" role="alert">
            <strong data-replace="title">Alert</strong>
            <span data-replace="message">Message here</span>
        </div>
    """,
    )

    library.register(
        "user-card",
        """
        <div class="user-card">
            <img src="/avatar.jpg" class="avatar" alt="User">
            <h4 data-replace="name">User Name</h4>
            <p data-replace="role">Role</p>
        </div>
    """,
    )

    # Use templates
    alert = library.get(
        "alert", title="Success!", message="Your changes have been saved."
    )
    print("Alert from template:")
    print(alert.render())

    user = library.get("user-card", name="John Doe", role="Administrator")
    print("\nUser card from template:")
    print(user.render())


def external_html_import():
    """Simulating import from external HTML sources."""
    print("\n=== External HTML Import ===\n")

    # Simulated external HTML (e.g., from a CMS, API, or file)
    external_content = """
    <div class="cms-content">
        <h2>Welcome to Our Service</h2>
        <p>We provide the best solutions for your needs.</p>
        <ul class="features">
            <li>Fast and reliable</li>
            <li>24/7 support</li>
            <li>Affordable pricing</li>
        </ul>
        <a href="/signup" class="cta-button">Get Started</a>
    </div>
    """

    # Parse external content
    content = from_html(external_content)

    # Wrap in NitroUI page structure
    page = HTML(
        Head(
            Title("Our Service"),
            Meta(charset="utf-8"),
            HtmlLink(rel="stylesheet", href="/styles.css"),
        ),
        Body(
            Header(
                Nav(
                    Link("Home", href="/"),
                    Link("Services", href="/services"),
                    class_name="main-nav",
                )
            ),
            Main(content),  # Insert parsed external content
            Footer(Paragraph("Copyright 2025")),
        ),
    )

    print("Page with external content:")
    print(page.render(pretty=True))


if __name__ == "__main__":
    basic_parsing()
    parse_nested_structure()
    parse_fragment()
    modify_parsed_elements()
    using_class_method()
    parse_self_closing_tags()
    parse_data_attributes()
    migrate_existing_html()
    combine_parsed_and_new()
    parse_and_search()
    convert_template_snippet()
    build_template_library()
    external_html_import()
