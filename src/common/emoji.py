import emoji

from pydantic import BaseModel


class EmojiName(BaseModel):
    emoji: str | None
    name: str


class EmojiParser:
    def __init__(self, raw_text: str) -> None:
        self._raw = raw_text

    @property
    def contains_emoji(self) -> bool:
        return bool(emoji.emoji_count(self._raw))

    def extract_emojis(self, text: str) -> list[str]:
        return [char for char in text if char in emoji.EMOJI_DATA]

    def extract_emojis_string(self, text: str) -> str:
        return ''.join(char for char in text if char in emoji.EMOJI_DATA)

    def remove_emojis(self, text: str) -> str:
        return ''.join(char if char not in emoji.EMOJI_DATA else '' for char in text).strip()

    def parse(self) -> EmojiName:
        """
        Parse emoji from text

        :return: emoji name
        """

        if not self.contains_emoji:
            return EmojiName(emoji=None, name=self._raw)

        emojis: str = self.extract_emojis_string(self._raw)
        demojis_name: str = self.remove_emojis(self._raw)

        return EmojiName(emoji=emojis, name=demojis_name)
