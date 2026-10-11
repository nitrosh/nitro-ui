from nitro_ui.core.element import HTMLElement, DEFAULT_MAX_DEPTH


class Partial(HTMLElement):
    """Embeds raw HTML directly without escaping.

    Use for trusted static content like analytics snippets, third-party
    embeds, or legacy HTML that should not be escaped.

    Warning: Content is rendered without any HTML escaping. Only use
    with trusted content to avoid XSS vulnerabilities.

    Example:
        Partial("<script>console.log('hello')</script>")
        Partial(file="partials/analytics.html")
    """

    __slots__ = ["_html", "_file"]

    def __init__(self, html: str = None, *, file: str = None):
        if html is not None and file is not None:
            raise ValueError("Cannot specify both 'html' and 'file'")
        if html is None and file is None:
            raise ValueError("Must specify either 'html' or 'file'")
        if html is not None and not isinstance(html, str):
            raise TypeError(f"'html' must be a string, got {type(html).__name__}")
        if file is not None and (not isinstance(file, str) or not file):
            raise ValueError("'file' must be a non-empty path string")

        super().__init__(tag="partial")
        self._html = html
        self._file = file

    def render(
        self,
        pretty: bool = False,
        _indent: int = 0,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> str:
        """Renders the raw HTML content.

        Args:
            pretty: Ignored (raw HTML is returned as-is)
            _indent: Ignored (raw HTML is returned as-is)
            max_depth: Ignored (no recursion needed)

        Returns:
            The raw HTML string

        Raises:
            FileNotFoundError: If file path doesn't exist
            IOError: If file cannot be read
        """
        self.on_before_render()

        if self._file is not None:
            with open(self._file, "r", encoding="utf-8") as f:
                result = f.read()
        else:
            result = self._html

        self.on_after_render()
        return result

    def to_dict(self, _depth: int = 0, max_depth: int = DEFAULT_MAX_DEPTH) -> dict:
        """Return a dict with ``type="partial"`` plus the source marker.

        Either the inline ``html`` string or the ``file`` path is stored
        - whichever was provided at construction time.
        """
        result = {"type": "partial"}
        if self._html is not None:
            result["html"] = self._html
        if self._file is not None:
            result["file"] = self._file
        return result

    def to_json(self, indent: int = None) -> str:
        """Serialize this Partial to a JSON string.

        Args:
            indent: Spaces for pretty-printed JSON, or ``None`` for
                compact output.
        """
        import json

        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict, allow_files: bool = False) -> "Partial":
        """Reconstruct a ``Partial`` from a ``to_dict()`` result.

        Args:
            data: Dict produced by ``to_dict()``.
            allow_files: Allow a ``file`` source. Off by default so that
                untrusted data can't make ``render()`` read files from disk.

        Raises:
            ValueError: If ``data["type"]`` is not ``"partial"``, or it
                names a file and ``allow_files`` is ``False``.
        """
        if not isinstance(data, dict) or data.get("type") != "partial":
            raise ValueError("Not a Partial element")
        if data.get("file") is not None and not allow_files:
            raise ValueError(
                "Refusing to load a file-backed Partial from serialized data. "
                "Pass allow_files=True (or allow_partial_files=True) if the "
                "data is trusted."
            )
        return cls(html=data.get("html"), file=data.get("file"))

    @classmethod
    def from_json(cls, json_str: str, allow_files: bool = False) -> "Partial":
        """Reconstruct a ``Partial`` from a ``to_json()`` result.

        See ``from_dict()`` for ``allow_files``.
        """
        import json

        data = json.loads(json_str)
        return cls.from_dict(data, allow_files=allow_files)
