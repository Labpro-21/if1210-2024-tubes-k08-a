from game.database import *
from typing import TypedDict, NamedTuple, Literal, Union, Optional

_UserSchemaType = NamedTuple("User", [
    ("id", int),
    ("username", str),
    ("password", str),
    ("role", Union[Literal["admin"], Literal["agent"]]),
    ("money", float),
])
_UserSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("username", str, lambda x: x, lambda x: x),
    database_property_new("password", str, lambda x: x, lambda x: x),
    database_property_new("role", str, lambda x: x, lambda x: x),
    database_property_new("money", int, lambda x: float(x), lambda x: str(x)),
]
_UserSchema = database_schema_new("csv", _UserSchemaType, _UserSchemaProperties)
_UserDatabase = Database[_UserSchemaType]

_MonsterSchemaType = NamedTuple("Monster", [
    ("id", int),
    ("type", str),
    ("level", int),
    ("name", str), # Each level, an OWCA might have different name. Except when the user overrides it in inventoryMonsterDatabase.
    ("healthPoints", float), # All these fields are the base properties. These might get overriden in inventoryMonsterDatabase.
    ("attackPower", float),
    ("defensePower", float),
])
_MonsterSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("type", str, lambda x: x, lambda x: x),
    database_property_new("level", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("name", str, lambda x: x, lambda x: x),
    database_property_new("healthPoints", int, lambda x: float(x), lambda x: str(x)),
    database_property_new("attackPower", int, lambda x: float(x), lambda x: str(x)),
    database_property_new("defensePower", int, lambda x: float(x), lambda x: str(x)),
]
_MonsterSchema = database_schema_new("csv", _MonsterSchemaType, _MonsterSchemaProperties)
_MonsterDatabase = Database[_MonsterSchemaType]

_PotionSchemaType = NamedTuple("Potion", [
    ("id", int),
    ("name", str),
    ("strengthAmount", float),
    ("resilienceAmount", float),
    ("healingAmount", float),
])
_PotionSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("name", str, lambda x: x, lambda x: x),
    database_property_new("strengthAmount", int, lambda x: float(x), lambda x: str(x)),
    database_property_new("resilienceAmount", int, lambda x: float(x), lambda x: str(x)),
    database_property_new("healingAmount", int, lambda x: float(x), lambda x: str(x)),
]
_PotionSchema = database_schema_new("csv", _PotionSchemaType, _PotionSchemaProperties)
_PotionDatabase = Database[_PotionSchemaType]

_BattleSchemaType = NamedTuple("Battle", [
    ("id", int),
    ("player1Id", int), # Reference to userDatabase
    ("player2Id", int), # Reference to userDatabase
    ("verdict", Union[Literal[-1], Literal[0], Literal[1], Literal[2] ]), # -1 means the battle is not finished yet, 0 means draw, 1 means player 1 wins, 2 means player 2 wins.
])
_BattleSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("player1Id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("player2Id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("verdict", int, lambda x: int(x), lambda x: str(x)),
]
_BattleSchema = database_schema_new("csv", _BattleSchemaType, _BattleSchemaProperties)
_BattleDatabase = Database[_BattleSchemaType]

_ArenaSchemaType = NamedTuple("Arena", [
    ("id", int),
    ("playerId", int), # Reference to userDatabase
    ("seed", int), # Arena is randomised, this is a way to make sure the random is stable accross runtime.
    ("stage", Union[Literal[1], Literal[2], Literal[3], Literal[4], Literal[5]]), # Stage is between 1 to 5
    ("verdict", Union[Literal[-1], Literal[0], Literal[1]]), # -1 means the training is not yet over, 0 means the player wins, 1 means the player lose
])
_ArenaSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("playerId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("seed", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("stage", int, lambda x: int(x), lambda x: str(x)),
]
_ArenaSchema = database_schema_new("csv", _ArenaSchemaType, _ArenaSchemaProperties)
_ArenaDatabase = Database[_ArenaSchemaType]

_ShopSchemaType = NamedTuple("Shop", [
    ("id", int),
    ("referenceType", Union[Literal["monster"], Literal["item"]]), # A way for `referenceId` to know which database to look for.
    ("referenceId", int), # if `referenceType` is "monster" then look for `id` in monsterDatabase, otherwise look for `id` in potionDatabase
    ("cost", float),
])
_ShopSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("referenceType", str, lambda x: x, lambda x: x),
    database_property_new("referenceId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("cost", int, lambda x: float(x), lambda x: str(x)),
]
_ShopSchema = database_schema_new("csv", _ShopSchemaType, _ShopSchemaProperties)
_ShopDatabase = Database[_ShopSchemaType]

_LaboratorySchemaType = NamedTuple("Laboratory", [
    ("id", int),
    ("fromMonsterId", int), # Reference to monsterDatabase
    ("toMonsterId", int), # Reference to monsterDatabase, note that both `fromMonsterId` and `toMonsterId` reference must have the same monster type.
    ("cost", float),
])
_LaboratorySchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("fromMonsterId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("toMonsterId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("cost", int, lambda x: float(x), lambda x: str(x)),
]
_LaboratorySchema = database_schema_new("csv", _LaboratorySchemaType, _LaboratorySchemaProperties)
_LaboratoryDatabase = Database[_LaboratorySchemaType]

_InventoryItemSchemaType = NamedTuple("InventoryItem", [
    ("id", int),
    ("ownerId", int), # Reference to userDatabase
    ("referenceId", int), # Reference to potionDatabase
    ("quantity", int),
])
_InventoryItemSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("ownerId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("referenceId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("quantity", int, lambda x: int(x), lambda x: str(x)),
]
_InventoryItemSchema = database_schema_new("csv", _InventoryItemSchemaType, _InventoryItemSchemaProperties)
_InventoryItemDatabase = Database[_InventoryItemSchemaType]

_InventoryMonsterSchemaType = NamedTuple("InventoryMonster", [
    ("id", int),
    ("ownerId", int), # Reference to userDatabase
    ("referenceId", int), # Reference to monsterDatabase. Note: this schema does not have property "level", because the information is already available in referenced monster.
    ("name", str), # This field might be null, if it is null then display the name from referenced monster default name. This is a way for user to customise the name.
    ("healthPoints", float), # These fields are modifiers, usually it should be copied from the fields in referenced monster.
    ("attackPower", float),
    ("defensePower", float),
])
_InventoryMonsterSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("ownerId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("referenceId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("name", str, lambda x: x, lambda x: x),
    database_property_new("healthPoints", int, lambda x: float(x), lambda x: str(x)),
    database_property_new("attackPower", int, lambda x: float(x), lambda x: str(x)),
    database_property_new("defensePower", int, lambda x: float(x), lambda x: str(x)),
]
_InventoryMonsterSchema = database_schema_new("csv", _InventoryMonsterSchemaType, _InventoryMonsterSchemaProperties)
_InventoryMonsterDatabase = Database[_InventoryMonsterSchemaType]

_GameState = TypedDict("GameState",
    userDatabase=_UserDatabase, # readonly
    monsterDatabase=_MonsterDatabase, # readonly
    potionDatabase=_PotionDatabase, # readonly
    battleDatabase=_BattleDatabase, # readonly
    arenaDatabase=_ArenaDatabase, # readonly
    shopDatabase=_ShopDatabase, # readonly
    laboratoryDatabase=_LaboratoryDatabase, # readonly
    inventoryItemDatabase=_InventoryItemDatabase, # readonly
    inventoryMonsterDatabase=_InventoryMonsterDatabase, # readonly
    userId=Optional[int] # If the user is logged in, the value must refer to userDatabase, otherwise it must be None
)

def _gamestate_new():
    userDatabase=database_new("", _UserSchema)
    monsterDatabase=database_new("", _MonsterSchema)
    potionDatabase=database_new("", _PotionSchema)
    battleDatabase=database_new("", _BattleSchema)
    arenaDatabase=database_new("", _ArenaSchema)
    shopDatabase=database_new("", _ShopSchema)
    laboratoryDatabase=database_new("", _LaboratorySchema)
    inventoryItemDatabase=database_new("", _InventoryItemSchema)
    inventoryMonsterDatabase=database_new("", _InventoryMonsterSchema)
    return dict(
        userDatabase=userDatabase,
        monsterDatabase=monsterDatabase,
        potionDatabase=potionDatabase,
        battleDatabase=battleDatabase,
        arenaDatabase=arenaDatabase,
        shopDatabase=shopDatabase,
        laboratoryDatabase=laboratoryDatabase,
        inventoryItemDatabase=inventoryItemDatabase,
        inventoryMonsterDatabase=inventoryMonsterDatabase,
    )

def _gamestate_get_user_database(gameState: _GameState) -> _UserDatabase:
    return gameState["userDatabase"]

def _gamestate_get_monster_database(gameState: _GameState) -> _MonsterDatabase:
    return gameState["monsterDatabase"]

def _gamestate_get_potion_database(gameState: _GameState) -> _PotionDatabase:
    return gameState["potionDatabase"]

def _gamestate_get_battle_database(gameState: _GameState) -> _BattleDatabase:
    return gameState["battleDatabase"]

def _gamestate_get_arena_database(gameState: _GameState) -> _ArenaDatabase:
    return gameState["arenaDatabase"]
    
def _gamestate_get_shop_database(gameState: _GameState) -> _ShopDatabase:
    return gameState["shopDatabase"]
    
def _gamestate_get_laboratory_database(gameState: _GameState) -> _LaboratoryDatabase:
    return gameState["laboratoryDatabase"]
    
def _gamestate_get_inventory_item_database(gameState: _GameState) -> _InventoryItemDatabase:
    return gameState["inventoryItemDatabase"]

def _gamestate_get_inventory_monster_database(gameState: _GameState) -> _InventoryMonsterDatabase:
    return gameState["inventoryMonsterDatabase"]

def _gamestate_get_user_id(gameState: _GameState) -> Optional[int]:
    return gameState["userId"]

def _gamestate_set_user_id(gameState: _GameState, userId: Optional[int]) -> None:
    gameState["userId"] = userId
