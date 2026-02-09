"""Tests for SVG camelCase attribute preservation.

Covers:
- Parser restoring camelCase after HTMLParser lowercases attrs
- Element constructor mapping snake_case kwargs to SVG camelCase
- Full round-trip: parse SVG HTML -> render -> verify camelCase
"""

import unittest

from nitro_ui.core.element import HTMLElement
from nitro_ui.core.parser import from_html


class TestSVGParserCamelCase(unittest.TestCase):
    """Parser should restore camelCase on known SVG attributes."""

    def test_viewbox_preserved(self):
        """viewBox should be preserved through parse + render."""
        el = from_html('<svg viewBox="0 0 100 100"></svg>')
        self.assertIsNotNone(el)
        rendered = el.render()
        self.assertIn('viewBox="0 0 100 100"', rendered)

    def test_preserve_aspect_ratio(self):
        """preserveAspectRatio should survive parse + render."""
        el = from_html(
            '<svg preserveAspectRatio="xMidYMid meet"></svg>'
        )
        rendered = el.render()
        self.assertIn('preserveAspectRatio="xMidYMid meet"', rendered)

    def test_gradient_units(self):
        """gradientUnits should survive parse + render."""
        html = (
            '<linearGradient gradientUnits="userSpaceOnUse">'
            "</linearGradient>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('gradientUnits="userSpaceOnUse"', rendered)

    def test_gradient_transform(self):
        """gradientTransform should survive parse + render."""
        html = (
            '<linearGradient gradientTransform="rotate(90)">'
            "</linearGradient>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('gradientTransform="rotate(90)"', rendered)

    def test_std_deviation(self):
        """stdDeviation should survive parse + render."""
        html = '<feGaussianBlur stdDeviation="5" />'
        el = from_html(html)
        rendered = el.render()
        self.assertIn('stdDeviation="5"', rendered)

    def test_spread_method(self):
        """spreadMethod should survive parse + render."""
        html = (
            '<radialGradient spreadMethod="pad">'
            "</radialGradient>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('spreadMethod="pad"', rendered)

    def test_pattern_units(self):
        """patternUnits should survive parse + render."""
        html = (
            '<pattern patternUnits="userSpaceOnUse">'
            "</pattern>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('patternUnits="userSpaceOnUse"', rendered)

    def test_clip_path_units(self):
        """clipPathUnits should survive parse + render."""
        html = (
            '<clipPath clipPathUnits="objectBoundingBox">'
            "</clipPath>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn(
            'clipPathUnits="objectBoundingBox"', rendered
        )

    def test_marker_dimensions(self):
        """markerWidth / markerHeight should survive."""
        html = (
            '<marker markerWidth="10" markerHeight="10">'
            "</marker>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('markerWidth="10"', rendered)
        self.assertIn('markerHeight="10"', rendered)

    def test_ref_x_y(self):
        """refX and refY should survive parse + render."""
        html = '<marker refX="5" refY="5"></marker>'
        el = from_html(html)
        rendered = el.render()
        self.assertIn('refX="5"', rendered)
        self.assertIn('refY="5"', rendered)

    def test_multiple_svg_attrs_on_one_element(self):
        """Multiple SVG camelCase attrs on one element."""
        html = (
            '<svg viewBox="0 0 100 100" '
            'preserveAspectRatio="xMidYMid">'
            "</svg>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('viewBox="0 0 100 100"', rendered)
        self.assertIn('preserveAspectRatio="xMidYMid"', rendered)

    def test_mixed_svg_and_normal_attrs(self):
        """SVG camelCase attrs mixed with normal attrs."""
        html = (
            '<svg viewBox="0 0 100 100" '
            'id="icon" class="my-svg">'
            "</svg>"
        )
        el = from_html(html)
        rendered = el.render()
        self.assertIn('viewBox="0 0 100 100"', rendered)
        self.assertIn('id="icon"', rendered)
        self.assertIn('class="my-svg"', rendered)

    def test_full_svg_roundtrip(self):
        """Full SVG document round-trip through parse + render."""
        svg = (
            '<svg viewBox="0 0 24 24" '
            'preserveAspectRatio="xMidYMid meet">'
            '<linearGradient gradientUnits="userSpaceOnUse" '
            'gradientTransform="rotate(45)">'
            "</linearGradient>"
            "</svg>"
        )
        el = from_html(svg)
        rendered = el.render()
        self.assertIn("viewBox=", rendered)
        self.assertIn("preserveAspectRatio=", rendered)
        self.assertIn("gradientUnits=", rendered)
        self.assertIn("gradientTransform=", rendered)

    def test_non_svg_attrs_unchanged(self):
        """Normal HTML attrs should not be affected."""
        html = '<div data-value="123" class="box"></div>'
        el = from_html(html)
        rendered = el.render()
        self.assertIn('data-value="123"', rendered)
        self.assertIn('class="box"', rendered)


class TestSVGElementConstruction(unittest.TestCase):
    """Element constructor should map snake_case -> SVG camelCase."""

    def test_view_box_kwarg(self):
        """view_box kwarg should render as viewBox."""
        el = HTMLElement(tag="svg", view_box="0 0 100 100")
        rendered = el.render()
        self.assertIn('viewBox="0 0 100 100"', rendered)

    def test_preserve_aspect_ratio_kwarg(self):
        """preserve_aspect_ratio -> preserveAspectRatio."""
        el = HTMLElement(
            tag="svg", preserve_aspect_ratio="xMidYMid"
        )
        rendered = el.render()
        self.assertIn('preserveAspectRatio="xMidYMid"', rendered)

    def test_gradient_units_kwarg(self):
        """gradient_units -> gradientUnits."""
        el = HTMLElement(
            tag="lineargradient",
            gradient_units="userSpaceOnUse",
        )
        rendered = el.render()
        self.assertIn(
            'gradientUnits="userSpaceOnUse"', rendered
        )

    def test_std_deviation_kwarg(self):
        """std_deviation -> stdDeviation."""
        el = HTMLElement(
            tag="fegaussianblur",
            self_closing=True,
            std_deviation="5",
        )
        rendered = el.render()
        self.assertIn('stdDeviation="5"', rendered)

    def test_spread_method_kwarg(self):
        """spread_method -> spreadMethod."""
        el = HTMLElement(
            tag="radialgradient", spread_method="pad"
        )
        rendered = el.render()
        self.assertIn('spreadMethod="pad"', rendered)

    def test_text_length_kwarg(self):
        """text_length -> textLength."""
        el = HTMLElement(tag="text", text_length="100")
        rendered = el.render()
        self.assertIn('textLength="100"', rendered)

    def test_path_length_kwarg(self):
        """path_length -> pathLength."""
        el = HTMLElement(tag="path", path_length="100")
        rendered = el.render()
        self.assertIn('pathLength="100"', rendered)

    def test_start_offset_kwarg(self):
        """start_offset -> startOffset."""
        el = HTMLElement(
            tag="textpath", start_offset="50%"
        )
        rendered = el.render()
        self.assertIn('startOffset="50%"', rendered)

    def test_ref_x_y_kwarg(self):
        """ref_x / ref_y -> refX / refY."""
        el = HTMLElement(
            tag="marker", ref_x="5", ref_y="5"
        )
        rendered = el.render()
        self.assertIn('refX="5"', rendered)
        self.assertIn('refY="5"', rendered)

    def test_filter_units_kwarg(self):
        """filter_units -> filterUnits."""
        el = HTMLElement(
            tag="filter", filter_units="userSpaceOnUse"
        )
        rendered = el.render()
        self.assertIn(
            'filterUnits="userSpaceOnUse"', rendered
        )

    def test_num_octaves_kwarg(self):
        """num_octaves -> numOctaves."""
        el = HTMLElement(
            tag="feturbulence",
            self_closing=True,
            num_octaves="3",
        )
        rendered = el.render()
        self.assertIn('numOctaves="3"', rendered)

    def test_base_frequency_kwarg(self):
        """base_frequency -> baseFrequency."""
        el = HTMLElement(
            tag="feturbulence",
            self_closing=True,
            base_frequency="0.05",
        )
        rendered = el.render()
        self.assertIn('baseFrequency="0.05"', rendered)

    def test_non_svg_underscore_still_hyphenated(self):
        """Normal (non-SVG) underscore attrs still become hyphens."""
        el = HTMLElement(
            tag="div", data_value="123", aria_label="test"
        )
        rendered = el.render()
        self.assertIn('data-value="123"', rendered)
        self.assertIn('aria-label="test"', rendered)

    def test_direct_camel_case_kwarg(self):
        """viewBox passed directly as kwarg (valid Python)."""
        el = HTMLElement(tag="svg", viewBox="0 0 24 24")
        rendered = el.render()
        self.assertIn('viewBox="0 0 24 24"', rendered)


class TestSVGGetAttribute(unittest.TestCase):
    """Attribute access should work with SVG camelCase names."""

    def test_get_attribute_by_camel_name(self):
        """get_attribute with camelCase key should work."""
        el = HTMLElement(tag="svg", view_box="0 0 100 100")
        self.assertEqual(
            el.get_attribute("viewBox"), "0 0 100 100"
        )

    def test_has_attribute_by_camel_name(self):
        """has_attribute with camelCase key should work."""
        el = HTMLElement(tag="svg", view_box="0 0 100 100")
        self.assertTrue(el.has_attribute("viewBox"))

    def test_parsed_svg_get_attribute(self):
        """Parsed SVG attrs accessible by camelCase key."""
        el = from_html('<svg viewBox="0 0 24 24"></svg>')
        self.assertEqual(
            el.get_attribute("viewBox"), "0 0 24 24"
        )


class TestSVGSerializationRoundtrip(unittest.TestCase):
    """SVG attrs should survive to_dict/from_dict round-trip."""

    def test_to_dict_preserves_camel_case(self):
        """to_dict should store the camelCase key."""
        el = HTMLElement(tag="svg", view_box="0 0 100 100")
        d = el.to_dict()
        self.assertIn("viewBox", d["attributes"])

    def test_round_trip_preserves_svg_attrs(self):
        """from_dict(to_dict(el)) should preserve SVG attrs."""
        el = HTMLElement(
            tag="svg",
            view_box="0 0 100 100",
            preserve_aspect_ratio="xMidYMid",
        )
        d = el.to_dict()
        restored = HTMLElement.from_dict(d)
        rendered = restored.render()
        self.assertIn('viewBox="0 0 100 100"', rendered)
        self.assertIn(
            'preserveAspectRatio="xMidYMid"', rendered
        )


if __name__ == "__main__":
    unittest.main()
