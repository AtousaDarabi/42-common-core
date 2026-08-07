class GardenError(Exception):
    def __init__(self, message: str
                 = "A general garden error occurred") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    if not plant_name or plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")

    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plant_list: list[str]) -> None:
    print("Opening watering system")
    try:
        for plant in plant_list:
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")

    print("Testing valid plants...")
    valid_plants = ["Tomato", "Lettuce", "Carrots"]
    test_watering_system(valid_plants)

    print("\nTesting invalid plants...")
    invalid_plants = ["Tomato", "lettuce", "Carrots"]
    test_watering_system(invalid_plants)

    print("\nCleanup always happens, even with errors!")
