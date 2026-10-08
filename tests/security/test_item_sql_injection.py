import sqlite3

from app import app


def test_item_name_cannot_change_sql_literal_meaning(tmp_path, monkeypatch):
    """Apostrophes must remain data, or the input must be rejected."""
    monkeypatch.chdir(tmp_path)
    with sqlite3.connect("shop.db") as connection:
        connection.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
        connection.executemany(
            "INSERT INTO items (id, name) VALUES (?, ?)",
            [(1, "plain"), (2, "a'b"), (3, "a''b")],
        )

    client = app.test_client()
    baseline = client.get("/item", query_string={"name": "plain"})
    assert baseline.status_code == 200
    assert baseline.get_json() == {"items": [[1, "plain"]]}

    # SQL interprets doubled apostrophes as one apostrophe inside a literal.
    # Both names are ordinary data: neither contains SQL commands or operators.
    response = client.get("/item", query_string={"name": "a''b"})
    if 400 <= response.status_code < 500:
        return  # Explicit input validation is also a secure outcome.
    assert response.status_code == 200
    assert response.get_json() == {"items": [[3, "a''b"]]}, (
        "The lookup must preserve the supplied name exactly, without interpreting "
        "its apostrophes as SQL syntax."
    )
