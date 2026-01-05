# note that this is vibecoded and therefore not good at all (we only used it for data collection)

from openfoodfacts import API, APIVersion, Country, Environment, Flavor

TARGET_FILE = "ingredients_list.py"

api = API(
    user_agent="tastyBarcodes/v0.1 (boom@thetwoboom.xyz)",
    username=None,
    password=None,
    country=Country.world,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)


def fetch_ingredients(barcode: str) -> list[str]:
    product = api.product.get(barcode)

    if not product:
        print(f"❌ Product not found: {barcode}")
        return []

    ingredients = product.get("ingredients")
    if ingredients:
        return [
            ing.get("text").strip()
            for ing in ingredients
            if ing.get("text")
        ]

    text = product.get("ingredients_text")
    if text:
        return [i.strip() for i in text.split(",") if i.strip()]

    return []


def append_ingredients_inside_list(file_path: str, ingredients: list[str]):
    if not ingredients:
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # find closing bracket of the list
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "]":
            insert_at = i
            break
    else:
        raise RuntimeError("No closing ']' found in ingredients_list.py")

    new_lines = [f'    "{ing}",\n' for ing in ingredients]

    lines[insert_at:insert_at] = new_lines

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    print("Enter barcodes (one per line). Empty line to finish.\n")

    while True:
        barcode = input("Barcode: ").strip()
        if not barcode:
            break

        items = fetch_ingredients(barcode)
        append_ingredients_inside_list(TARGET_FILE, items)
        print(f"✅ Added {len(items)} ingredients\n")
