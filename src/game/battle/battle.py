from utils.primordials import *
from game.state import *
from game.database import *
from game.inventory import *
from typing import Optional, Callable, Literal, Union

def _battle_get(gameState: GameState, battleId: int) -> BattleSchemaType:
    battleDatabase = gamestate_get_battle_database(gameState)
    return database_get_entry_at(battleDatabase, battleId)

def _battle_set(gameState: GameState, battleId: int, modifier: Union[BattleSchemaType, Callable[[BattleSchemaType], BattleSchemaType]]) -> BattleSchemaType:
    battleDatabase = gamestate_get_battle_database(gameState)
    battle = modifier(database_get_entry_at(battleDatabase, battleId)) if callable(modifier) else modifier
    database_set_entry_at(battleDatabase, battleId, battle)
    return battle

def _battle_new(gameState: GameState) -> BattleSchemaType:
    battleDatabase = gamestate_get_battle_database(gameState)
    battleId = database_get_entries_length(battleDatabase)
    battle = BattleSchemaType(
        id=battleId,
        turn=None,
        player1Id=None,
        player2Id=None,
        monster1Id=None,
        monster2Id=None,
        verdict=None,
        handler=None,
    )
    database_set_entry_at(battleDatabase, battleId, battle)
    return battle

def _battle_end_player_draw(gameState: GameState, battle: BattleSchemaType) -> BattleSchemaType:
    return _battle_set(gameState, battle.id, namedtuple_with(battle, verdict=0))

def _battle_end_player_won(gameState: GameState, battle: BattleSchemaType, player12: Literal[1, 2]) -> BattleSchemaType:
    return _battle_set(gameState, battle.id, namedtuple_with(battle, verdict=1 if player12 == 1 else 2))

def _battle_end_player_escaped(gameState: GameState, battle: BattleSchemaType, player12: Literal[1, 2]) -> BattleSchemaType:
    return _battle_set(gameState, battle.id, namedtuple_with(battle, verdict=3 if player12 == 1 else 4))

def _battle_verdict_is_finished(verdict: int) -> bool:
    return verdict != -1

def _battle_verdict_is_player_draw(verdict: int) -> bool:
    return verdict == 0

def _battle_verdict_is_player_won(verdict: int) -> Optional[Literal[1, 2]]:
    return 1 if verdict == 1 else 2 if verdict == 2 else None

def _battle_verdict_is_player_escaped(verdict: int) -> Optional[Literal[1, 2]]:
    return 1 if verdict == 3 else 2 if verdict == 4 else None

def _battle_action_attack(gameState: GameState, battle: BattleSchemaType) -> tuple[float, float]:
    selfMonsterId = battle.monster1Id if battle.turn == 1 else battle.monster2Id if battle.turn == 2 else None
    opponentMonsterId = battle.monster2Id if battle.turn == 1 else battle.monster1Id if battle.turn == 2 else None
    selfMonster = inventory_monster_get(gameState, selfMonsterId)
    opponentMonster = inventory_monster_get(gameState, opponentMonsterId)
    selfMonsterAttack = inventory_monster_get_calculated_attack_power(gameState, selfMonster)
    selfMonsterAttack = selfMonsterAttack * 1.5 + selfMonsterAttack * 0.3 * (gamestate_rand(gameState) * 2 - 1)
    opponentMonsterDefense = inventory_monster_get_calculated_defense_power(gameState, opponentMonster)
    opponentMonsterDefense = opponentMonsterDefense * 0.2 + opponentMonsterDefense * 0.2 * (gamestate_rand(gameState) * 2 - 1)
    selfMonsterAttack = max(0, selfMonsterAttack - opponentMonsterDefense)
    opponentMonsterHealth = max(0, opponentMonster.healthPoints - selfMonsterAttack)
    inventory_monster_set(gameState, opponentMonsterId, namedtuple_with(opponentMonster, healthPoints=opponentMonsterHealth))
    # THIS IS A HACK TO CONFORM THE RULES. Count the damage given.
    # God, please forgive me.
    __battleSelfAttackCounter = f"__battle-{battle.id}-turn-{battle.turn}-attack"
    if __battleSelfAttackCounter in gameState:
        gameState[__battleSelfAttackCounter] += selfMonsterAttack
    else:
        gameState[__battleSelfAttackCounter] = selfMonsterAttack
    return selfMonsterAttack, opponentMonsterHealth
