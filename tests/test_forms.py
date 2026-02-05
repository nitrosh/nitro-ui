import unittest

from nitro_ui import Field, Form, Button
from nitro_ui.core.fragment import Fragment
from nitro_ui.tags.layout import Div


class TestFieldText(unittest.TestCase):
    """Test text input fields."""

    def test_text_basic(self):
        """Test basic text field."""
        field = Field.text("username")
        rendered = str(field)
        self.assertIn('type="text"', rendered)
        self.assertIn('id="username"', rendered)
        self.assertIn('name="username"', rendered)

    def test_text_with_label(self):
        """Test text field with label."""
        field = Field.text("username", label="Username")
        rendered = str(field)
        self.assertIn('<label for="username">Username</label>', rendered)
        self.assertIn("<input", rendered)

    def test_text_required(self):
        """Test required text field."""
        field = Field.text("username", required=True)
        self.assertIn("required", str(field))

    def test_text_min_max_length(self):
        """Test text field with length constraints."""
        field = Field.text("username", min_length=3, max_length=20)
        rendered = str(field)
        self.assertIn('minlength="3"', rendered)
        self.assertIn('maxlength="20"', rendered)

    def test_text_pattern(self):
        """Test text field with pattern."""
        field = Field.text("username", pattern="[a-z]+")
        self.assertIn('pattern="[a-z]+"', str(field))

    def test_text_placeholder(self):
        """Test text field with placeholder."""
        field = Field.text("username", placeholder="Enter username")
        self.assertIn('placeholder="Enter username"', str(field))

    def test_text_value(self):
        """Test text field with default value."""
        field = Field.text("username", value="john")
        self.assertIn('value="john"', str(field))

    def test_text_custom_id(self):
        """Test text field with custom id."""
        field = Field.text("user_name", id="username-input", label="Username")
        rendered = str(field)
        self.assertIn('id="username-input"', rendered)
        self.assertIn('name="user_name"', rendered)
        self.assertIn('for="username-input"', rendered)


class TestFieldEmail(unittest.TestCase):
    """Test email input fields."""

    def test_email_basic(self):
        """Test basic email field."""
        field = Field.email("email")
        rendered = str(field)
        self.assertIn('type="email"', rendered)
        self.assertIn('name="email"', rendered)

    def test_email_with_all_options(self):
        """Test email field with all options."""
        field = Field.email(
            "email", label="Email", required=True, placeholder="you@example.com"
        )
        rendered = str(field)
        self.assertIn('<label for="email">Email</label>', rendered)
        self.assertIn('type="email"', rendered)
        self.assertIn("required", rendered)
        self.assertIn('placeholder="you@example.com"', rendered)


class TestFieldPassword(unittest.TestCase):
    """Test password input fields."""

    def test_password_basic(self):
        """Test basic password field."""
        field = Field.password("password")
        self.assertIn('type="password"', str(field))

    def test_password_min_length(self):
        """Test password field with min length."""
        field = Field.password("password", min_length=8)
        self.assertIn('minlength="8"', str(field))


class TestFieldUrl(unittest.TestCase):
    """Test URL input fields."""

    def test_url_basic(self):
        """Test basic URL field."""
        field = Field.url("website")
        self.assertIn('type="url"', str(field))


class TestFieldTel(unittest.TestCase):
    """Test telephone input fields."""

    def test_tel_basic(self):
        """Test basic tel field."""
        field = Field.tel("phone")
        self.assertIn('type="tel"', str(field))

    def test_tel_pattern(self):
        """Test tel field with pattern."""
        field = Field.tel("phone", pattern="[0-9]{3}-[0-9]{4}")
        self.assertIn('pattern="[0-9]{3}-[0-9]{4}"', str(field))


class TestFieldSearch(unittest.TestCase):
    """Test search input fields."""

    def test_search_basic(self):
        """Test basic search field."""
        field = Field.search("q")
        self.assertIn('type="search"', str(field))


class TestFieldTextarea(unittest.TestCase):
    """Test textarea fields."""

    def test_textarea_basic(self):
        """Test basic textarea."""
        field = Field.textarea("message")
        rendered = str(field)
        self.assertIn("<textarea", rendered)
        self.assertIn('name="message"', rendered)

    def test_textarea_rows_cols(self):
        """Test textarea with rows and cols."""
        field = Field.textarea("message", rows=5, cols=40)
        rendered = str(field)
        self.assertIn('rows="5"', rendered)
        self.assertIn('cols="40"', rendered)

    def test_textarea_value(self):
        """Test textarea with default value."""
        field = Field.textarea("message", value="Hello world")
        self.assertIn("Hello world", str(field))


class TestFieldNumber(unittest.TestCase):
    """Test number input fields."""

    def test_number_basic(self):
        """Test basic number field."""
        field = Field.number("age")
        self.assertIn('type="number"', str(field))

    def test_number_min_max(self):
        """Test number field with min/max."""
        field = Field.number("age", min=0, max=120)
        rendered = str(field)
        self.assertIn('min="0"', rendered)
        self.assertIn('max="120"', rendered)

    def test_number_step(self):
        """Test number field with step."""
        field = Field.number("price", step=0.01)
        self.assertIn('step="0.01"', str(field))


class TestFieldRange(unittest.TestCase):
    """Test range input fields."""

    def test_range_basic(self):
        """Test basic range field."""
        field = Field.range("volume")
        rendered = str(field)
        self.assertIn('type="range"', rendered)
        self.assertIn('min="0"', rendered)
        self.assertIn('max="100"', rendered)

    def test_range_custom_min_max(self):
        """Test range field with custom min/max."""
        field = Field.range("brightness", min=1, max=10)
        rendered = str(field)
        self.assertIn('min="1"', rendered)
        self.assertIn('max="10"', rendered)


class TestFieldDate(unittest.TestCase):
    """Test date input fields."""

    def test_date_basic(self):
        """Test basic date field."""
        field = Field.date("birthdate")
        self.assertIn('type="date"', str(field))

    def test_date_min_max(self):
        """Test date field with min/max."""
        field = Field.date("birthdate", min="1900-01-01", max="2020-12-31")
        rendered = str(field)
        self.assertIn('min="1900-01-01"', rendered)
        self.assertIn('max="2020-12-31"', rendered)


class TestFieldTime(unittest.TestCase):
    """Test time input fields."""

    def test_time_basic(self):
        """Test basic time field."""
        field = Field.time("appointment")
        self.assertIn('type="time"', str(field))


class TestFieldDatetimeLocal(unittest.TestCase):
    """Test datetime-local input fields."""

    def test_datetime_local_basic(self):
        """Test basic datetime-local field."""
        field = Field.datetime_local("meeting")
        self.assertIn('type="datetime-local"', str(field))


class TestFieldSelect(unittest.TestCase):
    """Test select fields."""

    def test_select_string_options(self):
        """Test select with string options."""
        field = Field.select("country", ["USA", "Canada", "Mexico"])
        rendered = str(field)
        self.assertIn("<select", rendered)
        self.assertIn('<option value="USA">USA</option>', rendered)
        self.assertIn('<option value="Canada">Canada</option>', rendered)
        self.assertIn('<option value="Mexico">Mexico</option>', rendered)

    def test_select_tuple_options(self):
        """Test select with tuple options."""
        field = Field.select("status", [("active", "Active"), ("inactive", "Inactive")])
        rendered = str(field)
        self.assertIn('<option value="active">Active</option>', rendered)
        self.assertIn('<option value="inactive">Inactive</option>', rendered)

    def test_select_dict_options(self):
        """Test select with dict options."""
        field = Field.select(
            "priority",
            [
                {"value": "1", "label": "Low"},
                {"value": "2", "label": "High", "disabled": True},
            ],
        )
        rendered = str(field)
        self.assertIn('<option value="1">Low</option>', rendered)
        self.assertIn("disabled", rendered)

    def test_select_with_value(self):
        """Test select with pre-selected value."""
        field = Field.select("country", ["USA", "Canada"], value="Canada")
        self.assertIn("selected", str(field))

    def test_select_with_label(self):
        """Test select with label."""
        field = Field.select("country", ["USA", "Canada"], label="Country")
        rendered = str(field)
        self.assertIn('<label for="country">Country</label>', rendered)


class TestFieldCheckbox(unittest.TestCase):
    """Test checkbox fields."""

    def test_checkbox_basic(self):
        """Test basic checkbox."""
        field = Field.checkbox("subscribe")
        rendered = str(field)
        self.assertIn('type="checkbox"', rendered)
        self.assertIn('name="subscribe"', rendered)
        self.assertIn('value="on"', rendered)

    def test_checkbox_checked(self):
        """Test checked checkbox."""
        field = Field.checkbox("subscribe", checked=True)
        self.assertIn("checked", str(field))

    def test_checkbox_with_label(self):
        """Test checkbox with label wrapping input."""
        field = Field.checkbox("subscribe", label="Subscribe to newsletter")
        rendered = str(field)
        self.assertIn("<label>", rendered)
        self.assertIn("Subscribe to newsletter", rendered)
        # Label wraps input, with input first
        self.assertIn("<label><input", rendered)
        self.assertIn("</label>", rendered)

    def test_checkbox_custom_value(self):
        """Test checkbox with custom value."""
        field = Field.checkbox("agree", value="yes")
        self.assertIn('value="yes"', str(field))

    def test_checkbox_required(self):
        """Test required checkbox."""
        field = Field.checkbox("terms", required=True)
        self.assertIn("required", str(field))


class TestFieldRadio(unittest.TestCase):
    """Test radio button fields."""

    def test_radio_basic(self):
        """Test basic radio buttons."""
        field = Field.radio("plan", [("free", "Free"), ("pro", "Pro")])
        rendered = str(field)
        self.assertIn("<fieldset", rendered)
        self.assertIn('type="radio"', rendered)
        self.assertIn('name="plan"', rendered)
        self.assertIn('value="free"', rendered)
        self.assertIn('value="pro"', rendered)

    def test_radio_with_legend(self):
        """Test radio buttons with legend."""
        field = Field.radio("plan", [("free", "Free")], label="Select Plan")
        rendered = str(field)
        self.assertIn("<legend>Select Plan</legend>", rendered)

    def test_radio_with_value(self):
        """Test radio buttons with pre-selected value."""
        field = Field.radio("plan", [("free", "Free"), ("pro", "Pro")], value="pro")
        # The pro option should be checked
        self.assertIn("checked", str(field))


class TestFieldFile(unittest.TestCase):
    """Test file input fields."""

    def test_file_basic(self):
        """Test basic file field."""
        field = Field.file("document")
        self.assertIn('type="file"', str(field))

    def test_file_accept(self):
        """Test file field with accept."""
        field = Field.file("image", accept="image/*")
        self.assertIn('accept="image/*"', str(field))

    def test_file_multiple(self):
        """Test file field with multiple."""
        field = Field.file("documents", multiple=True)
        self.assertIn("multiple", str(field))


class TestFieldHidden(unittest.TestCase):
    """Test hidden input fields."""

    def test_hidden_basic(self):
        """Test basic hidden field."""
        field = Field.hidden("csrf_token", "abc123")
        rendered = str(field)
        self.assertIn('type="hidden"', rendered)
        self.assertIn('name="csrf_token"', rendered)
        self.assertIn('value="abc123"', rendered)


class TestFieldColor(unittest.TestCase):
    """Test color input fields."""

    def test_color_basic(self):
        """Test basic color field."""
        field = Field.color("theme_color")
        self.assertIn('type="color"', str(field))

    def test_color_with_value(self):
        """Test color field with default value."""
        field = Field.color("theme_color", value="#ff0000")
        self.assertIn('value="#ff0000"', str(field))


class TestFieldWrapper(unittest.TestCase):
    """Test wrapper functionality."""

    def test_wrapper_string(self):
        """Test wrapper with string class name."""
        field = Field.text("username", label="Username", wrapper="form-field")
        rendered = str(field)
        self.assertIn('<div class="form-field">', rendered)
        self.assertIn("<label", rendered)
        self.assertIn("<input", rendered)
        self.assertIn("</div>", rendered)

    def test_wrapper_dict(self):
        """Test wrapper with dict attributes."""
        field = Field.text(
            "username",
            label="Username",
            wrapper={"cls": "form-group", "id": "username-field"},
        )
        rendered = str(field)
        self.assertIn('class="form-group"', rendered)
        self.assertIn('id="username-field"', rendered)

    def test_no_label_no_wrapper(self):
        """Test field without label or wrapper returns just input."""
        field = Field.text("username")
        rendered = str(field)
        self.assertTrue(rendered.startswith("<input"))
        self.assertNotIn("<div", rendered)
        self.assertNotIn("<label", rendered)


class TestFieldExtraAttrs(unittest.TestCase):
    """Test extra HTML attributes."""

    def test_extra_attrs(self):
        """Test passing extra attributes."""
        field = Field.text("username", autocomplete="off", data_validate="true")
        rendered = str(field)
        self.assertIn('autocomplete="off"', rendered)
        self.assertIn('data-validate="true"', rendered)

    def test_htmx_attrs(self):
        """Test HTMX attributes work with fields."""
        field = Field.text(
            "search", hx_get="/search", hx_trigger="keyup changed delay:300ms"
        )
        rendered = str(field)
        self.assertIn('hx-get="/search"', rendered)
        self.assertIn('hx-trigger="keyup changed delay:300ms"', rendered)


class TestFieldInForm(unittest.TestCase):
    """Test fields composing in forms."""

    def test_complete_form(self):
        """Test building a complete form with fields."""
        form = Form(
            Field.email("email", label="Email", required=True),
            Field.password("password", label="Password", min_length=8),
            Field.checkbox("remember", label="Remember me"),
            Button("Log In", type="submit"),
            action="/login",
            method="post",
        )
        rendered = str(form)
        self.assertIn("<form", rendered)
        self.assertIn('action="/login"', rendered)
        self.assertIn('method="post"', rendered)
        self.assertIn('type="email"', rendered)
        self.assertIn('type="password"', rendered)
        self.assertIn('type="checkbox"', rendered)
        self.assertIn("<button", rendered)


if __name__ == "__main__":
    unittest.main()
