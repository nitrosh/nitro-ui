from typing import Callable, Optional, Type

from nitro_ui.core.element import HTMLElement, register_tag


def simple_tag_class(
    tag: str,
    self_closing: bool = False,
    extra_init: Optional[Callable[[HTMLElement, dict], None]] = None,
) -> Type[HTMLElement]:
    """Build a lightweight ``HTMLElement`` subclass bound to a tag name.

    Most public tag classes in NitroUI (``Div``, ``H1``, ``Input``,
    ``Meta``, ...) are produced by this factory. Each generated class
    accepts the same arguments as ``HTMLElement`` - positional children
    and keyword attributes - but hard-codes the ``tag`` and
    ``self_closing`` values so callers never specify them.

    The produced class is also registered in the tag registry so that
    ``HTMLElement.from_dict()`` and ``from_html()`` can round-trip
    instances back into the same subclass.

    Args:
        tag: HTML tag name to bind (e.g. ``"div"``, ``"img"``).
        self_closing: If ``True``, the generated class renders as
            ``<tag />`` with no closing tag. Use for void elements like
            ``img``, ``br``, ``input``, ``meta``.
        extra_init: Optional callback invoked at construction time with
            ``(instance, kwargs)``. The callback may mutate the kwargs
            dict in place to rewrite or inject attributes before
            ``HTMLElement.__init__`` runs - used, for example, by
            ``Label`` to convert a ``for_element`` kwarg to ``for``.

    Returns:
        A new ``HTMLElement`` subclass named after ``tag`` (e.g.
        ``"div"`` -> class named ``Div``).

    Raises:
        TypeError: If ``tag`` is not a string, or ``extra_init`` is not
            callable.

    Example:
        >>> MyTag = simple_tag_class("my-tag")
        >>> MyTag("Hello", id="t1").render()
        '<my-tag id="t1">Hello</my-tag>'
    """
    if not isinstance(tag, str):
        raise TypeError(f"tag must be a string, got {type(tag)}")

    if extra_init is not None and not callable(extra_init):
        raise TypeError("extra_init must be callable")

    class _Tag(HTMLElement):
        """HTML element class for a single fixed tag.

        Accepts positional children (elements or strings) and keyword
        attributes; ``tag`` and ``self_closing`` are bound at class
        creation time. See :func:`simple_tag_class` for details.
        """

        def __init__(self, *args, **kwargs):
            if extra_init:
                extra_init(self, kwargs)
            super().__init__(
                *args,
                **{
                    **kwargs,
                    "tag": tag,
                    **({"self_closing": True} if self_closing else {}),
                },
            )

    # __qualname__ is set so pickling and serialization refer to the
    # logical class name (e.g. "Div") rather than "_Tag".
    class_name = tag.capitalize() if tag.islower() else tag
    _Tag.__name__ = class_name
    _Tag.__qualname__ = class_name

    register_tag(tag, _Tag)

    return _Tag
