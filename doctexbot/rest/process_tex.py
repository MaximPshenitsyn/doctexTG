import json
import requests
from .connections import send_tex

headers = {'Content-Type': 'application/json'}


def _process_file(file: str):
    with open(f'../uploads/{file}', 'r', encoding='utf-8') as f:
        body = json.dumps({'text': f.read()})
        r = requests.post(url=send_tex, json=json.loads(body), headers=headers)
        return json.loads(r.content).get('downloadLink')


def _process_tex(tex: str):
    body = json.dumps({'text': tex})
    r = requests.post(url=send_tex, json=json.loads(body), headers=headers)
    return json.loads(r.content).get('downloadLink')


def _download_file(link: str):
    r = requests.get(url=link, stream=True)
    path = f'generated/{link[link.rfind("/") + 1:]}'
    with open(path, 'wb') as out:
        out.write(r.content)
    return path


def convert_file(file: str) -> str:
    d_link = _process_file(file)
    return _download_file(d_link)


def convert_tex(tex: str) -> str:
    d_link = _process_tex(tex)
    return _download_file(d_link)
