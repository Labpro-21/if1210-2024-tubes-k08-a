from utils.primordials import *
from game.state import *
from game.database import *
from typing import Callable, Literal

def _monster_get(gameState: GameState, monsterId: int) -> MonsterSchemaType:
    monsterDatabase = gamestate_get_monster_database(gameState)
    return database_get_entry_at(monsterDatabase, monsterId)

def _monster_set(gameState: GameState, monsterId: int, modifier: Callable[[MonsterSchemaType], MonsterSchemaType]) -> MonsterSchemaType:
    monsterDatabase = gamestate_get_monster_database(gameState)
    monster = modifier(database_get_entry_at(monsterDatabase, monsterId))
    database_set_entry_at(monsterDatabase, monsterId, monster)
    return monster

def _monster_new(gameState: GameState) -> MonsterSchemaType:
    monsterDatabase = gamestate_get_monster_database(gameState)
    monsterId = database_get_entries_length(monsterDatabase)
    monster = MonsterSchemaType(
        id=monsterId,
        name=None,
		description=None,
		family=None,
		level=None,
		healthPoints=None,
		attackPower=None,
		defensePower=None,
		spriteDefault=None,
		spriteFront=None,
		spriteBack=None,
    )
    database_set_entry_at(monsterDatabase, monsterId, monster)
    return monster

def _monster_get_all_monsters(gameState: GameState) -> list[MonsterSchemaType]:
    monsterDatabase = gamestate_get_monster_database(gameState)
    monsterEntries = database_get_entries(monsterDatabase)
    return monsterEntries
