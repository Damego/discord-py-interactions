from enum import IntEnum
from typing import Iterable, List, Optional, Union
from uuid import uuid1

from discord import Emoji, InvalidArgument, PartialEmoji

__all__ = (
    "emoji_to_dict",
    "Component",
    "ButtonStyle",
    "Button",
    "TextInputStyle",
    "TextInput",
    "Modal",
    "Select",
    "SelectOption",
    "ActionRow",
    "_get_component_type",
)


def emoji_to_dict(emoji: Union[Emoji, PartialEmoji, str]) -> dict:
    """
    Converts a default or custom emoji into a partial emoji dict.

    :param emoji: The emoji to convert.
    :type emoji: Union[discord.Emoji, discord.PartialEmoji, str]
    """
    if isinstance(emoji, Emoji):
        emoji = {"name": emoji.name, "id": emoji.id, "animated": emoji.animated}
    elif isinstance(emoji, PartialEmoji):
        emoji = emoji.to_dict()
    elif isinstance(emoji, str):
        emoji = {"name": emoji, "id": None}
    return emoji or {}


class Component:
    """
    Base class for components.
    """

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: dict):
        raise NotImplementedError


class TextInputStyle(IntEnum):
    SHORT = 1
    PARAGRAPH = 2


class TextInput(Component):
    """
    Creates a text input component for modal(form). Must be inside an ActionRow to be used (see :meth:`ActionRow`).

    :param style: Style of the text input. Refer to :class:`TextInputStyle`.
    :type style: Union[TextInputStyle, int]
    :param custom_id: A custom identifier.
    :type custom_id: str
    :param label: The label of text input.
    :type label: str
    :param placeholer: Custom placeholder text if nothing is inputted.
    :type placeholer: str
    :param min_length: The minimum input length for a text input.
    :type min_length: int
    :param max_length: The maximum input length for a text input.
    :type max_length: int
    :param value: A pre-filled value.
    :type value: str
    :returns: :class:`TextInput`
    """

    __slots__ = (
        "_type",
        "_style",
        "_custom_id",
        "_label",
        "_placeholder",
        "_min_length",
        "_max_length",
        "_value",
    )

    def __init__(
        self,
        *,
        style: Union[TextInputStyle, int] = None,
        custom_id: str = None,
        label: str = None,
        min_length: int = None,
        max_length: int = None,
        required: bool = True,
        value: str = None,
        placeholder: str = None,
    ):
        self._type = 4
        self._custom_id = custom_id or str(uuid1())
        self._style = style
        self._label = label
        self._min_length = min_length
        self._max_length = max_length
        self._required = required
        self._value = value
        self._placeholder = placeholder

    @property
    def custom_id(self):
        return self._custom_id

    @custom_id.setter
    def custom_id(self, value: str):
        self._custom_id = value

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value: Union[TextInputStyle, int]):
        self._style = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @property
    def min_length(self):
        return self._min_length

    @min_length.setter
    def min_length(self, value: int):
        self._min_length = value

    @property
    def max_length(self):
        return self._max_length

    @max_length.setter
    def max_length(self, value: int):
        self._max_length = value

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value: bool):
        self._required = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value: str):
        self._placeholder = value

    def to_dict(self) -> dict:
        data = {
            "type": 4,
            "custom_id": self._custom_id,
            "style": self._style,
            "label": self._label,
            "min_length": self._min_length,
            "max_length": self._max_length,
            "required": self._required,
            "value": self._value,
            "placeholder": self._placeholder,
        }
        return data

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            custom_id=data.get("custom_id"),
            style=data.get("style"),
            label=data.get("label"),
            min_length=data.get("min_length"),
            max_length=data.get("max_length"),
            required=data.get("required"),
            value=data.get("value"),
            placeholder=data.get("placeholder"),
        )


class Modal(Component):
    """
    Creates a popup modal(form).

    :param custom_id: A custom identifier.
    :type custom_id: str
    :param title: The title of popup modal.
    :type title: str
    :param components: Between 1 and 5 (inclusive) components that make up the modal.
    :type components: List[TextInput]
    :returns: :class:`Modal`
    """

    __slots__ = ("_custom_id", "_title", "_components")

    def __init__(
        self, *, custom_id: str = None, title: str = None, components: List[TextInput] = None
    ):
        self._custom_id = custom_id or str(uuid1)
        self._title = title
        self._components = components

    def to_dict(self) -> dict:
        data = {
            "custom_id": self._custom_id,
            "title": self._title,
            "components": [ActionRow(component).to_dict() for component in self._components],
        }
        return data


class SelectOption(Component):
    """
    Creates an option for Select components.

    :param label: The user-facing name of the option that will be displayed in discord client.
    :type label: str
    :param value: The value that the bot will receive when this option is selected.
    :type value: str
    :param emoji: The emoji of the option.
    :type emoji: Union[Emoji, PartialEmoji, str]
    :param description: An additional description of the option.
    :type description: str
    :param default: Whether or not this is the default option.
    :type default: bool
    :returns: :class:`SelectOption`
    """

    __slots__ = ("_label", "_value", "_emoji", "_description", "_default")

    def __init__(
        self,
        *,
        label: str,
        value: str,
        emoji: Union[Emoji, PartialEmoji, str] = None,
        description: str = None,
        default: bool = False,
    ):
        self._label = label
        self._value = value
        self._description = description
        self._default = default

        if emoji is not None:
            self.emoji = emoji_to_dict(emoji)
        else:
            self._emoji = None

    def to_dict(self) -> dict:
        data = {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "default": self.default,
        }
        if self.emoji is not None:
            data["emoji"] = self.emoji.to_dict()
        return data

    @property
    def label(self) -> str:
        return self._label

    @property
    def value(self) -> str:
        return self._value

    @property
    def emoji(self) -> Optional[PartialEmoji]:
        return self._emoji

    @property
    def description(self) -> str:
        return self._description

    @property
    def default(self) -> bool:
        return self._default

    @label.setter
    def label(self, value: str):
        if not len(value):
            raise InvalidArgument("Label must not be empty.")

        self._label = value

    @value.setter
    def value(self, value: str):
        self._value = value

    @emoji.setter
    def emoji(self, emoji: Union[Emoji, PartialEmoji, str]):
        self._emoji = emoji_to_dict(emoji)

    @description.setter
    def description(self, value: str):
        self._description = value

    @default.setter
    def default(self, value: bool):
        self._default = value

    def set_label(self, value: str):
        self.label = value

    def set_value(self, value: str):
        self.value = value

    def set_emoji(self, emoji: Union[Emoji, PartialEmoji, str]):
        self.emoji = emoji

    def set_description(self, value: str):
        self.description = value

    def set_default(self, value: bool):
        self.default = value

    @classmethod
    def from_json(cls, data: dict):
        emoji = data.get("emoji")
        return cls(
            label=data.get("label"),
            value=data.get("value"),
            emoji=PartialEmoji(
                name=emoji["name"],
                animated=emoji.get("animated", False),
                id=emoji.get("id"),
            )
            if emoji
            else None,
            description=data.get("description"),
            default=data.get("default", False),
        )


class Select(Component):
    """
    Creates a select (dropdown) component for use with the ``components`` field. Must be inside an ActionRow to be used (see :meth:`ActionRow`).

    :param options: The choices the user can pick from.
    :type options: List[SelectOption]
    :param custom_id: A custom identifier, like buttons.
    :type custom_id: str
    :param placeholder: Custom placeholder text if nothing is selected.
    :type placeholder: str
    :param min_values: The minimum number of items that **must** be chosen.
    :type min_values: int
    :param max_values: The maximum number of items that **can** be chosen.
    :type max_values: int
    :param disabled: Disables this component. Defaults to ``False``.
    :type disabled: bool
    :returns: :class:`Select`
    """

    __slots__ = (
        "_custom_id",
        "_options",
        "_placeholder",
        "_min_values",
        "_max_values",
        "_disabled",
    )

    def __init__(
        self,
        *,
        options: List[SelectOption],
        custom_id: str = None,
        placeholder: str = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
    ):
        if (not len(options)) or (len(options) > 25):
            raise InvalidArgument("Options length should be between 1 and 25.")

        self._custom_id = custom_id or str(uuid1())
        self._options = options
        self._placeholder = placeholder
        self._min_values = min_values
        self._max_values = max_values
        self._disabled = disabled

    def to_dict(self) -> dict:
        return {
            "type": 3,
            "options": list(map(lambda option: option.to_dict(), self.options)),
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled,
        }

    @property
    def custom_id(self) -> str:
        return self._custom_id

    @property
    def options(self) -> List[SelectOption]:
        return self._options

    @property
    def placeholder(self) -> str:
        return self._placeholder

    @property
    def min_values(self) -> int:
        return self._min_values

    @property
    def max_values(self) -> int:
        return self._max_values

    @property
    def disabled(self) -> bool:
        return self._disabled

    @custom_id.setter
    def custom_id(self, value: str):
        self.custom_id = value

    @options.setter
    def options(self, value: List[SelectOption]):
        if (not len(value)) or (len(value) > 25):
            raise InvalidArgument("Options length should be between 1 and 25.")

        self._options = value

    @placeholder.setter
    def placeholder(self, value: str):
        self._placeholder = value

    @min_values.setter
    def min_values(self, value: int):
        self._min_values = value

    @max_values.setter
    def max_values(self, value: int):
        self._max_values = value

    @disabled.setter
    def disabled(self, value: bool):
        self._disabled = value

    def set_custom_id(self, value: str):
        self.custom_id = value

    def set_options(self, value: List[SelectOption]):
        self.options = value

    def set_placeholder(self, value: str):
        self.placeholder = value

    def set_min_values(self, value: int):
        self.min_values = value

    def set_max_values(self, value: int):
        self.max_values = value

    def set_disabled(self, value: bool):
        self.disabled = value

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            custom_id=data.get("custom_id"),
            options=list(map(lambda x: SelectOption.from_json(x), data.get("options"))),
            placeholder=data.get("placeholder"),
            min_values=data.get("min_values"),
            max_values=data.get("max_values"),
            disabled=data.get("disabled", False),
        )


class ButtonStyle(IntEnum):
    blue = 1
    gray = 2
    grey = 2
    green = 3
    red = 4
    URL = 5


class Button(Component):
    """
    Creates a button component for use with the ``components`` field. Must be used within an ``ActionRow`` to be used (see :meth:`ActionRow`).

    .. note::
        At least a label or emoji is required for a button. You can have both, but not neither of them.

    :param style: Style of the button. Refer to :class:`ButtonStyle`.
    :type style: Union[ButtonStyle, int]
    :param label: The label of the button.
    :type label: Optional[str]
    :param emoji: The emoji of the button.
    :type emoji: Union[discord.Emoji, discord.PartialEmoji, dict]
    :param custom_id: The custom_id of the button. Needed for non-link buttons.
    :type custom_id: Optional[str]
    :param url: The URL of the button. Needed for link buttons.
    :type url: Optional[str]
    :param disabled: Whether the button is disabled or not. Defaults to `False`.
    :type disabled: bool
    :returns: :class:`Button`
    """

    __slots__ = ("_style", "_label", "_custom_id", "_url", "_disabled", "_emoji")

    def __init__(
        self,
        *,
        label: str = None,
        style: int = ButtonStyle.gray,
        custom_id: str = None,
        url: str = None,
        disabled: bool = False,
        emoji: Union[Emoji, PartialEmoji, str] = None,
    ):

        self._style = style
        self._label = label
        self._url = url
        self._disabled = disabled

        if emoji is not None:
            self._emoji = emoji_to_dict(emoji)
        else:
            self._emoji = None

        if not self.style == ButtonStyle.URL:
            self.custom_id = custom_id or str(uuid1())
        else:
            self.custom_id = None

    def to_dict(self) -> dict:
        data = {
            "type": 2,
            "style": self.style,
            "label": self.label,
            "custom_id": self.custom_id,
            "url": self.url if self.style == ButtonStyle.URL else None,
            "disabled": self.disabled,
        }
        if self.emoji:
            data["emoji"] = self.emoji.to_dict()
        return data

    @property
    def style(self) -> int:
        return self._style

    @property
    def label(self) -> str:
        return self._label

    @property
    def custom_id(self) -> str:
        return self._custom_id

    @property
    def url(self) -> Optional[str]:
        return self._url

    @property
    def disabled(self) -> bool:
        return self._disabled

    @property
    def emoji(self) -> PartialEmoji:
        return self._emoji

    @style.setter
    def style(self, value: int):
        if value == ButtonStyle.URL and self.custom_id:
            raise InvalidArgument("Both ID and URL are set.")
        if not (1 <= value <= ButtonStyle.URL):
            raise InvalidArgument(f"Style must be between 1, {ButtonStyle.URL}.")

        self._style = value

    @label.setter
    def label(self, value: str):
        if not value and not self.emoji:
            raise InvalidArgument("Label should not be empty.")

        self._label = value

    @url.setter
    def url(self, value: str):
        if value and self.style != ButtonStyle.URL:
            raise InvalidArgument("Button style is not URL. You shouldn't provide URL.")

        self._url = value

    @custom_id.setter
    def custom_id(self, value: str):
        if self.style == ButtonStyle.URL:
            raise InvalidArgument("Button style is set to URL. You shouldn't provide ID.")

        self._custom_id = value

    @disabled.setter
    def disabled(self, value: bool):
        self._disabled = value

    @emoji.setter
    def emoji(self, emoji: Union[Emoji, PartialEmoji, str]):
        self._emoji = emoji_to_dict(emoji)

    def set_style(self, value: int):
        self.style = value

    def set_label(self, value: int):
        self.label = value

    def set_url(self, value: int):
        self.url = value

    def set_custom_id(self, value: str):
        self.custom_id = value

    def set_disabled(self, value: bool):
        self.disabled = value

    def set_emoji(self, emoji: Union[Emoji, PartialEmoji, str]):
        self.emoji = emoji

    @classmethod
    def from_json(cls, data: dict):
        emoji = data.get("emoji")
        return cls(
            style=data.get("style"),
            label=data.get("label"),
            custom_id=data.get("custom_id"),
            url=data.get("url"),
            disabled=data.get("disabled", False),
            emoji=PartialEmoji(
                name=emoji["name"],
                animated=emoji.get("animated", False),
                id=emoji.get("id"),
            )
            if emoji
            else None,
        )


class ActionRow(Component):
    """
    ActionRow for message components.

    :param components: Components to go within the ActionRow.
    :returns: :class:`ActionRow`
    """

    __slots__ = ("_components",)

    def __init__(self, *args: List[Component]):
        self._components = list(args) if args is not None else []

    def disable_components(self) -> List[Component]:
        def disable(component: Component):
            component.disabled = True
            return component

        self._components = list(map(disable, self._components))
        return self

    def __list__(self) -> List[Component]:
        return self.components

    def __len__(self) -> int:
        return len(self.components)

    def __iter__(self) -> Iterable[Component]:
        return iter(self.components)

    def __getitem__(self, index: int) -> Component:
        return self.components[index]

    def __setitem__(self, index: int, value: Component):
        self._components[index] = value

    def __delitem__(self, index: int):
        del self._components[index]

    def to_dict(self) -> dict:
        data = {
            "type": 1,
            "components": [component.to_dict() for component in self.components],
        }
        return data

    def append(self, component: Component):
        self.components.append(component)

    @property
    def components(self) -> List[Component]:
        return self._components

    @components.setter
    def components(self, value: List[Component]):
        self._components = value

    def set_components(self, value: List[Component]):
        self.components = value

    def add_component(self, value: Component):
        self.components.append(value)

    @classmethod
    def from_json(cls, data: dict):
        components = data.get("components")
        if all(component.get("type") == 2 for component in components):
            return cls(*[Button.from_json(component) for component in data.get("components")])
        elif all(component.get("type") == 4 for component in components):
            return cls(*[TextInput.from_json(component) for component in data.get("components")])


def _get_component_type(type: int):
    return {1: ActionRow, 2: Button, 3: Select, 4: TextInput}[type]


def _get_components_json(
    components: List[Union[ActionRow, Component, List[Component]]] = None
) -> Optional[List[dict]]:
    if components is None:
        return None

    for i in range(len(components)):
        if isinstance(components[i], list):
            components[i] = ActionRow(*components[i])
        elif not isinstance(components[i], ActionRow):
            components[i] = ActionRow(components[i])

    lines = components
    return [row.to_dict() for row in lines] if lines else []
