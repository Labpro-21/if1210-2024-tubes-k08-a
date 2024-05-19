from utils.primordials import *
from game.state import *
from game.database import *
from typing import Callable, Literal

def _potion_get(gameState: GameState, potionId: int) -> PotionSchemaType:
    potionDatabase = gamestate_get_potion_database(gameState)
    return database_get_entry_at(potionDatabase, potionId)

def _potion_set(gameState: GameState, potionId: int, modifier: Callable[[PotionSchemaType], PotionSchemaType]) -> PotionSchemaType:
    potionDatabase = gamestate_get_potion_database(gameState)
    potion = modifier(database_get_entry_at(potionDatabase, potionId))
    database_set_entry_at(potionDatabase, potionId, potion)
    return potion

def _potion_new(gameState: GameState) -> PotionSchemaType:
    potionDatabase = gamestate_get_potion_database(gameState)
    potionId = database_get_entries_length(potionDatabase)
    potion = PotionSchemaType(
        id=potionId,
        name=None,
        description=None,
        type=None,
        baseAmount=None,
        multiplierAmount=None,
        duration=None,
        curve=None,
        nextId=None
    )
    database_set_entry_at(potionDatabase, potionId, potion)
    return potion

def _potion_get_type_generic(type: str) -> Literal["healing", "strength", "resilience"]:
    if type == "HealingDefinite" or type == "HealingIndefinite":
        return "healing"
    if type == "StrengthDefinite" or type == "StrengthIndefinite":
        return "strength"
    if type == "ResilienceDefinite" or type == "ResilienceIndefinite":
        return "resilience"
    return None

def _potion_is_type_definite(type: str) -> bool:
    return string_ends_with(type, "Definite")

def _potion_is_type_indefinite(type: str) -> bool:
    return string_ends_with(type, "Indefinite")

def _potion_get_calculated_definite_base_amount(potion: PotionSchemaType, remainingTime: float) -> float:
    curveValue = __curve_value(potion.curve, potion.duration, remainingTime)
    return potion.baseAmount * curveValue

def _potion_get_calculated_definite_multiplier_amount(potion: PotionSchemaType, remainingTime: float) -> float:
    curveValue = __curve_value(potion.curve, potion.duration, remainingTime)
    return potion.multiplierAmount * curveValue

def _potion_get_calculated_indefinite_amount(potion: PotionSchemaType, remainingTime: float, deltaTime: float) -> float:
    curveValue = __curve_value(potion.curve, potion.duration, remainingTime + deltaTime)
    return (potion.baseAmount / __get_curve_area(potion.curve)) * (deltaTime / potion.duration) * curveValue

def __curve_value(curve: int, duration: float, remainingTime: float) -> float:
    if curve == 0:
        return 1
    x = max(0, min(1, (duration - remainingTime) / duration))
    if curve == 1:
        return 1 - x ** 5

def __get_curve_area(curve: int) -> float:
    if curve == 0:
        return 1
    if curve == 1:
        return 0.8333 # integral from 0 to 1 of (1 - x ** 5)
