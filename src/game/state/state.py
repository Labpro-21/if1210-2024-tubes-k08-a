from utils.primordials import *
from utils.math import *
from game.database import *
from .visual import _Visual, _visual_new
from typing import TypedDict, NamedTuple, Literal, Optional
from os import path

_UserSchemaType = NamedTuple("User", [
    ("id", int),
    ("username", str),
    ("password", str),
    ("role", Literal["admin", "agent", "system", "npc"]), # Battle in arena or wild area has a monster whose user has the role system (basically bot account).
    ("money", float),
])
_UserSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("username", str, lambda x: x, lambda x: x),
    database_property_new("password", str, lambda x: x, lambda x: x),
    database_property_new("role", str, lambda x: x, lambda x: x),
    database_property_new("money", float, lambda x: float(x), lambda x: str(x)),
]
_UserSchema = database_schema_new("csv", _UserSchemaType, _UserSchemaProperties)
_UserDatabase = Database[_UserSchemaType]

_MonsterSchemaType = NamedTuple("Monster", [
    ("id", int),
    ("name", str), # Each level, an OWCA might have different name. Except when the user overrides it in inventoryMonsterDatabase.
    ("description", str),
    ("family", str),
    ("level", int),
    ("healthPoints", float), # All these fields are the base properties. These might get overriden in inventoryMonsterDatabase.
    ("attackPower", float),
    ("defensePower", float),
    ("spriteDefault", str),
    ("spriteFront", str),
    ("spriteBack", str),
])
_MonsterSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("name", str, lambda x: x, lambda x: x),
    database_property_new("description", str, lambda x: x, lambda x: x),
    database_property_new("family", str, lambda x: x, lambda x: x),
    database_property_new("level", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("healthPoints", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("attackPower", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("defensePower", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("spriteDefault", str, lambda x: x, lambda x: x),
    database_property_new("spriteFront", str, lambda x: x, lambda x: x),
    database_property_new("spriteBack", str, lambda x: x, lambda x: x),
]
_MonsterSchema = database_schema_new("csv", _MonsterSchemaType, _MonsterSchemaProperties)
_MonsterDatabase = Database[_MonsterSchemaType]

_PotionSchemaType = NamedTuple("Potion", [
    ("id", int),
    ("name", str),
    ("description", str),
    ("type", Literal["HealingDefinite", "StrengthDefinite", "ResilienceDefinite", "HealingIndefinite", "StrengthIndefinite", "ResilienceIndefinite"]),
    ("baseAmount", float),
    ("multiplierAmount", float), # Multiplier amount is not used in indefinite type.
    ("duration", float),
    ("curve", int), # 0 means linear, 1 means ease-out-quint, to be implemented for other curves.
    # ("flags", list[int]),
    ("nextId", Optional[int]), # Reference to potionDatabase, this allows a potion to have multiple effects. The referenced potion typically is an internal one.
])
_PotionSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("name", str, lambda x: x, lambda x: x),
    database_property_new("description", str, lambda x: x, lambda x: x),
    database_property_new("type", str, lambda x: x, lambda x: x),
    database_property_new("baseAmount", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("multiplierAmount", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("duration", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("curve", int, lambda x: int(x), lambda x: str(x)),
    # database_property_new("flags", list[int], lambda x: array_map(string_split(x, "|"), lambda v: int(v)), lambda x: array_join(array_map(x, lambda v: str(v)), "|")),
    database_property_new("nextId", int, lambda x: int(x) if x != "" else None, lambda x: str(x) if x != None else ""),
]
_PotionSchema = database_schema_new("csv", _PotionSchemaType, _PotionSchemaProperties)
_PotionDatabase = Database[_PotionSchemaType]

_BattleSchemaType = NamedTuple("Battle", [
    ("id", int),
    ("turn", Literal[0, 1, 2]), # Which turn is it. 0 means have not been decided, 1 means player 1 turn, 2 means player 2 turn.
    ("player1Id", int), # Reference to userDatabase
    ("player2Id", int), # Reference to userDatabase
    ("monster1Id", Optional[int]), # Reference to player 1's currently fighting monster, reference to inventoryMonsterDatabase, might be None if the player haven't chose the monster yet, or do not have any remaining monster
    ("monster2Id", Optional[int]), # Reference to player 2's currently fighting monster, reference to inventoryMonsterDatabase, might be None if the player haven't chose the monster yet, or do not have any remaining monster
    ("verdict", Literal[-1, 0, 1, 2, 3, 4]), # -1 means the battle is not finished yet, 0 means draw, 1 means player 1 wins, 2 means player 2 wins, 3 means player 1 escaped, 4 means player 2 escaped
    ("handler", str), # Handler or logic for current battle
])
_BattleSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("turn", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("player1Id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("player2Id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("monster1Id", int, lambda x: int(x) if x != "" else None, lambda x: str(x) if x != None else ""),
    database_property_new("monster2Id", int, lambda x: int(x) if x != "" else None, lambda x: str(x) if x != None else ""),
    database_property_new("verdict", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("handler", str, lambda x: x, lambda x: x),
]
_BattleSchema = database_schema_new("csv", _BattleSchemaType, _BattleSchemaProperties)
_BattleDatabase = Database[_BattleSchemaType]

_ArenaSchemaType = NamedTuple("Arena", [
    ("id", int),
    ("playerId", int), # Reference to userDatabase
    ("battleIds", list[Optional[int]]), # Reference to battleDatabase. The last id might be null, if it's not null it means the last battle still happening. This array should have at least one element.
    ("handler", str), # Handler or logic for current arena
])
_ArenaSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("playerId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("battleIds", list[int], lambda x: array_map(string_split(x, "|"), lambda v: int(v) if len(v) > 0 else None), lambda x: array_join(array_map(x, lambda v: str(v) if v is not None else ""), "|")),
    database_property_new("handler", str, lambda x: x, lambda x: x),
]
_ArenaSchema = database_schema_new("csv", _ArenaSchemaType, _ArenaSchemaProperties)
_ArenaDatabase = Database[_ArenaSchemaType]

_ShopSchemaType = NamedTuple("Shop", [
    ("id", int),
    ("referenceType", Literal["monster", "item"]), # A way for `referenceId` to know which database to look for.
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
    ("toMonsterId", int), # Reference to monsterDatabase, note that both `fromMonsterId` and `toMonsterId` reference should have the same monster type.
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
    ("referenceId", int), # Reference to potionDatabase, this is a bit awkward since all of the item type available currently is potion only.
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
    ("experiencePoints", float),
    ("healthPoints", float), # These fields are modifiers, usually it should be copied from the fields in referenced monster.
    ("attackPower", float),
    ("defensePower", float),
    ("activePotions", list[tuple[float, float, int]]), # Reference to potionDatabase, [lastTick, remainingTime, potionType]
])
_InventoryMonsterSchemaProperties = [
    database_property_new("id", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("ownerId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("referenceId", int, lambda x: int(x), lambda x: str(x)),
    database_property_new("name", str, lambda x: x, lambda x: x),
    database_property_new("experiencePoints", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("healthPoints", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("attackPower", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("defensePower", float, lambda x: float(x), lambda x: str(x)),
    database_property_new("activePotions", list[tuple[float, float, int]], 
        lambda x: array_filter(array_map(string_split(x, "|"), lambda v, *_: (float(string_split(v, "`")[0]), float(string_split(v, "`")[1]), int(string_split(v, "`")[2])) if len(v) > 0 else None), lambda p, *_: p is not None), 
        lambda x: array_join(array_map(x, lambda v, *_: (str(v[0]) + "`" + str(v[1]) + "`" + str(v[2])) if v is not None else "", "|"))),
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
    userId=Optional[int], # If the user is logged in, the value must refer to userDatabase, otherwise it must be None
    visual=_Visual
)

def _gamestate_new(directory: str) -> _GameState:
    userDatabase = database_new(path.join(directory, "database_user.csv"), _UserSchema)
    monsterDatabase = database_new(path.join(directory, "database_monster.csv"), _MonsterSchema)
    potionDatabase = database_new(path.join(directory, "database_potion.csv"), _PotionSchema)
    battleDatabase = database_new(path.join(directory, "database_battle.csv"), _BattleSchema)
    arenaDatabase = database_new(path.join(directory, "database_arena.csv"), _ArenaSchema)
    shopDatabase = database_new(path.join(directory, "database_shop.csv"), _ShopSchema)
    laboratoryDatabase = database_new(path.join(directory, "database_laboratory.csv"), _LaboratorySchema)
    inventoryItemDatabase = database_new(path.join(directory, "database_inventory_item.csv"), _InventoryItemSchema)
    inventoryMonsterDatabase = database_new(path.join(directory, "database_inventory_monster.csv"), _InventoryMonsterSchema)
    database_load(userDatabase)
    database_load(monsterDatabase)
    database_load(potionDatabase)
    database_load(battleDatabase)
    database_load(arenaDatabase)
    database_load(shopDatabase)
    database_load(laboratoryDatabase)
    database_load(inventoryItemDatabase)
    database_load(inventoryMonsterDatabase)
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
        userId=None,
        visual=_visual_new()
    )
def _gamestate_save(gameState: _GameState) -> None:
    database_save(gameState["userDatabase"])
    database_save(gameState["monsterDatabase"])
    database_save(gameState["potionDatabase"])
    database_save(gameState["battleDatabase"])
    database_save(gameState["arenaDatabase"])
    database_save(gameState["shopDatabase"])
    database_save(gameState["laboratoryDatabase"])
    database_save(gameState["inventoryItemDatabase"])
    database_save(gameState["inventoryMonsterDatabase"])
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
def _gamestate_get_visual(gameState: _GameState) -> _Visual:
    return gameState["visual"]
def _gamestate_set_user_id(gameState: _GameState, userId: Optional[int]) -> None:
    gameState["userId"] = userId

# this is different from time.time(), this time is local to the game save. Updated every tick, may return same value if it is on the same tick.
def _gamestate_time(gameState: _GameState) -> float:
    return 0
def _gamestate_deltatime(gameState: _GameState) -> float:
    return 0
def _gamestate_rand(gameState: _GameState) -> float:
    return rand()
