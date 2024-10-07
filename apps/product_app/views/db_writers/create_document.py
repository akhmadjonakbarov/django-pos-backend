from apps.user_app.models import CustomUserModel
from ...models import DocumentModel
from django.db import transaction


def create_document(doc_type: str, user: CustomUserModel) -> DocumentModel:
    with transaction.atomic():
        document = DocumentModel.objects.create(
            doc_type=doc_type,
            user=user,
        )
    return document
