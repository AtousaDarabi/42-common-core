#! /usr/bin/env python3

class Plant:

    def __init__(self, name, height, age) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        days = "day" if self.age == 1 else "days"
        print(f"Created: {self.name.capitalize()}: {round(self.height, 1)}cm, {self.age} {days} old")
    
    def grow_plant(self) -> None:
        growth = 0.8
        self.height += growth
    
    def age_plant(self) -> None:
        self.age += 1
    
    def age_grow_plant(self) -> None:
        self.grow_plant()
        self.age_plant()

def main() -> None:
    i = 1
    print("=== Plant Factory Output ===")
    plant = {}
    plant["rose"] = Plant("rose", 25.0, 30)
    plant["oak"] = Plant("oak", 200.0, 365)
    plant["cactus"] = Plant("cactus", 5.0, 90)
    plant["sunflower"] = Plant("sunflower", 80.0, 40)
    plant["fern"] = Plant("fern", 15.0, 120)

    for p in plant.values():
        p.show()

if __name__ == "__main__":
    main()
