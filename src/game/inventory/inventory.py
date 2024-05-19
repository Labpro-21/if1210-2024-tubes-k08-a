from utils.primordials import *
from game.state import *
from game.database import *
from game.potion import *
from typing import Callable, Optional, Union

def _inventory_monster_get(gameState: GameState, inventoryMonsterId: int) -> InventoryMonsterSchemaType:
    inventoryMonsterDatabase = gamestate_get_inventory_monster_database(gameState)
    return database_get_entry_at(inventoryMonsterDatabase, inventoryMonsterId)

def _inventory_monster_set(gameState: GameState, inventoryMonsterId: int, modifier: Union[InventoryMonsterSchemaType, Callable[[InventoryMonsterSchemaType], InventoryMonsterSchemaType]]) -> InventoryMonsterSchemaType:
    inventoryMonsterDatabase = gamestate_get_inventory_monster_database(gameState)
    inventoryMonster = modifier(database_get_entry_at(inventoryMonsterDatabase, inventoryMonsterId)) if callable(modifier) else modifier
    database_set_entry_at(inventoryMonsterDatabase, inventoryMonsterId, inventoryMonster)
    return inventoryMonster

def _inventory_monster_new(gameState: GameState) -> InventoryMonsterSchemaType:
    inventoryMonsterDatabase = gamestate_get_inventory_monster_database(gameState)
    inventoryMonsterId = database_get_entries_length(inventoryMonsterDatabase)
    inventoryMonster = InventoryMonsterSchemaType(
        id=inventoryMonsterId,
        ownerId=None,
        referenceId=None,
        name=None,
        experiencePoints=None,
        healthPoints=None,
        attackPower=None,
        defensePower=None,
        activePotions=None,
    )
    database_set_entry_at(inventoryMonsterDatabase, inventoryMonsterId, inventoryMonster)
    return inventoryMonster

def _inventory_monster_get_user_monsters(gameState: GameState, userId: int) -> list[InventoryMonsterSchemaType]:
    inventoryMonsterDatabase = gamestate_get_inventory_monster_database(gameState)
    inventoryMonsterEntries = database_get_entries(inventoryMonsterDatabase)
    return array_filter(inventoryMonsterEntries, lambda m, *_: m.ownerId == userId)

def _inventory_monster_get_calculated_health_points(gameState: GameState, inventoryMonster: InventoryMonsterSchemaType) -> float:
    activePotions = array_map(inventoryMonster.activePotions, lambda p, *_: (p[0], p[1], potion_get(gameState, p[2])))
    activePotions = array_filter(activePotions, lambda p, *_: potion_is_type_definite(p[2].type) and potion_get_type_generic(p[2].type) == "healing")
    baseAmounts = array_reduce(activePotions, lambda c, p, *_: c + potion_get_calculated_definite_base_amount(p[2], [1]), 0)
    multiplierAmounts = array_reduce(activePotions, lambda c, p, *_: c * potion_get_calculated_definite_multiplier_amount(p[2], p[1]), inventoryMonster.healthPoints)
    return baseAmounts + multiplierAmounts

def _inventory_monster_get_calculated_attack_power(gameState: GameState, inventoryMonster: InventoryMonsterSchemaType) -> float:
    activePotions = array_map(inventoryMonster.activePotions, lambda p, *_: (p[0], p[1], potion_get(gameState, p[2])))
    activePotions = array_filter(activePotions, lambda p, *_: potion_is_type_definite(p[2].type) and potion_get_type_generic(p[2].type) == "strength")
    baseAmounts = array_reduce(activePotions, lambda c, p, *_: c + potion_get_calculated_definite_base_amount(p[2], [1]), 0)
    multiplierAmounts = array_reduce(activePotions, lambda c, p, *_: c * potion_get_calculated_definite_multiplier_amount(p[2], p[1]), inventoryMonster.attackPower)
    return baseAmounts + multiplierAmounts

def _inventory_monster_get_calculated_defense_power(gameState: GameState, inventoryMonster: InventoryMonsterSchemaType) -> float:
    activePotions = array_map(inventoryMonster.activePotions, lambda p, *_: (p[0], p[1], potion_get(gameState, p[2])))
    activePotions = array_filter(activePotions, lambda p, *_: potion_is_type_definite(p[2].type) and potion_get_type_generic(p[2].type) == "resilience")
    baseAmounts = array_reduce(activePotions, lambda c, p, *_: c + potion_get_calculated_definite_base_amount(p[2], [1]), 0)
    multiplierAmounts = array_reduce(activePotions, lambda c, p, *_: c * potion_get_calculated_definite_multiplier_amount(p[2], p[1]), inventoryMonster.defensePower)
    return baseAmounts + multiplierAmounts

def _inventory_monster_use_potion(gameState: GameState, inventoryMonster: InventoryMonsterSchemaType, potion: PotionSchemaType) -> InventoryMonsterSchemaType:
    gameTime = gamestate_time(gameState)
    newHealthPoints = inventoryMonster.healthPoints
    newAttackPower = inventoryMonster.attackPower
    newDefensePower = inventoryMonster.defensePower
    newActivePotions = array_slice(inventoryMonster.activePotions)
    while potion is not None:
        additionalHealthPoints, additionalAttackPower, additionalDefensePower, newActivePotion = __tick_potion(gameTime, (gameTime - 1, potion.duration, potion))
        newHealthPoints += additionalHealthPoints
        newAttackPower += additionalAttackPower
        newDefensePower += additionalDefensePower
        if newActivePotion is not None:
            array_push(newActivePotions, (newActivePotion[0], newActivePotion[1], newActivePotion[2].id))
        potion = potion_get(gameState, potion.nextId)
    return _inventory_monster_set(gameState, inventoryMonster.id, namedtuple_with(inventoryMonster, healthPoints=newHealthPoints, attackPower=newAttackPower, defensePower=newDefensePower, activePotions=newActivePotions))

def _inventory_monster_tick(gameState: GameState, inventoryMonster: InventoryMonsterSchemaType) -> InventoryMonsterSchemaType:
    def tickPotions(inventoryMonster: InventoryMonsterSchemaType) -> InventoryMonsterSchemaType:
        gameTime = gamestate_time(gameState)
        activePotions = array_map(inventoryMonster.activePotions, lambda p, *_: (p[0], p[1], potion_get(gameState, p[2])))
        newHealthPoints = inventoryMonster.healthPoints
        newAttackPower = inventoryMonster.attackPower
        newDefensePower = inventoryMonster.defensePower
        newActivePotions: list[tuple[float, float, int]] = []
        for activePotion in activePotions:
            additionalHealthPoints, additionalAttackPower, additionalDefensePower, newActivePotion = __tick_potion(gameTime, activePotion)
            newHealthPoints += additionalHealthPoints
            newAttackPower += additionalAttackPower
            newDefensePower += additionalDefensePower
            if newActivePotion is not None:
                array_push(newActivePotions, (newActivePotion[0], newActivePotion[1], newActivePotion[2].id))
        return namedtuple_with(inventoryMonster, healthPoints=newHealthPoints, attackPower=newAttackPower, defensePower=newDefensePower, activePotions=newActivePotions)
    return _inventory_monster_set(gameState, inventoryMonster.id, tickPotions(inventoryMonster))

def __tick_potion(gameTime: float, activePotion: tuple[float, float, PotionSchemaType]) -> tuple[float, float, float, Optional[tuple[float, float, PotionSchemaType]]]:
    deltaTime = gameTime - activePotion[0]
    remainingTime = activePotion[1] - deltaTime
    potion = activePotion[2]
    additionalHealthPoints = 0
    additionalAttackPower = 0
    additionalDefensePower = 0
    if potion_is_type_indefinite(potion.type):
        potionType = potion_get_type_generic(potion.type)
        if potionType == "healing":
            additionalHealthPoints += potion_get_calculated_indefinite_amount(potion, remainingTime, deltaTime)
        if potionType == "strength":
            additionalAttackPower += potion_get_calculated_indefinite_amount(potion, remainingTime, deltaTime)
        if potionType == "resilience":
            additionalDefensePower += potion_get_calculated_indefinite_amount(potion, remainingTime, deltaTime)
    if remainingTime <= 0:
        return (additionalHealthPoints, additionalAttackPower, additionalDefensePower, None)
    newActivePotion = tuple_with(activePotion, _0=gameTime, _1=remainingTime)
    return (additionalHealthPoints, additionalAttackPower, additionalDefensePower, newActivePotion)

# immediate permanent buffs: set type="HealthIndefinite", duration=1
