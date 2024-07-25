from dotenv import load_dotenv
from os import getenv
import requests

from constants import ENDPOINT_OFFICE_LIST


def run():
    print("script!")
    load_dotenv()

    api_token = getenv("API_TOKEN_PSALUD")

    r = requests.get(
        ENDPOINT_OFFICE_LIST,
        headers={"access_token": api_token},
    )
    print(r.status_code)
    print(r.json)
    return
