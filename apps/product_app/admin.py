from django.contrib import admin
from .models import ItemModel, DocumentItemModel, \
    CompanyModel, DocumentModel, CategoryModel, \
    DocumentItemBalanceModel, UnitModel, ColorModel, ItemColor


@admin.register(ColorModel)
class ColorModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemColor)
class ItemColorAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemModel)
class ItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentItemModel)
class DocumentItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentItemBalanceModel)
class DocumentItemBalanceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyModel)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(DocumentModel)
class DocumentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitModel)
class UnitModelAdmin(admin.ModelAdmin):
    pass
