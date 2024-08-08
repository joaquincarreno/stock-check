from dotenv import load_dotenv
from os import getenv
import requests

from constants import (
    ENDPOINT_VARIANT
)
from api.models import (
    Conglomerate,
    Company,
    Office,
    BsaleUser,
    Product,
    ProductType,
    Variant,
)


def run():
    load_dotenv()
    api_token = getenv("API_TOKEN_SPA")
    # print(ENDPOINT_VARIANT + "/3232.json")
    # r_var = requests.get("https://api.bsale.io/v1/variants/3232.json", 
    #     headers={"access_token": api_token})
    # data = r_var.json()
    # prodId = data["product"]["id"]
    # print(prodId)
    # prods = Product.objects.filter(bsaleId=prodId)
    # print(Product.objects.get(bsaleId=prodId))
    print(len(list(Product.objects.all().values("bsaleId").distinct())))
    for p in list(Product.objects.all().values("bsaleId").distinct()):
        print(p)