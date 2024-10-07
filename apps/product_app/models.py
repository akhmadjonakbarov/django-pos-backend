from django.db import models

from apps.base_app.models import BaseModel
from apps.builder_app.models import BuilderModel
from apps.currency_app.models import CurrencyModel
from apps.provider_app.models import ProviderModel
from apps.user_app.models import CustomUserModel


class CompanyModel(BaseModel):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'company'
        ordering = ['-id']
        verbose_name_plural = 'companies'


class ColorModel(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'color'
        ordering = ['-id']
        verbose_name_plural = 'colors'


class CategoryModel(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'category'
        ordering = ['-id']
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)


class UnitModel(BaseModel):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'unit'
        verbose_name_plural = 'units'

    def __str__(self):
        return str(self.value)


class ItemModel(BaseModel):
    name = models.CharField(max_length=500)
    barcode = models.CharField(max_length=500, unique=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    unit = models.ForeignKey(UnitModel, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'item'
        ordering = ['-id']
        verbose_name_plural = 'items'

    def __str__(self):
        return str(self.name)


class ItemColor(BaseModel):
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorModel, on_delete=models.CASCADE, null=True, blank=True)  # Nullable color reference

    class Meta:
        ordering = ['-id']
        unique_together = ('item', 'color')  # Prevents duplicate color entries for the same product

    def __str__(self):
        return f"{self.item.name} - {self.color.name if self.color else 'No Color'}"


class DocumentModel(BaseModel):
    SELL = 'sell'
    BUY = 'buy'

    TRANSACTION_CHOICES = [
        (SELL, 'Sell'),
        (BUY, 'Buy'),
    ]
    reg_date = models.DateTimeField(auto_now_add=True)
    doc_type = models.CharField(
        max_length=4,
        choices=TRANSACTION_CHOICES,
    )

    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, blank=True, null=True)
    builder = models.ForeignKey(BuilderModel, on_delete=models.CASCADE, blank=True, null=True, related_name='documents')

    def __str__(self):
        return f'{self.doc_type} - {self.reg_date}'

    class Meta:
        db_table = 'document'
        ordering = ['-id']
        verbose_name_plural = 'documents'


class DocumentItemModel(BaseModel):
    qty = models.IntegerField(default=0, null=False)
    can_be_cheaper = models.BooleanField(default=False, null=False)
    document = models.ForeignKey(
        DocumentModel,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey(
        ItemModel,
        on_delete=models.CASCADE,
        related_name='doc_items'
    )
    income_price_usd = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    income_price = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    selling_price = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    discount_price = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    selling_percentage = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.CASCADE,
        null=True,
        related_name='doc_items'
    )
    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name='doc_items'
    )

    class Meta:
        db_table = 'doc_item'  # Specify the database table name
        verbose_name_plural = 'document items'  # Specify the plural form of the model name for admin panel display
        ordering = ['-id']  # Specify the order in which objects will be displayed in the admin panel

    def __str__(self):
        return f'{self.document} - {self.item}'


class DocumentItemBalanceModel(BaseModel):
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE, related_name='doc_item_balances')
    qty = models.IntegerField(default=0)
    can_be_cheaper = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='doc_item_balances')
    income_price_usd = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    income_price = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    selling_price = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    discount_price = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    selling_percentage = models.DecimalField(decimal_places=3, max_digits=15, default=0.0, blank=True)
    document = models.ForeignKey(DocumentModel, on_delete=models.CASCADE, related_name='doc_item_balances')
    doc_item = models.ForeignKey(DocumentItemModel, on_delete=models.CASCADE, related_name='balances')
    currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.CASCADE,
        null=True,
        related_name='doc_item_balances'
    )

    class Meta:
        ordering = ['-id']
        db_table = 'doc_item_balance'  # Specify the database table name
        verbose_name_plural = 'document item balances'

    def __str__(self):
        return f'ProductDocItemBalance(item={self.item}, qty={self.qty})'
