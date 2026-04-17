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
    """Factory of static methods that emit common HTML5 form inputs.

    Every method returns a regular NitroUI ``HTMLElement`` so results
    compose with the rest of the library. Two optional knobs are shared
    across most methods:

    - ``label``: when provided, wraps the input with a ``<label>``.
      Checkboxes and radios are special-cased so the label behaves
      correctly for their semantics.
    - ``wrapper``: when provided, nests the field inside a ``<div>``.
      Pass a string to use it as the wrapper's class, or a dict to
      forward arbitrary attributes.

    Example:
        >>> from nitro_ui import Form, Button
        >>> from nitro_ui.forms import Field
        >>> form = Form(
        ...     Field.email("email", label="Email", required=True),
        ...     Field.password("password", label="Password", min_length=8),
        ...     Button("Log In", type="submit"),
        ... )
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
        **attrs,
    ) -> HTMLElement:
        """Build a single-line ``<input type="text">`` with validation attrs.

        Args:
            name: Form field name; also used as the default ``id``.
            label: Optional visible ``<label>`` text.
            required: Emit the HTML ``required`` attribute.
            min_length: Minimum character count (``minlength``).
            max_length: Maximum character count (``maxlength``).
            pattern: JS regex source for client-side validation.
            placeholder: Placeholder text shown when empty.
            value: Initial value of the input.
            wrapper: ``<div>`` wrapper - a CSS class string or an
                attribute dict.
            id: Override the default id (defaults to ``name``).
            **attrs: Extra attributes passed through to the ``<input>``.

        Returns:
            An ``<input>``, a ``Fragment(<label>, <input>)``, or the
            pair wrapped in a ``<div>`` - depending on which optional
            arguments were supplied.
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
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="email">`` with browser-side format validation.

        Same shared options as :meth:`text` (``label``, ``wrapper``,
        ``id``, ``**attrs``). Browsers validate the value against their
        internal email grammar when ``required`` is set.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="email",
            id=field_id,
            name=name,
            required=required if required else None,
            placeholder=placeholder,
            value=value,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="password">`` with optional length constraints.

        Has no ``value`` parameter - passwords should not be
        round-tripped. Use ``min_length`` / ``max_length`` for strength
        hints. Same shared options as :meth:`text`.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="password",
            id=field_id,
            name=name,
            required=required if required else None,
            minlength=min_length,
            maxlength=max_length,
            placeholder=placeholder,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="url">`` with browser-side URL validation.

        Same shared options as :meth:`text`. Browsers validate against a
        basic absolute-URL grammar when ``required`` is set.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="url",
            id=field_id,
            name=name,
            required=required if required else None,
            placeholder=placeholder,
            value=value,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="tel">`` for phone-number entry.

        The ``tel`` input type enables mobile keyboards but browsers do
        no format validation - supply a ``pattern`` for client-side
        checks. Same shared options as :meth:`text`.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="tel",
            id=field_id,
            name=name,
            required=required if required else None,
            pattern=pattern,
            placeholder=placeholder,
            value=value,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="search">`` with browser-provided clear affordance.

        Same shared options as :meth:`text`. Browsers typically render a
        built-in "clear" control and inline search decorations.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="search",
            id=field_id,
            name=name,
            required=required if required else None,
            placeholder=placeholder,
            value=value,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build a multi-line ``<textarea>`` input.

        Any ``value`` is inserted as the textarea's text content (not an
        attribute, per the HTML spec). Supports ``rows`` / ``cols`` sizing
        and ``min_length`` / ``max_length`` validation.
        """
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
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="number">`` for numeric entry.

        Use ``min`` / ``max`` / ``step`` to constrain the allowed values.
        ``step="any"`` permits arbitrary decimals. Same shared options
        as :meth:`text`.
        """
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
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="range">`` slider with a bounded numeric range.

        Defaults to ``min=0`` and ``max=100``. The slider value is
        always within the inclusive ``[min, max]`` range; ``step``
        controls the snap increment.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="range",
            id=field_id,
            name=name,
            min=min,
            max=max,
            step=step,
            value=value,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="date">`` picker constrained to ``YYYY-MM-DD`` dates.

        Browsers render a native date picker. Same shared options as
        :meth:`text`.

        Args:
            min: Earliest selectable date as ``YYYY-MM-DD``.
            max: Latest selectable date as ``YYYY-MM-DD``.
            value: Initial date as ``YYYY-MM-DD``.
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
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="time">`` picker constrained to ``HH:MM`` times.

        Browsers render a native time picker. Same shared options as
        :meth:`text`.

        Args:
            min: Earliest selectable time as ``HH:MM``.
            max: Latest selectable time as ``HH:MM``.
            value: Initial time as ``HH:MM``.
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
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="datetime-local">`` picker for local datetimes.

        The value is timezone-naive; browsers submit it as
        ``YYYY-MM-DDTHH:MM``. Same shared options as :meth:`text`.

        Args:
            min: Earliest selectable value as ``YYYY-MM-DDTHH:MM``.
            max: Latest selectable value as ``YYYY-MM-DDTHH:MM``.
            value: Initial value as ``YYYY-MM-DDTHH:MM``.
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
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build a ``<select>`` dropdown populated from a flexible options list.

        Options accept three shapes, in order of flexibility:

        - ``str``: ``"USA"`` - value and label are identical.
        - ``tuple``: ``("us", "United States")`` - ``(value, label)``.
        - ``dict``: ``{"value": "us", "label": "United States",
          "disabled": True}`` - arbitrary extra keys become
          ``<option>`` attributes.

        Args:
            name: Form field name; also used as the default id.
            options: Iterable of option descriptors (see above).
            label: Optional ``<label>`` text.
            required: Emit the HTML ``required`` attribute.
            value: Pre-select the option whose value matches (compared
                as strings).
            wrapper: ``<div>`` wrapper - class string or attribute dict.
            id: Override the default id (defaults to ``name``).
            **attrs: Extra attributes passed to the ``<select>``.
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
                opt_attrs = {
                    k: v for k, v in opt.items() if k not in ("value", "label")
                }
            else:
                continue

            # Check if this option should be selected
            if value is not None and str(opt_value) == str(value):
                opt_attrs["selected"] = True

            option_elements.append(Option(opt_label, value=opt_value, **opt_attrs))

        select_attrs = _filter_none(
            id=field_id, name=name, required=required if required else None, **attrs
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="checkbox">``, with the label wrapping the input.

        Unlike other field factories, the label here wraps the checkbox
        - clicking the label text toggles the state, which is the
        conventional accessible layout.

        Args:
            name: Form field name; also used as the default id.
            label: Label text. When provided, wraps ``<input>`` and a
                ``<span>`` containing the text.
            checked: Emit the ``checked`` attribute.
            value: Value submitted when the box is checked. Defaults
                to ``"on"``, matching browser behaviour.
            wrapper: ``<div>`` wrapper - class string or attribute dict.
            id: Override the default id (defaults to ``name``).
            required: Emit the ``required`` attribute - the box must
                be ticked for the form to submit.
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="checkbox",
            id=field_id,
            name=name,
            value=value,
            checked=checked if checked else None,
            required=required if required else None,
            **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build a radio-button group wrapped in an accessible ``<fieldset>``.

        Every option produces an ``<input type="radio">`` that shares
        ``name`` with its siblings; a ``<legend>`` carries the group
        label. Only the first option receives the ``required`` attribute
        - that is sufficient for the entire group.

        Args:
            name: Shared form field name for the group.
            options: Iterable of ``(value, label)`` tuples or option
                dicts with ``value``/``label``/extra keys, mirroring
                :meth:`select`.
            label: Text for the group's ``<legend>``.
            required: Require a selection before the form submits.
            value: Value of the option to pre-check (compared as strings).
            wrapper: ``<div>`` wrapper - class string or attribute dict.
            **attrs: Extra attributes applied to every ``<input>``.
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
                opt_attrs = {
                    k: v for k, v in opt.items() if k not in ("value", "label")
                }
            else:
                continue

            radio_id = f"{name}_{i}"
            input_attrs = _filter_none(
                type="radio",
                id=radio_id,
                name=name,
                value=opt_value,
                required=(
                    required if required and i == 0 else None
                ),  # Only first needs required
                checked=(
                    True if value is not None and str(opt_value) == str(value) else None
                ),
                **opt_attrs,
                **attrs,
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
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="file">`` for attaching files from the client.

        Args:
            name: Form field name; also used as the default id.
            label: Optional ``<label>`` text.
            required: Emit the ``required`` attribute.
            accept: Filter the native picker by MIME types or
                extensions (e.g. ``"image/*"``, ``".pdf,.doc"``).
            multiple: Allow selecting more than one file at once.
            wrapper: ``<div>`` wrapper - class string or attribute dict.
            id: Override the default id (defaults to ``name``).
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="file",
            id=field_id,
            name=name,
            required=required if required else None,
            accept=accept,
            multiple=multiple if multiple else None,
            **attrs,
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)

    @staticmethod
    def hidden(name: str, value: str, **attrs) -> HTMLElement:
        """Build an ``<input type="hidden">`` for carrying state through a form.

        Always returns a bare ``<input>`` - no label, no wrapper - since
        hidden inputs are not user-visible.

        Args:
            name: Form field name.
            value: Value submitted with the form.
            **attrs: Extra attributes passed through to the ``<input>``.
        """
        return Input(type="hidden", name=name, value=value, **attrs)

    @staticmethod
    def color(
        name: str,
        label: Optional[str] = None,
        value: Optional[str] = None,
        wrapper: Optional[Union[str, Dict[str, Any]]] = None,
        id: Optional[str] = None,
        **attrs,
    ) -> HTMLElement:
        """Build an ``<input type="color">`` color picker.

        Browsers submit colors as ``#RRGGBB`` lowercase hex; the picker
        UI is browser-native.

        Args:
            name: Form field name; also used as the default id.
            label: Optional ``<label>`` text.
            value: Initial color as ``#RRGGBB`` hex.
            wrapper: ``<div>`` wrapper - class string or attribute dict.
            id: Override the default id (defaults to ``name``).
        """
        field_id = id or name
        input_attrs = _filter_none(
            type="color", id=field_id, name=name, value=value, **attrs
        )
        inp = Input(**input_attrs)
        return _build_field(inp, name, label, wrapper, id)
