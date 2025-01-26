import pytest
import time
import docker

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session", autouse=True)
def start_container():
    """
    Start the application container and ensure it's ready for API requests.
    """
    client = docker.from_env()

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
