#! /usr/bin/env python

from flask import Flask, request
import requests
import json

from wppt.config import TRANSFORMERS_PATH
from wppt.utils import parse_definitions, traverse_format_dict

app = Flask(__name__)


@app.route("/")
def hello():
    return "Webhooks Transformer is running!"


@app.route("/<transformer>/", methods=["POST"])
def dinamic_transformer(transformer: str):
    data = request.json
    definitions = parse_definitions(TRANSFORMERS_PATH)
    for _transformer, definition in definitions.items():
        if _transformer.lower() == transformer.lower():
            if definition.get("enabled"):
                translations = definition.get("translations")
                webhook_url = definition.get("target_webhook")
            else:
                return f"Transformer {_transformer} is disabled", 200

        headers = {"Content-type": "application/json"}
        try:
            traverse_format_dict(translations, data)
        except KeyError as ಠ_ಠ:
            return f"{ಠ_ಠ}", 400
        response = requests.post(
            webhook_url, headers=headers, data=json.dumps(translations)
        )

        print(response.status_code)
        print(response.text)

    return f"Transformers executed.", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
