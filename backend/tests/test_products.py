"""
Test suite for the products endpoints.
"""

from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from server import app as flask_app


@pytest.fixture
def app() -> Generator[Flask, Flask, Flask]:
    """
    This fixture provides a Flask application instance
    for testing purposes.
    """
    yield flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    This fixture provides a test client that can be used
    to simulate HTTP requests to the Flask application.
    """
    return app.test_client()


def test_get_products(client: FlaskClient) -> None:
    """
    Test the GET /products endpoint.
    """
    # Simulate a GET request to /products endpoint
    response = client.get("/products")

    # Ensure the request is successful (status code 200)
    assert response.status_code == 200

    # Ensure the response is in JSON format
    assert response.content_type == "application/json"

    # Store the response body into a variable
    products = response.get_json()

    # Check that the response contains a list of products
    assert isinstance(products, list)

    # Perform more specific checks
    # Since I know the structure of data
    # I check the fields of the first product (a dictionary object)
    if products:
        product = products[0]
        assert "product_id" in product
        assert "name" in product
        assert "uom_id" in product
        assert "price_per_unit" in product
        assert "uom_name" in product


def test_get_single_product(client: FlaskClient) -> None:
    """
    Test the GET /products/{product_id} endpoint.
    """
    # Define a variable containing an existing ID in the db
    product_id: int = 1

    # Simulate a GET request to /products/1 endpoint
    response = client.get(f"/products/{product_id}")

    # Ensure the request is successful (status code 200)
    assert response.status_code == 200

    # Ensure the response is in JSON format
    assert response.content_type == "application/json"

    # Store the response body into a variable
    product = response.get_json()

    # Check that the response contains a dictionary
    assert isinstance(product, dict)

    # I know the product with the ID 1 in the db
    # So, I check the values in the dictionary
    if product:
        assert product.get("product_id") == 1
        assert product.get("name") == "toothpaste"
        assert product.get("price_per_unit") == 1000.0
        assert product.get("uom_id") == 2


def test_get_nonexistent_product(client: FlaskClient) -> None:
    """
    Test the GET /products/{product_id} endpoint for a nonexisting product.
    """
    # Define a variable containing a nonexisting ID in the db
    nonexistent_id = 9999

    # Simulate a GET request to /products/{nonexistent_id} endpoint
    response = client.get(f"/products/{nonexistent_id}")

    # Ensure the request failed (status code 404)
    assert response.status_code == 404

    # Ensure the response is in JSON format
    assert response.content_type == "application/json"

    # Store the response body (the error message in this case) into a variable
    error_message = response.get_json()

    # Ensure the error message contains the "error" field
    assert "error" in error_message

    # Ensure the value of the "error" field is the same
    # as defined in the routes implementation
    assert error_message["error"] == "Product not found"
