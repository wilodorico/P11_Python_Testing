import json

import pytest

from json_services import JSONServices


def test_load_valid_json_file(mocker):
    mock_data = {"clubs": [{"email": "clubtest@test.com", "name": "Club Test"}]}

    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_data)))
    result = JSONServices.load("clubs.json")
    assert result == mock_data


def test_load_non_existent_json_file(mocker):
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError) as exc_info:
        JSONServices.load("non_existent_file.json")
    assert str(exc_info.value) == "File non_existent_file.json not found."
