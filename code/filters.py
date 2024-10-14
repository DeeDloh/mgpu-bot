from aiogram.filters import Filter
from aiogram.types import Message
import json


class NameGroup(Filter):
    def __init__(self) -> None:
        with open('../pars/groups.json', encoding='UTF-8') as f:
            self.avail_groups = list(json.load(f).keys())

    async def __call__(self, message: Message) -> bool:
        return message.text in self.avail_groups
