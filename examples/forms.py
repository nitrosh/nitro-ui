"""Form examples for NitroUI.

This module demonstrates building HTML forms:
- Basic form elements
- Input types
- Select and option elements
- Fieldsets and legends
- Form validation attributes
- Complex form layouts
"""

from nitro_ui import *


def basic_form():
    """Basic form with common elements."""
    print("=== Basic Form ===\n")

    form = Form(
        Div(
            Label("Username:", for_element="username"),
            Input(type="text", id="username", name="username", required="true"),
            class_name="form-group",
        ),
        Div(
            Label("Email:", for_element="email"),
            Input(type="email", id="email", name="email", required="true"),
            class_name="form-group",
        ),
        Div(
            Label("Password:", for_element="password"),
            Input(type="password", id="password", name="password", required="true"),
            class_name="form-group",
        ),
        Div(
            Button("Submit", type="submit"),
            Button("Reset", type="reset"),
            class_name="form-actions",
        ),
        action="/register",
        method="post",
    )

    print(form.render(pretty=True))


def input_types():
    """Demonstrating various input types."""
    print("\n=== Input Types ===\n")

    form = Form(
        H2("All Input Types"),
        # Text inputs
        Fieldset(
            Legend("Text Inputs"),
            Div(
                Label("Text:", for_element="text"),
                Input(type="text", id="text", name="text", placeholder="Enter text"),
            ),
            Div(
                Label("Email:", for_element="email"),
                Input(
                    type="email",
                    id="email",
                    name="email",
                    placeholder="user@example.com",
                ),
            ),
            Div(
                Label("Password:", for_element="password"),
                Input(type="password", id="password", name="password"),
            ),
            Div(
                Label("URL:", for_element="url"),
                Input(
                    type="url", id="url", name="url", placeholder="https://example.com"
                ),
            ),
            Div(
                Label("Phone:", for_element="tel"),
                Input(type="tel", id="tel", name="tel", placeholder="+1-234-567-8900"),
            ),
            Div(
                Label("Search:", for_element="search"),
                Input(
                    type="search", id="search", name="search", placeholder="Search..."
                ),
            ),
        ),
        # Number inputs
        Fieldset(
            Legend("Number Inputs"),
            Div(
                Label("Number:", for_element="number"),
                Input(
                    type="number",
                    id="number",
                    name="number",
                    min="0",
                    max="100",
                    step="1",
                ),
            ),
            Div(
                Label("Range:", for_element="range"),
                Input(
                    type="range",
                    id="range",
                    name="range",
                    min="0",
                    max="100",
                    value="50",
                ),
            ),
        ),
        # Date/time inputs
        Fieldset(
            Legend("Date/Time Inputs"),
            Div(
                Label("Date:", for_element="date"),
                Input(type="date", id="date", name="date"),
            ),
            Div(
                Label("Time:", for_element="time"),
                Input(type="time", id="time", name="time"),
            ),
            Div(
                Label("DateTime-Local:", for_element="datetime"),
                Input(type="datetime-local", id="datetime", name="datetime"),
            ),
            Div(
                Label("Month:", for_element="month"),
                Input(type="month", id="month", name="month"),
            ),
            Div(
                Label("Week:", for_element="week"),
                Input(type="week", id="week", name="week"),
            ),
        ),
        # Other inputs
        Fieldset(
            Legend("Other Inputs"),
            Div(
                Label("Color:", for_element="color"),
                Input(type="color", id="color", name="color", value="#007bff"),
            ),
            Div(
                Label("File:", for_element="file"),
                Input(type="file", id="file", name="file", accept=".jpg,.png,.pdf"),
            ),
            Div(
                Input(type="hidden", name="csrf_token", value="abc123"),
            ),
        ),
        Button("Submit", type="submit"),
        action="/submit",
        method="post",
    )

    print(form.render(pretty=True))


def checkbox_and_radio():
    """Checkbox and radio button examples."""
    print("\n=== Checkboxes and Radio Buttons ===\n")

    form = Form(
        # Checkboxes
        Fieldset(
            Legend("Select your interests:"),
            Div(
                Input(type="checkbox", id="tech", name="interests", value="tech"),
                Label("Technology", for_element="tech"),
            ),
            Div(
                Input(type="checkbox", id="sports", name="interests", value="sports"),
                Label("Sports", for_element="sports"),
            ),
            Div(
                Input(
                    type="checkbox",
                    id="music",
                    name="interests",
                    value="music",
                    checked="true",
                ),
                Label("Music", for_element="music"),
            ),
            Div(
                Input(type="checkbox", id="travel", name="interests", value="travel"),
                Label("Travel", for_element="travel"),
            ),
        ),
        # Radio buttons
        Fieldset(
            Legend("Select subscription plan:"),
            Div(
                Input(
                    type="radio", id="free", name="plan", value="free", checked="true"
                ),
                Label("Free - $0/month", for_element="free"),
            ),
            Div(
                Input(type="radio", id="basic", name="plan", value="basic"),
                Label("Basic - $9.99/month", for_element="basic"),
            ),
            Div(
                Input(type="radio", id="premium", name="plan", value="premium"),
                Label("Premium - $19.99/month", for_element="premium"),
            ),
        ),
        Button("Submit", type="submit"),
        action="/preferences",
        method="post",
    )

    print(form.render(pretty=True))


def select_elements():
    """Select dropdown examples."""
    print("\n=== Select Elements ===\n")

    form = Form(
        # Basic select
        Div(
            Label("Country:", for_element="country"),
            Select(
                Option("Select a country...", value=""),
                Option("United States", value="us"),
                Option("United Kingdom", value="uk"),
                Option("Canada", value="ca"),
                Option("Australia", value="au"),
                id="country",
                name="country",
                required="true",
            ),
            class_name="form-group",
        ),
        # Select with optgroup
        Div(
            Label("Car:", for_element="car"),
            Select(
                Optgroup(
                    Option("Volvo", value="volvo"),
                    Option("Saab", value="saab"),
                    label="Swedish Cars",
                ),
                Optgroup(
                    Option("Mercedes", value="mercedes"),
                    Option("Audi", value="audi"),
                    Option("BMW", value="bmw"),
                    label="German Cars",
                ),
                Optgroup(
                    Option("Toyota", value="toyota"),
                    Option("Honda", value="honda"),
                    label="Japanese Cars",
                ),
                id="car",
                name="car",
            ),
            class_name="form-group",
        ),
        # Multiple select
        Div(
            Label("Skills (select multiple):", for_element="skills"),
            Select(
                Option("Python", value="python"),
                Option("JavaScript", value="js"),
                Option("Go", value="go"),
                Option("Rust", value="rust"),
                Option("Java", value="java"),
                id="skills",
                name="skills",
                multiple="true",
                size="5",
            ),
            class_name="form-group",
        ),
        Button("Submit", type="submit"),
        action="/submit",
        method="post",
    )

    print(form.render(pretty=True))


def textarea_element():
    """Textarea examples."""
    print("\n=== Textarea Element ===\n")

    form = Form(
        Div(
            Label("Short bio:", for_element="bio"),
            Textarea(
                "Default text goes here...",
                id="bio",
                name="bio",
                rows="4",
                cols="50",
                placeholder="Tell us about yourself...",
            ),
            class_name="form-group",
        ),
        Div(
            Label("Feedback:", for_element="feedback"),
            Textarea(
                id="feedback",
                name="feedback",
                rows="6",
                cols="50",
                placeholder="Share your thoughts...",
                maxlength="500",
            ),
            Small("Maximum 500 characters"),
            class_name="form-group",
        ),
        Button("Submit", type="submit"),
        action="/feedback",
        method="post",
    )

    print(form.render(pretty=True))


def form_validation():
    """Form with validation attributes."""
    print("\n=== Form Validation ===\n")

    form = Form(
        Div(
            Label("Username:", for_element="username"),
            Input(
                type="text",
                id="username",
                name="username",
                required="true",
                minlength="3",
                maxlength="20",
                pattern="[a-zA-Z0-9_]+",
                title="Username can only contain letters, numbers, and underscores",
            ),
            Small("3-20 characters, letters, numbers, underscores only"),
            class_name="form-group",
        ),
        Div(
            Label("Email:", for_element="email"),
            Input(type="email", id="email", name="email", required="true"),
            class_name="form-group",
        ),
        Div(
            Label("Age:", for_element="age"),
            Input(
                type="number",
                id="age",
                name="age",
                min="18",
                max="120",
                required="true",
            ),
            Small("Must be 18 or older"),
            class_name="form-group",
        ),
        Div(
            Label("Website:", for_element="website"),
            Input(
                type="url",
                id="website",
                name="website",
                placeholder="https://example.com",
            ),
            class_name="form-group",
        ),
        Div(
            Label("Confirm agreement:", for_element="agree"),
            Input(type="checkbox", id="agree", name="agree", required="true"),
            Label("I agree to the terms and conditions", for_element="agree"),
            class_name="form-group",
        ),
        Button("Submit", type="submit"),
        action="/register",
        method="post",
        novalidate="false",  # Enable HTML5 validation
    )

    print(form.render(pretty=True))


def progress_and_meter():
    """Progress and meter elements."""
    print("\n=== Progress and Meter Elements ===\n")

    content = Div(
        H2("Progress Indicators"),
        Div(
            Label("Download progress:", for_element="download"),
            Progress(value="70", max="100", id="download"),
            Span(" 70%"),
            class_name="progress-group",
        ),
        Div(
            Label("Upload progress:", for_element="upload"),
            Progress(value="30", max="100", id="upload"),
            Span(" 30%"),
            class_name="progress-group",
        ),
        Div(
            Label("Indeterminate:", for_element="loading"),
            Progress(id="loading"),  # No value = indeterminate
            class_name="progress-group",
        ),
        H2("Meter Elements"),
        Div(
            Label("Disk usage:", for_element="disk"),
            Meter(
                value="0.6",
                min="0",
                max="1",
                low="0.3",
                high="0.7",
                optimum="0.5",
                id="disk",
            ),
            Span(" 60%"),
            class_name="meter-group",
        ),
        Div(
            Label("Battery level:", for_element="battery"),
            Meter(
                value="0.2",
                min="0",
                max="1",
                low="0.25",
                high="0.75",
                optimum="1",
                id="battery",
            ),
            Span(" 20% (Low!)"),
            class_name="meter-group",
        ),
        Div(
            Label("Score:", for_element="score"),
            Meter(
                value="85",
                min="0",
                max="100",
                low="40",
                high="80",
                optimum="100",
                id="score",
            ),
            Span(" 85 (Good!)"),
            class_name="meter-group",
        ),
    )

    print(content.render(pretty=True))


def output_element():
    """Output element example."""
    print("\n=== Output Element ===\n")

    form = Form(
        Div(
            Label("Value A:", for_element="a"),
            Input(type="range", id="a", name="a", value="50", min="0", max="100"),
        ),
        Div(
            Label("Value B:", for_element="b"),
            Input(type="number", id="b", name="b", value="50"),
        ),
        Div(
            Label("Result:", for_element="result"),
            Output(name="result", for_element="a b", id="result"),
        ),
        Paragraph(Small("Note: JavaScript needed to calculate and display result")),
        oninput="result.value=parseInt(a.value)+parseInt(b.value)",
    )

    print(form.render(pretty=True))


def datalist_element():
    """Datalist for autocomplete suggestions."""
    print("\n=== Datalist Element ===\n")

    form = Form(
        Div(
            Label("Browser:", for_element="browser"),
            Input(
                type="text",
                id="browser",
                name="browser",
                list="browsers",
                placeholder="Start typing...",
            ),
            Datalist(
                Option(value="Chrome"),
                Option(value="Firefox"),
                Option(value="Safari"),
                Option(value="Edge"),
                Option(value="Opera"),
                Option(value="Brave"),
                id="browsers",
            ),
            class_name="form-group",
        ),
        Div(
            Label("Programming Language:", for_element="language"),
            Input(
                type="text",
                id="language",
                name="language",
                list="languages",
                placeholder="Select or type...",
            ),
            Datalist(
                Option(value="Python"),
                Option(value="JavaScript"),
                Option(value="TypeScript"),
                Option(value="Go"),
                Option(value="Rust"),
                Option(value="Java"),
                Option(value="C++"),
                Option(value="Ruby"),
                id="languages",
            ),
            class_name="form-group",
        ),
        Button("Submit", type="submit"),
        action="/submit",
        method="post",
    )

    print(form.render(pretty=True))


def complex_form():
    """Complex multi-section form."""
    print("\n=== Complex Form ===\n")

    form = Form(
        H1("Job Application"),
        # Personal Information
        Fieldset(
            Legend("Personal Information"),
            Div(
                Div(
                    Label("First Name:", for_element="first-name"),
                    Input(
                        type="text", id="first-name", name="first_name", required="true"
                    ),
                ),
                Div(
                    Label("Last Name:", for_element="last-name"),
                    Input(
                        type="text", id="last-name", name="last_name", required="true"
                    ),
                ),
                class_name="form-row",
            ),
            Div(
                Label("Email:", for_element="email"),
                Input(type="email", id="email", name="email", required="true"),
            ),
            Div(
                Label("Phone:", for_element="phone"),
                Input(type="tel", id="phone", name="phone"),
            ),
        ),
        # Address
        Fieldset(
            Legend("Address"),
            Div(
                Label("Street Address:", for_element="street"),
                Input(type="text", id="street", name="street"),
            ),
            Div(
                Div(
                    Label("City:", for_element="city"),
                    Input(type="text", id="city", name="city"),
                ),
                Div(
                    Label("State:", for_element="state"),
                    Select(
                        Option("Select state...", value=""),
                        Option("California", value="CA"),
                        Option("New York", value="NY"),
                        Option("Texas", value="TX"),
                        id="state",
                        name="state",
                    ),
                ),
                Div(
                    Label("ZIP:", for_element="zip"),
                    Input(type="text", id="zip", name="zip", pattern="[0-9]{5}"),
                ),
                class_name="form-row",
            ),
        ),
        # Position
        Fieldset(
            Legend("Position Details"),
            Div(
                Label("Position Applied For:", for_element="position"),
                Select(
                    Option("Select position...", value=""),
                    Option("Software Engineer", value="swe"),
                    Option("Product Manager", value="pm"),
                    Option("Designer", value="design"),
                    Option("Data Scientist", value="ds"),
                    id="position",
                    name="position",
                    required="true",
                ),
            ),
            Div(
                Label("Desired Salary:", for_element="salary"),
                Input(type="number", id="salary", name="salary", min="0", step="1000"),
            ),
            Div(
                Label("Start Date:", for_element="start-date"),
                Input(type="date", id="start-date", name="start_date"),
            ),
        ),
        # Experience
        Fieldset(
            Legend("Experience"),
            Div(
                Label("Years of Experience:", for_element="experience"),
                Input(
                    type="range",
                    id="experience",
                    name="experience",
                    min="0",
                    max="20",
                    value="5",
                ),
                Output(id="exp-output", for_element="experience"),
            ),
            Div(
                Label("Cover Letter:", for_element="cover"),
                Textarea(
                    id="cover",
                    name="cover_letter",
                    rows="6",
                    placeholder="Tell us why you'd be a great fit...",
                ),
            ),
            Div(
                Label("Resume:", for_element="resume"),
                Input(
                    type="file", id="resume", name="resume", accept=".pdf,.doc,.docx"
                ),
            ),
        ),
        # Submit
        Div(
            Div(
                Input(type="checkbox", id="terms", name="terms", required="true"),
                Label("I agree to the terms and conditions", for_element="terms"),
            ),
            Div(
                Button("Submit Application", type="submit"),
                Button("Clear Form", type="reset"),
                class_name="form-actions",
            ),
        ),
        action="/apply",
        method="post",
        enctype="multipart/form-data",
    )

    print(form.render(pretty=True))


def dynamic_form():
    """Building forms dynamically."""
    print("\n=== Dynamic Form ===\n")

    # Define form fields as data
    fields = [
        {"name": "username", "type": "text", "label": "Username", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "age", "type": "number", "label": "Age", "min": 18, "max": 120},
        {"name": "bio", "type": "textarea", "label": "Bio", "rows": 4},
        {"name": "newsletter", "type": "checkbox", "label": "Subscribe to newsletter"},
    ]

    def build_field(field):
        """Build a form field from a dictionary definition."""
        field_id = f"field-{field['name']}"

        if field["type"] == "textarea":
            input_el = Textarea(
                id=field_id, name=field["name"], rows=str(field.get("rows", 4))
            )
        elif field["type"] == "checkbox":
            return Div(
                Input(type="checkbox", id=field_id, name=field["name"]),
                Label(field["label"], for_element=field_id),
                class_name="form-group checkbox-group",
            )
        else:
            attrs = {"type": field["type"], "id": field_id, "name": field["name"]}
            if field.get("required"):
                attrs["required"] = "true"
            if "min" in field:
                attrs["min"] = str(field["min"])
            if "max" in field:
                attrs["max"] = str(field["max"])

            input_el = Input(**attrs)

        return Div(
            Label(f"{field['label']}:", for_element=field_id),
            input_el,
            class_name="form-group",
        )

    # Build form dynamically
    form = Form(
        H2("Dynamic Form"),
        *[build_field(f) for f in fields],
        Button("Submit", type="submit"),
        action="/submit",
        method="post",
    )

    print(form.render(pretty=True))


if __name__ == "__main__":
    basic_form()
    input_types()
    checkbox_and_radio()
    select_elements()
    textarea_element()
    form_validation()
    progress_and_meter()
    output_element()
    datalist_element()
    complex_form()
    dynamic_form()
