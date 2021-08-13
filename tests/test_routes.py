import requests

def test_get_user_info_check_status_code_equals_200():
    response = requests.get("http://localhost:5000/api/draftjoker2?key=_R5mj3woyovq1z3J12sktw")
    assert response.status_code == 200

def test_get_user_info_check_json_response_schema():
    response = requests.get("http://localhost:5000/api/draftjoker2?key=_R5mj3woyovq1z3J12sktw")
    body = response.json()
    assert body["draftjoker2"]["API Key"] == "_R5mj3woyovq1z3J12sktw"