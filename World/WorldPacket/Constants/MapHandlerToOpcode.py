from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.WorldPacket.Constants.LoginOpCode import LoginOpCode

from Server.Handlers.PingHandler import PingHandler

from World.Object.Unit.Player.Handlers.CharacterEnum import CharacterEnum
from World.Object.Unit.Player.Handlers.CharacterCreate import CharacterCreate
from World.Object.Unit.Player.Handlers.CharacterDelete import CharacterDelete

from Server.Auth.Handlers.LoginChallenge import LoginChallenge
from Server.Auth.Handlers.LoginProof import LoginProof
from Server.Auth.Handlers.Realmlist import Realmlist
from Server.Auth.Handlers.AuthSession import AuthSession

from World.WorldEnter.Handlers.LoginVerifyWorld import LoginVerifyWorld
from World.WorldEnter.Handlers.TutorialFlags import TutorialFlags
from World.WorldEnter.Handlers.AccountDataTimes import AccountDataTimes
from World.WorldEnter.Handlers.TimeSync import TimeSync
from World.WorldEnter.Handlers.GameSpeed import GameSpeed
from World.WorldEnter.Handlers.MOTD import MOTD
from World.WorldEnter.Handlers.InitialSpells import InitialSpells

from World.Object.Unit.Player.Handlers.PlayerInit import PlayerInit
from World.Object.Unit.Player.Handlers.PlayerSpawn import PlayerSpawn
from World.Object.Unit.Player.Handlers.PlayerTarget import PlayerTarget
from World.Object.Unit.Player.Inventory.Equipment.Handlers.Sheathed import Sheathed

from World.Query.Handlers.QueryHandler import QueryHandler
from World.Query.Handlers.Logout import Logout
from World.Query.Handlers.Exit import Exit
from World.Query.Handlers.ActiveMover import ActiveMover

from World.Object.Unit.Movement.Handlers.MovementHandler import MovementHandler

from World.Chat.TextEmote import TextEmote
from World.Chat.Handlers.MessageHandler import MessageHandler

from World.Object.Unit.Spell.Handlers.SpellResult import SpellResult

from World.Object.Item.Handlers.ItemInfo import ItemInfo
from World.Object.Item.Handlers.SwapItem import SwapItem

from World.Region.Handlers.ZoneUpdate import ZoneUpdate

from Realm.Handlers.RealmSplit import RealmSplit


MAP_HANDLER_TO_OPCODE = {
    WorldOpCode.CMSG_PING: [PingHandler],

    # Character
    WorldOpCode.CMSG_CHAR_ENUM: [CharacterEnum],
    WorldOpCode.CMSG_CHAR_CREATE: [CharacterCreate],
    WorldOpCode.CMSG_CHAR_DELETE: [CharacterDelete],

    # WorldEnter
    LoginOpCode.LOGIN_CHALL: [LoginChallenge],
    LoginOpCode.LOGIN_PROOF: [LoginProof],
    LoginOpCode.REALMLIST: [Realmlist],
    WorldOpCode.CMSG_AUTH_SESSION: [AuthSession],
    WorldOpCode.CMSG_PLAYER_LOGIN: [
        PlayerInit,
        MOTD,
        TutorialFlags,
        LoginVerifyWorld,
        AccountDataTimes,
        InitialSpells,
        PlayerSpawn,
        GameSpeed,
        TimeSync,
    ],
    WorldOpCode.CMSG_UPDATE_ACCOUNT_DATA: [],
    WorldOpCode.CMSG_REQUEST_ACCOUNT_DATA: [],
    WorldOpCode.CMSG_REALM_SPLIT: [RealmSplit],
    WorldOpCode.CMSG_QUERY_TIME: [QueryHandler],
    WorldOpCode.CMSG_NAME_QUERY: [QueryHandler],
    WorldOpCode.CMSG_ZONEUPDATE: [ZoneUpdate],

    # Movement handling
    WorldOpCode.CMSG_SET_ACTIVE_MOVER: [ActiveMover],
    WorldOpCode.MSG_MOVE_START_FORWARD: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_TURN_LEFT: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_TURN_RIGHT: [MovementHandler],
    WorldOpCode.MSG_MOVE_STOP_STRAFE: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_STRAFE_LEFT: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_STRAFE_RIGHT: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_BACKWARD: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_SWIM: [MovementHandler],
    WorldOpCode.MSG_MOVE_STOP_SWIM: [MovementHandler],
    WorldOpCode.MSG_MOVE_SET_PITCH: [MovementHandler],
    WorldOpCode.MSG_MOVE_START_ASCEND: [MovementHandler],
    WorldOpCode.MSG_MOVE_JUMP: [MovementHandler],
    WorldOpCode.MSG_MOVE_FALL_LAND: [MovementHandler],
    WorldOpCode.MSG_MOVE_STOP: [MovementHandler],
    WorldOpCode.MSG_MOVE_STOP_TURN: [MovementHandler],
    WorldOpCode.MSG_MOVE_SET_FACING: [MovementHandler],
    WorldOpCode.MSG_MOVE_HEARTBEAT: [MovementHandler],

    # Query
    WorldOpCode.CMSG_LOGOUT_REQUEST: [Logout],
    WorldOpCode.CMSG_LOGOUT_CANCEL: [Exit],
    WorldOpCode.CMSG_CANCEL_TRADE: [Exit],
    WorldOpCode.CMSG_TIME_SYNC_RESP: [],

    # Chat
    WorldOpCode.CMSG_TEXT_EMOTE: [TextEmote],
    WorldOpCode.CMSG_MESSAGECHAT: [MessageHandler],

    # TODO: return actual data in this handlers
    # Spell
    WorldOpCode.CMSG_CAST_SPELL: [
        #SpellStart,
        #SpellGo,
        #AuraDuration,
        #ExtraAuraInfo,
        SpellResult
    ],
    WorldOpCode.CMSG_CANCEL_CAST: [],
    WorldOpCode.CMSG_CANCEL_AURA: [],

    # Action buttons
    WorldOpCode.CMSG_SET_ACTION_BUTTON: [],

    # Action
    WorldOpCode.CMSG_SET_SELECTION: [PlayerTarget],

    # Items
    WorldOpCode.CMSG_ITEM_QUERY_SINGLE: [ItemInfo],
    WorldOpCode.CMSG_SWAP_INV_ITEM: [SwapItem],
    WorldOpCode.CMSG_SETSHEATHED: [Sheathed],
}