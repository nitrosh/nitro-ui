"""Table examples for NitroUI.

This module demonstrates building HTML tables:
- Basic tables
- Table with header and body
- Table with footer
- Table with caption
- Column groups
- Complex table layouts
- Dynamic data tables
"""

from nitro_ui import *


def basic_table():
    """Basic table example."""
    print("=== Basic Table ===\n")

    table = Table(
        TableRow(
            TableHeaderCell("Name"), TableHeaderCell("Age"), TableHeaderCell("City")
        ),
        TableRow(
            TableDataCell("Alice"), TableDataCell("28"), TableDataCell("New York")
        ),
        TableRow(
            TableDataCell("Bob"), TableDataCell("34"), TableDataCell("Los Angeles")
        ),
        TableRow(
            TableDataCell("Charlie"), TableDataCell("22"), TableDataCell("Chicago")
        ),
    )

    print(table.render(pretty=True))


def table_with_sections():
    """Table with thead, tbody, and tfoot."""
    print("\n=== Table with Sections ===\n")

    table = Table(
        TableHeader(
            TableRow(
                TableHeaderCell("Product"),
                TableHeaderCell("Price"),
                TableHeaderCell("Quantity"),
                TableHeaderCell("Total"),
            )
        ),
        TableBody(
            TableRow(
                TableDataCell("Widget"),
                TableDataCell("$10.00"),
                TableDataCell("2"),
                TableDataCell("$20.00"),
            ),
            TableRow(
                TableDataCell("Gadget"),
                TableDataCell("$25.00"),
                TableDataCell("1"),
                TableDataCell("$25.00"),
            ),
            TableRow(
                TableDataCell("Gizmo"),
                TableDataCell("$15.00"),
                TableDataCell("3"),
                TableDataCell("$45.00"),
            ),
        ),
        TableFooter(
            TableRow(
                TableDataCell(""),
                TableDataCell(""),
                TableDataCell("Subtotal:"),
                TableDataCell("$90.00"),
            ),
            TableRow(
                TableDataCell(""),
                TableDataCell(""),
                TableDataCell("Tax (10%):"),
                TableDataCell("$9.00"),
            ),
            TableRow(
                TableDataCell(""),
                TableDataCell(""),
                TableHeaderCell("Total:"),
                TableHeaderCell("$99.00"),
            ),
        ),
    )

    print(table.render(pretty=True))


def table_with_caption():
    """Table with caption."""
    print("\n=== Table with Caption ===\n")

    table = Table(
        Caption("Monthly Sales Report - Q4 2024"),
        TableHeader(
            TableRow(
                TableHeaderCell("Month"),
                TableHeaderCell("Revenue"),
                TableHeaderCell("Growth"),
            )
        ),
        TableBody(
            TableRow(
                TableDataCell("October"),
                TableDataCell("$125,000"),
                TableDataCell("+5%"),
            ),
            TableRow(
                TableDataCell("November"),
                TableDataCell("$142,000"),
                TableDataCell("+13%"),
            ),
            TableRow(
                TableDataCell("December"),
                TableDataCell("$198,000"),
                TableDataCell("+39%"),
            ),
        ),
    )

    print(table.render(pretty=True))


def table_with_colgroup():
    """Table with column groups for styling."""
    print("\n=== Table with Column Groups ===\n")

    table = Table(
        Colgroup(
            Col(span="1", class_name="col-name"),
            Col(span="2", class_name="col-data"),
            Col(span="1", class_name="col-highlight"),
        ),
        TableHeader(
            TableRow(
                TableHeaderCell("Employee"),
                TableHeaderCell("Department"),
                TableHeaderCell("Role"),
                TableHeaderCell("Status"),
            )
        ),
        TableBody(
            TableRow(
                TableDataCell("John Smith"),
                TableDataCell("Engineering"),
                TableDataCell("Senior Developer"),
                TableDataCell("Active"),
            ),
            TableRow(
                TableDataCell("Jane Doe"),
                TableDataCell("Marketing"),
                TableDataCell("Manager"),
                TableDataCell("Active"),
            ),
            TableRow(
                TableDataCell("Bob Wilson"),
                TableDataCell("Sales"),
                TableDataCell("Representative"),
                TableDataCell("On Leave"),
            ),
        ),
    )

    print(table.render(pretty=True))


def table_with_spanning():
    """Table with rowspan and colspan."""
    print("\n=== Table with Rowspan/Colspan ===\n")

    table = Table(
        TableHeader(
            TableRow(
                TableHeaderCell("Category", rowspan="2"),
                TableHeaderCell("Q1 2024", colspan="2"),
                TableHeaderCell("Q2 2024", colspan="2"),
            ),
            TableRow(
                TableHeaderCell("Revenue"),
                TableHeaderCell("Units"),
                TableHeaderCell("Revenue"),
                TableHeaderCell("Units"),
            ),
        ),
        TableBody(
            TableRow(
                TableDataCell("Electronics"),
                TableDataCell("$50,000"),
                TableDataCell("500"),
                TableDataCell("$65,000"),
                TableDataCell("620"),
            ),
            TableRow(
                TableDataCell("Clothing"),
                TableDataCell("$30,000"),
                TableDataCell("1,200"),
                TableDataCell("$35,000"),
                TableDataCell("1,400"),
            ),
            TableRow(
                TableDataCell("Home & Garden"),
                TableDataCell("$20,000"),
                TableDataCell("300"),
                TableDataCell("$28,000"),
                TableDataCell("420"),
            ),
        ),
        TableFooter(
            TableRow(
                TableHeaderCell("Total"),
                TableDataCell("$100,000"),
                TableDataCell("2,000"),
                TableDataCell("$128,000"),
                TableDataCell("2,440"),
            )
        ),
    )

    print(table.render(pretty=True))


def styled_table():
    """Table with inline styles."""
    print("\n=== Styled Table ===\n")

    table = Table(
        TableHeader(
            TableRow(
                TableHeaderCell("Name").add_styles(
                    {"background": "#4a90d9", "color": "white", "padding": "12px"}
                ),
                TableHeaderCell("Email").add_styles(
                    {"background": "#4a90d9", "color": "white", "padding": "12px"}
                ),
                TableHeaderCell("Role").add_styles(
                    {"background": "#4a90d9", "color": "white", "padding": "12px"}
                ),
            )
        ),
        TableBody(
            TableRow(
                TableDataCell("Alice").add_style("padding", "10px"),
                TableDataCell("alice@example.com").add_style("padding", "10px"),
                TableDataCell("Admin").add_style("padding", "10px"),
            ).add_style("background", "#f8f9fa"),
            TableRow(
                TableDataCell("Bob").add_style("padding", "10px"),
                TableDataCell("bob@example.com").add_style("padding", "10px"),
                TableDataCell("User").add_style("padding", "10px"),
            ).add_style("background", "#ffffff"),
            TableRow(
                TableDataCell("Charlie").add_style("padding", "10px"),
                TableDataCell("charlie@example.com").add_style("padding", "10px"),
                TableDataCell("User").add_style("padding", "10px"),
            ).add_style("background", "#f8f9fa"),
        ),
    ).add_styles(
        {"border-collapse": "collapse", "width": "100%", "border": "1px solid #dee2e6"}
    )

    print(table.render(pretty=True))


def dynamic_data_table():
    """Building tables from dynamic data."""
    print("\n=== Dynamic Data Table ===\n")

    # Sample data
    users = [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "role": "Admin",
            "status": "Active",
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "email": "bob@example.com",
            "role": "Editor",
            "status": "Active",
        },
        {
            "id": 3,
            "name": "Charlie Brown",
            "email": "charlie@example.com",
            "role": "Viewer",
            "status": "Inactive",
        },
        {
            "id": 4,
            "name": "Diana Prince",
            "email": "diana@example.com",
            "role": "Editor",
            "status": "Active",
        },
        {
            "id": 5,
            "name": "Eve Wilson",
            "email": "eve@example.com",
            "role": "Viewer",
            "status": "Active",
        },
    ]

    columns = ["ID", "Name", "Email", "Role", "Status", "Actions"]

    def render_status_badge(status):
        """Render a status badge."""
        color = "#28a745" if status == "Active" else "#dc3545"
        return Span(status).add_styles(
            {
                "background": color,
                "color": "white",
                "padding": "2px 8px",
                "border-radius": "4px",
                "font-size": "12px",
            }
        )

    def render_actions(user_id):
        """Render action buttons."""
        return Fragment(
            Button("Edit", type="button", data_action="edit", data_id=str(user_id)),
            Button("Delete", type="button", data_action="delete", data_id=str(user_id)),
        )

    # Build table
    table = Table(
        TableHeader(TableRow(*[TableHeaderCell(col) for col in columns])),
        TableBody(
            *[
                TableRow(
                    TableDataCell(str(user["id"])),
                    TableDataCell(user["name"]),
                    TableDataCell(user["email"]),
                    TableDataCell(user["role"]),
                    TableDataCell(render_status_badge(user["status"])),
                    TableDataCell(render_actions(user["id"])),
                )
                for user in users
            ]
        ),
        class_name="data-table",
    )

    print(table.render(pretty=True))


def sortable_table():
    """Table with sortable column headers."""
    print("\n=== Sortable Table (Structure) ===\n")

    def sortable_header(text, column):
        """Create a sortable header cell."""
        return TableHeaderCell(
            Link(
                text,
                Span(" ↕", class_name="sort-icon"),
                href=f"?sort={column}",
                class_name="sortable",
            ),
            data_column=column,
        )

    table = Table(
        TableHeader(
            TableRow(
                sortable_header("Name", "name"),
                sortable_header("Date", "date"),
                sortable_header("Amount", "amount"),
                TableHeaderCell("Actions"),  # Not sortable
            )
        ),
        TableBody(
            TableRow(
                TableDataCell("Order #1001"),
                TableDataCell("2024-01-15"),
                TableDataCell("$150.00"),
                TableDataCell(Button("View", type="button")),
            ),
            TableRow(
                TableDataCell("Order #1002"),
                TableDataCell("2024-01-16"),
                TableDataCell("$275.50"),
                TableDataCell(Button("View", type="button")),
            ),
            TableRow(
                TableDataCell("Order #1003"),
                TableDataCell("2024-01-17"),
                TableDataCell("$89.99"),
                TableDataCell(Button("View", type="button")),
            ),
        ),
        class_name="sortable-table",
    )

    print(table.render(pretty=True))


def responsive_table():
    """Table wrapped for responsive display."""
    print("\n=== Responsive Table Wrapper ===\n")

    # Wrap table in a scrollable container
    container = Div(
        Table(
            TableHeader(
                TableRow(
                    TableHeaderCell("ID"),
                    TableHeaderCell("Product"),
                    TableHeaderCell("Category"),
                    TableHeaderCell("Price"),
                    TableHeaderCell("Stock"),
                    TableHeaderCell("Status"),
                    TableHeaderCell("Last Updated"),
                    TableHeaderCell("Actions"),
                )
            ),
            TableBody(
                TableRow(
                    TableDataCell("SKU-001"),
                    TableDataCell("Wireless Mouse"),
                    TableDataCell("Electronics"),
                    TableDataCell("$29.99"),
                    TableDataCell("150"),
                    TableDataCell("In Stock"),
                    TableDataCell("2024-01-15"),
                    TableDataCell(Button("Edit", type="button")),
                ),
                TableRow(
                    TableDataCell("SKU-002"),
                    TableDataCell("USB Keyboard"),
                    TableDataCell("Electronics"),
                    TableDataCell("$49.99"),
                    TableDataCell("75"),
                    TableDataCell("In Stock"),
                    TableDataCell("2024-01-14"),
                    TableDataCell(Button("Edit", type="button")),
                ),
                TableRow(
                    TableDataCell("SKU-003"),
                    TableDataCell("Monitor Stand"),
                    TableDataCell("Accessories"),
                    TableDataCell("$39.99"),
                    TableDataCell("0"),
                    TableDataCell("Out of Stock"),
                    TableDataCell("2024-01-13"),
                    TableDataCell(Button("Edit", type="button")),
                ),
            ),
        ).add_styles({"width": "100%", "border-collapse": "collapse"}),
        class_name="table-responsive",
    ).add_styles({"overflow-x": "auto", "max-width": "100%"})

    print(container.render(pretty=True))


def comparison_table():
    """Feature comparison table."""
    print("\n=== Comparison Table ===\n")

    def check_mark():
        return Span("✓").add_style("color", "#28a745")

    def x_mark():
        return Span("✗").add_style("color", "#dc3545")

    table = Table(
        Caption("Plan Comparison"),
        TableHeader(
            TableRow(
                TableHeaderCell("Feature"),
                TableHeaderCell("Free"),
                TableHeaderCell("Pro"),
                TableHeaderCell("Enterprise"),
            )
        ),
        TableBody(
            TableRow(
                TableDataCell("Basic Features"),
                TableDataCell(check_mark()),
                TableDataCell(check_mark()),
                TableDataCell(check_mark()),
            ),
            TableRow(
                TableDataCell("API Access"),
                TableDataCell(x_mark()),
                TableDataCell(check_mark()),
                TableDataCell(check_mark()),
            ),
            TableRow(
                TableDataCell("Custom Branding"),
                TableDataCell(x_mark()),
                TableDataCell(check_mark()),
                TableDataCell(check_mark()),
            ),
            TableRow(
                TableDataCell("Priority Support"),
                TableDataCell(x_mark()),
                TableDataCell(x_mark()),
                TableDataCell(check_mark()),
            ),
            TableRow(
                TableDataCell("SLA Guarantee"),
                TableDataCell(x_mark()),
                TableDataCell(x_mark()),
                TableDataCell(check_mark()),
            ),
            TableRow(
                TableDataCell("Users"),
                TableDataCell("1"),
                TableDataCell("Up to 10"),
                TableDataCell("Unlimited"),
            ),
            TableRow(
                TableDataCell("Storage"),
                TableDataCell("1 GB"),
                TableDataCell("50 GB"),
                TableDataCell("Unlimited"),
            ),
        ),
        TableFooter(
            TableRow(
                TableDataCell(""),
                TableDataCell(
                    Button("Get Started", type="button", class_name="btn-outline")
                ),
                TableDataCell(
                    Button("Start Trial", type="button", class_name="btn-primary")
                ),
                TableDataCell(
                    Button("Contact Sales", type="button", class_name="btn-enterprise")
                ),
            )
        ),
    )

    print(table.render(pretty=True))


def nested_table():
    """Table with nested tables (for complex layouts)."""
    print("\n=== Nested Table ===\n")

    table = Table(
        TableHeader(
            TableRow(TableHeaderCell("Department"), TableHeaderCell("Employees"))
        ),
        TableBody(
            TableRow(
                TableDataCell("Engineering"),
                TableDataCell(
                    Table(
                        TableRow(
                            TableDataCell("Alice"), TableDataCell("Senior Engineer")
                        ),
                        TableRow(TableDataCell("Bob"), TableDataCell("Engineer")),
                        TableRow(
                            TableDataCell("Charlie"), TableDataCell("Junior Engineer")
                        ),
                    ).add_style("width", "100%")
                ),
            ),
            TableRow(
                TableDataCell("Marketing"),
                TableDataCell(
                    Table(
                        TableRow(
                            TableDataCell("Diana"), TableDataCell("Marketing Manager")
                        ),
                        TableRow(
                            TableDataCell("Eve"), TableDataCell("Marketing Specialist")
                        ),
                    ).add_style("width", "100%")
                ),
            ),
        ),
    )

    print(table.render(pretty=True))


def schedule_table():
    """Schedule/calendar style table."""
    print("\n=== Schedule Table ===\n")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    times = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM"]

    schedule = {
        ("9:00 AM", "Monday"): "Team Standup",
        ("10:00 AM", "Monday"): "Code Review",
        ("9:00 AM", "Wednesday"): "Sprint Planning",
        ("2:00 PM", "Wednesday"): "1:1 Meeting",
        ("11:00 AM", "Friday"): "Demo",
        ("2:00 PM", "Friday"): "Retrospective",
    }

    table = Table(
        TableHeader(
            TableRow(TableHeaderCell("Time"), *[TableHeaderCell(day) for day in days])
        ),
        TableBody(
            *[
                TableRow(
                    TableDataCell(time),
                    *[
                        TableDataCell(schedule.get((time, day), "")).add_styles(
                            {
                                "background": (
                                    "#e3f2fd"
                                    if schedule.get((time, day))
                                    else "transparent"
                                ),
                                "text-align": "center",
                            }
                        )
                        for day in days
                    ],
                )
                for time in times
            ]
        ),
        class_name="schedule-table",
    ).add_styles({"width": "100%", "border-collapse": "collapse"})

    print(table.render(pretty=True))


if __name__ == "__main__":
    basic_table()
    table_with_sections()
    table_with_caption()
    table_with_colgroup()
    table_with_spanning()
    styled_table()
    dynamic_data_table()
    sortable_table()
    responsive_table()
    comparison_table()
    nested_table()
    schedule_table()
