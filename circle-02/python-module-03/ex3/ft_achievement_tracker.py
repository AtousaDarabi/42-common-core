import random
from typing import List, Set

ALL_ACHIEVEMENTS = [
    "Crafting Genius",
    "World Savior",
    "Master Explorer",
    "Collector Supreme",
    "Untouchable",
    "Boss Slayer",
    "Strategist",
    "Unstoppable",
    "Speed Runner",
    "Survivor",
    "Treasure Hunter",
    "First Steps",
    "Sharp Mind",
    "Hidden Path Finder",
]

PLAYER_NAMES = ["Alice", "Bob", "Charlie", "Dylan"]


def gen_player_achievements() -> Set[str]:
    num_achievements = random.randint(6, 10)
    player_set = set(random.sample(ALL_ACHIEVEMENTS, num_achievements))
    return player_set


def main() -> None:
    print("=== Achievement Tracker System ===\n")

    player_sets: List[Set[str]] = [
        gen_player_achievements() for _ in PLAYER_NAMES
    ]

    for index in range(len(PLAYER_NAMES)):
        print(f"Player {PLAYER_NAMES[index]}: {player_sets[index]}")

    all_unlocked: Set[str] = set()
    for achievements in player_sets:
        all_unlocked = all_unlocked.union(achievements)

    print(f"\nAll distinct achievements: {all_unlocked}\n")

    common_achievements = player_sets[0]
    for p_set in player_sets[1:]:
        common_achievements = common_achievements.intersection(p_set)

    print(f"Common achievements: {common_achievements}\n")

    for index in range(len(PLAYER_NAMES)):
        others_combined: Set[str] = set()
        for other_index in range(len(PLAYER_NAMES)):
            if other_index != index:
                others_combined = others_combined.union(
                    player_sets[other_index]
                )

        only_this_player = player_sets[index].difference(others_combined)
        print(f"Only {PLAYER_NAMES[index]} has: {only_this_player}")

    print("\n")
    full_game_set = set(ALL_ACHIEVEMENTS)
    for index in range(len(PLAYER_NAMES)):
        missing_achievements = full_game_set.difference(player_sets[index])
        print(f"{PLAYER_NAMES[index]} is missing: {missing_achievements}")


if __name__ == "__main__":
    main()

# empty_set = set()
# print(empty_set)  # Output: set()
# d = {}
# print(type(d))  # <class 'dict'>
