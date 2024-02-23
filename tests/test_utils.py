from unittest.mock import patch
from wppt.utils import parse_definitions, walk_dir, read_yaml, traverse_format_dict

class TestUtils:

    @patch('wppt.utils.walk_dir')
    @patch('wppt.utils.read_yaml')
    def test_parse_definitions(self, mock_read_yaml, mock_walk_dir):
        mock_walk_dir.return_value = ['/path/to/file1.yaml', '/path/to/file2.yaml']
        mock_read_yaml.side_effect = [{'key1': 'value1'}, {'key2': 'value2'}]

        directory = '/path/to/directory'
        expected_definitions = {'key1': 'value1', 'key2': 'value2'}
        assert parse_definitions(directory) == expected_definitions

    def test_walk_dir(self):
        directory = 'tests/fixtures/transformers'
        file_extension = '.yaml'
        expected_file_list = ['tests/fixtures/transformers/test.yaml']

        assert walk_dir(directory, file_extension) == expected_file_list

    def test_read_yaml(self):
        file_path = '../wppt/transformers/gitlab2jira.yaml'
        expected_yaml_definitions = {'key1': 'value1', 'key2': 'value2'}

        # Mocking the yaml.load function
        with patch('yaml.load') as mock_yaml_load:
            mock_yaml_load.return_value = {'key1': 'value1', 'key2': 'value2'}

            file_path = '../wppt/transformers/gitlab2jira.yaml'
            expected_yaml_definitions = {'key1': 'value1', 'key2': 'value2'}

            with patch('builtins.open', create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = 'key1: value1\nkey2: value2\n'
                yaml_definitions = read_yaml(file_path)
                assert yaml_definitions == expected_yaml_definitions

    def test_traverse_format_dict(self):
        dictionary = {'key1': 'Hello {payload}', 'key2': 'Welcome {payload}'}
        data = 'World'
        expected_dictionary = {'key1': 'Hello World', 'key2': 'Welcome World'}

        traverse_format_dict(dictionary, data)
        assert dictionary == expected_dictionary
