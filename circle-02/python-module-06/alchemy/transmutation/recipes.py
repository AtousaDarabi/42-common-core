import elements

from alchemy.potions import strength_potion

from ..elements import create_air


def lead_to_gold() -> str:
    air = create_air()
    potion = strength_potion()
    fire = elements.create_fire()
    return (
        f"Recipe transmuting Lead to Gold: brew '{air}' and "
        f"'{potion}' mixed with '{fire}'"
    )
