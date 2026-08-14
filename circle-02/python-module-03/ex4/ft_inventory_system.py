import sys
from typing import Dict, List


def parse_inventory(args: List[str]) -> Dict[str, int]:
    inventory: Dict[str, int] = {}

    for arg in args:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue

        parts = arg.split(":")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            print(f"Error - invalid parameter '{arg}'")
            continue

        item_name = parts[0]
        value_str = parts[1]

        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue

        try:
            inventory[item_name] = int(value_str)
        except ValueError:
            print(
                f"Quantity error for '{item_name}': "
                f"invalid literal for int() with base 10: '{value_str}'"
            )

    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")

    raw_args = sys.argv[1:]
    inventory = parse_inventory(raw_args)

    print(f"Got inventory: {inventory}")

    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    total_quantity = sum(inventory.values())
    print(f"Total quantity of the {len(item_list)} items: {total_quantity}")

    if total_quantity > 0:
        for item in item_list:
            qty = inventory[item]
            percentage = round((qty / total_quantity) * 100, 1)
            print(f"Item {item} represents {percentage:.1f}%")

    most_abundant = None
    least_abundant = None

    for item in item_list:
        qty = inventory[item]
        if most_abundant is None or qty > inventory[most_abundant]:
            most_abundant = item
        if least_abundant is None or qty < inventory[least_abundant]:
            least_abundant = item

    if most_abundant and least_abundant:
        print(
            f"Item most abundant: {most_abundant} "
            f"with quantity {inventory[most_abundant]}"
        )
        print(
            f"Item least abundant: {least_abundant} "
            f"with quantity {inventory[least_abundant]}"
        )

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
