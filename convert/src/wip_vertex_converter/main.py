import json
from pathlib import Path
from pprint import pprint
from typing import List

import fitz
from fitz import Page
from pydantic import BaseModel, Field


class Offset(BaseModel):
    begin: int
    end: int


class BadgerdocToken(BaseModel):
    type_: str = Field(default="text", alias="type")
    bbox: List[float]
    text: str
    offset: Offset


def generate_chunks(text: str, n=70) -> List[str]:
    return [text[i:i + n] for i in range(0, len(text), n)]


class PlainTextToBadgerdocTokenConverter:
    PAGE_WIDTH = 595
    PAGE_BORDER_OFFSET = 15
    FONT_HEIGHT = 11
    FONT_WIDTH = 7

    def draw_tokens(self, tokens: List[BadgerdocToken], save_path):
        doc = fitz.open()
        width = max((token.bbox[2] for token in tokens)) + self.PAGE_BORDER_OFFSET
        height = max((token.bbox[3] for token in tokens)) + self.PAGE_BORDER_OFFSET
        page = doc.new_page(height=height, width=width)
        for token in tokens:
            self.draw_token(token, page)
        doc.save(save_path)

    def draw_token(self, token: BadgerdocToken, page: Page) -> None:
        rect = fitz.Rect(token.bbox[0], token.bbox[1], token.bbox[2], token.bbox[3])
        shape = page.new_shape()
        shape.draw_rect(rect)
        shape.finish(width=0.3, color=(0.8, 0.8, 1))
        shape.insert_textbox(rect, token.text, fontname='cour')
        shape.commit()

    @property
    def line_length_token(self):
        return int((self.PAGE_WIDTH - 2 * self.PAGE_BORDER_OFFSET) / self.FONT_WIDTH)

    def convert(self, text: str) -> List[BadgerdocToken]:
        tokens = []
        line_offset = 0
        paragraphs = (paragraph + "\n" for paragraph in text.split("\n"))

        y = self.PAGE_BORDER_OFFSET
        for paragraph in paragraphs:
            lines = generate_chunks(paragraph, self.line_length_token)
            for line in lines:
                self.convert_line(line, tokens, y, line_offset=line_offset)
                y += self.FONT_HEIGHT * 2
                line_offset += len(line)
            y += self.FONT_HEIGHT

        return tokens

    def convert_line(self, line, tokens, y, line_offset: int):
        x = self.PAGE_BORDER_OFFSET
        for i, char in enumerate(line):
            begin = line_offset + i
            end = begin + 1
            offset = Offset(begin=begin, end=end)
            token = BadgerdocToken(bbox=[x, y, x + self.FONT_WIDTH, y + self.FONT_HEIGHT], text=char, offset=offset)
            tokens.append(token)
            x += self.FONT_WIDTH


class VertexToBadgerdocAnnotationConverter:
    def __init__(self, vertex_file: Path):
        self._vertext_file = vertex_file
        self.vertex_annotation = json.loads(self._vertext_file.read_text())

    def convert(self, badgerdoc_tokens: List[BadgerdocToken]):
        pass


def main():
    text = Path("tests/test.txt").read_text() * 3

    converter = PlainTextToBadgerdocTokenConverter()
    tokens = converter.convert(text)
    pprint(tokens)
    converter.draw_tokens(tokens, "result.pdf")


if __name__ == "__main__":
    main()
