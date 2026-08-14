import math
from typing import Tuple


def get_player_pos() -> Tuple[float, float, float]:
    while True:
        try:
            user_input = input("Enter new coordinates as floats in format "
                               "'x,y,z': ")
            parts = user_input.split(",")

            if len(parts) != 3:
                print("Invalid syntax")
                continue

            coords = []
            for part in parts:
                cleaned_part = part.strip()
                try:
                    coords.append(float(cleaned_part))
                except ValueError:
                    print(
                        f"Error on parameter '{cleaned_part}': could not "
                        f"convert string to float: '{cleaned_part}'"
                    )
                    raise ValueError

            return (coords[0], coords[1], coords[2])

        except ValueError:
            pass


def main() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1 = get_player_pos()

    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_to_center = math.sqrt(pos1[0] ** 2 + pos1[1] ** 2 + pos1[2] ** 2)
    print(f"Distance to center: {round(dist_to_center, 4)}")

    print("\nGet a second set of coordinates")
    pos2 = get_player_pos()

    dist_between = math.sqrt(
        (pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2
        + (pos2[2] - pos1[2]) ** 2
    )
    print("Distance between the 2 sets of coordinates: "
          f"{round(dist_between, 4)}")


if __name__ == "__main__":
    main()
