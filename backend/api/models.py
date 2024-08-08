from django.db import models


class Conglomerate(models.Model):
    name = models.TextField(null=False)


# models for bsale-retrieved resources
class Company(models.Model):
    conglomerate = models.ForeignKey(Conglomerate, on_delete=models.PROTECT)
    name = models.TextField(null=False)
    api_token = models.TextField(null=False, default="")
    email = models.TextField(null=False, default="ejemplo@correo.cl")
    rut = models.TextField(null=False, default="1111111-k")


class Office(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # campos bsale
    name = models.TextField()
    bsaleId = models.IntegerField(null=False)
    descripcion = models.TextField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    isVirtual = models.BooleanField()
    country = models.TextField()
    municipality = models.TextField()
    city = models.TextField()
    zipCode = models.TextField()
    costCenter = models.TextField()
    state = models.BooleanField()


class BsaleUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    bsaleId = models.IntegerField()
    firstName = models.TextField()
    lastName = models.TextField()
    email = models.TextField()
    state = models.BooleanField()
    defaultOffice = models.ForeignKey(Office, on_delete=models.CASCADE)


class ProductType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    bsaleId = models.IntegerField()
    name = models.TextField()
    editable = models.BooleanField()
    state = models.BooleanField()


product_classifications = ((0, "product"), (1, "service"), (3, "pack/promotion"))


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    bsaleId = models.IntegerField()
    name = models.TextField()
    description = models.TextField(null=True)
    classification = models.IntegerField(choices=product_classifications)
    ledgerAccount = models.TextField(null=True)
    costCenter = models.TextField(null=True)
    allowDecimal = models.BooleanField()
    stockControl = models.BooleanField()
    state = models.BooleanField()
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)


class Variant(models.Model):
    bsaleId = models.IntegerField()
    description = models.TextField()
    state = models.BooleanField()
    barCode = models.TextField()
    code = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


user_choices = ((0, "Admin"), (1, "Seller"))


class User(models.Model):
    userType = models.IntegerField(choices=user_choices, default=1)
    conglomerate = models.ForeignKey(
        Conglomerate, on_delete=models.PROTECT
    )  # cambiar a conglomerado


# models for inventary data
class StockReport(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reporter = models.ForeignKey(BsaleUser, on_delete=models.DO_NOTHING)


class VirtualStock(models.Model):
    quantity = models.FloatField()
    quantityReserved = models.FloatField()
    quantityAvailable = models.FloatField()
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    report = models.ForeignKey(StockReport, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class FisicalStock(models.Model):
    quantity = models.FloatField()
    report = models.ForeignKey(StockReport, on_delete=models.CASCADE)

    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# many to many relations
class bsaleUserXoffice(models.Model):
    bsaleUser = models.ForeignKey(BsaleUser, on_delete=models.DO_NOTHING)
    office = models.ForeignKey(Office, on_delete=models.DO_NOTHING)


class userXbsaleUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bsaleUser = models.ForeignKey(BsaleUser, on_delete=models.DO_NOTHING)
