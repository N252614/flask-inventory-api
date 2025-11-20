# Helper functions for working with the OpenFoodFacts API

import requests

# Base URL for OpenFoodFacts product lookup by barcode
BASE_URL = "https://world.openfoodfacts.org/api/v0/product/{}.json"


def fetch_product_by_barcode(barcode: str):
    """
    Fetch product information from OpenFoodFacts by barcode.

    Returns a simplified dictionary with selected fields
    or None if the product is not found or request fails.
    """
    try:
        url = BASE_URL.format(barcode)
        response = requests.get(url, timeout=5)

        # If request failed, return None
        if response.status_code != 200:
            return None

        data = response.json()

        # OpenFoodFacts returns status 1 if product is found
        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "barcode": barcode,
            "name": product.get("product_name"),
            "brand": product.get("brands"),
            "ingredients": product.get("ingredients_text"),
            "categories": product.get("categories"),
        }

    except Exception:
        # In case of network error, timeouts, etc.
        return None