from app import app


def test_routes_are_registered():
    rules = {r.rule for r in app.url_map.iter_rules()}
    assert '/ping' in rules
    assert '/item' in rules
    assert '/file' in rules
