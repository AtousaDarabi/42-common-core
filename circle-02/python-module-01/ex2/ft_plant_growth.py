#! /usr/bin/env python3

class Plant:

    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        days = "day" if self.age == 1 else "days"
        print(f"{self.name.capitalize()}: {round(self.height, 1)}cm, {self.age} {days} old")
    
    def grow_plant(self) -> None:
        growth = 0.8
        self.height += growth
    
    def age_plant(self) -> None:
        self.age += 1
    
    def age_grow_plant(self) -> None:
        self.grow_plant()
        self.age_plant()

def main() -> None:
    name = "rose"
    height = 25.0
    age = 30
    rose = Plant(name, height, age)

    print("=== Garden Plant Growth ===")
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.show()
        rose.age_grow_plant()
    print(f"Growth this week: {round(rose.height - height)}cm")

if __name__ == "__main__":
    main()
