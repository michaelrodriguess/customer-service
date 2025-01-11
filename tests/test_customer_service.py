from pytest import raises


def test_delete_customer_calls_storage(service):
    service = service
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    service.storage.delete_customer(customer_id)
    service.storage.delete_customer.assert_called_once_with(customer_id)


def test_delete_customer_key_error(service):
    service = service
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    service.storage.delete_customer.side_effect = KeyError("Simulating the KeyError")

    with raises(KeyError):
        service.delete_customer(customer_id)

    service.storage.delete_customer.assert_called_once()
