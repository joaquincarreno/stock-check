from dotenv import load_dotenv
from os import getenv
import requests

from constants import (
    ENDPOINT_OFFICE_LIST,
    ENDPOINT_USER_LIST,
    ENDPOINT_PRODUCT_LIST,
    ENDPOINT_VARIANT_LIST,
    ENDPOINT_PRODUCT_TYPES_LIST,
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


def getAllDataFromAPI(endpoint, api_token, debug=False):
    r = requests.get(
        endpoint + "?limit=50",
        headers={"access_token": api_token},
    )
    data = r.json()
    if debug:
        print(data)
    count = data["count"]
    items = data["items"]
    while len(items) < count:
        r = requests.get(
            endpoint + "?limit=50&offset=" + str(len(items)),
            headers={"access_token": api_token},
        )
        data = r.json()
        items += data["items"]
    return items


def getSampleDataFromAPI(endpoint, api_token, debug=False):
    r = requests.get(
        endpoint + "?limit=50",
        headers={"access_token": api_token},
    )
    data = r.json()
    if debug:
        print(data)
    count = 100
    items = data["items"]
    while len(items) < count:
        r = requests.get(
            endpoint + "?limit=50&offset=" + str(len(items)),
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
                state=userData["state"] == 0,
                defaultOffice=office[0],
            ).save()
        # print(users)
    print("users:", len(BsaleUser.objects.all()))

    for comp in [comp1, comp2]:
        print("fetching product types for", comp.name)
        products = getAllDataFromAPI(ENDPOINT_PRODUCT_TYPES_LIST, comp.api_token)
        print("fetched", len(products), "items")
        for productTypeData in products:
            ProductType(
                company=comp,
                bsaleId=productTypeData["id"],
                name=productTypeData["name"],
                editable=productTypeData["isEditable"] == 1,
                state=productTypeData["state"] == 1,
            ).save()
    print("product types:", len(ProductType.objects.all()))

    for comp in [comp1, comp2]:
        ids = []
        print("fetching products for", comp.name)
        products = getAllDataFromAPI(ENDPOINT_PRODUCT_LIST, comp.api_token)
        print("fetched", len(products), "items")
        for productData in products:
            p_type = ProductType.objects.get(
                company=comp, bsaleId=productData["product_type"]["id"]
            )
            product = Product(
                company=comp,
                bsaleId=productData["id"],
                name=productData["name"],
                description=productData["description"],
                classification=productData["classification"],
                ledgerAccount=productData["ledgerAccount"],
                costCenter=productData["costCenter"],
                allowDecimal=productData["allowDecimal"] == 1,
                stockControl=productData["stockControl"] == 1,
                state=productData["state"] == 1,
                productType=p_type,
            ).save()
    print("products:", len(Product.objects.all()))

    for comp in [comp1, comp2]:
        print("fetching variants for", comp.name)
        variants = getAllDataFromAPI(ENDPOINT_VARIANT_LIST, comp.api_token)
        print("fetched", len(variants), "items")
        for variantData in variants:
            # print(variantData["id"], len(Product.objects.filter(bsaleId=variantData["product"]["id"])))
            product = Product.objects.get(
                bsaleId=variantData["product"]["id"], company=comp
            )
            variant = Variant(
                product=product,
                bsaleId=variantData["id"],
                description=variantData["description"],
                state=variantData["state"] == 1,
                barCode=variantData["barCode"],
                code=variantData["code"],
            ).save()
    print("variants:", len(Variant.objects.all()))

    print("script done!")
    return
