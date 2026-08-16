import elements as base_elements

from .elements import create_air, create_earth


def strength_potion() -> str:
    fire = base_elements.create_fire()
    water = base_elements.create_water()
    return f"Strength potion brewed with '{fire}' and '{water}'"


def healing_potion() -> str:
    earth = create_earth()
    air = create_air()
    return f"Healing potion brewed with '{earth}' and '{air}'"
