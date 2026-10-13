from unittest import TestCase

from nitro_ui import (Ul, UnorderedList,
                      Ol, OrderedList,
                      Li, ListItem,
                      Dt, DescriptionTerm,
                      Dl, DescriptionList,
                      Dd, DescriptionDetails)
from nitro_ui import (Division, Div,
                      Navigation, Nav,
                      Img, Image)
from nitro_ui import (TFoot, TableFooter,
                      Th, TableHeaderCell,
                      THead, TableHeader,
                      TBody, TableBody,
                      Td, TableDataCell,
                      Tr, TableRow,
                      Column, Col,
                      ColumnGroup, Colgroup)
from nitro_ui import (Head1, H1,
                      Head2, H2,
                      Head3, H3,
                      Head4, H4,
                      Head5, H5,
                      Head6, H6)
from nitro_ui import (
    P, p, Paragraph,
    Preformatted, Pre,
    Q, Quote,
    Emphasis, Em,
    I, Italic,
    Abbreviation, Abbr,
    A, Anchor,
    Sub, Subscript,
    Sup, Superscript,
    B, Bold,
    Deleted, Del,
    Inserted, Ins,
    S, Strikethrough,
    U, Underline,
    KeyboardInput, Kbd,
    SampleOutput, Samp,
    Variable, Var,
    Definition, Dfn,
    Break, Br,
    WordBreak, Wbr,
    BiDirectionalIndependent, Bdi,
    BiDirectionalOverride, Bdo,
    RubyText, Rt,
    RubyParenthesis, Rp
)

class TestAliases(TestCase):

    def test_list_aliases(self):
        testing = [
            (Ul, UnorderedList),
            (Ol, OrderedList),
            (Li, ListItem),
            (Dt, DescriptionTerm),
            (Dl, DescriptionList),
            (Dd, DescriptionDetails),
        ]
        for alias, real in testing:
            with self.subTest(alias=alias, real=real):
                self.assertIs(alias, real)

    def test_media_and_layout(self):
        testing = [
            (Img, Image),
            (Division, Div),
            (Navigation, Nav),
        ]

        for alias, real in testing:
            with self.subTest(alias=alias, real=real):
                self.assertIs(alias, real)

    def test_table(self):
        testing = [
            (TFoot, TableFooter),
            (Th, TableHeaderCell),
            (THead, TableHeader),
            (TBody, TableBody),
            (Td, TableDataCell),
            (Tr, TableRow),
            (Column, Col),
            (ColumnGroup, Colgroup)
        ]
        for alias, real in testing:
            with self.subTest(alias=alias, real=real):
                self.assertIs(alias, real)

    def test_text_heads(self):
        testing = [
            (Head1, H1),
            (Head2, H2),
            (Head3, H3),
            (Head4, H4),
            (Head5, H5),
            (Head6, H6)
        ]

        for alias, real in testing:
            with self.subTest(alias=alias, real=real):
                self.assertIs(alias, real)

    def test_etc_in_text_excluding_heads(self):
        testing = [
            (P, Paragraph),
            (p, Paragraph),
            (Preformatted, Pre),
            (Q, Quote),
            (Emphasis, Em),
            (I, Italic),
            (Abbreviation, Abbr),
            (A, Anchor),
            (Sub, Subscript),
            (Sup, Superscript),
            (B, Bold),
            (Deleted, Del),
            (Inserted, Ins),
            (S, Strikethrough),
            (U, Underline),
            (KeyboardInput, Kbd),
            (SampleOutput, Samp),
            (Variable, Var),
            (Definition, Dfn),
            (Break, Br),
            (WordBreak, Wbr),
            (BiDirectionalIndependent, Bdi),
            (BiDirectionalOverride, Bdo),
            (RubyText, Rt),
            (RubyParenthesis, Rp)
        ]

        for alias, real in testing:
            with self.subTest(alias=alias, real=real):
                self.assertIs(alias, real)
