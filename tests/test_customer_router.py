
def test_route_delete_customer(router):
    mock_service, client = router
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    mock_service.delete_customer.return_value = None
    response = client.delete(f"/customers/{customer_id}")

    assert response.status_code == 204
    mock_service.delete_customer.assert_called_once_with(customer_id)
