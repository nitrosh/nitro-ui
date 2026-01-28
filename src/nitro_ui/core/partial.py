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

        if self._file:
            with open(self._file, "r", encoding="utf-8") as f:
                result = f.read()
        else:
            result = self._html

        self.on_after_render()
        return result

    def to_dict(self) -> dict:
        """Serializes the Partial to a dictionary."""
        result = {"type": "partial"}
        if self._html is not None:
            result["html"] = self._html
        if self._file is not None:
            result["file"] = self._file
        return result

    def to_json(self, indent: int = None) -> str:
        """Serializes the Partial to a JSON string."""
        import json

        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "Partial":
        """Reconstructs a Partial from a dictionary."""
        if data.get("type") != "partial":
            raise ValueError("Not a Partial element")
        return cls(html=data.get("html"), file=data.get("file"))

    @classmethod
    def from_json(cls, json_str: str) -> "Partial":
        """Reconstructs a Partial from a JSON string."""
        import json

        data = json.loads(json_str)
        return cls.from_dict(data)
