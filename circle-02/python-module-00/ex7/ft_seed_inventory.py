def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    name = seed_type.capitalize()
    string = None
    match unit:
        case "packets":
            string = f"{name} seeds: {quantity} {unit} available"
        case "grams":
            string = f"{name} seeds: {quantity} {unit} total"
        case "area":
            string = f"{name} seeds: covers {quantity} square meters"
        case _:
            string = "Unknown unit type"
    print(string)

# ft_seed_inventory("tomato", 15, "packets")
# ft_seed_inventory("carrot", 8, "grams")
# ft_seed_inventory("lettuce", 12, "area")
