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


def test_save_json_file(mocker):
    mock_data = {"clubs": [{"email": "clubtest@test.com", "name": "Club Test", "points": "10"}]}

    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    mock_json_dump = mocker.patch("json.dump")

    JSONServices.save("clubs.json", mock_data)

    mock_open.assert_called_once_with("clubs.json", "w")
    mock_json_dump.assert_called_once_with(mock_data, mock_open(), indent=4)
