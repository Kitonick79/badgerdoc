import json
from pathlib import Path
from typing import List

import fitz
from fitz import Page


def draw_char(char: str, x0: int, y0: int, page: Page, font_height=11, font_width=7) -> None:
    x1, y1 = x0 + font_width, y0 + font_height
    rect = fitz.Rect(x0, y0, x1, y1)
    shape = page.new_shape()
    shape.draw_rect(rect)
    shape.finish(width = 0.3, color = (0.5, 0.9, 0.9))
    shape.insert_textbox(rect, char, fontname='cour')
    shape.commit()


def draw_string(string: str, x0: int, y0: int, page: Page, font_height=11, font_width=7) -> None:
    x, y = x0, y0
    for char in string:
        draw_char(char, x, y, page)
        x += font_width


def generate_chunks(text: str, n=70) -> List[str]:
    return [text[i:i+n] for i in range(0, len(text), n)]


def draw_pharagraph(text: str, x0: int, y0: int, page: Page, font_height = 11, font_width = 7, n = 80) -> None:
    # chunks = [text[i:i+n] for i in range(0, len(text), n)]
    chunks = generate_chunks(text, n=n)
    x, y = x0, y0
    for chunk in chunks:
        draw_string(chunk, x, y, page)
        y += font_height * 2


def draw_text(text: str, x0: int, y0: int, page: Page, font_height = 11, font_width = 7, n = 80) -> None:
    # draw_pharagraph(text, x0, y0, page, font_height, font_width, n)
    text_lines = text.split("\n")
    x, y = x0, y0
    for text_line in text_lines:
        # chunks = [text_line[i:i+n] for i in range(0, len(text_line), n)]
        chunks = generate_chunks(text_line, n=n)
        pharagraph_height = len(chunks) * font_height * 2
        print(f"draw pharagraph, <<<<< {len(chunks)=} >>>>>>>>>>")
        print(f"draw pharagraph, <<<<< {pharagraph_height=} >>>>>>>>>>")
        print(f"draw pharagraph, <<<<< {y=} >>>>>>>>>>")
        draw_pharagraph(text_line + "\n", x, y, page, font_height, font_width, n)
        # draw_pharagraph(text_line, x, y, page, font_height, font_width, n)
        y += pharagraph_height
    


def main():
    doc = fitz.open()
    page = doc.new_page(height = 2000)

    import string
    # draw_text(string.printable, 5, 20, page)

    # text = Path("./tests/page.txt").read_text().replace('&#10;', "\n")
    # text = Path("./tests/page.txt").read_text()
    text = Path("./tests/test.txt").read_text() * 10
    draw_text(text, 20, 60, page)

    doc.save("allmyimages.pdf")
    print(len(text))


if __name__ == "__main__":
    main()
