from uuid import uuid4

import edgedb


def test_edgedb():
    uuid = uuid4()
    client = edgedb.create_client()
    client.query(
        """
        INSERT counter{
                 uuid := <uuid>$uuid,
                 name := <str>$name
                 }
        """,
        uuid=uuid,
        name="test",
    )
    row = client.query("SELECT counter{uuid, name} FILTER .uuid = <uuid>$uuid", uuid=uuid)
    assert row[0].uuid == uuid
