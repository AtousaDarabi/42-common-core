class GardenError(Exception):
    def __init__(self, message: str
                 = "A general garden error occurred") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown watering error") -> None:
        super().__init__(message)


def check_garden_element(element_type: str) -> None:
    if element_type == "plant":
        raise PlantError("The tomato plant is wilting!")
    elif element_type == "water":
        raise WaterError("Not enough water in the tank!")
    else:
        raise GardenError()


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")

    print("\nTesting PlantError...")
    try:
        check_garden_element("plant")
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("\nTesting WaterError...")
    try:
        check_garden_element("water")
    except WaterError as e:
        print(f"Caught WaterError: {e}")

    print("\nTesting catching all garden errors...")
    for element in ["plant", "water"]:
        try:
            check_garden_element(element)
        except GardenError as e:
            print(f"Caught GardenError: {e}")

    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
