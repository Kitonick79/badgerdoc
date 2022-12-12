# Example: start_offset = 146, end_offset = 158, entity type = IMPOSITION, entity name = “VAT, 19”.
#
# Relations (e.g. “links”, according to BadgerDoc terminology) should be defined by the governor and dependent
# entity tags (so each entity tag should be associated with some id).
#
# The format of exported annotations should be sufficient for retrieving the above info. Moreover, the pre-labeled
# annotations should follow the same format to be imported into BadgerDoc.
import json
from pathlib import Path

#
# INPUT_EXAMPLE_FILE_PATH = "./input_example.json"
#
#
# input_data = json.loads(Path(INPUT_EXAMPLE_FILE_PATH).read_text())
#
# output_badgerdoc_tokens = {
#     # In additional we will generate PDF file for these tokens.
#     "size": {"width": 123, "height": 123},
#     "page_num": 1,
#     "objs": [
#         {
#             "type": "text",
#             "bbox": [74.986, 82.455, 201.588, 99.671],
#             "text": "w",
#             "offset": {"begin": 0, "end": 1}
#         },
#         {
#             "type": "text",
#             "bbox": [205.892, 82.455, 301.248, 99.671],
#             "text": "1",
#             "offset": {"begin": 1, "end": 2}
#         },
#         {
#             "type": "text",
#             "bbox": [205.892, 82.455, 301.248, 99.671],
#             "text": " ",
#             "offset": {"begin": 2, "end": 3}
#         },
#         {
#             "type": "text",
#             "bbox": [305.552, 82.455, 328.844, 99.671],
#             "text": "2",
#             "offset": {"begin": 3, "end": 4}
#         },
#         {
#             "type": "text",
#             "bbox": [305.552, 82.455, 328.844, 99.671],
#             "text": "\n",
#             "offset": {"begin": 4, "end": 5}
#         },
#         {
#             "type": "text",
#             "bbox": [305.552, 82.455, 328.844, 99.671],
#             "text": "3",
#             "offset": {"begin": 5, "end": 6}
#         },
#         {
#             "type": "text",
#             "bbox": [305.552, 82.455, 328.844, 99.671],
#             "text": "\t",
#             "offset": {"begin": 6, "end": 7}
#         },
#         {
#             "type": "text",
#             "bbox": [305.552, 82.455, 328.844, 99.671],
#             "text": "4",
#             "offset": {"begin": 7, "end": 8}
#         },
#     ]
# }
#
# output_badgerdoc_annotation = {
#     "revision": "revision-1",  # TODO: What is it?
#     "pages": [  # As far as we understand we will fill only this field
#         {
#             "size": {
#                 "width": 0,
#                 "height": 0
#             },
#             "page_num": 1,
#             "objs": [
#                 {
#                     "id": 1,
#                     "type": "box",  # Which type should we use?
#                     "bbox": [75, 82, 537, 119],
#                     "category": "some, VAT, 19",  # We suppose we should put here entity type and entity name?
#                     "entity_type": "some",
#                     "entity_name": "VAT, 19"
#                 },
#                 {
#                     "id": 42,
#                     "type": "box",
#                     "bbox": [53, 266, 295, 487],
#                     "category": "IMPOSITION, VAT, 19",
#                     "entity_type": "IMPOSITION",
#                     "entity_name": "VAT, 19"
#                 },
#                 {
#                     "id": 43,
#                     "type": "box",
#                     "bbox": [317, 406, 558, 447],
#                     "category": "232323, VAT, 19",
#                     "entity_type": "232323",
#                     "entity_name": "VAT, 19",
#                     "links": [42, 1]
#                 }
#             ]
#         }
#     ],
#     "validated": [],
#     "failed_validation_pages": []
# }
#
# badgerdoc_data = {
#     "pdf_file": "path/to/file",
#     "tokens": output_badgerdoc_tokens,
#     "annotation": output_badgerdoc_annotation
# }


# def test_convert_tokens():
#     input_text = "q we"  # TODO: add `\n`
#     calculated_width = 612.0
#     calculated_height = 792.0
#
#     expected_tokens = [
#         {
#             "size": {"width": calculated_width, "height": calculated_height},
#             "page_num": 1,
#             "objs": [
#                 {
#                     "type": "text",
#                     "bbox": [74.986, 82.455, 201.588, 99.671],
#                     "text": "q",
#                     "offset": {"begin": 0, "end": 1}
#                 },
#                 {
#                     "type": "text",
#                     "bbox": [205.892, 82.455, 301.248, 99.671],
#                     "text": " ",
#                     "offset": {"begin": 1, "end": 2}
#                 },
#                 {
#                     "type": "text",
#                     "bbox": [205.892, 82.455, 301.248, 99.671],
#                     "text": "w",
#                     "offset": {"begin": 2, "end": 3}
#                 },
#                 {
#                     "type": "text",
#                     "bbox": [305.552, 82.455, 328.844, 99.671],
#                     "text": "e",
#                     "offset": {"begin": 3, "end": 4}
#                 },
#             ]
#         }
#     ]
#
#
def test_convert_annotation():
    ...
