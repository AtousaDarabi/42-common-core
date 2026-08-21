def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda a: a["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    powers = list(map(lambda m: m["power"], mages))
    max_p = max(powers)
    min_p = min(powers)
    avg_p = round(sum(powers) / len(powers), 2)

    return {"max_power": max_p, "min_power": min_p, "avg_power": avg_p}


def main() -> None:
    print("Testing artifact sorter...")
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "divination"},
        {"name": "Fire Staff", "power": 92, "type": "evocation"},
        {"name": "Wooden Wand", "power": 25, "type": "focus"},
    ]
    sorted_artifacts = artifact_sorter(artifacts)
    first, second = sorted_artifacts[0], sorted_artifacts[1]
    print(
        f"{first['name']} ({first['power']} power) comes before "
        f"{second['name']} ({second['power']} power)"
    )

    print("\nTesting power filter...")
    mages = [
        {"name": "Gandalf", "power": 95, "element": "light"},
        {"name": "Apprentice", "power": 40, "element": "fire"},
        {"name": "Saruman", "power": 90, "element": "many-colors"},
    ]
    filtered_mages = power_filter(mages, 50)
    print(
        f"Filtered Mages (>= 50 power): {[m['name'] for m in filtered_mages]}"
        )

    print("\nTesting spell transformer...")
    spells = ["fireball", "heal", "shield"]
    transformed = spell_transformer(spells)
    print(" ".join(transformed))

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Mage Stats: {stats}")


if __name__ == "__main__":
    main()
