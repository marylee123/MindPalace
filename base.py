import os
import io
import dropbox
from dropbox.files import FileMetadata
from PyPDF2 import PdfReader
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

ACCESS_TOKEN = "sl.u.AGOTHX3J6G6dD4vvaxgUCl0QT7B8wXt7K2t2AgFNOhfAE5VajtRqt6gW6EbD3F2TkkuPI9dJ20f0HgDjq8fDICX1bfj7wrCaXq8WeORlyxcmhTzqx8Run2d1Fmi5ZO_wYe04T-FtPfpV__9tITu1EmleDDuJfedbJToP-AKYjBeReHuAmCn2UqdZX3CgJxLbutNAGmXsDAGKTHkdW33QBhf1-LLvjCcP_UDAuSIkLKmQQbdyptLtLZCjNU8k13s1X9xEyN2FTC1PN--ZR6Xdvl80DdbRsU5l5Cfw2QPP9_LefN1s6iw3k6mwx7TepWr43BOsXyIMPWB6T-PWhCgy0hoozwrIXCr_sygyYmK7-KCGkI1FIeEYn4JXkXDTl06NQ0LnhbxJLLEnQ3dg06ebzIFJ_IGDkXhNnbWDR_rA6KCH8NvnyT4Wh4JP6ARGlM3x8oKbtTeqwB2PHcCqs61uEnCRFjU50PSUsb9P8ihOtUapmo9gnF6vPgsoI2gKNqPSUc4i_FJSBDcZQH80cSusn0_D_Vyz36ZMxeAffCfpwtUC9Sb1eNp_BIPAu84ghCh5btZYL3GvGa3WPCZUrX7Zp5d54imoKPXTkzH-rZfj0FFaYEAcu1wLoWozUuYEmmVNuDntYyGoIln1kZp4t7j3jOkOCfQVYYCXfEDx4uZz-FM0nGDW5Bqq8ztwPP3NVQ8mJxMUVIphi7zIJGlmZ2tbPaoVnwq82WxPgZTN1KaPjbbUEPEsLoiH3E7gGhKuBwt1ShrZUsDEl2_LAoulY9iDKfQ_QOmFOhtcpCGgYv2oTkkksu1ZVCGFJVff5vr-PWWZULACtMmfW_zOw1_pxvfjX_3oGhTkea46TFEiSJPgi9yEOF2jkFKSwledAFogy-GtADYh3iSM6ZkvaLI-aNiPv2RUsqPeiWVcvKX__oryDUgHXNT80t5wBmUFTGTfpHvjQ2aVyhke4wMrqngHeJUP23seWEgY9KF6Lesd0RchBMeqXfCccYnnOdAXKgd8UUuCPkDnbfrEd40PM8cOyFhDNk3oE2O_WOH8-F7rGQXsDlfcpCPDtBbviP7sKEcjYEPn68oX3nTsEbYWnvFghBG2LFzMAo0LT7pwZmCj4ffVhx31I_26EueC244V8ibv5vePPTCN8uAYRRnk08JC5G0YGfmJqftn1pdl4w8NFSdl4ZMDz7LOpv2XgP2ExKdIEHYpxb4RirRulXgSAkZYs-i89b63Cy4OhiX2lXbSq9ydIg2qAG3v60HaFplgKPBr-y-tSeyDdgNnnorpyhGwtD9LWIr5td-ekR72Camke4sMKrkk2yk78VPEJMJSzR3tUohKmpwkEyRHz48BureD-nix-3d9AGkV-DhPBWiSUH-XoKTlBWqGcJtRaEwsL7Ijy43lmbrEVfJ2EaP81AhjDGioB7u2"
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# file / text extraction
def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() for page in reader.pages)
def download_and_extract(client):
    all_texts = {}
    result = client.files_list_folder("/math/MMA", recursive=True) # can pass "" or "/math/MMA", etc
                                                   # recursive means go into subfolders
    entries = result.entries
    while result.has_more:
        result = client.files_list_folder_continue(result.cursor)
        entries.extend(result.entries)
    for entry in result.entries:
        if isinstance(entry,FileMetadata):
            path = entry.path_lower
            print(f"Found file: {path}")
            try:
                metadata, response = client.files_download(path)
                file_bytes = response.content
                text = extract_text_from_pdf(file_bytes)
                all_texts[path] = text
            except Exception as e:
                print(f"Error dowloading/extracting {path}: {e}")

    return all_texts


if __name__=="__main__":
    texts = download_and_extract(dbx)
    print(f"\nExtracted text from {len(texts)} files:")
    for file_path, content in texts.items():
        print(f"\n---- {file_path} ----")
        print(content[:300] + "...")
