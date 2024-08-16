import pytest

from server import app as flask_app


@pytest.fixture
def app():
    """
    This fixture provides a Flask application instance
    for testing purposes.
    """
    yield flask_app


@pytest.fixture
def client(app):
    """
    This fixture provides a test client that can be used
    to simulate HTTP requests to the Flask application.
    """
    return app.test_client()


def test_get_products(client):
    """
    Test the GET /products endpoint.
    """
    # Simulate a GET request to the /products endpoint
    response = client.get("/products")

    # Ensure that the request was successful (status code 200)
    assert response.status_code == 200

    # Ensure the response is in JSON format
    assert response.content_type == "application/json"

    # Check that the response contains a list of products
    data = response.get_json()
    assert isinstance(data, list)

    # If you have known data in your database, you can perform more specific checks:
    if data:
        product = data[0]
        assert "product_id" in product
        assert "name" in product
        assert "uom_id" in product
        assert "price_per_unit" in product
        assert "uom_name" in product
