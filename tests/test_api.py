TOP_TRACKS_RESPONSE = {
    "items": [
        {
            "id": "track1",
            "name": "Test Track",
            "artists": [{"name": "Test Artist"}],
            "album": {"name": "Test Album"},
            "popularity": 80,
        }
    ]
}

TOP_ARTISTS_RESPONSE = {
    "items": [
        {
            "name": "Test Artist",
            "genres": ["hip-hop"],
            "popularity": 85,
            "followers": {"total": 500000},
        }
    ]
}

RECENTLY_PLAYED_RESPONSE = {
    "items": [
        {
            "track": {
                "id": "track1",
                "name": "Test Track",
                "artists": [{"name": "Test Artist"}],
            },
            "played_at": "2026-06-28T12:00:00.000Z",
        }
    ]
}


def test_get_top_tracks(client, mock_sp):
    mock_sp.current_user_top_tracks.return_value = TOP_TRACKS_RESPONSE

    response = client.get("/tracks/top")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Track"
    assert data[0]["artist"] == "Test Artist"
    assert data[0]["popularity"] == 80


def test_get_top_tracks_passes_params(client, mock_sp):
    mock_sp.current_user_top_tracks.return_value = TOP_TRACKS_RESPONSE

    client.get("/tracks/top?time_range=short_term&limit=10")

    mock_sp.current_user_top_tracks.assert_called_once_with(time_range="short_term", limit=10)


def test_get_recently_played(client, mock_sp):
    mock_sp.current_user_recently_played.return_value = RECENTLY_PLAYED_RESPONSE

    response = client.get("/tracks/recently-played")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["track_name"] == "Test Track"
    assert data[0]["played_at"] == "2026-06-28T12:00:00.000Z"


def test_get_top_artists(client, mock_sp):
    mock_sp.current_user_top_artists.return_value = TOP_ARTISTS_RESPONSE

    response = client.get("/artists/top")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Artist"
    assert data[0]["genres"] == ["hip-hop"]
    assert data[0]["followers"] == 500000


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
