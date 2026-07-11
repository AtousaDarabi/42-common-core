#! /usr/bin/env python3

class Plant:
    class PlantStats:
        def __init__(self) -> None:
            self._grow_count = 0
            self._age_count = 0
            self._show_count = 0

        def increment_grow(self) -> None:
            self._grow_count += 1

        def increment_age(self) -> None:
            self._age_count += 1

        def increment_show(self) -> None:
            self._show_count += 1

        def display(self) -> None:
            print(f"Stats: {self._grow_count} grow, {self._age_count} age, "
                  f"{self._show_count} show")

    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name
        self._stats = self.PlantStats()

        if height >= 0:
            self._height = float(height)
        else:
            print(f"{self._name}: Error, height can't be negative")
            self._height = 0.0

        if age >= 0:
            self._age = int(age)
        else:
            print(f"{self._name}: Error, age can't be negative")
            self._age = 0

    @staticmethod
    def is_older_than_year(age_days: int) -> bool:
        return age_days > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    def get_name(self) -> str:
        return self._name

    def get_stats(self) -> PlantStats:
        return self._stats

    def grow(self, value: float) -> None:
        if value >= 0:
            self._height += float(value)
            self._stats.increment_grow()

    def age_by(self, days: int) -> None:
        if days >= 0:
            self._age += int(days)
            self._stats.increment_age()

    def show(self) -> None:
        self._stats.increment_show()
        print(f"{self._name}: {self._height:.1f}cm, {self._age} days old")


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self._color = color
        self._has_bloomed = False

    def bloom(self) -> None:
        self._has_bloomed = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._has_bloomed:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter = trunk_diameter
        self._shade_count = 0

    def produce_shade(self) -> None:
        self._shade_count += 1
        print(f"Tree {self._name} now produces a shade of {self._height:.1f}cm"
              f" long and {self._trunk_diameter:.1f}cm wide.")

    def get_shade_count(self) -> int:
        return self._shade_count

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter:.1f}cm")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str) -> None:
        super().__init__(name, height, age)
        self._harvest_season = harvest_season
        self._nutritional_value = 0

    def grow_and_age(self, days: int, height_increase: float) -> None:
        self.age_by(days)
        self.grow(height_increase)
        self._nutritional_value += days

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


class Seed(Flower):
    def __init__(self, name: str, heigh: float, age: int, color: str) -> None:
        super().__init__(name, heigh, age, color)
        self._seed_count = 0

    def bloom(self) -> None:
        super().bloom()
        self._seed_count = 42

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self._seed_count}")


def display_plant_statistics(plant: Plant) -> None:
    plant.get_stats().display()
    if hasattr(plant, 'get_shade_count'):
        print(f"{plant.get_shade_count()} shade")


def main() -> None:
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[statistics for Rose]")
    display_plant_statistics(rose)

    print("[asking the rose to grow and bloom]")
    rose.grow(8.0)
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_plant_statistics(rose)

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[statistics for Oak]")
    display_plant_statistics(oak)

    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    display_plant_statistics(oak)

    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow(30.0)
    sunflower.age_by(20)
    sunflower.bloom()
    sunflower.show()
    print("[statistics for Sunflower]")
    display_plant_statistics(sunflower)

    print("=== Anonymous")
    anon_plant = Plant.create_anonymous()
    anon_plant.show()
    print("[statistics for Unknown plant]")
    display_plant_statistics(anon_plant)


if __name__ == "__main__":
    main()
