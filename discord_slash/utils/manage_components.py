import logging
import typing

import discord

from ..error import IncorrectType
from ..model import ComponentType

logger = logging.getLogger("discord_slash")


def get_components_ids(component: typing.Union[str, dict, list]) -> typing.Iterator[str]:
    """
    Returns generator with the ``custom_id`` of a component or list of components.
    :param component: Custom ID or component dict (actionrow or button) or list of the two.
    :returns: typing.Iterator[str]
    """

    if isinstance(component, str):
        yield component
    elif isinstance(component, dict):
        if component["type"] == ComponentType.actionrow:
            yield from (
                comp["custom_id"] for comp in component["components"] if "custom_id" in comp
            )
        elif "custom_id" in component:
            yield component["custom_id"]
    elif isinstance(component, list):
        # Either list of components (actionrows or buttons) or list of ids
        yield from (comp_id for comp in component for comp_id in get_components_ids(comp))
    else:
        raise IncorrectType(
            f"Unknown component type of {component} ({type(component)}). "
            f"Expected str, dict or list"
        )


def get_messages_ids(message: typing.Union[int, discord.Message, list]) -> typing.Iterator[int]:
    """
    Returns generator with the ``id`` of message or list messages.
    :param message: message ID or message object or list of previous two.
    :returns: typing.Iterator[int]
    """
    if isinstance(message, int):
        yield message
    elif isinstance(message, discord.Message):
        yield message.id
    elif isinstance(message, list):
        yield from (msg_id for msg in message for msg_id in get_messages_ids(msg))
    else:
        raise IncorrectType(
            f"Unknown component type of {message} ({type(message)}). "
            f"Expected discord.Message, int or list"
        )
