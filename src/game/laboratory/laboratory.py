from utils.primordials import *
from game.state import *
from game.database import *
from typing import Callable, Union

def _laboratory_get(gameState: GameState, laboratoryId: int) -> LaboratorySchemaType:
    laboratoryDatabase = gamestate_get_laboratory_database(gameState)
    return database_get_entry_at(laboratoryDatabase, laboratoryId)

def _laboratory_set(gameState: GameState, laboratoryId: int, modifier: Union[LaboratorySchemaType, Callable[[LaboratorySchemaType], LaboratorySchemaType]]) -> LaboratorySchemaType:
    laboratoryDatabase = gamestate_get_laboratory_database(gameState)
    laboratory = modifier(database_get_entry_at(laboratoryDatabase, laboratoryId)) if callable(modifier) else modifier
    database_set_entry_at(laboratoryDatabase, laboratoryId, laboratory)
    return laboratory

def _laboratory_new(gameState: GameState) -> LaboratorySchemaType:
    laboratoryDatabase = gamestate_get_laboratory_database(gameState)
    laboratoryId = database_get_entries_length(laboratoryDatabase)
    laboratory = LaboratorySchemaType(
        id=laboratoryId,
        fromMonsterId=None,
        toMonsterId=None,
        cost=None,
    )
    database_set_entry_at(laboratoryDatabase, laboratoryId, laboratory)
    return laboratory

def _laboratory_get_all_upgrades(gameState: GameState) -> list[LaboratorySchemaType]:
    laboratoryDatabase = gamestate_get_laboratory_database(gameState)
    laboratoryEntries = database_get_entries(laboratoryDatabase)
    return laboratoryEntries
