import json
from datetime import datetime

from rest.process_compile import compile_doc_to_tex
from rest.process_tex import convert_tex


def _process_ro(mentorJob, mentorName, masterJob, masterName, studentGroup, studentName, projectName, link) -> str:
    body = {
        "headers": {
            "mentorJob": mentorJob,
            "mentorName": mentorName,
            "masterJob": masterJob,
            "masterName": masterName,
            "studentGroup": studentGroup,
            "studentName": studentName,
            "projectName": projectName,
            "year": str(datetime.now().year)
        },
        "link": link
    }
    return json.dumps(body)


def process_ro_full(args: dict):
    data = _process_ro(args.get('mentorJob'), args.get('mentorName'), args.get('masterJob'), args.get('masterName'),
                       args.get('studentGroup'), args.get('studentName'), args.get('projectName'), args.get('link'))
    tex = compile_doc_to_tex('ro', data)
    return convert_tex(tex)
