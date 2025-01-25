import pytest
import httpx
import time
import docker

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session", autouse=True)
def start_container():
    """
    Start the application container and ensure it's ready for API requests.
    """
    client = docker.from_env()

    # Ensure the image is built
    try:
        client.images.get("neureality:1.0.0")
    except docker.errors.ImageNotFound:
        client.images.build(path=".", tag="neureality:1.0.0")

    # Start the container
    container = client.containers.run(
        "neureality:1.0.0",
        ports={"8000/tcp": 8000},
        detach=True
    )
    time.sleep(5)  # Allow the container some time to start

    yield

    container.stop()
    container.remove()


def test_reverse_api():
    """
    Test the /reverse API with various inputs to ensure correct output.
    """
    input_cases = ["Hello my name is Noa Lemberg",
                   "This is my home assignment for neureality",
                   "what do you think about it?",
                   "single",
                   "",
                   "This test will fail!"
                   ]

    test_cases = [
        (case, {"data": {"result": " ".join(case.split()[::-1])}})
        for case in input_cases[:-1]
    ]

    # uncomment next line to test a failure
    # test_cases.append((input_cases[-1], {"data": {"result": "HO NO! this is not the revert input!"}}))

    for user_input, expected_response in test_cases:
        response = httpx.get(f"{BASE_URL}/reverse", params={"in": user_input})
        assert response.status_code == 200
        assert response.json() == expected_response
        print(response.json())


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
