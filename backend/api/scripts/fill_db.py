from dotenv import load_dotenv
from os import getenv
import requests

from constants import (
    ENDPOINT_OFFICE_LIST,
    ENDPOINT_USER_LIST,
    ENDPOINT_PRODUCT_LIST,
    ENDPOINT_VARIANT_LIST,
)
from api.models import Conglomerate, Company, Office, BsaleUser, Product, Variant


def getAllDataFromAPI(endpoint, api_token, debug=False):
    r = requests.get(
        endpoint,
        headers={"access_token": api_token},
    )
    data = r.json()
    if debug:
        print(data)
    count = data["count"]
    items = data["items"]
    while len(items) < count:
        r = requests.get(
            endpoint + "?offset=",
            str(count),
            headers={"access_token": api_token},
        )
        data = r.json()
        items += data["items"]
    return items


def run():
    load_dotenv()
    print("flushing DB")
    Company.objects.all().delete()
    Conglomerate.objects.all().delete()

    cong = Conglomerate(name="Punto Saludes")
    cong.save()

    print("conglomerates:", len(Conglomerate.objects.all()))

    comp1 = Company(
        conglomerate=cong,
        name="ARTICULOS MEDICOS PUNTOSALUD SPA",
        email="ccarreno@psalud.cl",
        rut="77383983-2",
        api_token=getenv("API_TOKEN_SPA"),
    )
    comp1.save()

    comp2 = Company(
        conglomerate=cong,
        name="Comercializadora Artículo médicos Punto Salud S.A",
        email="ccarreno@psalud.cl",
        rut="76091474-6",
        api_token=getenv("API_TOKEN_PSALUD"),
    )
    comp2.save()

    print("companies:", len(Company.objects.all()))

    for comp in [comp1, comp2]:
        print("fetching offices for", comp.name)
        offices = getAllDataFromAPI(ENDPOINT_OFFICE_LIST, comp.api_token)
        print("fetched", len(offices), "items")
        for officeData in offices:
            # print("office:", officeData["name"])
            office = Office(
                company=comp,
                # campos bsale
                name=officeData["name"],
                bsaleId=officeData["id"],
                descripcion=officeData["description"],
                address=officeData["address"],
                latitude=(
                    0 if officeData["latitude"] == "" else float(officeData["latitude"])
                ),
                longitude=(
                    0
                    if officeData["longitude"] == ""
                    else float(officeData["longitude"])
                ),
                isVirtual=(officeData["isVirtual"] == 1),
                country=officeData["country"],
                municipality=officeData["municipality"],
                city=officeData["city"],
                zipCode=officeData["zipCode"],
                costCenter=officeData["costCenter"],
                state=(officeData["state"] == 1),
            ).save()
    print("offices:", len(Office.objects.all()))

    for comp in [comp1, comp2]:
        print("fetching users for", comp.name)
        users = getAllDataFromAPI(ENDPOINT_USER_LIST, comp.api_token)
        print("fetched", len(users), "items")
        offices = Office.objects.filter(company=comp.id)
        # print(offices)
        for userData in users:
            # print("user:", userData["firstName"], userData["lastName"])
            office = offices.filter(bsaleId=userData["office"]["id"])
            assert len(office) == 1
            bsaleuser = BsaleUser(
                company=comp,
                bsaleId=userData["id"],
                firstName=userData["firstName"],
                lastName=userData["lastName"],
                email=userData["email"],
                state=userData["state"] == 1,
                defaultOffice=office[0],
            ).save()
        # print(users)
    print("users:", len(BsaleUser.objects.all()))

    for comp in [comp1, comp2]:
        print("fetching products for", comp.name)
        products = getAllDataFromAPI(ENDPOINT_PRODUCT_LIST, comp.api_token)
        print("fetched", len(products), "items")
        for productData in products:
            # print(productData)
            product = Product(
                company=comp,
                bsaleId=productData["id"],
                name=productData["name"],
                editable=productData["isEditable"] == 1,
                state=productData["state"] == 1,
            ).save()
    print("products:", len(Product.objects.all()))

    for comp in [comp1, comp2]:
        print("fetching variants for", comp.name)
        variants = getAllDataFromAPI(ENDPOINT_VARIANT_LIST, comp.api_token)
        print("fetched", len(variants), "items")
        products = Product.objects.filter(company=comp.id)
        # print(offices)
        for variantData in variants:
            product = products.filter(
                bsaleId=variantData["product"]["id"], company=comp
            )
            assert len(product) == 1
            variant = Variant(
                product=product[0],
                bsaleId=variantData["id"],
                description=variantData["description"],
                state=variantData["state"] == 1,
                barCode=variantData["barCode"],
                code=variantData["code"],
            ).save()
    print("variants:", len(Variant.objects.all()))

    print("script done!")
    return
