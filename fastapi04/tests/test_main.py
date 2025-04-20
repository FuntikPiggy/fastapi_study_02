import pytest


@pytest.mark.parametrize(
    "json_data, expected_status, expected_result",
    [
        ({"username": "Valeriy", "age": 40, "email": "email@email.ru", "password": "1111111111", "phone": "+1111111"},
         200, {"username": "Valeriy", "age": 40, "email": "email@email.ru", "phone": "+1111111"}),
        ({"username": "Valentina", "age": 40, "email": "email@email.ru", "password": "2222222222", "phone": "+2222222"},
         200, {"username": "Valentina", "age": 40, "email": "email@email.ru", "phone": "+2222222"}),
        ({"username": "valentina", "age": 40, "email": "email@email.ru", "password": "123456789", "phone": "+222222"},
         200, {"username": "valentina", "age": 40, "email": "email@email.ru", "phone": "+222222"}),
        ({"username": "Kira", "age": 19, "email": "email@email.ru", "password": "123456789", "phone": "+33333333"},
         200, {"username": "Kira", "age": 19, "email": "email@email.ru", "phone": "+33333333"}),
        ({"username": "KiraKira", "age": 19, "email": "email@email.ru", "password": "123456789", "phone": "33333333"},
         400, {"1": "The phone number must start with a \" + \" and contain from 1 to 12 digits."}),
        ({"username": "KiraKira", "age": 17, "email": "email@email.ru", "password": "123456789", "phone": "+33333333"},
         400, {"1": "The age must be an integer between 18 and 100."}),
        ({"username": "KiraKira", "age": 17, "email": "email@email.ru", "password": "1239", "phone": "+33333333"},
         400, {"1": "The age must be an integer between 18 and 100.",
               "2": "The password must be a string between 8 and 16 characters long."}),
        ({"username": "Kira", "age": 19, "email": "email@email.ru", "password": "123456789", "phone": "+33333333"},
         409, "Invalid user data"),
        ({"username": "Sergey", "age": 40, "email": "email@email.ru", "password": "1111111111", "phone": "+8888888"},
         200, {"username": "Sergey", "age": 40, "email": "email@email.ru", "phone": "+8888888"}),
    ]
)
async def test_new_user(json_data, expected_status, expected_result, client):
    response = client.post("/new_user", json=json_data)
    assert response.status_code == expected_status
    assert response.json() == expected_result


@pytest.mark.parametrize(
    "username, expected_status, expected_result",
    [
        ("Valeriy", 200, {"username": "Valeriy", "age": 40, "email": "email@email.ru", "phone": "+1111111"}),
        ("Kirill", 404, "User not found"),
    ]
)
async def test_load_user(username, expected_status, expected_result, client):
    response = client.get(f"/load_user/{username}")
    assert response.status_code == expected_status
    assert response.json() == expected_result


@pytest.mark.parametrize(
    "username, expected_status, expected_result",
    [
        ("valentina", 200, {"message": "User valentina deleted"}),
        ("Anna", 409, "Invalid user data"),
    ]
)
async def test_del_user(username, expected_status, expected_result, client):
    response = client.get(f"/del_user/{username}")
    assert response.status_code == expected_status
    assert response.json() == expected_result
