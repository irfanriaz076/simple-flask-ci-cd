from app.app import create_app
from app.models import add_user, get_users

def test_add_and_get_users(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"

    import app.models as models
    monkeypatch.setattr(models, "DB_PATH", str(db_path))

    app = create_app()
    client = app.test_client()

    add_user("Alice")
    users = get_users()
    assert len(users) == 1
    assert users[0]["name"] == "Alice"

    response = client.get("/")
    assert response.status_code == 200
