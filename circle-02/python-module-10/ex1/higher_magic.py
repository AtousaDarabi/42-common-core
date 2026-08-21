from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))

    return combined_spell


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified_spell


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def conditional_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional_spell


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence_spell(target: str, power: int) -> list[str]:
        return [s(target, power) for s in spells]

    return sequence_spell


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def main() -> None:
    target = "Dragon"

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    res1, res2 = combined(target, 10)
    print(f"Combined spell result: {res1}, {res2}")

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    orig_res = fireball(target, 10)
    amp_res = mega_fireball(target, 10)
    print(f"Original: {orig_res}")
    print(f"Amplified: {amp_res}")

    print("\nTesting conditional caster...")
    high_power_only = conditional_caster(
        lambda t, p: p >= 50, fireball
    )
    print(f"Power 20: {high_power_only(target, 20)}")
    print(f"Power 80: {high_power_only(target, 80)}")

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal])
    results = combo(target, 25)
    print(f"Sequence results: {results}")


if __name__ == "__main__":
    main()
