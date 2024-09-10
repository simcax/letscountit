"""Base class for letscountit"""

from uuid import uuid4


class Basecounting:
    """Base class for a base counting object."""

    __version = "0.0.1"

    def __init__(self) -> None:
        pass

    def version(self):
        return self.__version


class Counterthing:
    def __init__(self, name: str, uuid=None, start_count: int = 0) -> None:
        """Initializes the counter with a uuid and a start count"""
        self.uuid = uuid if uuid is not None else self._generate_uuid()
        self.count = start_count
        self.name = name

    def __str__(self):
        return (
            f"Counterthing: {self.uuid} with count: {self.count} and name: {self.name}"
        )

    def __repr__(self):
        return (
            f"Counterthing: {self.uuid} with count: {self.count} and name: {self.name}"
        )

    def __eq__(self, other):
        if isinstance(other, Counterthing):
            return (
                self.uuid == other.uuid
                and self.count == other.count
                and self.name == other.name
            )
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def _generate_uuid(self):
        return uuid4()

    def up(self, count: int = 1):
        """Increases the count by the given amount, default is 1."""
        if isinstance(count, int):
            self.count += count
        else:
            raise ValueError("count needs to be an int")

    def down(self, count=1):
        """Decreases the count by the given amount, default is 1."""
        if isinstance(count, int):
            self.count -= count
        else:
            raise ValueError("count needs to be an int")
