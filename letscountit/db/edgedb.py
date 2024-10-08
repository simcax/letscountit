"""A module to help interface with the EdgeDB database."""

from os import environ
from uuid import UUID

import edgedb

from letscountit.base import Counterthing


class Database:
    """A class to help interface with the EdgeDB database."""

    def __init__(self):
        if environ.get("EDGEDB_DSN"):
            environ["EDGEDB_CLIENT_SECURITY"] = "insecure_dev_mode"
            self.client = edgedb.create_client(dsn=environ.get("EDGEDB_DSN"))

        else:
            self.client = edgedb.create_client()

    def query(self, query: str, **kwargs):
        """Query the EdgeDB database."""
        return self.client.query_single(query, **kwargs)

    def query_multiple(self, query: str, **kwargs):
        """Query the EdgeDB database and return multiple results."""
        return self.client.query(query, **kwargs)

    def get_counter(self, uuid: str) -> list:
        """Get a counter from the EdgeDB database."""
        try:
            result = self.query(
                "SELECT counter{uuid, name, count} FILTER .uuid = <uuid>$uuid",
                uuid=uuid,
            )
        except edgedb.errors.InvalidArgumentError as e:
            raise TypeError(f"Error getting counter: {e}")
        return result

    def get_counter_by_id(self, id: str) -> list:
        """Get a counter by id from the EdgeDB database."""
        try:
            result = self.query("SELECT counter{uuid, name, count} FILTER .id = <uuid>$id", id=id)
        except edgedb.errors.InvalidArgumentError as e:
            raise TypeError(f"Error getting counter: {e}")
        return result

    def create_counter(self, name: str, count: int = 0) -> list:
        """Create a named counter in the EdgeDB database. This will automatically assign a UUID."""
        counter = Counterthing(name=name, start_count=count)
        result = self.insert_counter(counter.uuid, counter.name, counter.count)
        result = self.get_counter_by_id(result.id)
        return result

    def insert_counter(self, uuid: UUID, name: str, count: int) -> list:
        """Insert a counter into the EdgeDB database."""
        try:
            result = self.query(
                """
                INSERT counter{
                        uuid := <uuid>$uuid,
                        name := <str>$name,
                        count := <int64>$count
                        }
                """,
                uuid=uuid,
                name=name,
                count=count,
            )
        except edgedb.errors.InvalidArgumentError as e:
            raise TypeError(f"Error inserting counter: {e}")
        return result

    def update_counter(self, uuid: str, count: int) -> list:
        """Update a counter in the EdgeDB database."""
        try:
            result = self.query(
                """
                UPDATE counter
                FILTER .uuid = <uuid>$uuid
                SET {
                    count := <int64>$count
                }
                """,
                uuid=uuid,
                count=count,
            )
        except edgedb.errors.InvalidArgumentError as e:
            raise TypeError(f"Error updating counter: {e}")
        return result
