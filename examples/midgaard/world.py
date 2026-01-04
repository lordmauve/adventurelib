"""Game world construction for the Midgaard adventure.

This module builds the locations, items, and initial flags for the
self-aware sword-and-sorcery romp.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from adventurelib import Bag, Item, Room


@dataclass
class WorldState:
    """Container object for Midgaard's initial state."""

    starting_room: Room
    rooms: Dict[str, Room]
    inventory: Bag
    flags: Dict[str, bool]


def build_world() -> WorldState:
    """Construct the rooms, items, and flags for Midgaard.

    :returns: A populated :class:`WorldState` with the starting room and flags.
    """
    Room.items = Bag()

    camp = Room(
        """
        A pine-framed trail camp sits under a sky the colour of forge smoke.
        Bedrolls are kicked askew and a cooking tripod still smells of sage
        and questionable bravery. An abandoned kettle wheezes steam as if it
        were giving you side-eye.
        """
    )
    waystone = Room(
        """
        The Kingfisher Road runs beneath a mossy waystone, its runes politely
        glowing to be dramatic. A dozen boot prints point in every direction
        because the last adventuring party could not agree on brunch plans.
        Birds heckle you from above.
        """
    )
    inn = Room(
        """
        The Laughing Lantern Inn leans into the road like an old bard telling
        a story to his own drink. Lanterns sway gently indoors despite the
        absence of wind. A chalkboard menu promises soup, sarcasm, and exact
        change.
        """
    )
    bridge = Room(
        """
        A half-collapsed bridge spans a shallow ravine. Someone has installed
        tasteful skulls as decor. A troll loiters here with the self-importance
        of a bureaucrat and the personal hygiene of a compost heap.
        """
    )
    market = Room(
        """
        Ruins of the old Midgaard market spread out like a cracked chessboard.
        Stalls lie in splinters, but wildflowers have decided commerce is over
        and reclaimed the prime retail frontage.
        """
    )
    cavern_entrance = Room(
        """
        A fissure yawns behind a fallen statue. Cool air spills out, smelling
        of mineral water and unfiled paperwork. Faint luminescence pulses
        deeper inside, promising either treasure or actionable spores.
        """
    )
    glow_grotto = Room(
        """
        A grotto unfolds in blues and greens. Bioluminescent fungi paint
        delicate constellations on the walls. Somewhere, dripping water keeps
        perfect comedic timing. The air tingles with quiet anticipation.
        """
    )
    barrows = Room(
        """
        A ring of barrow mounds rises from fog like sleeping dragons that
        overslept their alarms. A wight paces nearby, reading a self-help
        scroll titled "Unfinished Business and You".
        """
    )

    camp.north = waystone
    waystone.east = inn
    waystone.west = bridge
    bridge.west = market
    market.north = cavern_entrance
    cavern_entrance.north = glow_grotto
    waystone.north = barrows

    sword = Item("battered longsword", "sword", "blade")
    trail_rations = Item("trail rations", "rations", "snack")
    map_fragment = Item("ink-splotched map fragment", "map", "fragment")
    lantern = Item("ever-warm lantern", "lantern", "lamp")
    troll_toll = Item("troll toll chit", "chit", "toll")
    mushroom = Item("sparkleaf mushroom", "sparkleaf", "mushroom")
    coin = Item("ancient dragon-stamped coin", "coin", "dragcoin")

    camp.items = Bag({sword, trail_rations})
    waystone.items = Bag({map_fragment})
    inn.items = Bag({lantern})
    bridge.items = Bag({troll_toll})
    market.items = Bag({coin})
    glow_grotto.items = Bag({mushroom})

    inventory = Bag({Item("crumpled apology note", "note", "apology")})

    flags = {
        "troll_blocking": True,
        "wight_grumpy": True,
        "mushroom_delivered": False,
        "lantern_lit": False,
        "market_gossip_heard": False,
    }

    rooms = {
        "camp": camp,
        "waystone": waystone,
        "inn": inn,
        "bridge": bridge,
        "market": market,
        "cavern_entrance": cavern_entrance,
        "glow_grotto": glow_grotto,
        "barrows": barrows,
    }

    return WorldState(starting_room=camp, rooms=rooms, inventory=inventory, flags=flags)
