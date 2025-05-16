import json

from json_services import JSONServices


def test_load_valid_json_file(mocker):
    mock_data = {"clubs": [{"email": "clubtest@test.com", "name": "Club Test"}]}

    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_data)))
    result = JSONServices.load("clubs.json")
    assert result == mock_data
