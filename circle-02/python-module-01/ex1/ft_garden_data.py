#!/usr/bin/env python3

class Plant:

    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        print(f"{self.name.capitalize()}: {self.height}cm, {self.age} "
              "days old")


def main() -> None:
    print("=== Garden Plant Registry ===")

    rose = Plant("rose", 25, 30)
    sunflower = Plant("sunflower", 80, 45)
    cactus = Plant("cactus", 15, 120)

    rose.show()
    sunflower.show()
    cactus.show()


if __name__ == "__main__":
    main()
