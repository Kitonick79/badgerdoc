import json
from pathlib import Path
from pprint import pprint
from typing import List, Dict, Any, Tuple

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


class VertexAnnotationToken(BaseModel):
    id_: str = Field(alias="id")
    begin: int
    end: int
    entity_type: str
    entity_name: str
    links: List[str]


class BadgerdocAnnotationToken(BaseModel):
    id_: int = Field(alias="id")
    type_: str = Field(default="text", alias="type")
    bbox: List[float]
    tokens: List[int]
    category: str
    links: List[int]
    data: Dict[str, Any]


def generate_chunks(text: str, n=70) -> List[str]:
    return [text[i:i + n] for i in range(0, len(text), n)]


PAGE_BORDER_OFFSET = 15


class PlainTextToBadgerdocTokenConverter:
    PAGE_WIDTH = 595
    PAGE_BORDER_OFFSET = PAGE_BORDER_OFFSET
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
        paragraphs = [paragraph + "\n" for paragraph in text.split("\n")]
        paragraphs[-1] = paragraphs[-1][:-1]

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

    def convert(self, badgerdoc_tokens: List[BadgerdocToken], vertext_annotation_raw: List[Dict]):
        vertext_annotation = [VertexAnnotationToken.parse_obj(i) for i in vertext_annotation_raw]
        bd_annotation = []
        for vertex_token in vertext_annotation:
            tokens = badgerdoc_tokens[vertex_token.begin: vertex_token.end]
            bbox = [
                min([t.bbox[0] for t in tokens]),
                min([t.bbox[1] for t in tokens]),
                max([t.bbox[2] for t in tokens]),
                max([t.bbox[3] for t in tokens]),
            ]
            bd_token = BadgerdocAnnotationToken(
                id=int(vertex_token.id_),
                links=[int(i) for i in vertex_token.links],
                category=vertex_token.entity_type,
                data={"entity": {"id": vertex_token.entity_name}},
                tokens=list(range(vertex_token.begin, vertex_token.end)),
                bbox=bbox
            )
            bd_annotation.append(bd_token)

        page_width = max([t.bbox[2] for t in badgerdoc_tokens]) + PAGE_BORDER_OFFSET
        page_height = max([t.bbox[2] for t in badgerdoc_tokens]) + PAGE_BORDER_OFFSET
        return {
            "revision": "revision-1",
            "pages": [
                {
                    "size": {
                        "width": page_width,
                        "height": page_height
                    },
                    "page_num": 1,
                    "objs": [i.dict(by_alias=True) for i in bd_annotation],
                    "validated": [],
                    "failed_validation_pages": []
                }
            ]
        }


def read_vertex_annotation(path_to_file) -> Dict:
    return json.loads(Path(path_to_file).read_text())


def gather_badgerdoc_token_dict(tokens):
    return {
        "size": {
            "width": 123,
            "height": 123
        },
        "page_num": 1,
        "objs": [i.dict(by_alias=True) for i in tokens]
    }


def main():
    converter = PlainTextToBadgerdocTokenConverter()

    vertex = read_vertex_annotation("tests/input_from_vertex.json")

    tokens = converter.convert(vertex["text"])
    converter.draw_tokens(tokens, "result.pdf")

    annot_converter = VertexToBadgerdocAnnotationConverter().convert(tokens, vertex["annotations"])




if __name__ == "__main__":
    main()
