from typing import List, Tuple
from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)


def run_tournament(opponents: List[Tuple[CreatureFactory,
                                         BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    participants = [(fac.create_base(), strat) for fac, strat in opponents]

    for i in range(len(participants)):
        for j in range(i + 1, len(participants)):
            c1, strat1 = participants[i]
            c2, strat2 = participants[j]

            print()
            print("* Battle *")
            print(c1.describe())
            print("vs.")
            print(c2.describe())
            print("now fight!")

            try:
                strat1.act(c1)
                strat2.act(c2)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal_strat = NormalStrategy()
    aggressive_strat = AggressiveStrategy()
    defensive_strat = DefensiveStrategy()

    print("Tournament 0 (basic)")
    run_tournament([(flame_factory, normal_strat),
                    (healing_factory, defensive_strat)])
    print()

    print("Tournament 1 (error)")
    run_tournament(
        [(flame_factory, aggressive_strat), (healing_factory, defensive_strat)]
    )
    print()

    print("Tournament 2 (multiple)")
    run_tournament(
        [
            (aqua_factory, normal_strat),
            (healing_factory, defensive_strat),
            (transform_factory, aggressive_strat),
        ]
    )


if __name__ == "__main__":
    main()
