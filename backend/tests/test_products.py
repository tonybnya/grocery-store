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
    products = response.get_json()
    assert isinstance(products, list)

    # Perform more specific checks (assuming I know the data in the db)
    if products:
        product = products[0]
        assert "product_id" in product
        assert "name" in product
        assert "uom_id" in product
        assert "price_per_unit" in product
        assert "uom_name" in product


def test_get_single_product(client):
    """
    Test the GET /products/{product_id} endpoint.
    """
    # Define an existing ID in the database
    product_id: int = 1

    # Simulate a GET request to the /products/1 endpoint
    response = client.get("/products/" + str(product_id))

    # Ensure that the request was successful (status code 200)
    assert response.status_code == 200

    # Ensure the response is in JSON format
    assert response.content_type == "application/json"

    # Check that the response contains a dictionary
    product = response.get_json()
    assert isinstance(product, dict)

    # I know the product with the ID 1 in the db
    if product:
        assert product.get("product_id") == 1
        assert product.get("name") == "toothpaste (Colgate)"
        assert product.get("price_per_unit") == 1500.0
        assert product.get("uom_id") == 2
