#! /usr/bin/env python3

class Plant:

    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name

        if height >= 0:
            self._height = float(height)
        else:
            print(f"{self._name}: Height can't be negative")
            self._height = 0.0

        if age >= 0:
            self._age = age
        else:
            print(f"{self._name}: Age can't be negative")
            self._age = 0
        
        print(f"Plant created: {self._name}: {self._height}cm, {self._age} days old")


    # getter
    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age
    # getter
    
    # setter
    def set_height(self, value: float):
        if value >= 0:
            print(f"{self._name}: Height updated: {value}cm")
            self._height = value
        else:
            print(f"{self._name}: Error, height can't be negative")
            print(f"Height update rejected")
    
    def set_age(self, value: int):
        if value >= 0:
            print(f"Age updated: {value} days")
            self._age = value
        else:
            print(f"{self._name}: Error, age can't be negative")
            print(f"Age update rejected")
    # setter

    def print_status(self):
        print(f"Current state: {self._name}: {self._height:.1f}cm, {self._age} days old")

def main() -> None:
    i = 1
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10)
    rose.set_height(25)
    rose.set_age(30)
    rose.set_height(-5)
    rose.set_age(-10)
    rose.display_status()

if __name__ == "__main__":
    main()
