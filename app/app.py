from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated
from typing import Any

app = FastAPI()


class GenericResponse(BaseModel):
    """
    A class to store and handle the last response from any API.
    """
    data: Any  # Generic field to store any type of data


def set_last_response(response: GenericResponse):
    setattr(app.state, "last_response", response)


def get_last_response() -> GenericResponse:
    return getattr(app.state, "last_response", GenericResponse(data=None))


@app.get("/reverse", response_model=GenericResponse)
def reverse_string(user_input: Annotated[str, Query(alias="in")]):
    """
    Reverse the words in the input string.
    """
    reversed_input = " ".join(user_input.split()[::-1])
    response = GenericResponse(data={"result": reversed_input})
    set_last_response(response)  # Store the last response
    return response


@app.get("/restore", response_model=GenericResponse)
def restore_last_result():
    """
    Return the last stored response.
    """
    return get_last_response()
