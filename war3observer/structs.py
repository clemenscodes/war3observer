from construct import Int8ub, Int32sl, Int16sl, Float32l, Float32l, CString, Struct, Adapter, Byte, Padding, Padded, PaddedString, Enum

"""
  Formats: War3StatsObserverSharedMemory
  Version: 0

  The structure of the memory mapped observer API file. It can be read
  in-game with the mmap python module.
"""

Byte = Int8ub()
Integer = Int32sl()
Short = Int16sl()
Float = Float32l()
String = CString("utf8")

class ByteStringAdapter(Adapter):
  def _decode(self, obj, context, path):
    return bytes(obj)

  def _encode(self, obj, context, path):
    return list(obj)

ByteId = ByteStringAdapter(Byte[4])

class BooleanAdapter(Adapter):
  def __init__(self, subcon, falseval=0, trueval=1):
    super(BooleanAdapter, self).__init__(subcon)
    self.falseval = falseval if isinstance(falseval, list) else [falseval]
    self.trueval = trueval if isinstance(trueval, list) else [trueval]

  def _decode(self, obj, context, path):
    return obj not in self.falseval

  def _encode(self, obj, context, path):
    return self.trueval[0] if obj else self.falseval[0]

IntegerBoolean = BooleanAdapter(Integer)

Color = Struct(
  "r" / Byte,
  "g" / Byte,
  "b" / Byte,
  "a" / Byte
)
class Utf8FallbackAdapter(Adapter):
  """Utf8FallbackAdapter class

  This adapter is necessary due to a bug in construct that fails to
  catch unicode decoding exceptions with the `Optional`, `Select`, etc
  structs. There is an issue on their tracker about it already.
  """
  def _decode(self, obj, context, path):
    try:
      return obj.decode('utf-8')
    except UnicodeDecodeError:
      return None

  def _encode(self, obj, context, path):
    try:
      return obj.encode('utf-8')
    except UnicodeEncodeError:
      return None

class FlippedByteStringAdapter(Adapter):
  def _decode(self, obj, context, path):
    return bytes(obj[::-1]).decode('utf-8')

  def _encode(self, obj, context, path):
    return list(obj.encode('utf-8'))[::-1]

FlippedByteId = FlippedByteStringAdapter(Byte[4])

ObserverPlayerResearch = Struct(
  "id" / FlippedByteId,
  Padding(100), # name
                # names are intentionally dismissed due to encoding
                # issues on different warcraft locales
                # if you need an object's name, you must get it from
                # the tables in the game data files
  "progress_percent" / Integer,
  "type" / Enum(Byte, UPGRADE=0, UNIT=1, REVIVAL=2),
  "art" / PaddedString(100, "utf8")
)

ObserverPlayerUnit = Struct(
  "id" / FlippedByteId,
  Padding(100), # name
  "owning_player_id" / Integer, # maybe?
  "alive_count" / Integer,
  "total_count" / Integer,
  "art" / PaddedString(100, "utf8"),
  "is_worker" / BooleanAdapter(Byte),
  "is_busy_worker" / BooleanAdapter(Byte),
  "damage_dealt" / Integer,
  "damage_received" / Integer,
  "damage_healed" / Integer
)

ObserverPlayerUpgrade = Struct(
  "id" / FlippedByteId,
  "class" / Enum(PaddedString(100, "utf8"),
    NONE="_",
    ARMOR="armor",
    ARTILLERY="artillery",
    MELEE="melee",
    RANGED="ranged",
    CASTER="caster"
  ),
  "level" / Integer,
  "level_max" / Integer,
  "unknown_int_1" / Integer, # ?
  "art" / PaddedString(100, "utf8")
)

ObserverPlayerBuilding = Struct(
  "id" / FlippedByteId,
  Padding(100), # name
  "progress_percent" / Integer,
  "upgrade_progress_percent" / Integer,
  "art" / PaddedString(100, "utf8")
)

ObserverPlayerHeroItem = Struct(
  "id" / FlippedByteId,
  Padding(100), # name
  "slot" / Integer,
  "charges" / Integer,
  "art" / PaddedString(100, "utf8")
)

ObserverPlayerHeroAbility = Struct(
  "id" / FlippedByteId,
  Padding(36), # name
  "cooldown_time" / Float, # in seconds
  "cooldown" / Float, # in seconds
  "level" / Integer,
  "art" / PaddedString(100, "utf8"),
  "is_hero_ability" / BooleanAdapter(Byte),
  "damage_dealt" / Integer,
  "damage_healed" / Integer
)

ObserverPlayerHero = Struct(
  "id" / FlippedByteId,
  "class" / PaddedString(100, "utf8"),
  "art" / PaddedString(100, "utf8"),
  "level" / Integer,
  "experience" / Integer,
  "experience_max" / Integer,
  "hitpoints" / Integer,
  "hitpoints_max" / Integer,
  "mana" / Integer,
  "mana_max" / Integer,
  "damage_dealt" / Integer,
  "damage_received" / Integer,
  "damage_self" / Integer,
  "index" / Integer,
  "damage_healed" / Integer,
  "deaths_count" / Integer,
  "kills_count" / Integer,
  "kills_self" / Integer,
  "kills_heroes" / Integer,
  "kills_buildings" / Integer,
  "time_alive" / Integer, # in ms
  "abilities_count" / Integer,
  "abilities" / Padded(24 * ObserverPlayerHeroAbility.sizeof(), Array(this.abilities_count, ObserverPlayerHeroAbility)),
  "inventory_count" / Integer,
  "inventory" / Padded(6 * ObserverPlayerHeroItem.sizeof(), Array(this.inventory_count, ObserverPlayerHeroItem))
)

ObserverPlayer = Struct(
  "name" / Utf8FallbackAdapter(FixedSized(36, NullStripped(GreedyBytes))), # fallback to None if name fails
                                                                           # to be decoded
  "race_preference" / Enum(Byte,
    HUMAN=0x01,
    ORC=0x02,
    NIGHTELF=0x04,
    UNDEAD=0x08,
    DEMON=0x10,
    RANDOM=0x20,
    SELECTABLE=0x40
  ),
  "race" / Enum(Byte,
    UNKNOWN=0,
    HUMAN=1,
    ORC=2,
    UNDEAD=3,
    NIGHTELF=4,
    DEMON=5,
    LAST=6,
    OTHER=7,
    CREEP=8,
    COMMONER=9,
    CRITTER=10,
    NAGA=11
  ),
  "id" / Byte,
  "team_index" / Byte,
  "team_color" / Byte,
  "type" / Enum(Byte, EMPTY=0, PLAYER=1, COMPUTER=2, NEUTRAL=3, OBSERVER=4, NONE=5, OTHER=6),
  "handicap" / Integer,
  "game_result" / Enum(Byte, VICTORY=0, DEFEAT=1, TIE=2, IN_PROGRESS=3),
  "slot_state" / Enum(Byte, EMPTY=0, PLAYING=1, LEFT=2),
  "ai_difficulty" / Enum(Byte, EASY=0, NORMAL=1, INSANE=2),
  "apm" / Integer,
  "apm_realtime" / Integer,
  "gold" / Integer,
  "gold_mined" / Integer,
  "gold_taxed" / Integer,
  "gold_tax" / Integer,
  "lumber" / Integer,
  "lumber_harvested" / Integer,
  "lumber_taxed" / Integer,
  "lumber_tax" / Integer,
  "food_max" / Integer,
  "food" / Integer,
  # paddings are done on every array, usually with 999 maximums: every struct must be of fixed size
  "heroes_count" / Integer,
  "heroes" / Padded(999 * ObserverPlayerHero.sizeof(), Array(this.heroes_count, ObserverPlayerHero)),
  "buildings_on_map_count" / Integer,
  "buildings_on_map" / Padded(999 * ObserverPlayerBuilding.sizeof(), Array(this.buildings_on_map_count, ObserverPlayerBuilding)),
  "upgrades_completed_count" / Integer,
  "upgrades_completed" / Padded(999 * ObserverPlayerUpgrade.sizeof(), Array(this.upgrades_completed_count, ObserverPlayerUpgrade)),
  "units_on_map_count" / Integer,
  "units_on_map" / Padded(999 * ObserverPlayerUnit.sizeof(), Array(this.units_on_map_count, ObserverPlayerUnit)), # including heroes and corpses
  "researches_in_progress_count" / Integer,
  "researches_in_progress" / Padded(999 * ObserverPlayerResearch.sizeof(), Array(this.researches_in_progress_count, ObserverPlayerResearch)), # including unit training
  Padding(135868), # item history and count, dismissed for now
  Padding(40) # ? upkeep times, dismissed for now
)

ObserverGame = Struct(
  "refresh_rate" / Integer,
  "is_in_game" / BooleanAdapter(Byte),
  "game_time" / Integer, # in ms
  "players_count" / Byte,
  "game_name" / PaddedString(256, "utf8"),
  "map_name" / PaddedString(256, "utf8")
)

ObserverFile = Struct(
  "version" / Integer,
  "game" / ObserverGame,
  "players" / Array(28, ObserverPlayer),
  Padding(1547451) # shops on map, dismissed for now
)
