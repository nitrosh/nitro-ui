"""JSON serialization examples for NitroUI.

This module demonstrates NitroUI's serialization capabilities:
- Converting elements to JSON
- Reconstructing elements from JSON
- Saving and loading page structures
- Use cases for serialization
"""

from nitro_ui import *
from nitro_ui.core.element import HTMLElement
import json


def basic_serialization():
    """Basic JSON serialization."""
    print("=== Basic Serialization ===\n")

    # Create a simple element
    element = Div(
        H1("Hello World"),
        Paragraph("This is a paragraph."),
        id="container",
        class_name="main",
    )

    # Serialize to JSON
    json_data = element.to_json(indent=2)
    print("JSON output:")
    print(json_data)


def serialize_complex_structure():
    """Serializing a complex nested structure."""
    print("\n=== Complex Structure Serialization ===\n")

    page = Div(
        Header(
            Nav(
                Link("Home", href="/", class_name="nav-link"),
                Link("About", href="/about", class_name="nav-link"),
                class_name="main-nav",
            )
        ),
        Main(
            Article(
                H1("Article Title"),
                Paragraph("First paragraph of content."),
                Paragraph("Second paragraph with ", Strong("bold text"), "."),
                class_name="article",
            )
        ),
        Footer(Paragraph("Copyright 2025")),
        id="page",
        class_name="container",
    )

    # Serialize
    json_data = page.to_json(indent=2)
    print("Complex structure as JSON:")
    print(json_data[:500] + "..." if len(json_data) > 500 else json_data)


def deserialize_from_json():
    """Reconstructing elements from JSON."""
    print("\n=== Deserialize from JSON ===\n")

    # JSON string (could come from a database, API, or file)
    json_str = """
    {
        "tag": "div",
        "self_closing": false,
        "attributes": {
            "id": "card",
            "class_name": "card-container"
        },
        "text": "",
        "children": [
            {
                "tag": "h2",
                "self_closing": false,
                "attributes": {},
                "text": "Card Title",
                "children": []
            },
            {
                "tag": "p",
                "self_closing": false,
                "attributes": {},
                "text": "Card content goes here.",
                "children": []
            }
        ]
    }
    """

    # Reconstruct element
    element = HTMLElement.from_json(json_str)

    print("Reconstructed element:")
    print(element.render(pretty=True))

    # You can now modify it
    element.append(Paragraph("Added after deserialization"))
    element.add_style("border", "1px solid #ddd")

    print("After modification:")
    print(element.render(pretty=True))


def round_trip():
    """Demonstrating serialize -> deserialize round trip."""
    print("\n=== Round Trip ===\n")

    # Original element
    original = Div(
        H1("Test"),
        Paragraph("Content with ", Em("emphasis"), " and ", Strong("strong"), "."),
        UnorderedList(ListItem("Item 1"), ListItem("Item 2"), ListItem("Item 3")),
        id="test",
        class_name="container",
        data_value="123",
    )

    print("Original HTML:")
    print(original.render())

    # Serialize
    json_data = original.to_json()

    # Deserialize
    restored = HTMLElement.from_json(json_data)

    print("\nRestored HTML:")
    print(restored.render())

    print("\nHTML matches:", original.render() == restored.render())


def to_dict_example():
    """Using to_dict() for Python dict operations."""
    print("\n=== to_dict() Example ===\n")

    element = Div(H1("Title"), Paragraph("Content"), id="my-element")

    # Convert to dictionary
    data = element.to_dict()

    print("As dictionary:")
    print(json.dumps(data, indent=2))

    # Manipulate the dict
    data["attributes"]["class_name"] = "modified"
    data["children"].append(
        {
            "tag": "p",
            "self_closing": False,
            "attributes": {"class_name": "added"},
            "text": "Added via dict manipulation",
            "children": [],
        }
    )

    # Reconstruct
    modified = HTMLElement.from_dict(data)
    print("\nModified element:")
    print(modified.render(pretty=True))


def save_to_file():
    """Saving page structure to a file."""
    print("\n=== Save to File ===\n")

    page = HTML(
        Head(Title("My Page"), Meta(charset="utf-8")),
        Body(
            Header(H1("Welcome")),
            Main(Paragraph("Main content")),
            Footer(Paragraph("Footer")),
        ),
    )

    # Save to file (demonstration - not actually writing)
    json_data = page.to_json(indent=2)

    print("JSON to save:")
    print(json_data[:400] + "...")

    print("\n# To save to a file:")
    print("# with open('page.json', 'w') as f:")
    print("#     f.write(page.to_json(indent=2))")


def load_from_file():
    """Loading page structure from a file."""
    print("\n=== Load from File ===\n")

    # Simulated file content
    file_content = """
    {
        "tag": "html",
        "self_closing": false,
        "attributes": {"lang": "en"},
        "text": "",
        "children": [
            {
                "tag": "head",
                "self_closing": false,
                "attributes": {},
                "text": "",
                "children": [
                    {
                        "tag": "title",
                        "self_closing": false,
                        "attributes": {},
                        "text": "Loaded Page",
                        "children": []
                    }
                ]
            },
            {
                "tag": "body",
                "self_closing": false,
                "attributes": {},
                "text": "",
                "children": [
                    {
                        "tag": "h1",
                        "self_closing": false,
                        "attributes": {},
                        "text": "Hello from JSON!",
                        "children": []
                    }
                ]
            }
        ]
    }
    """

    # Load and reconstruct
    page = HTMLElement.from_json(file_content)

    print("Loaded page:")
    print(page.render(pretty=True))

    print("\n# To load from a file:")
    print("# with open('page.json', 'r') as f:")
    print("#     page = HTMLElement.from_json(f.read())")


def template_storage():
    """Storing reusable templates as JSON."""
    print("\n=== Template Storage ===\n")

    # Define some templates
    templates = {
        "card": Div(
            Div(class_name="card-header"),
            Div(class_name="card-body"),
            Div(class_name="card-footer"),
            class_name="card",
        ).to_dict(),
        "alert": Div(
            Span(class_name="alert-icon"),
            Span(class_name="alert-message"),
            class_name="alert",
            role="alert",
        ).to_dict(),
        "modal": Div(
            Div(
                Div(class_name="modal-header"),
                Div(class_name="modal-body"),
                Div(class_name="modal-footer"),
                class_name="modal-content",
            ),
            class_name="modal",
            role="dialog",
        ).to_dict(),
    }

    # Save templates
    templates_json = json.dumps(templates, indent=2)
    print("Templates JSON:")
    print(templates_json[:500] + "...")

    # Load and use a template
    card_template = HTMLElement.from_dict(templates["card"])

    # Customize the template
    card_header = card_template.find_by_attribute("class_name", "card-header")
    if card_header:
        card_header.append(H3("My Card Title"))

    card_body = card_template.find_by_attribute("class_name", "card-body")
    if card_body:
        card_body.append(Paragraph("Card content here"))

    print("\nCustomized card from template:")
    print(card_template.render(pretty=True))


def undo_redo_system():
    """Implementing undo/redo with serialization."""
    print("\n=== Undo/Redo System ===\n")

    class UndoableEditor:
        def __init__(self, initial_element):
            self.history = [initial_element.to_json()]
            self.current_index = 0

        def save_state(self, element):
            # Remove any redo history
            self.history = self.history[: self.current_index + 1]
            # Save new state
            self.history.append(element.to_json())
            self.current_index = len(self.history) - 1

        def undo(self):
            if self.current_index > 0:
                self.current_index -= 1
                return HTMLElement.from_json(self.history[self.current_index])
            return None

        def redo(self):
            if self.current_index < len(self.history) - 1:
                self.current_index += 1
                return HTMLElement.from_json(self.history[self.current_index])
            return None

        def current(self):
            return HTMLElement.from_json(self.history[self.current_index])

    # Demo
    editor = UndoableEditor(Div(H1("Initial")))

    # Make changes
    element = editor.current()
    element.append(Paragraph("Added paragraph"))
    editor.save_state(element)
    print("State 1:", editor.current().render())

    element = editor.current()
    element.append(Paragraph("Added another"))
    editor.save_state(element)
    print("State 2:", editor.current().render())

    # Undo
    element = editor.undo()
    print("After undo:", element.render() if element else "Cannot undo")

    # Undo again
    element = editor.undo()
    print("After undo:", element.render() if element else "Cannot undo")

    # Redo
    element = editor.redo()
    print("After redo:", element.render() if element else "Cannot redo")


def api_communication():
    """Using JSON for API communication."""
    print("\n=== API Communication ===\n")

    # Server-side: Generate page structure
    def generate_page_for_client():
        page = Div(
            H1("Dynamic Page"),
            Paragraph("This structure was generated server-side."),
            UnorderedList(
                ListItem("Feature 1"), ListItem("Feature 2"), ListItem("Feature 3")
            ),
            id="dynamic-content",
        )
        return page.to_json()

    # Simulate API response
    api_response = generate_page_for_client()
    print("API Response (JSON):")
    print(api_response[:300] + "...")

    # Client-side: Reconstruct and render
    def client_render(json_response):
        element = HTMLElement.from_json(json_response)
        return element.render(pretty=True)

    print("\nClient renders:")
    print(client_render(api_response))


def drag_and_drop_builder():
    """Simulating a drag-and-drop website builder."""
    print("\n=== Drag-and-Drop Builder ===\n")

    # Current page state
    page_state = {
        "tag": "div",
        "self_closing": False,
        "attributes": {"id": "page", "class_name": "page-builder"},
        "text": "",
        "children": [],
    }

    def add_component(page_dict, component_type, position=None):
        """Add a component to the page."""
        components = {
            "heading": {
                "tag": "h1",
                "text": "New Heading",
                "attributes": {},
                "children": [],
                "self_closing": False,
            },
            "paragraph": {
                "tag": "p",
                "text": "New paragraph text",
                "attributes": {},
                "children": [],
                "self_closing": False,
            },
            "image": {
                "tag": "img",
                "text": "",
                "attributes": {"src": "/placeholder.jpg", "alt": "Image"},
                "children": [],
                "self_closing": True,
            },
            "button": {
                "tag": "button",
                "text": "Click Me",
                "attributes": {"class_name": "btn"},
                "children": [],
                "self_closing": False,
            },
        }

        if component_type in components:
            if position is not None and position < len(page_dict["children"]):
                page_dict["children"].insert(
                    position, components[component_type].copy()
                )
            else:
                page_dict["children"].append(components[component_type].copy())

        return page_dict

    # Simulate building a page
    print("Building page by adding components...")

    page_state = add_component(page_state, "heading")
    page_state = add_component(page_state, "paragraph")
    page_state = add_component(page_state, "image")
    page_state = add_component(page_state, "button")

    # Reconstruct and render
    page = HTMLElement.from_dict(page_state)
    print("\nBuilt page:")
    print(page.render(pretty=True))

    # Save for later
    saved_state = json.dumps(page_state, indent=2)
    print("\nSaved state for later:")
    print(saved_state[:300] + "...")


if __name__ == "__main__":
    basic_serialization()
    serialize_complex_structure()
    deserialize_from_json()
    round_trip()
    to_dict_example()
    save_to_file()
    load_from_file()
    template_storage()
    undo_redo_system()
    api_communication()
    drag_and_drop_builder()
