"""Form field helpers that generate HTML5 form elements with validation attributes."""

from typing import Any, Dict, List, Optional, Union

from nitro_ui.core.element import HTMLElement
from nitro_ui.core.fragment import Fragment
from nitro_ui.tags.layout import Div
from nitro_ui.tags.form import Input, Label, Select, Option, Textarea, Fieldset, Legend


def _build_field(
    input_element: HTMLElement,
    name: str,
    label: Optional[str] = None,
    wrapper: Optional[Union[str, Dict[str, Any]]] = None,
    id: Optional[str] = None,
) -> HTMLElement:
    """Build a field with optional label and wrapper.

    Args:
        input_element: The input element to wrap
        name: Field name (used for label's for attribute if no id)
        label: Optional label text
        wrapper: Optional wrapper - string for class name, dict for attributes
        id: Optional custom id (defaults to name)

    Returns:
        HTMLElement - the input alone, with label, or wrapped in div
    """
    field_id = id or name

    # Build elements list
    elements = []

    if label:
        elements.append(Label(label, for_element=field_id))

    elements.append(input_element)

    # No label and no wrapper - just return the input
    if len(elements) == 1 and not wrapper:
        return input_element

    # Has label but no wrapper - return fragment
    if not wrapper:
        return Fragment(*elements)

    # Has wrapper - wrap in div
    if isinstance(wrapper, str):
        return Div(*elements, cls=wrapper)
    elif isinstance(wrapper, dict):
        return Div(*elements, **wrapper)
    else:
        return Div(*elements)


def _filter_none(**kwargs) -> Dict[str, Any]:
    """Filter out None values from kwargs."""
    return {k: v for k, v in kwargs.items() if v is not None}


class Field:
    """Static methods for generating HTML5 form fields with validation attributes.

    All methods return standard NitroUI elements that can be composed with
    other elements. Use the `label` parameter to add a label, and `wrapper`
    to wrap the field in a div for styling.

    Example:
        from nitro_ui import Form, Button
        from nitro_ui.forms import Field

        form = Form(
            Field.email("email", label="Email", required=True),
            Field.password("password", label="Password", min_length=8),
            Button("Log In", type="submit")
        )
    """

    # =========================================================================
    # Text Inputs
    # =========================================================================

    @staticmethod
    def text(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a text input field.

        Args:
            name: Field name and default id
            label: Optional label text
            required: Whether the field is required
            min_length: Minimum character length
            max_length: Maximum character length
            pattern: Regex pattern for validation
            placeholder: Placeholder text
            value: Default value
            wrapper: Wrapper div class name or attributes dict
            id: Custom id (defaults to name)
            **attrs: Additional HTML attributes
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="text",
            id=field_id,
            name=name,
            required=required if required else None,
            minlength=min_length,
            maxlength=max_length,
            pattern=pattern,
            placeholder=placeholder,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def email(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create an email input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="email",
            id=field_id,
            name=name,
            required=required if required else None,
            placeholder=placeholder,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def password(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        placeholder: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a password input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="password",
            id=field_id,
            name=name,
            required=required if required else None,
            minlength=min_length,
            maxlength=max_length,
            placeholder=placeholder,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def url(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a URL input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="url",
            id=field_id,
            name=name,
            required=required if required else None,
            placeholder=placeholder,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def tel(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        pattern: Optional[str] = None,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a telephone input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="tel",
            id=field_id,
            name=name,
            required=required if required else None,
            pattern=pattern,
            placeholder=placeholder,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def search(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a search input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="search",
            id=field_id,
            name=name,
            required=required if required else None,
            placeholder=placeholder,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def textarea(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        rows: Optional[int] = None,
        cols: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a textarea field."""
        field_id = id or name
        textarea_attrs = _filter_none(
            id=field_id,
            name=name,
            required=required if required else None,
            rows=rows,
            cols=cols,
            minlength=min_length,
            maxlength=max_length,
            placeholder=placeholder,
            **attrs
        )
        # Textarea takes content as children, not value attribute
        if value:
            ta = Textarea(value, **textarea_attrs)
        else:
            ta = Textarea(**textarea_attrs)
        return _build_field(ta, name, label, wrapper, id)

    # =========================================================================
    # Numeric Inputs
    # =========================================================================

    @staticmethod
    def number(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        step: Optional[Union[int, float, str]] = None,
        value: Optional[Union[int, float]] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a number input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="number",
            id=field_id,
            name=name,
            required=required if required else None,
            min=min,
            max=max,
            step=step,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def range(
        name: str,
        label: Optional[str] = None,
        min: Union[int, float] = 0,
        max: Union[int, float] = 100,
        step: Optional[Union[int, float, str]] = None,
        value: Optional[Union[int, float]] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a range slider input field."""
        field_id = id or name
        input_attrs = _filter_none(
            type="range",
            id=field_id,
            name=name,
            min=min,
            max=max,
            step=step,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    # =========================================================================
    # Date/Time Inputs
    # =========================================================================

    @staticmethod
    def date(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        min: Optional[str] = None,
        max: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a date input field.

        Args:
            min/max/value: Date strings in YYYY-MM-DD format
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="date",
            id=field_id,
            name=name,
            required=required if required else None,
            min=min,
            max=max,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def time(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        min: Optional[str] = None,
        max: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a time input field.

        Args:
            min/max/value: Time strings in HH:MM format
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="time",
            id=field_id,
            name=name,
            required=required if required else None,
            min=min,
            max=max,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def datetime_local(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        min: Optional[str] = None,
        max: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a datetime-local input field.

        Args:
            min/max/value: Datetime strings in YYYY-MM-DDTHH:MM format
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="datetime-local",
            id=field_id,
            name=name,
            required=required if required else None,
            min=min,
            max=max,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    # =========================================================================
    # Selection Inputs
    # =========================================================================

    @staticmethod
    def select(
        name: str,
        options: List[Union[str, tuple, Dict[str, Any]]],
        label: Optional[str] = None,
        required: bool = False,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a select dropdown field.

        Args:
            name: Field name
            options: List of options - can be:
                - strings: ["USA", "Canada"] - value and label are the same
                - tuples: [("us", "United States")] - (value, label)
                - dicts: [{"value": "us", "label": "United States", "disabled": True}]
            label: Optional label text
            required: Whether selection is required
            value: Pre-selected value
            wrapper: Wrapper div class name or attributes dict
            id: Custom id (defaults to name)
        """
        field_id = id or name

        # Build option elements
        option_elements = []
        for opt in options:
            if isinstance(opt, str):
                opt_value = opt
                opt_label = opt
                opt_attrs = {}
            elif isinstance(opt, tuple):
                opt_value, opt_label = opt
                opt_attrs = {}
            elif isinstance(opt, dict):
                opt_value = opt.get("value", "")
                opt_label = opt.get("label", opt_value)
                opt_attrs = {k: v for k, v in opt.items() if k not in ("value", "label")}
            else:
                continue

            # Check if this option should be selected
            if value is not None and str(opt_value) == str(value):
                opt_attrs["selected"] = True

            option_elements.append(Option(opt_label, value=opt_value, **opt_attrs))

        select_attrs = _filter_none(
            id=field_id,
            name=name,
            required=required if required else None,
            **attrs
        )
        sel = Select(*option_elements, **select_attrs)
        return _build_field(sel, name, label, wrapper, id)

    @staticmethod
    def checkbox(
        name: str,
        label: Optional[str] = None,
        checked: bool = False,
        value: str = "on",
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        required: bool = False,
        **attrs
    ) -> HTMLElement:
        """Create a checkbox field.

        For checkboxes, the label wraps the input for better UX.

        Args:
            name: Field name
            label: Label text (wraps the checkbox)
            checked: Whether the checkbox is pre-checked
            value: Value sent when checked (default "on")
            wrapper: Wrapper div class name or attributes dict
            id: Custom id (defaults to name)
            required: Whether the checkbox must be checked
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="checkbox",
            id=field_id,
            name=name,
            value=value,
            checked=checked if checked else None,
            required=required if required else None,
            **attrs
        )
        inp = Input(**input_attrs)

        # For checkbox, label wraps the input (input first, then text)
        if label:
            # Use a fragment inside label to control order: input, space, text
            from nitro_ui.tags.text import Span
            labeled = Label(inp, Span(" " + label))
            if wrapper:
                if isinstance(wrapper, str):
                    return Div(labeled, cls=wrapper)
                elif isinstance(wrapper, dict):
                    return Div(labeled, **wrapper)
            return labeled

        if wrapper:
            if isinstance(wrapper, str):
                return Div(inp, cls=wrapper)
            elif isinstance(wrapper, dict):
                return Div(inp, **wrapper)
        return inp

    @staticmethod
    def radio(
        name: str,
        options: List[Union[tuple, Dict[str, Any]]],
        label: Optional[str] = None,
        required: bool = False,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        **attrs
    ) -> HTMLElement:
        """Create a radio button group.

        Radio buttons are wrapped in a fieldset with legend for accessibility.

        Args:
            name: Field name (shared by all radio buttons)
            options: List of options - tuples or dicts like select()
            label: Legend text for the fieldset
            required: Whether selection is required
            value: Pre-selected value
            wrapper: Wrapper div class name or attributes dict
        """
        # Build radio button elements
        radio_elements = []
        for i, opt in enumerate(options):
            if isinstance(opt, tuple):
                opt_value, opt_label = opt
                opt_attrs = {}
            elif isinstance(opt, dict):
                opt_value = opt.get("value", "")
                opt_label = opt.get("label", opt_value)
                opt_attrs = {k: v for k, v in opt.items() if k not in ("value", "label")}
            else:
                continue

            radio_id = f"{name}_{i}"
            input_attrs = _filter_none(
                type="radio",
                id=radio_id,
                name=name,
                value=opt_value,
                required=required if required and i == 0 else None,  # Only first needs required
                checked=True if value is not None and str(opt_value) == str(value) else None,
                **opt_attrs,
                **attrs
            )
            inp = Input(**input_attrs)
            radio_elements.append(Label(inp, " ", opt_label))

        # Wrap in fieldset with legend
        if label:
            fieldset = Fieldset(Legend(label), *radio_elements)
        else:
            fieldset = Fieldset(*radio_elements)

        if wrapper:
            if isinstance(wrapper, str):
                return Div(fieldset, cls=wrapper)
            elif isinstance(wrapper, dict):
                return Div(fieldset, **wrapper)
        return fieldset

    # =========================================================================
    # Other Inputs
    # =========================================================================

    @staticmethod
    def file(
        name: str,
        label: Optional[str] = None,
        required: bool = False,
        accept: Optional[str] = None,
        multiple: bool = False,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a file upload field.

        Args:
            name: Field name
            label: Optional label text
            required: Whether file selection is required
            accept: Accepted file types (e.g., "image/*", ".pdf,.doc")
            multiple: Allow multiple file selection
            wrapper: Wrapper div class name or attributes dict
            id: Custom id (defaults to name)
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="file",
            id=field_id,
            name=name,
            required=required if required else None,
            accept=accept,
            multiple=multiple if multiple else None,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def hidden(
        name: str,
        value: str,
        **attrs
    ) -> HTMLElement:
        """Create a hidden input field.

        Args:
            name: Field name
            value: Hidden value
        """
        return Input(type="hidden", name=name, value=value, **attrs)

    @staticmethod
    def color(
        name: str,
        label: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs
    ) -> HTMLElement:
        """Create a color picker field.

        Args:
            name: Field name
            label: Optional label text
            value: Default color in #RRGGBB format
            wrapper: Wrapper div class name or attributes dict
            id: Custom id (defaults to name)
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="color",
            id=field_id,
            name=name,
            value=value,
            **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)
