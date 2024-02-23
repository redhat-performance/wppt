from unittest.mock import patch

import requests


class TestApp:
    @patch("wppt.app.parse_definitions")
    @patch("wppt.app.traverse_format_dict")
    @patch("wppt.app.requests.post")
    def test_dinamic_transformer_enabled_transformer(
        self, mock_post, mock_traverse_format_dict, mock_parse_definitions, test_client
    ):
        mock_parse_definitions.return_value = {
            "transformer1": {
                "enabled": True,
                "translations": {"key1": "value1"},
                "target_webhook": "https://example.com/webhook",
            }
        }
        mock_traverse_format_dict.return_value = None
        mock_post.return_value.status_code = 200

        response = test_client.post("/transformer1/", json={"key1": "value1"})

        assert response.status_code == 200
        assert response.json == {
            "status_code": 200,
            "message": "Transformers executed.",
        }
        mock_traverse_format_dict.assert_called_once_with(
            {"key1": "value1"}, {"key1": "value1"}
        )

    @patch("wppt.app.parse_definitions")
    def test_dinamic_transformer_disabled_transformer(
        self, mock_parse_definitions, test_client
    ):
        mock_parse_definitions.return_value = {
            "transformer1": {
                "enabled": False,
                "translations": {"key1": "value1"},
                "target_webhook": "https://example.com/webhook",
            }
        }
        response = test_client.post("/transformer1/", json={"key1": "value1"})

        assert response.json[0] == "Transformer transformer1 is disabled"
        assert response.json[1] == 400

    @patch("wppt.app.parse_definitions")
    @patch("wppt.app.traverse_format_dict", side_effect=KeyError("Invalid key"))
    def test_dinamic_transformer_invalid_key(
        self, mock_traverse_format_dict, mock_parse_definitions, test_client
    ):
        mock_parse_definitions.return_value = {
            "transformer1": {
                "enabled": True,
                "translations": {"key1": "value1"},
                "target_webhook": "https://example.com/webhook",
            }
        }

        response = test_client.post("/transformer1/", json={"key1": "value1"})

        assert response.json[0] == "'Invalid key'"
        assert response.json[1] == 400
        mock_traverse_format_dict.assert_called_once_with(
            {"key1": "value1"}, {"key1": "value1"}
        )

    @patch("wppt.app.parse_definitions")
    @patch("wppt.app.traverse_format_dict")
    @patch(
        "wppt.app.requests.post",
        side_effect=requests.exceptions.RequestException("Failed to send request"),
    )
    def test_dinamic_transformer_failed_request(
        self, mock_post, mock_traverse_format_dict, mock_parse_definitions, test_client
    ):
        mock_parse_definitions.return_value = {
            "transformer1": {
                "enabled": True,
                "translations": {"key1": "value1"},
                "target_webhook": "https://example.com/webhook",
            }
        }
        mock_traverse_format_dict.return_value = None
        mock_post.side_effect = requests.exceptions.RequestException(
            "Failed to send request"
        )

        response = test_client.post("/transformer1/", json={"key1": "value1"})

        assert (
            response.json["message"]
            == "Failed to send the transformed webhook for transformer1."
        )
        assert response.json["status_code"] == 400
        mock_traverse_format_dict.assert_called_once_with(
            {"key1": "value1"}, {"key1": "value1"}
        )
