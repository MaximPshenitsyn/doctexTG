import json

import requests
from .connections import compile_tex

headers = {'Content-Type': 'application/json'}


def compile_doc_to_tex(doc: str, data: str) -> str:
    r = requests.post(url=compile_tex + doc, json=json.loads(data), headers=headers)
    if r.status_code == 200:
        return json.loads(r.content).get('text')
    raise 'unavailable to compile file!'
