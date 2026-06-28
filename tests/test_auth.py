from app.auth import create_jwt, decode_jwt


def test_jwt_roundtrip():
    token = create_jwt("test_user_id")
    assert decode_jwt(token) == "test_user_id"


def test_decode_invalid_token():
    assert decode_jwt("invalid.token.here") is None


def test_decode_tampered_token():
    token = create_jwt("test_user_id")
    tampered = token[:-5] + "XXXXX"
    assert decode_jwt(tampered) is None
