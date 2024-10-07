from django.db import transaction

# Assuming you have a Debt model
from apps.debt_app.models import DebtModel


def create_debt_for_builder(builder_id, doc_id, user_id) -> DebtModel:
    # Use a transaction block to ensure the atomicity of the operation
    with transaction.atomic():
        # Create the Debt object and save it to the database
        debt = DebtModel.objects.create(
            builder_id=builder_id,
            user_id=user_id,
            document_id=doc_id
        )
    return debt


def create_debt(name, phone_number, phone_number2, address, doc_id, user_id, amount) -> DebtModel:
    # Use a transaction block to ensure atomicity of the operation
    with transaction.atomic():
        # Create the Debt object and save it to the database
        debt = DebtModel.objects.create(
            name=name,
            phone_number=phone_number,
            phone_number2=phone_number2,
            address=address,
            document_id=doc_id,
            user_id=user_id,
            amount=amount
        )
    return debt
