"""Framework integration examples for NitroUI.

This module demonstrates integrating NitroUI with popular Python web frameworks:
- FastAPI
- Flask
- Django
- Starlette
- ASGI/WSGI patterns
"""

from nitro_ui import *


# =============================================================================
# SHARED COMPONENTS
# =============================================================================


def base_layout(title, *content):
    """Shared base layout for all frameworks."""
    return HTML(
        Head(
            Title(title),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            HtmlLink(rel="stylesheet", href="/static/styles.css"),
            Style(
                """
                body { font-family: system-ui, sans-serif; margin: 0; padding: 0; }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                .nav { background: #333; padding: 10px 20px; }
                .nav a { color: white; margin-right: 20px; text-decoration: none; }
                .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 20px; margin: 10px 0; }
            """
            ),
        ),
        Body(
            Nav(
                Link("Home", href="/", class_name="nav-link"),
                Link("Users", href="/users", class_name="nav-link"),
                Link("API", href="/api/status", class_name="nav-link"),
                class_name="nav",
            ),
            Main(Div(*content, class_name="container")),
            Footer(Paragraph("Powered by NitroUI"), class_name="container"),
        ),
    )


def user_card(user):
    """Reusable user card component."""
    return Div(
        H3(user["name"]),
        Paragraph(f"Email: {user['email']}"),
        Paragraph(f"Role: {user['role']}"),
        Link("View Profile", href=f"/users/{user['id']}"),
        class_name="card",
    )


def error_page(code, message):
    """Error page template."""
    return base_layout(
        f"Error {code}",
        Div(
            H1(f"Error {code}"),
            Paragraph(message),
            Link("Go Home", href="/"),
            class_name="error-page",
        ),
    )


# =============================================================================
# FASTAPI INTEGRATION
# =============================================================================


def fastapi_example():
    """FastAPI integration example."""
    print("=== FastAPI Integration ===\n")

    code = '''
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from nitro_ui import *

app = FastAPI()

# Sample data
users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "User"},
]

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page."""
    page = HTML(
        Head(Title("Home - FastAPI + NitroUI")),
        Body(
            H1("Welcome to FastAPI + NitroUI"),
            Paragraph("Build HTML with Python, not templates."),
            Link("View Users", href="/users")
        )
    )
    return page.render()


@app.get("/users", response_class=HTMLResponse)
async def list_users():
    """List all users."""
    page = HTML(
        Head(Title("Users")),
        Body(
            H1("Users"),
            Div(
                *[
                    Div(
                        H3(user["name"]),
                        Paragraph(f"Email: {user['email']}"),
                        Link("View", href=f"/users/{user['id']}"),
                        class_name="card"
                    )
                    for user in users_db
                ]
            )
        )
    )
    return page.render()


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(user_id: int):
    """Get user by ID."""
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return HTMLResponse(
            HTML(
                Head(Title("Not Found")),
                Body(H1("User Not Found"))
            ).render(),
            status_code=404
        )

    page = HTML(
        Head(Title(f"User: {user['name']}")),
        Body(
            H1(user["name"]),
            Paragraph(f"Email: {user['email']}"),
            Paragraph(f"Role: {user['role']}"),
            Link("Back to Users", href="/users")
        )
    )
    return page.render()


@app.get("/api/status")
async def api_status():
    """JSON API endpoint (NitroUI not needed here)."""
    return {"status": "ok", "users_count": len(users_db)}


# Run with: uvicorn main:app --reload
'''

    print(code)


# =============================================================================
# FLASK INTEGRATION
# =============================================================================


def flask_example():
    """Flask integration example."""
    print("\n=== Flask Integration ===\n")

    code = '''
from flask import Flask, request, abort
from nitro_ui import *

app = Flask(__name__)

# Sample data
products = [
    {"id": 1, "name": "Widget", "price": 9.99},
    {"id": 2, "name": "Gadget", "price": 19.99},
    {"id": 3, "name": "Gizmo", "price": 14.99},
]


def layout(title, *content):
    """Base layout function."""
    return HTML(
        Head(
            Title(title),
            Meta(charset="utf-8"),
            HtmlLink(rel="stylesheet", href="/static/style.css")
        ),
        Body(
            Header(
                Nav(
                    Link("Home", href="/"),
                    Link("Products", href="/products"),
                    Link("About", href="/about")
                )
            ),
            Main(*content),
            Footer(Paragraph("Flask + NitroUI"))
        )
    ).render()


@app.route("/")
def home():
    return layout(
        "Home",
        H1("Welcome to Flask + NitroUI"),
        Paragraph("A lightweight way to build HTML in Python.")
    )


@app.route("/products")
def list_products():
    return layout(
        "Products",
        H1("Products"),
        Table(
            TableHeader(
                TableRow(
                    TableHeaderCell("Name"),
                    TableHeaderCell("Price"),
                    TableHeaderCell("Action")
                )
            ),
            TableBody(
                *[
                    TableRow(
                        TableDataCell(p["name"]),
                        TableDataCell(f"${p['price']:.2f}"),
                        TableDataCell(Link("View", href=f"/products/{p['id']}"))
                    )
                    for p in products
                ]
            )
        )
    )


@app.route("/products/<int:product_id>")
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        abort(404)

    return layout(
        product["name"],
        H1(product["name"]),
        Paragraph(f"Price: ${product['price']:.2f}"),
        Link("Back to Products", href="/products")
    )


@app.errorhandler(404)
def not_found(error):
    return layout(
        "Not Found",
        H1("404 - Page Not Found"),
        Paragraph("The page you requested could not be found."),
        Link("Go Home", href="/")
    ), 404


if __name__ == "__main__":
    app.run(debug=True)
'''

    print(code)


# =============================================================================
# DJANGO INTEGRATION
# =============================================================================


def django_example():
    """Django integration example."""
    print("\n=== Django Integration ===\n")

    code = '''
# views.py
from django.http import HttpResponse
from django.views import View
from nitro_ui import *


def layout(title, *content):
    """Base layout for Django views."""
    return HTML(
        Head(
            Title(title),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            # Django static files
            HtmlLink(rel="stylesheet", href="/static/css/styles.css")
        ),
        Body(
            Header(
                Nav(
                    Link("Home", href="/"),
                    Link("Articles", href="/articles/"),
                    Link("Contact", href="/contact/")
                )
            ),
            Main(Div(*content, class_name="container")),
            Footer(Paragraph("Django + NitroUI"))
        )
    )


def home(request):
    """Function-based view."""
    page = layout(
        "Home",
        H1("Welcome"),
        Paragraph("Django with NitroUI for HTML generation.")
    )
    return HttpResponse(page.render())


def article_list(request):
    """View with database query."""
    from .models import Article  # Your Django model

    articles = Article.objects.all()[:10]

    page = layout(
        "Articles",
        H1("Latest Articles"),
        Div(
            *[
                Article(
                    H2(Link(a.title, href=f"/articles/{a.id}/")),
                    Paragraph(a.excerpt),
                    Small(f"Published: {a.published_date}")
                )
                for a in articles
            ]
        )
    )
    return HttpResponse(page.render())


class ArticleDetailView(View):
    """Class-based view."""

    def get(self, request, article_id):
        from .models import Article
        from django.shortcuts import get_object_or_404

        article = get_object_or_404(Article, id=article_id)

        page = layout(
            article.title,
            Article(
                H1(article.title),
                Paragraph(article.content),
                Small(f"By {article.author} on {article.published_date}"),
                Link("Back to Articles", href="/articles/")
            )
        )
        return HttpResponse(page.render())


def contact(request):
    """View with form."""
    if request.method == "POST":
        # Handle form submission
        message = "Thank you for your message!"
    else:
        message = None

    form_content = Form(
        Div(
            Label("Name:", for_element="name"),
            Input(type="text", id="name", name="name", required="true"),
            class_name="form-group"
        ),
        Div(
            Label("Email:", for_element="email"),
            Input(type="email", id="email", name="email", required="true"),
            class_name="form-group"
        ),
        Div(
            Label("Message:", for_element="message"),
            Textarea(id="message", name="message", rows="5", required="true"),
            class_name="form-group"
        ),
        # Django CSRF token placeholder - use template tag in real app
        Input(type="hidden", name="csrfmiddlewaretoken", value="{{ csrf_token }}"),
        Button("Send", type="submit"),
        action="/contact/",
        method="post"
    )

    content = [H1("Contact Us")]
    if message:
        content.append(Paragraph(message, class_name="success-message"))
    content.append(form_content)

    page = layout("Contact", *content)
    return HttpResponse(page.render())


# urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("articles/", views.article_list, name="article_list"),
    path("articles/<int:article_id>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("contact/", views.contact, name="contact"),
]
"""
'''

    print(code)


# =============================================================================
# STARLETTE INTEGRATION
# =============================================================================


def starlette_example():
    """Starlette integration example."""
    print("\n=== Starlette Integration ===\n")

    code = """
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from nitro_ui import *


def layout(title, *content):
    return HTML(
        Head(Title(title)),
        Body(*content)
    ).render()


async def homepage(request):
    html = layout(
        "Home",
        H1("Welcome to Starlette + NitroUI"),
        Paragraph("ASGI at its finest.")
    )
    return HTMLResponse(html)


async def user_page(request):
    user_id = request.path_params["user_id"]
    html = layout(
        f"User {user_id}",
        H1(f"User Profile: {user_id}"),
        Link("Back", href="/")
    )
    return HTMLResponse(html)


async def not_found(request, exc):
    html = layout(
        "Not Found",
        H1("404 - Not Found"),
        Paragraph("Page does not exist."),
        Link("Home", href="/")
    )
    return HTMLResponse(html, status_code=404)


routes = [
    Route("/", homepage),
    Route("/users/{user_id:int}", user_page),
]

exception_handlers = {
    404: not_found
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)

# Run with: uvicorn main:app
"""

    print(code)


# =============================================================================
# HTMX INTEGRATION
# =============================================================================


def htmx_example():
    """HTMX integration example."""
    print("\n=== HTMX Integration ===\n")

    code = '''
"""
NitroUI works great with HTMX for dynamic updates.
This example shows how to build HTMX-powered components.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nitro_ui import *

app = FastAPI()


def base_page(title, *content):
    """Base page with HTMX script."""
    return HTML(
        Head(
            Title(title),
            # Include HTMX
            Script(src="https://unpkg.com/htmx.org@1.9.10")
        ),
        Body(*content)
    )


@app.get("/", response_class=HTMLResponse)
async def home():
    page = base_page(
        "HTMX Demo",
        H1("HTMX + NitroUI"),

        # Button that loads content via HTMX
        Button(
            "Load Users",
            hx_get="/api/users",
            hx_target="#user-list",
            hx_swap="innerHTML"
        ),

        # Container for dynamic content
        Div(id="user-list"),

        # Form with HTMX submission
        Form(
            Input(type="text", name="search", placeholder="Search..."),
            Button("Search", type="submit"),
            hx_post="/api/search",
            hx_target="#results",
            hx_trigger="submit"
        ),

        Div(id="results")
    )
    return page.render()


@app.get("/api/users", response_class=HTMLResponse)
async def get_users():
    """Return HTML fragment for HTMX."""
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]

    # Return just the HTML fragment, not a full page
    fragment = UnorderedList(
        *[
            ListItem(
                Span(user["name"]),
                Button(
                    "Delete",
                    hx_delete=f"/api/users/{user['id']}",
                    hx_target="closest li",
                    hx_swap="outerHTML"
                )
            )
            for user in users
        ]
    )
    return fragment.render()


@app.delete("/api/users/{user_id}", response_class=HTMLResponse)
async def delete_user(user_id: int):
    """Delete user and return empty response."""
    # In real app, delete from database
    return ""  # Empty response removes the element


@app.post("/api/search", response_class=HTMLResponse)
async def search(search: str = ""):
    """Search and return results fragment."""
    # Simulated search results
    results = [f"Result for '{search}' #{i}" for i in range(1, 4)]

    fragment = UnorderedList(
        *[ListItem(r) for r in results]
    )
    return fragment.render()
'''

    print(code)


# =============================================================================
# API WITH HTML RESPONSES
# =============================================================================


def api_html_responses():
    """Building HTML responses for APIs."""
    print("\n=== API HTML Responses ===\n")

    code = '''
"""
Sometimes APIs need to return HTML (e.g., for web crawlers, email, or embeds).
NitroUI makes this clean and type-safe.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from nitro_ui import *

app = FastAPI()


def accept_html(request: Request) -> bool:
    """Check if client accepts HTML."""
    accept = request.headers.get("accept", "")
    return "text/html" in accept


@app.get("/api/product/{product_id}")
async def get_product(product_id: int, request: Request):
    """Return JSON or HTML based on Accept header."""
    product = {
        "id": product_id,
        "name": "Widget Pro",
        "price": 29.99,
        "description": "The best widget money can buy."
    }

    if accept_html(request):
        # Return HTML for browsers/crawlers
        page = HTML(
            Head(
                Title(product["name"]),
                Meta(property="og:title", content=product["name"]),
                Meta(property="og:description", content=product["description"]),
            ),
            Body(
                H1(product["name"]),
                Paragraph(product["description"]),
                Paragraph(f"Price: ${product['price']:.2f}"),
                Script(src="/static/app.js")  # Client-side app takes over
            )
        )
        return HTMLResponse(page.render())
    else:
        # Return JSON for API clients
        return JSONResponse(product)


@app.get("/embed/product/{product_id}", response_class=HTMLResponse)
async def embed_product(product_id: int):
    """Embeddable product widget."""
    product = {"name": "Widget", "price": 29.99}

    widget = Div(
        H3(product["name"]),
        Paragraph(f"${product['price']:.2f}"),
        Link("Buy Now", href=f"https://yoursite.com/products/{product_id}"),
        class_name="product-widget"
    ).add_styles({
        "border": "1px solid #ddd",
        "padding": "16px",
        "border-radius": "8px",
        "font-family": "system-ui, sans-serif"
    })

    return widget.render()


@app.get("/email/welcome/{user_id}", response_class=HTMLResponse)
async def welcome_email(user_id: int):
    """Generate HTML email content."""
    user = {"name": "Alice", "email": "alice@example.com"}

    # Emails need inline styles (no external CSS)
    email = HTML(
        Head(
            Title("Welcome!"),
            Meta(charset="utf-8")
        ),
        Body(
            Table(
                TableRow(
                    TableDataCell(
                        H1("Welcome, " + user["name"] + "!"),
                        Paragraph("Thanks for signing up."),
                        Paragraph("Click below to get started:"),
                        Link(
                            "Get Started",
                            href="https://yoursite.com/onboard"
                        ).add_styles({
                            "display": "inline-block",
                            "background": "#007bff",
                            "color": "white",
                            "padding": "12px 24px",
                            "text-decoration": "none",
                            "border-radius": "4px"
                        }),
                        Paragraph("Best,"),
                        Paragraph("The Team")
                    ).add_style("padding", "20px")
                )
            ).add_styles({
                "max-width": "600px",
                "margin": "0 auto",
                "font-family": "Arial, sans-serif"
            })
        ).add_style("background", "#f4f4f4")
    )

    return email.render()
'''

    print(code)


# =============================================================================
# DEMONSTRATION OUTPUT
# =============================================================================


def demo_output():
    """Generate sample output."""
    print("\n=== Sample HTML Output ===\n")

    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "User"},
    ]

    page = base_layout(
        "Users - Demo", H1("User List"), Div(*[user_card(u) for u in users])
    )

    print("Generated HTML:")
    print(page.render(pretty=True))


if __name__ == "__main__":
    print("=" * 60)
    print("FRAMEWORK INTEGRATION EXAMPLES")
    print("=" * 60)
    print()
    print("These examples show how to integrate NitroUI with various")
    print("Python web frameworks. Copy the relevant code to your project.")
    print()

    fastapi_example()
    flask_example()
    django_example()
    starlette_example()
    htmx_example()
    api_html_responses()
    demo_output()
