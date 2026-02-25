from fastapi import APIRouter


finance_endpoints = APIRouter()


@finance_endpoints.get()
def list_documents():
    return


@finance_endpoints.post()
def create_document():
    return


@finance_endpoints.patch()
def update_document():
    return


@finance_endpoints.delete()
def delete_document():
    return
