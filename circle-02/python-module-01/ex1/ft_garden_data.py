#!/usr/bin/env python3

class Plant:

    def __init__(self, name, height, age) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self):
        print(f"{self.name.capitalize()}: {self.height}, {self.age} days old")

def main() -> None:
    print("=== Garden Plant Registry ===")

    rose = Plant("rose", "25cm", 30)
    sunflower = Plant("sunflower", "80cm", 45)
    cactus = Plant("cactus", "15cm", 120)

    rose.show()
    sunflower.show()
    cactus.show()

if __name__ == "__main__":
    main()
