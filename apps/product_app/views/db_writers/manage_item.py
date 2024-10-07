from django.db import transaction
from ...models import DocumentItemModel, DocumentItemBalanceModel


def create_doc_item(element: dict, document_id, user_id) -> DocumentItemModel:
    """
    Create a new ProductDocItem in the database within a transaction.

    Args:
        element: A dictionary containing item data.
        document_id: The ID of the product document.
        user_id: The ID of the user creating the document item.

    Returns:
        ProductDocItem: The created document item instance.
    """
    with transaction.atomic():  # Begin a transaction
        discount_price = 0
        if 'discount_price' in element:
            discount_price = element['discount_price']
        doc_item = DocumentItemModel.objects.create(
            document_id=document_id,
            qty=element['qty'],
            currency_id=element['currency']['id'] if element['currency']['id'] != -1 else None,
            income_price=element['income_price'],
            selling_price=element['selling_price'],
            discount_price=discount_price,
            income_price_usd=element['income_price_usd'],
            can_be_cheaper=element['can_be_cheaper'],
            selling_percentage=element['selling_percentage'],
            item_id=element['item']['id'],
            user_id=user_id,
        )
    return doc_item


def create_doc_item_balance(user_id, doc_item) -> DocumentItemBalanceModel:
    """
               Create a new ProductDocItemBalance in the database.

               Args:
                   user_id: The ID of the user creating the document item balance.
                   item_id: The ID of the item.
                   new_product_doc_item: An instance of the product document item.

               Returns:
                   ProductDocItemBalance: The created document item balance instance.
                   :param doc_item:
               """
    with transaction.atomic():  # Begin a transaction
        item_balance = DocumentItemBalanceModel.objects.create(
            item=doc_item.item,
            qty=doc_item.qty,
            can_be_cheaper=doc_item.can_be_cheaper,
            income_price=doc_item.income_price,
            selling_price=doc_item.selling_price,
            user_id=user_id,
            currency=doc_item.currency,
            income_price_usd=doc_item.income_price_usd,
            document=doc_item.document,
            doc_item=doc_item,
            selling_percentage=doc_item.selling_percentage,
        )
    return item_balance


def update_doc_item_balance(total_product, new_doc_item, product_item_balance):
    """
    Update an existing ProductDocItemBalance in the database.

    Args:
        total_product: The new total quantity of the product.
        new_doc_item: An instance of the product document item with updated values.
        product_item_balance: The instance of ProductDocItemBalance to update.

    Returns:
        ProductDocItemBalance: The updated document item balance instance.
    """
    with transaction.atomic():  # Begin a transaction
        product_item_balance.qty = total_product
        product_item_balance.can_be_cheaper = new_doc_item.can_be_cheaper
        product_item_balance.income_price = new_doc_item.income_price
        product_item_balance.income_price_usd = new_doc_item.income_price_usd
        product_item_balance.selling_price = new_doc_item.selling_price
        product_item_balance.selling_percentage = new_doc_item.selling_percentage

        product_item_balance.save()  # Save the updated instance

    return product_item_balance
