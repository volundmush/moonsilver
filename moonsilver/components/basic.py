from . base import BaseComponent
from typing import List, Set, Dict, Any
from datetime import timedelta


class ObjectComponent(BaseComponent):
    """
    This is a component used by all Entities that have a physical presence in the game world.
    Items, Characters, Spaceships, NPCs, etc. If it can be poked, punched, looked at, it needs
    one of these. Some other things with a more abstract presence, like Exits and Rooms, also
    need them.
    """
    name: str = ""
    color_name: str = ""
    key_words: Set[str] = set()
    alias: str = ""
    alias_words: Set[str] = set()
    # The short desc is used for displaying an item in the room.
    short_desc: str = ""
    # The internal desc is seen by objects that are 'inside' this. A Room's description is an
    # internal desc.
    internal_desc: str = ""
    # The external desc is seen by objects looking 'at' them. An Item's description is likely external.
    # There is a difference due to the possibility of an Entity that might be something can be inside.
    external_desc: str = ""

    def export(self):
        return {
            'name': self.name,
            'key_words': self.key_words,
            'alias': self.alias,
            'alias_words': self.alias_words,
            'short_desc': self.short_desc,
            'internal_desc': self.internal_desc,
            'external_desc': self.external_desc
        }


class RoomComponent(BaseComponent):
    """
    The Room component is used by Room Entities to manage properties like Terrain and their Exits.
    Automap tiling too.
    """
    # The key is used to identify a room within a Structure.
    # All Rooms within a structure must have different keys.
    key: str = ""
    tile: str = "O"
    exits: Dict[str, int]
    terrain: str = "normal"

    # All Rooms belong to a Structure.
    structure: int = 0

    # index of all objects that are lounging around inside this room.
    objects: Set[int] = set()

    def export(self):
        return {
            'key': self.key,
            'structure': self.structure,
            'tile': self.tile,
            'exits': self.exits,
            'terrain': self.terrain
        }


class ExitComponent(BaseComponent):
    """
    The ExitComponent is possessed by Exits.
    """
    # All Exits belong to a room.
    room: int = 0
    # All Exits have a direction. All Exits in the same Room must have different Directions.
    direction: str = ""
    # Destination is the ID of the Room Entity this points at. If this is 0, the Exit has no destination
    # and will not work.
    destination: int = 0
    # Gateway is the ID of the Gateway Entity this uses for properties like door locks.
    # If this 0, the Exit has no Gateway.
    gateway: int = 0

    def export(self):
        return {
            'room': self.room,
            'direction': self.direction,
            'destination': self.destination,
            'gateway': self.gateway
        }


class GatewayComponent(BaseComponent):
    """
    Gateways are Entities that sit 'between' Exits, offering services like door locks and bi-directional
    traversal rules.
    """
    # All Gateways belong to a Structure.
    structure: int = 0
    exits: Set[int] = set()
    state: str = "open"

    def export(self):
        return {
            'exits': self.exits,
            'state': self.state
        }


class StructureComponent(BaseComponent):
    """
    Structures are Entities that bundle up rooms, exits, and gateways into a single cohesive space.
    """
    # A structure may be inside another structure. If 0, it is not.
    inside: int = 0
    # And this property will keep track of such as a reverse lookup.
    structures: Set[int] = set()
    # Keeps an index of all Rooms and Gateways inside the structure.
    rooms: Dict[str, int] = dict()
    gateways: Dict[str, int] = dict()
    # An index of all non-room/exit/gateway objects directly inside this structure.
    # This does not include objects inside structures inside this one, or objects that are also structures.
    objects: Set[int] = set()


class MetaComponent(BaseComponent):
    """
    The Meta Component handles meta-data about an Entity, such as what 'kind' of Entity it is to be treated as
    and what bundle that 'kind' is defined in.
    """
    # All Entities should stem from a 'kind' contained/defined in a specific bundle.
    bundle: str = ""
    kind: str = ""
    # Database mode is probably some kind of table / collection identifier. key is its primary key.
    database_mode: Any = None
    database_key: Any = None


class RegionComponent(BaseComponent):
    """
    The RegionComponent is for Entities which are 'Regions', such as the Root, Galaxies, Sectors, Wilderness, etc.
    Regions can be inhabited by Objects and Structures, all of which should have 3D coordinates.
    Regions are arranged in a URL-like structure, with the Root having depth 0 and no key.
    """
    key: str = ""
    parent: int = 0
    depth: int = 0
    children: Dict[str, int]

    # The objects dictionary does NOT contain other Entities with RegionComponents. Those are Children.
    objects: Set[int] = set()


class RegionLocationComponent(BaseComponent):
    """
    RegionLocations are 3D vectors.
    """
    region: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class RoomLocationComponent(BaseComponent):
    """
    If an Object exists inside a room, this Component tracks that.
    """
    room: int = 0


class RealityLayerComponent(BaseComponent):
    """
    For locations that use the Reality Layer system, these properties allow for filtering of which events / objects
    are visible to who and how they can interact.
    """
    exists: Set[str] = set()
    transmits: Set[str] = set()
    perceives: Set[str] = set()
    interacts: Set[str] = set()


class ActionQueueComponent(BaseComponent):
    queue: List[Any] = list()
    delay: timedelta = timedelta(0)
    remaining: timedelta = timedelta(0)
