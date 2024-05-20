from utils.primordials import *
from game.state import *
from game.database import *
from typing import Callable

def _shop_get(gameState: GameState, shopId: int) -> ShopSchemaType:
    shopDatabase = gamestate_get_shop_database(gameState)
    return database_get_entry_at(shopDatabase, shopId)

def _shop_set(gameState: GameState, shopId: int, modifier: Callable[[ShopSchemaType], ShopSchemaType]) -> ShopSchemaType:
    shopDatabase = gamestate_get_shop_database(gameState)
    shop = modifier(database_get_entry_at(shopDatabase, shopId))
    database_set_entry_at(shopDatabase, shopId, shop)
    return shop

def _shop_new(gameState: GameState) -> ShopSchemaType:
    shopDatabase = gamestate_get_shop_database(gameState)
    shopId = database_get_entries_length(shopDatabase)
    shop = ShopSchemaType(
        id=shopId,
        referenceType=None,
        referenceId=None,
        cost=None
    )
    database_set_entry_at(shopDatabase, shopId, shop)
    return shop

def _shop_get_all_items(gameState: GameState) -> list[ShopSchemaType]:
    shopDatabase = gamestate_get_shop_database(gameState)
    shopEntries = database_get_entries(shopDatabase)
    return shopEntries
