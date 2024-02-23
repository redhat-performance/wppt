#! /usr/bin/env python

import json

import requests
from flask import Flask, Response, jsonify, request

from wppt.config import TRANSFORMERS_PATH
from wppt.utils import parse_definitions, traverse_format_dict

app = Flask(__name__)


@app.route("/")
def hello():
    return "Webhooks Transformer is running!"


@app.route("/<transformer>/", methods=["POST"])
def dinamic_transformer(transformer: str) -> Response:
    data = request.json
    definitions = parse_definitions(TRANSFORMERS_PATH)
    for _transformer, definition in definitions.items():
        if _transformer.lower() == transformer.lower():
            if definition.get("enabled"):
                translations = definition.get("translations")
                webhook_url = definition.get("target_webhook")

                headers = {"Content-`type": "application/json"}
                try:
                    traverse_format_dict(translations, data)
                except KeyError as ಠ_ಠ:
                    return jsonify(f"{ಠ_ಠ}", 400)
                
                try:
                    response = requests.post(
                        webhook_url, headers=headers, data=json.dumps(translations)
                    )
                except requests.exceptions.RequestException as e:
                    payload = {
                        "status_code": 400,
                        "error": f"{e}",
                        "message": f"Failed to send the transformed webhook for {_transformer}.",
                    }
                    return jsonify(payload)
                
                if response.status_code not in (200, 201, 202, 204):
                    payload = {
                        "status_code": response.status_code,
                        "error": response.text,
                        "message": f"Failed to send the transformed webhook for {_transformer}.",
                    }
                    return jsonify(payload)
            else:
                return jsonify(f"Transformer {_transformer} is disabled", 400)
        
    response = {
        "status_code": 200,
        "message": "Transformers executed.",
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
