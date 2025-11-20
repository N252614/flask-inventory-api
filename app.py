from flask import Flask, jsonify, request
from inventory_data import inventory
from external_api import fetch_product_by_barcode

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Inventory API is running!"})

# GET /inventory -> get all
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

# GET /inventory/<id> -> get one item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404
# POST /inventory -> add a new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    # create new ID
    new_id = max(item["id"] for item in inventory) + 1

    new_item = {
        "id": new_id,
        "barcode": data.get("barcode"),
        "name": data.get("name"),
        "brand": data.get("brand"),
        "price": data.get("price"),
        "stock": data.get("stock"),
        "details": data.get("details", {})
    }

    inventory.append(new_item)
    return jsonify(new_item), 201

# PATCH /inventory/<id> -> update an existing item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    # Get JSON data from the request
    data = request.get_json()

    # Find the item in the inventory list
    for item in inventory:
        if item["id"] == item_id:
            # Update only the fields that are provided
            if "price" in data:
                item["price"] = data["price"]
            if "stock" in data:
                item["stock"] = data["stock"]
            if "name" in data:
                item["name"] = data["name"]
            if "brand" in data:
                item["brand"] = data["brand"]
            if "details" in data:
                item["details"] = data["details"]

            # Return the updated item
            return jsonify(item), 200

    # If item is not found, return an error
    return jsonify({"error": "Item not found"}), 404

# DELETE /inventory/<id> -> delete an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    # Look for the item and remove it from the list
    for index, item in enumerate(inventory):
        if item["id"] == item_id:
            deleted_item = inventory.pop(index)  # remove the item by index
            return jsonify({
                "message": "Item deleted",
                "item": deleted_item
            }), 200

    # If the item is not found, return an error
    return jsonify({"error": "Item not found"}), 404

# GET /external/<barcode> -> fetch product data from OpenFoodFacts
@app.route("/external/<string:barcode>", methods=["GET"])
def get_external_product(barcode):
    """
    Fetch product info from the OpenFoodFacts API by barcode.
    """
    product = fetch_product_by_barcode(barcode)

    # If the external API didn't return a product, send an error
    if product is None:
        return jsonify({"error": "Product not found in external API"}), 404

    # Otherwise, return the product data
    return jsonify(product), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)