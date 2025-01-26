import pytest
import httpx

BASE_URL = "http://localhost:8000"


def test_reverse_api():
    """
    Test the /reverse API with various inputs to ensure correct output.
    """
    input_cases = ["Hello my name is Noa Lemberg",
                   "This is my home assignment for NeuReality",
                   "What do you think about it?",
                   "OneWord",
                   ""]

    test_cases = [
        (case, {"data": {"result": " ".join(case.split()[::-1])}})
        for case in input_cases
    ]

    for user_input, expected_response in test_cases:
        response = httpx.get(f"{BASE_URL}/reverse", params={"in": user_input})
        assert response.status_code == 200
        assert response.json() == expected_response
        print(response.json())


def test_reverse_api_negative_cases():
    """
    Test the /reverse API with invalid inputs and edge cases
    """
    negative_cases = [
        ("This test will fail!", {"data": {"result": "HO NO! this is not the revert input!"}}),
        # Incorrect expected result
        (None, {"detail": "Field required"})  # Missing query parameter
    ]

    for user_input, expected_response in negative_cases:
        if user_input is not None:
            # Invalid result case
            response = httpx.get(f"{BASE_URL}/reverse", params={"in": user_input})
        else:
            # Missing query parameter case
            response = httpx.get(f"{BASE_URL}/reverse")
        assert response.status_code == 422 if user_input is None else 200
        if user_input is not None:
            assert response.json() != expected_response  # Ensure the response is not the incorrect expectation
        else:
            assert "detail" in response.json()


def test_reverse_api_invalid_query_param():
    """
    Test the /reverse API with an invalid query parameter
    """
    # Query parameter 'on' instead of 'in'
    response = httpx.get(f"{BASE_URL}/reverse", params={"on": "This should fail"})
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "endpoint,params,expected_response",
    [
        ("/reverse", {"in": "Let's check the last response"}, {"data": {"result": "response last the check Let's"}}),
    ]
)
def test_restore_last_response(endpoint, params, expected_response):
    """
    Test the /restore API generically by setting and retrieving various responses.
    """
    # Step 1: Make a request to the given endpoint
    if params:
        response = httpx.get(f"{BASE_URL}{endpoint}", params=params)
    else:
        response = httpx.get(f"{BASE_URL}{endpoint}")
    assert response.status_code == 200
    assert response.json() == expected_response

    # Step 2: Call the /restore endpoint and ensure it matches the last response
    restore_response = httpx.get(f"{BASE_URL}/restore")
    assert restore_response.status_code == 200
    assert restore_response.json() == expected_response
