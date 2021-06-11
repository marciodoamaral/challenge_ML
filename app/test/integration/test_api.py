import requests


def test_status_request():
    response = requests.get('http://127.0.0.1/api/v1/resources/search?url=https://www.google.com/')
    assert response.status_code == 200


def test_list_should_not_be_empty():
    response = requests.get('http://127.0.0.1/api/v1/resources/search?url=https://www.google.com/')
    assert response.json() is not None


def test_list_number_item():
    response = requests.get('http://127.0.0.1/api/v1/resources/search?url=https://www.google.com/')
    assert len(list(response.json())) == 12
