import unittest

from nitro_ui import Button, Div, Form, Input, Span
from nitro_ui.tags.text import Href


class TestHTMXAttributes(unittest.TestCase):
    """Test that HTMX attributes work correctly with NitroUI."""

    def test_hx_get(self):
        """Test hx-get attribute."""
        btn = Button("Load", hx_get="/items")
        self.assertIn('hx-get="/items"', str(btn))

    def test_hx_post(self):
        """Test hx-post attribute."""
        btn = Button("Submit", hx_post="/submit")
        self.assertIn('hx-post="/submit"', str(btn))

    def test_hx_put(self):
        """Test hx-put attribute."""
        btn = Button("Update", hx_put="/items/1")
        self.assertIn('hx-put="/items/1"', str(btn))

    def test_hx_patch(self):
        """Test hx-patch attribute."""
        btn = Button("Patch", hx_patch="/items/1")
        self.assertIn('hx-patch="/items/1"', str(btn))

    def test_hx_delete(self):
        """Test hx-delete attribute."""
        btn = Button("Delete", hx_delete="/items/1")
        self.assertIn('hx-delete="/items/1"', str(btn))

    def test_hx_target(self):
        """Test hx-target attribute."""
        btn = Button("Load", hx_get="/items", hx_target="#list")
        self.assertIn('hx-target="#list"', str(btn))

    def test_hx_swap(self):
        """Test hx-swap attribute."""
        btn = Button("Load", hx_get="/items", hx_swap="outerHTML")
        self.assertIn('hx-swap="outerHTML"', str(btn))

    def test_hx_trigger(self):
        """Test hx-trigger attribute."""
        inp = Input(
            type="text", hx_get="/search", hx_trigger="keyup changed delay:500ms"
        )
        self.assertIn('hx-trigger="keyup changed delay:500ms"', str(inp))

    def test_hx_confirm(self):
        """Test hx-confirm attribute."""
        btn = Button("Delete", hx_delete="/items/1", hx_confirm="Are you sure?")
        self.assertIn('hx-confirm="Are you sure?"', str(btn))

    def test_hx_indicator(self):
        """Test hx-indicator attribute."""
        btn = Button("Load", hx_get="/items", hx_indicator="#spinner")
        self.assertIn('hx-indicator="#spinner"', str(btn))

    def test_hx_push_url(self):
        """Test hx-push-url attribute."""
        link = Href("Page 2", href="#", hx_get="/page/2", hx_push_url="true")
        self.assertIn('hx-push-url="true"', str(link))

    def test_hx_select(self):
        """Test hx-select attribute."""
        btn = Button("Load", hx_get="/items", hx_select="#content")
        self.assertIn('hx-select="#content"', str(btn))

    def test_hx_select_oob(self):
        """Test hx-select-oob attribute."""
        btn = Button("Load", hx_get="/items", hx_select_oob="#sidebar")
        self.assertIn('hx-select-oob="#sidebar"', str(btn))

    def test_hx_swap_oob(self):
        """Test hx-swap-oob attribute."""
        div = Div("Updated", id="notification", hx_swap_oob="true")
        self.assertIn('hx-swap-oob="true"', str(div))

    def test_hx_vals(self):
        """Test hx-vals attribute with JSON."""
        btn = Button("Submit", hx_post="/submit", hx_vals='{"key": "value"}')
        self.assertIn('hx-vals="{&quot;key&quot;: &quot;value&quot;}"', str(btn))

    def test_hx_boost(self):
        """Test hx-boost attribute."""
        link = Href("About", href="/about", hx_boost="true")
        self.assertIn('hx-boost="true"', str(link))

    def test_hx_include(self):
        """Test hx-include attribute."""
        btn = Button("Submit", hx_post="/submit", hx_include="[name='csrf']")
        self.assertIn('hx-include="[name=', str(btn))

    def test_hx_params(self):
        """Test hx-params attribute."""
        btn = Button("Submit", hx_post="/submit", hx_params="*")
        self.assertIn('hx-params="*"', str(btn))

    def test_hx_preserve(self):
        """Test hx-preserve attribute."""
        inp = Input(type="text", id="search", hx_preserve="true")
        self.assertIn('hx-preserve="true"', str(inp))

    def test_hx_disable(self):
        """Test hx-disable attribute."""
        btn = Button("Submit", hx_post="/submit", hx_disable="true")
        self.assertIn('hx-disable="true"', str(btn))

    def test_multiple_hx_attributes(self):
        """Test multiple HTMX attributes together."""
        btn = Button(
            "Load More",
            hx_get="/items",
            hx_target="#list",
            hx_swap="beforeend",
            hx_indicator="#spinner",
        )
        rendered = str(btn)
        self.assertIn('hx-get="/items"', rendered)
        self.assertIn('hx-target="#list"', rendered)
        self.assertIn('hx-swap="beforeend"', rendered)
        self.assertIn('hx-indicator="#spinner"', rendered)

    def test_hx_with_other_attributes(self):
        """Test HTMX attributes alongside regular HTML attributes."""
        btn = Button(
            "Delete",
            id="delete-btn",
            cls="btn btn-danger",
            hx_delete="/items/1",
            hx_confirm="Are you sure?",
            disabled=True,
        )
        rendered = str(btn)
        self.assertIn('id="delete-btn"', rendered)
        self.assertIn('class="btn btn-danger"', rendered)
        self.assertIn('hx-delete="/items/1"', rendered)
        self.assertIn('hx-confirm="Are you sure?"', rendered)

    def test_form_with_htmx(self):
        """Test form with HTMX attributes."""
        form = Form(
            Input(
                type="text",
                name="query",
                hx_get="/search",
                hx_trigger="keyup changed delay:300ms",
                hx_target="#results",
            ),
            Div(id="results"),
            hx_boost="true",
        )
        rendered = str(form)
        self.assertIn('hx-boost="true"', rendered)
        self.assertIn('hx-get="/search"', rendered)
        self.assertIn('hx-trigger="keyup changed delay:300ms"', rendered)


class TestHTMXExtensions(unittest.TestCase):
    """Test HTMX extension attributes."""

    def test_hx_ext(self):
        """Test hx-ext attribute for extensions."""
        div = Div(hx_ext="json-enc")
        self.assertIn('hx-ext="json-enc"', str(div))

    def test_sse_connect(self):
        """Test SSE extension attributes."""
        div = Div(hx_ext="sse", sse_connect="/events")
        self.assertIn('sse-connect="/events"', str(div))

    def test_ws_connect(self):
        """Test WebSocket extension attributes."""
        div = Div(hx_ext="ws", ws_connect="/ws")
        self.assertIn('ws-connect="/ws"', str(div))


if __name__ == "__main__":
    unittest.main()
