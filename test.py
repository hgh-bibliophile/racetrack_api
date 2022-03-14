from starlette.testclient import TestClient
import main
from racetrack_models import Track

def test_all_endpoints():
    # note that TestClient is only sync, don't use asyns here
    client = TestClient(main.app)
    # note that you need to connect to database manually
    # or use client as contextmanager during tests
    with client as client:
        response = client.post("/tracks/", json={"name": "Test Track"})
        track = Track(**response.json())
        assert track.pk is not None
