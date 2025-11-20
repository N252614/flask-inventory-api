import requests

# Base URL of our Flask API
BASE_URL = "http://127.0.0.1:5001"


def list_items():
    """Fetch and print all inventory items."""
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        print("\n--- Inventory items ---")
        for item in items:
            print(f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Stock: {item['stock']}")
        print("------------------------\n")
    else:
        print("Failed to fetch inventory.")


def get_item():
    """Fetch and print a single item by ID."""
    item_id = input("Enter item ID: ").strip()
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        item = response.json()
        print("\n--- Item details ---")
        print(item)
        print("--------------------\n")
    else:
        print("Item not found.")


def add_item():
    """Create a new inventory item."""
    print("Enter data for new item:")
    barcode = input("Barcode: ").strip()
    name = input("Name: ").strip()
    brand = input("Brand: ").strip()
    price = float(input("Price: ").strip())
    stock = int(input("Stock: ").strip())

    data = {
        "barcode": barcode,
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "details": {}
    }

    response = requests.post(f"{BASE_URL}/inventory", json=data)
    if response.status_code == 201:
        print("Item created:")
        print(response.json())
    else:
        print("Failed to create item.")


def update_item():
    """Update an existing item (price / stock / name / brand)."""
    item_id = input("Enter ID of item to update: ").strip()
    print("Leave field empty if you do NOT want to change it.")

    price_input = input("New price (optional): ").strip()
    stock_input = input("New stock (optional): ").strip()
    name_input = input("New name (optional): ").strip()
    brand_input = input("New brand (optional): ").strip()

    data = {}

    if price_input:
        data["price"] = float(price_input)
    if stock_input:
        data["stock"] = int(stock_input)
    if name_input:
        data["name"] = name_input
    if brand_input:
        data["brand"] = brand_input

    if not data:
        print("No fields to update.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
    if response.status_code == 200:
        print("Item updated:")
        print(response.json())
    else:
        print("Item not found or update failed.")


def delete_item():
    """Delete an item by ID."""
    item_id = input("Enter ID of item to delete: ").strip()
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print("Item deleted:")
        print(response.json())
    else:
        print("Item not found or delete failed.")


def lookup_external():
    """Use external API to fetch product info by barcode."""
    barcode = input("Enter product barcode: ").strip()
    response = requests.get(f"{BASE_URL}/external/{barcode}")
    if response.status_code == 200:
        product = response.json()
        print("\n--- External product info ---")
        print(product)
        print("-----------------------------\n")
    else:
        print("Product not found in external API.")


def main():
    """Main CLI loop."""
    while True:
        print("\n=== Inventory CLI ===")
        print("1. List all items")
        print("2. Get item by ID")
        print("3. Add new item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Lookup product via external API by barcode")
        print("7. Quit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            list_items()
        elif choice == "2":
            get_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            lookup_external()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()