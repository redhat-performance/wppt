#! /usr/bin/env python

import json

import requests
import logging
from flask import Flask, Response, jsonify, request

from wppt.config import TRANSFORMERS_PATH
from wppt.utils import parse_definitions, traverse_format_dict

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route("/")
def hello():
    return "Webhooks Transformer is running!"


@app.route("/<transformer>/", methods=["POST"])
def dinamic_transformer(transformer: str) -> Response:
    data = request.json
    logger.info(f"[{transformer}] Received data: {data}")
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

                if not translations:
                    translations = data

                payload = json.dumps(translations)
                logger.info(f"[{transformer}] Transformed data: {payload}") # noqa
                webhook_urls = webhook_url.split("|")
                payloads = []
                for url in webhook_urls:
                    try:
                        response = requests.post(
                            url,
                            headers=headers,
                            data=payload,
                            timeout=10,
                        )
                    except requests.exceptions.RequestException as ò_ó:
                        payload = {
                            "status_code": 400,
                            "error": f"{ò_ó}",
                            "message": f"Failed to send the transformed webhook for {_transformer}.",
                        }
                        payloads.append(payload)
                        continue

                    if response.status_code not in (200, 201, 202, 204):
                        payload = {
                            "status_code": response.status_code,
                            "error": response.text,
                            "message": f"Failed to send the transformed webhook for {_transformer}.",
                        }
                        payloads.append(payload)
                if payloads:
                    return jsonify(payloads)
            else:
                return jsonify(f"Transformer {_transformer} is disabled", 400)
            
    return jsonify(
        {
            "status_code": 200,
            "message": "Transformers executed.",
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
