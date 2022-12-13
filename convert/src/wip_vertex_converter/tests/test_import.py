# Example: start_offset = 146, end_offset = 158, entity type = IMPOSITION, entity name = “VAT, 19”.
#
# Relations (e.g. “links”, according to BadgerDoc terminology) should be defined by the governor and dependent
# entity tags (so each entity tag should be associated with some id).
#
# The format of exported annotations should be sufficient for retrieving the above info. Moreover, the pre-labeled
# annotations should follow the same format to be imported into BadgerDoc.
import json
from pathlib import Path

from ..main import PlainTextToBadgerdocTokenConverter, read_vertex_annotation, VertexToBadgerdocAnnotationConverter, \
    gather_badgerdoc_token_dict

INPUT_VERTEX_FILE = "./tests/input_from_vertex.json"
BADGERDOC_TOKENS_FILE = "./tests/badgerdoc_tokens.json"
BADGERDOC_ANNOTATIONS_FILE = "./tests/badgerdoc_annotation.json"


def general_test():
    vertex_data = read_vertex_annotation(INPUT_VERTEX_FILE)

    converter = PlainTextToBadgerdocTokenConverter()
    tokens = converter.convert(vertex_data["text"])
    converter.draw_tokens(tokens, "result.pdf")
    bd_annot = VertexToBadgerdocAnnotationConverter().convert(tokens, vertex_data["annotations"])
    tokens_dict = gather_badgerdoc_token_dict(tokens)

    expected_bd_tokens = json.loads(Path(BADGERDOC_TOKENS_FILE).read_text())
    expected_bd_annotation = json.loads(Path(BADGERDOC_ANNOTATIONS_FILE).read_text())

    json.dump(bd_annot, open("filename.json", 'w'), indent=4)
    assert tokens_dict == expected_bd_tokens
    assert bd_annot == expected_bd_annotation


general_test()
