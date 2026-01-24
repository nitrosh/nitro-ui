"""Tests for the lowercase HTML-like aliases in nitro_ui.html module."""

import unittest


class TestHTMLAliases(unittest.TestCase):
    """Test that lowercase aliases work correctly."""

    def test_import_all(self):
        """Test that all aliases can be imported."""
        from nitro_ui.html import (
            # Core
            HTMLElement,
            Fragment,
            from_html,
            # Form
            textarea,
            select,
            option,
            button,
            fieldset,
            form,
            input_,
            label,
            optgroup,
            legend,
            output,
            progress,
            meter,
            # Document
            html,
            head,
            body,
            title,
            meta,
            link,
            script,
            style,
            iframe,
            base,
            noscript,
            # Layout
            div,
            section,
            header,
            nav,
            footer,
            hr,
            main,
            article,
            aside,
            details,
            summary,
            dialog,
            # Lists
            ul,
            ol,
            li,
            datalist,
            dd,
            dl,
            dt,
            # Media
            img,
            video,
            audio,
            source,
            picture,
            figure,
            figcaption,
            canvas,
            track,
            embed,
            object_,
            param,
            map_,
            area,
            # Table
            table,
            tfoot,
            th,
            thead,
            tbody,
            td,
            tr,
            caption,
            col,
            colgroup,
            # Text
            h1,
            h2,
            h3,
            h4,
            h5,
            h6,
            p,
            blockquote,
            pre,
            q,
            cite,
            em,
            i,
            span,
            strong,
            abbr,
            a,
            small,
            sup,
            sub,
            time,
            code,
            b,
            del_,
            ins,
            s,
            u,
            kbd,
            samp,
            var,
            mark,
            dfn,
            br,
            wbr,
        )

        # If we get here, all imports succeeded
        self.assertTrue(True)

    def test_div_creates_div_element(self):
        """Test that div() creates a div element."""
        from nitro_ui.html import div

        element = div("Hello")
        self.assertEqual(element.tag, "div")
        self.assertEqual(element.text, "Hello")

    def test_paragraph_alias_is_p(self):
        """Test that p() creates a paragraph element."""
        from nitro_ui.html import p

        element = p("Content")
        self.assertEqual(element.tag, "p")
        self.assertEqual(element.text, "Content")

    def test_anchor_alias_is_a(self):
        """Test that a() creates an anchor element."""
        from nitro_ui.html import a

        element = a("Click me", href="/page")
        self.assertEqual(element.tag, "a")
        self.assertEqual(element.text, "Click me")
        self.assertEqual(element.get_attribute("href"), "/page")

    def test_image_alias_is_img(self):
        """Test that img() creates an image element."""
        from nitro_ui.html import img

        element = img(src="photo.jpg", alt="A photo")
        self.assertEqual(element.tag, "img")
        self.assertTrue(element.self_closing)
        self.assertEqual(element.get_attribute("src"), "photo.jpg")

    def test_list_aliases(self):
        """Test ul, ol, li aliases."""
        from nitro_ui.html import ul, ol, li

        unordered = ul(li("Item 1"), li("Item 2"))
        self.assertEqual(unordered.tag, "ul")
        self.assertEqual(len(unordered.children), 2)
        self.assertEqual(unordered.children[0].tag, "li")

        ordered = ol(li("First"), li("Second"))
        self.assertEqual(ordered.tag, "ol")

    def test_table_aliases(self):
        """Test table-related aliases."""
        from nitro_ui.html import table, thead, tbody, tr, th, td

        t = table(
            thead(tr(th("Header"))),
            tbody(tr(td("Cell"))),
        )
        self.assertEqual(t.tag, "table")
        self.assertEqual(t.children[0].tag, "thead")
        self.assertEqual(t.children[1].tag, "tbody")

    def test_heading_aliases(self):
        """Test h1-h6 aliases."""
        from nitro_ui.html import h1, h2, h3, h4, h5, h6

        self.assertEqual(h1("Title").tag, "h1")
        self.assertEqual(h2("Subtitle").tag, "h2")
        self.assertEqual(h3("Section").tag, "h3")
        self.assertEqual(h4("Subsection").tag, "h4")
        self.assertEqual(h5("Minor").tag, "h5")
        self.assertEqual(h6("Smallest").tag, "h6")

    def test_text_formatting_aliases(self):
        """Test text formatting aliases (b, i, u, s, etc.)."""
        from nitro_ui.html import b, i, u, s, strong, em, code, pre

        self.assertEqual(b("bold").tag, "b")
        self.assertEqual(i("italic").tag, "i")
        self.assertEqual(u("underline").tag, "u")
        self.assertEqual(s("strikethrough").tag, "s")
        self.assertEqual(strong("important").tag, "strong")
        self.assertEqual(em("emphasized").tag, "em")
        self.assertEqual(code("x = 1").tag, "code")
        self.assertEqual(pre("preformatted").tag, "pre")

    def test_python_keyword_aliases(self):
        """Test aliases for Python keywords use underscore suffix."""
        from nitro_ui.html import del_, input_, object_, map_

        # del_ creates a <del> element
        element = del_("deleted text")
        self.assertEqual(element.tag, "del")

        # input_ creates an <input> element
        inp = input_(type="text", name="username")
        self.assertEqual(inp.tag, "input")
        self.assertTrue(inp.self_closing)

        # object_ creates an <object> element
        obj = object_(data="movie.swf", type="application/x-shockwave-flash")
        self.assertEqual(obj.tag, "object")

        # map_ creates a <map> element
        m = map_(name="imagemap")
        self.assertEqual(m.tag, "map")

    def test_self_closing_elements(self):
        """Test that self-closing elements are correctly marked."""
        from nitro_ui.html import br, hr, img, input_, meta, link

        self.assertTrue(br().self_closing)
        self.assertTrue(hr().self_closing)
        self.assertTrue(img(src="x.jpg").self_closing)
        self.assertTrue(input_(type="text").self_closing)
        self.assertTrue(meta(charset="utf-8").self_closing)
        self.assertTrue(link(rel="stylesheet", href="style.css").self_closing)

    def test_nested_structure(self):
        """Test building nested HTML structures."""
        from nitro_ui.html import div, h1, p, ul, li, a

        page = div(
            h1("Welcome"),
            p("This is a paragraph."),
            ul(
                li(a("Home", href="/")),
                li(a("About", href="/about")),
            ),
            class_name="container",
        )

        self.assertEqual(page.tag, "div")
        self.assertEqual(page.get_attribute("class_name"), "container")
        self.assertEqual(len(page.children), 3)
        self.assertEqual(page.children[0].tag, "h1")
        self.assertEqual(page.children[1].tag, "p")
        self.assertEqual(page.children[2].tag, "ul")

    def test_attributes_work(self):
        """Test that attributes can be passed to aliases."""
        from nitro_ui.html import div, a

        element = div(
            "Content",
            id="main",
            class_name="wrapper",
            data_value="123",
        )
        self.assertEqual(element.get_attribute("id"), "main")
        self.assertEqual(element.get_attribute("class_name"), "wrapper")
        self.assertEqual(element.get_attribute("data-value"), "123")

        link = a("Click", href="https://example.com", target="_blank")
        self.assertEqual(link.get_attribute("href"), "https://example.com")
        self.assertEqual(link.get_attribute("target"), "_blank")

    def test_method_chaining_works(self):
        """Test that method chaining works with aliases."""
        from nitro_ui.html import div, p

        element = div().append(p("Added")).add_attribute("id", "test")
        self.assertEqual(element.tag, "div")
        self.assertEqual(len(element.children), 1)
        self.assertEqual(element.get_attribute("id"), "test")

    def test_render_output(self):
        """Test that rendered output is correct."""
        from nitro_ui.html import div, p, b

        element = div(p("Hello ", b("world"), "!"), class_name="greeting")
        rendered = element.render()

        self.assertIn("<div", rendered)
        self.assertIn('class="greeting"', rendered)
        self.assertIn("<p>", rendered)
        self.assertIn("<b>world</b>", rendered)
        self.assertIn("</div>", rendered)

    def test_document_structure(self):
        """Test building a complete HTML document structure."""
        from nitro_ui.html import html, head, body, title, meta, div, h1, p

        doc = html(
            head(
                meta(charset="utf-8"),
                title("My Page"),
            ),
            body(
                div(
                    h1("Hello World"),
                    p("Welcome to my page."),
                    class_name="container",
                )
            ),
        )

        self.assertEqual(doc.tag, "html")
        self.assertEqual(doc.children[0].tag, "head")
        self.assertEqual(doc.children[1].tag, "body")

        rendered = doc.render()
        # HTML element includes DOCTYPE prefix and default lang/dir attributes
        self.assertIn("<!DOCTYPE html>", rendered)
        self.assertIn("<html", rendered)
        self.assertIn("<head>", rendered)
        self.assertIn('<meta charset="utf-8"', rendered)
        self.assertIn("<title>My Page</title>", rendered)
        self.assertIn("</html>", rendered)

    def test_form_structure(self):
        """Test building form structures."""
        from nitro_ui.html import form, label, input_, button, select, option

        f = form(
            label("Username:", for_element="username"),
            input_(type="text", id="username", name="username"),
            label("Role:", for_element="role"),
            select(
                option("Admin", value="admin"),
                option("User", value="user"),
                id="role",
                name="role",
            ),
            button("Submit", type="submit"),
            action="/submit",
            method="post",
        )

        self.assertEqual(f.tag, "form")
        self.assertEqual(f.get_attribute("action"), "/submit")
        self.assertEqual(f.get_attribute("method"), "post")

    def test_aliases_are_same_classes(self):
        """Test that aliases reference the same classes as PascalCase versions."""
        from nitro_ui import Div, Paragraph, H1, UnorderedList, ListItem, Image
        from nitro_ui.html import div, p, h1, ul, li, img

        # They should be the exact same class objects
        self.assertIs(div, Div)
        self.assertIs(p, Paragraph)
        self.assertIs(h1, H1)
        self.assertIs(ul, UnorderedList)
        self.assertIs(li, ListItem)
        self.assertIs(img, Image)

    def test_fragment_available(self):
        """Test that Fragment is available in html module."""
        from nitro_ui.html import Fragment, h1, p

        frag = Fragment(h1("Title"), p("Content"))
        rendered = frag.render()

        self.assertIn("<h1>Title</h1>", rendered)
        self.assertIn("<p>Content</p>", rendered)
        # Fragment should not wrap in a tag
        self.assertNotIn("<fragment>", rendered)

    def test_styles_available(self):
        """Test that style classes are available in html module."""
        from nitro_ui.html import CSSStyle, StyleSheet, Theme, div

        style = CSSStyle(color="red", font_size="16px")
        self.assertIsNotNone(style)

        sheet = StyleSheet()
        cls = sheet.register("test", style)
        self.assertEqual(cls, "test")

        theme = Theme.modern()
        self.assertIsNotNone(theme)


class TestHTMLAliasesStarImport(unittest.TestCase):
    """Test that star import works correctly."""

    def test_star_import_provides_all_aliases(self):
        """Test from nitro_ui.html import * provides all expected names."""
        import nitro_ui.html as html_module

        # Check that __all__ is defined
        self.assertTrue(hasattr(html_module, "__all__"))

        # Check some key aliases are in __all__
        all_names = html_module.__all__
        self.assertIn("div", all_names)
        self.assertIn("p", all_names)
        self.assertIn("a", all_names)
        self.assertIn("h1", all_names)
        self.assertIn("ul", all_names)
        self.assertIn("li", all_names)
        self.assertIn("img", all_names)
        self.assertIn("table", all_names)
        self.assertIn("input_", all_names)
        self.assertIn("del_", all_names)


if __name__ == "__main__":
    unittest.main()
