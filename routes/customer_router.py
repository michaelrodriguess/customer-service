"""
Esse módulo lida com as rotas de clientes.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
import logging
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Response, Depends, Request

from services.customer_service import CustomerService
from models.customer_model import Customer, CustomerUpdate
from exceptions.customer_exceptions import EntityNotFound

router = APIRouter()
logger = logging.getLogger(__name__)


def get_customer_service(request: Request) -> CustomerService:
    """
    Recupera a instância do serviço de clientes do estado da requisição.

    Args:
        request (Request): Objeto da requisição atual.

    Returns:
        CustomerService: Serviço de clientes.
    """
    return request.state.customer_service


ServiceDep = Annotated[CustomerService, Depends(get_customer_service)]


@router.get("/customers", response_model=List[Customer])
def get_all_customers(service: ServiceDep):
    """
    Retorna todos os clientes cadastrados.

    Args:
        service (CustomerService): Serviço de clientes.

    Returns:
        List[Customer]: Lista de todos os clientes.
    """
    logger.info("Getting all customers")
    customers = service.get_all_customers()
    logger.info(
        "Get all data of customers request finished with response=%s", customers
    )
    return customers


@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer_by_id(customer_id: str, service: ServiceDep):
    """
    Retorna os detalhes de um cliente pelo ID.

    Args:
        customer_id (str): ID do cliente.
        service (CustomerService): Serviço de clientes.

    Returns:
        Customer: Cliente encontrado.

    Raises:
        HTTPException: Se o cliente não for encontrado.
    """
    try:
        logger.info("Getting customer with id=%s", customer_id)
        customer = service.get_customer_by_id(customer_id)
        logger.info("Get customer by id request finished with response=%s", customer)
        return customer
    except ValueError as ex:
        logger.warning("Customer not found: id=%s", id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {id}",
        ) from ex


@router.post("/customers", response_model=Customer)
def create_customer(customer_data: Customer, service: ServiceDep):
    """
    Cria um novo cliente.

    Args:
        customer_data (Customer): Dados do cliente a ser criado.
        service (CustomerService): Serviço de clientes.

    Returns:
        Customer: Cliente criado.
    """
    logger.info("Creating customer with this data=%s", customer_data)
    created_customer = service.create_customer(customer_data)
    logger.info("Create customer request finished with response=%s", created_customer)
    return created_customer


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str, service: ServiceDep):
    """
    Exclui um cliente pelo ID.

    Args:
        customer_id (str): ID do cliente.
        service (CustomerService): Serviço de clientes.

    Returns:
        Response: Resposta HTTP com status 204.

    Raises:
        HTTPException: Se o cliente não for encontrado.
    """
    try:
        logger.info("Deleting customer with id=%s", customer_id)
        service.delete_customer(customer_id)
        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.put("/customers", response_model=CustomerUpdate)
def update_customer(customer_update: Customer, service: ServiceDep):
    """
    Atualiza totalmente os dados de um cliente.

    Args:
        customer_update (Customer): Dados do cliente a serem atualizados.
        service (CustomerService): Serviço de clientes.

    Returns:
        CustomerUpdate: Cliente atualizado.

    Raises:
        HTTPException: Se o cliente não for encontrado.
    """
    logger.info("Starting the process to fully update customer %s", customer_update)
    try:
        updated_customer = service.update_customer(customer_update)
        logger.info(
            "Full update customer request finished with response=%s", updated_customer
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message) from e


@router.patch("/customers", response_model=CustomerUpdate)
def patch_customer(customer_update: CustomerUpdate, service: ServiceDep):
    """
    Atualiza parcialmente os dados de um cliente.

    Args:
        customer_update (CustomerUpdate): Dados do cliente a serem atualizados.
        service (CustomerService): Serviço de clientes.

    Returns:
        CustomerUpdate: Cliente atualizado.

    Raises:
        HTTPException: Se o cliente não for encontrado.
    """
    logger.info("Starting the process to partially update customer %s", customer_update)
    try:
        updated_customer = service.patch_customer(customer_update)
        logger.info(
            "Partial update customer request finished with response=%s",
            updated_customer,
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message) from e
