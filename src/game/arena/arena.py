from utils.primordials import *
from game.state import *
from game.database import *
from typing import Optional, Callable, Literal, Union

def _arena_get(gameState: GameState, arenaId: int) -> ArenaSchemaType:
    arenaDatabase = gamestate_get_arena_database(gameState)
    return database_get_entry_at(arenaDatabase, arenaId)

def _arena_set(gameState: GameState, arenaId: int, modifier: Union[ArenaSchemaType, Callable[[ArenaSchemaType], ArenaSchemaType]]) -> ArenaSchemaType:
    arenaDatabase = gamestate_get_arena_database(gameState)
    arena = modifier(database_get_entry_at(arenaDatabase, arenaId)) if callable(modifier) else modifier
    database_set_entry_at(arenaDatabase, arenaId, arena)
    return arena

def _arena_new(gameState: GameState) -> ArenaSchemaType:
    arenaDatabase = gamestate_get_arena_database(gameState)
    arenaId = database_get_entries_length(arenaDatabase)
    arena = ArenaSchemaType(
        id=arenaId,
        playerId=None,
        battleIds=None,
        handler=None,
    )
    database_set_entry_at(arenaDatabase, arenaId, arena)
    return arena


