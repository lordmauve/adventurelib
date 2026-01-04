"""Playable Midgaard example game built with Adventurelib."""
from __future__ import annotations

from typing import List

from adventurelib import Bag, Item, Room, say, set_context, start, when

from .world import WorldState, build_world


def describe_room(room: Room) -> None:
    """Print the current room description and any dynamic details.

    :param room: Room to describe.
    """
    say(room)

    if room is world.rooms["bridge"] and world.flags["troll_blocking"]:
        say(
            "The troll idly chews on a copy of 'Seven Habits of Highly Effective "
            "Lurkers' and eyes you like a misplaced footnote."
        )

    if room is world.rooms["barrows"]:
        if world.flags["wight_grumpy"]:
            say(
                "The wight flickers between corporeal and ghostly as it reads its "
                "scroll. It looks up hopefully when it hears your boots."
            )
        else:
            say("The wight is humming contentedly, absorbed in cross-stitching a sigil.")

    if room is world.rooms["glow_grotto"] and world.flags["lantern_lit"]:
        say(
            "The lantern's warm light mingles with the grotto's glow, and tiny "
            "motes swirl like they are applauding your aesthetic choices."
        )

    if room.items:
        for item in room.items:
            say(f"You notice {item} resting nearby.")

    exits = room.exits()
    if exits:
        say(f"Exits: {', '.join(exits)}")


def show_intro() -> None:
    """Print the opening narration."""
    say(
        "Welcome to Midgaard, where epic destiny makes time for sarcasm."
        " Type 'help' if the world tilts too dramatically."
    )


def go(direction: str) -> None:
    """Move the player in a direction if an exit exists.

    :param direction: Cardinal or relative direction to travel.
    """
    global current_room
    destination = current_room.exit(direction)
    if not destination:
        say("You stride confidently into nowhere. The nowhere files a complaint.")
        return

    if (
        current_room is world.rooms["bridge"]
        and direction == "west"
        and world.flags["troll_blocking"]
    ):
        say(
            "The troll blocks your way with a paw the size of a bread oven."
            " It demands a toll or at least a dramatic battle."
        )
        return

    current_room = destination
    set_context(None)
    look()


@when("north", direction="north")
@when("south", direction="south")
@when("east", direction="east")
@when("west", direction="west")
def move(direction: str) -> None:
    """Handle simple movement commands.

    :param direction: Desired travel direction.
    """
    go(direction)


@when("look")
def look() -> None:
    """Describe the current surroundings."""
    describe_room(current_room)


@when("inventory")
def show_inventory() -> None:
    """List items in the player's inventory."""
    if not inventory:
        say("Your inventory rattles with emptiness.")
        return

    say("You are currently carrying:")
    for item in inventory:
        say(f"- {item}")


@when("take ITEM")
def take(item: str) -> None:
    """Pick up an item from the current room.

    :param item: Name of the item to pick up.
    """
    picked_up = current_room.items.take(item)
    if picked_up:
        inventory.add(picked_up)
        say(f"You holster {picked_up} with all the swagger of a stage magician.")
    else:
        say("You grasp at empty air. The air is polite about it.")


@when("drop THING")
def drop(thing: str) -> None:
    """Drop an item from the inventory into the room.

    :param thing: Name of the item to drop.
    """
    dropped = inventory.take(thing)
    if dropped:
        current_room.items.add(dropped)
        say(f"You set down {dropped}. It looks relieved to be stationary.")
    else:
        say("You are not carrying that. Perhaps you left it in your other pockets.")


@when("inspect THING")
@when("examine THING")
def inspect(thing: str) -> None:
    """Inspect an item either nearby or in the inventory.

    :param thing: Name of the item to examine.
    """
    obj = inventory.find(thing) or current_room.items.find(thing)
    if not obj:
        say("You squint heroically, but nothing matches that description.")
        return

    lore = {
        "battered longsword": "The blade bears notches that spell out rude words in Elvish.",
        "trail rations": "A blend of oats, honey, and the concept of ambition.",
        "ink-splotched map fragment": (
            "The map shows Midgaard in careful ink, then smudges labelled 'here"
            " be editorial notes'."
        ),
        "ever-warm lantern": "A tinker's masterpiece that refuses to accept darkness quietly.",
        "troll toll chit": "A wooden token stamped 'IOU: One Heroic Pose'.",
        "ancient dragon-stamped coin": (
            "The coin's face bears a dragon with spectacles. The reverse lists tax exemptions."
        ),
        "sparkleaf mushroom": "It glows faintly and smells of petrichor and punchlines.",
        "crumpled apology note": "This note apologizes for 'incidental prophecy spillage'.",
    }
    description = lore.get(obj.name, "It looks important in a narrative kind of way.")
    say(description)


@when("attack TARGET")
def attack(target: str) -> None:
    """Attempt to attack a target.

    :param target: Name of the target to attack.
    """
    weapon = inventory.find("sword") or inventory.find("blade")
    target = target.lower()

    if target in {"troll", "bridge"}:
        if current_room is not world.rooms["bridge"]:
            say("You shadowbox the air. It yields immediately.")
            return
        if not weapon:
            say("You wind up a punch. The troll laughs in punctuation marks.")
            return
        world.flags["troll_blocking"] = False
        say(
            "You brandish the sword with theatrical flair. The troll applauds,"
            " declares bankruptcy, and scampers off."
        )
        return

    if target in {"wight", "ghost", "spirit"}:
        if current_room is not world.rooms["barrows"]:
            say("You swing at memories. They are unimpressed.")
            return
        if not world.flags["wight_grumpy"]:
            say("The wight waves cheerfully; it has moved on from duels.")
            return
        if not world.flags["lantern_lit"]:
            say("Steel passes through mist. Perhaps light would give it pause.")
            return
        world.flags["wight_grumpy"] = False
        say(
            "The lantern's glow steadies the wight. It bows, drops a vellum patch"
            " for your cloak, and returns to its nap."
        )
        charm = Item("vellum sigil patch", "sigil", "patch")
        inventory.add(charm)
        return

    say("You practice your battle cry on the horizon. It echoes back politely.")


@when("light ITEM")
def light(item: str) -> None:
    """Light an item if possible.

    :param item: Item name to ignite or illuminate.
    """
    if item.lower() not in {"lantern", "lamp"}:
        say("Pyromania denied. Only lanterns volunteer today.")
        return
    lamp = inventory.find(item)
    if not lamp:
        say("You pat your bags; the lantern is not among them.")
        return
    world.flags["lantern_lit"] = True
    say("The lantern blazes to life, smelling faintly of cinnamon and destiny.")


@when("talk to PERSON")
@when("speak to PERSON")
def talk(person: str) -> None:
    """Talk to a non-player character if present.

    :param person: Identifier of the person to address.
    """
    person = person.lower()
    if current_room is world.rooms["inn"] and person in {"innkeeper", "keeper", "barkeep"}:
        deliver_mushroom()
        if not world.flags["market_gossip_heard"]:
            world.flags["market_gossip_heard"] = True
            say(
                "The innkeeper shares gossip: a troll guards the bridge but fears"
                " union paperwork. He also mentions mushrooms that make soups glow."
            )
        else:
            say(
                "The innkeeper refills a mug that is not yours and asks you to avoid"
                " decapitating the furniture this time."
            )
        return

    if current_room is world.rooms["bridge"] and person in {"troll"}:
        say(
            "You attempt small talk. The troll counters with haikus about tolls."
            " This could go on for days."
        )
        return

    if current_room is world.rooms["barrows"] and person in {"wight", "ghost", "spirit"}:
        if world.flags["wight_grumpy"]:
            say(
                "The wight sighs. 'I cannot rest until someone respects fire safety,"
                "' it says, eyeing your unlit lantern."
            )
        else:
            say(
                "The wight thanks you for the light and recommends a bakery in the"
                " ruined market that still bakes spectral rye."
            )
        return

    say("You rehearse a conversation with an imaginary friend. It goes well.")


@when("rest")
def rest() -> None:
    """Take a brief rest to add flavor."""
    say(
        "You rest against a convenient narrative beat. Somewhere, a lute plays"
        " a riff about self-care and sharpened steel."
    )


@when("help")
def help_command() -> None:
    """Show helpful reminders of available actions."""
    commands: List[str] = [
        "north/south/east/west - move between rooms",
        "look - survey your surroundings",
        "take <item> / drop <item> - manage items",
        "inspect <item> - learn about something",
        "attack <target> - when diplomacy is overrated",
        "light lantern - turn on the ever-warm lantern",
        "talk to <person> - chat with locals",
        "inventory - view carried items",
        "rest - admire the ambience",
    ]
    say("Available commands:")
    for line in commands:
        say(f"  {line}")


def deliver_mushroom() -> None:
    """Handle giving the sparkleaf mushroom to the innkeeper."""
    if world.flags["mushroom_delivered"]:
        return
    prize = inventory.take("sparkleaf mushroom")
    if prize:
        world.flags["mushroom_delivered"] = True
        say(
            "The innkeeper ladles the mushroom into a bubbling pot. The soup glows"
            " emerald, patrons cheer, and someone names a sandwich after you."
        )


world: WorldState = build_world()
current_room: Room = world.starting_room
inventory: Bag = world.inventory
set_context(None)


def main() -> None:
    """Launch the Midgaard adventure."""
    show_intro()
    look()
    start()


if __name__ == "__main__":
    main()
