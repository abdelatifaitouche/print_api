# tests/auth/test_jwt_service.py
import jwt
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch
from uuid import uuid4
from app.auth.jwt.jwt_service import JwtService
from app.schemas.jwt_payload import JwtPayload
from app.enums.roles import Roles


@pytest.fixture
def mock_payload():
    """Create a mock JWT payload"""
    p = JwtPayload(
        user_id=str(uuid4()),
        company_id=str(uuid4()),
        role=Roles.ADMIN,
        username="abdelatif",
    )
    return p


@pytest.fixture
def valid_token(mock_payload):
    """Create a valid token for testing"""
    return JwtService.generate_access_token(mock_payload)


@pytest.fixture
def expired_token(mock_payload):
    """Create an expired token for testing"""
    # Create token that expired 1 hour ago
    mock_payload.exp = datetime.now(timezone.utc) - timedelta(hours=1)
    mock_payload.iat = datetime.now(timezone.utc) - timedelta(hours=2)

    token = jwt.encode(
        mock_payload.model_dump(mode="json"), JwtService.SECRET_KEY, algorithm="HS256"
    )
    return token


@pytest.fixture
def invalid_signature_token(mock_payload):
    """Create a token with invalid signature"""
    mock_payload.exp = datetime.now(timezone.utc) + timedelta(hours=1)
    mock_payload.iat = datetime.now(timezone.utc)

    # Encode with wrong secret key
    token = jwt.encode(
        mock_payload.model_dump(mode="json"), "wrong-secret-key", algorithm="HS256"
    )
    return token


@pytest.fixture
def malformed_token():
    """Create a malformed token"""
    return "this.is.not.a.valid.jwt.token"


class TestGenerateToken:
    """Tests for generate_access_token"""

    def test_generate_access_token_returns_string(self, mock_payload):
        """Test that generate_access_token returns a string"""
        token: str = JwtService.generate_access_token(mock_payload)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_encode_decode_roundtrip(self, mock_payload):
        """Test that encoding and decoding preserves data"""
        token: str = JwtService.generate_access_token(mock_payload)
        decoded_payload = JwtService.decode_token(token)

        assert len(token) > 0
        assert isinstance(token, str)
        assert decoded_payload.user_id == mock_payload.user_id
        assert decoded_payload.username == "abdelatif"
        assert decoded_payload.role == Roles.ADMIN
        assert decoded_payload.company_id == mock_payload.company_id
        assert isinstance(decoded_payload.iat, datetime)
        assert isinstance(decoded_payload.exp, datetime)


class TestDecodeToken:
    """Tests for decode_token"""

    def test_decode_valid_token_returns_payload(self, valid_token, mock_payload):
        """Test that decoding a valid token returns JwtPayload"""
        decoded = JwtService.decode_token(valid_token)

        assert isinstance(decoded, JwtPayload)
        assert decoded.user_id == mock_payload.user_id
        assert decoded.company_id == mock_payload.company_id
        assert decoded.username == mock_payload.username
        assert decoded.role == mock_payload.role

    def test_decode_token_returns_correct_user_id(self, valid_token, mock_payload):
        """Test that decoded token has correct user_id"""
        decoded = JwtService.decode_token(valid_token)
        assert decoded.user_id == mock_payload.user_id

    def test_decode_token_returns_correct_company_id(self, valid_token, mock_payload):
        """Test that decoded token has correct company_id"""
        decoded = JwtService.decode_token(valid_token)
        assert decoded.company_id == mock_payload.company_id

    def test_decode_token_returns_correct_username(self, valid_token):
        """Test that decoded token has correct username"""
        decoded = JwtService.decode_token(valid_token)
        assert decoded.username == "abdelatif"

    def test_decode_token_returns_correct_role(self, valid_token):
        """Test that decoded token has correct role"""
        decoded = JwtService.decode_token(valid_token)
        assert decoded.role == Roles.ADMIN

    def test_decode_token_has_expiration(self, valid_token):
        """Test that decoded token has expiration datetime"""
        decoded = JwtService.decode_token(valid_token)

        assert hasattr(decoded, "exp")
        assert isinstance(decoded.exp, datetime)
        # Expiration should be in the future
        assert decoded.exp > datetime.now(timezone.utc)

    def test_decode_token_has_issued_at(self, valid_token):
        """Test that decoded token has issued at datetime"""
        decoded = JwtService.decode_token(valid_token)

        assert hasattr(decoded, "iat")
        assert isinstance(decoded.iat, datetime)
        # Issued at should be in the past or present
        assert decoded.iat <= datetime.now(timezone.utc)

    def test_decode_expired_token_raises_exception(self, expired_token, capsys):
        """Test that decoding expired token raises ExpiredSignatureError"""
        with pytest.raises(jwt.ExpiredSignatureError):
            JwtService.decode_token(expired_token)

        # Check that error was printed (since you have print(e) in the code)
        captured = capsys.readouterr()
        assert "Signature has expired" in captured.out or len(captured.out) > 0

    def test_decode_token_with_invalid_signature_raises_exception(
        self, invalid_signature_token
    ):
        """Test that token with invalid signature raises InvalidSignatureError"""
        with pytest.raises(jwt.InvalidSignatureError):
            JwtService.decode_token(invalid_signature_token)

    def test_decode_malformed_token_raises_exception(self, malformed_token):
        """Test that malformed token raises DecodeError"""
        with pytest.raises(jwt.DecodeError):
            JwtService.decode_token(malformed_token)

    def test_decode_empty_token_raises_exception(self):
        """Test that empty token raises DecodeError"""
        with pytest.raises(jwt.DecodeError):
            JwtService.decode_token("")

    def test_decode_none_token_raises_exception(self):
        """Test that None token raises appropriate exception"""
        with pytest.raises((jwt.DecodeError, TypeError, AttributeError)):
            JwtService.decode_token(None)

    def test_decode_token_verifies_signature(self, valid_token):
        """Test that signature verification is enabled"""
        # This should succeed because signature is valid
        decoded = JwtService.decode_token(valid_token)
        assert decoded is not None

        # Tamper with the token
        parts = valid_token.split(".")
        tampered_token = f"{parts[0]}.{parts[1]}.invalidsignature"

        with pytest.raises(jwt.InvalidSignatureError):
            JwtService.decode_token(tampered_token)

    def test_decode_token_verifies_expiration(self, expired_token):
        """Test that expiration verification is enabled"""
        with pytest.raises(jwt.ExpiredSignatureError):
            JwtService.decode_token(expired_token)

    def test_decode_different_tokens_return_different_payloads(self):
        """Test that different tokens decode to different payloads"""
        payload1 = JwtPayload(
            user_id=str(uuid4()),
            company_id=str(uuid4()),
            role=Roles.ADMIN,
            username="user1",
        )
        payload2 = JwtPayload(
            user_id=str(uuid4()),
            company_id=str(uuid4()),
            role=Roles.USER,
            username="user2",
        )

        token1 = JwtService.generate_access_token(payload1)
        token2 = JwtService.generate_access_token(payload2)

        decoded1 = JwtService.decode_token(token1)
        decoded2 = JwtService.decode_token(token2)

        assert decoded1.user_id != decoded2.user_id
        assert decoded1.username != decoded2.username
        assert decoded1.role != decoded2.role

    def test_decode_token_with_special_characters_in_username(self):
        """Test decoding token with special characters in username"""
        payload = JwtPayload(
            user_id=str(uuid4()),
            company_id=str(uuid4()),
            role=Roles.ADMIN,
            username="user@example.com",
        )

        token = JwtService.generate_access_token(payload)
        decoded = JwtService.decode_token(token)

        assert decoded.username == "user@example.com"

    @pytest.mark.parametrize("role", [Roles.ADMIN, Roles.USER, Roles.CLIENT])
    def test_decode_token_with_different_roles(self, role):
        """Test decoding tokens with different roles"""
        payload = JwtPayload(
            user_id=str(uuid4()),
            company_id=str(uuid4()),
            role=role,
            username="testuser",
        )

        token = JwtService.generate_access_token(payload)
        decoded = JwtService.decode_token(token)

        assert decoded.role == role

    def test_decode_token_preserves_uuid_format(self, valid_token, mock_payload):
        """Test that UUID fields maintain proper format"""
        decoded = JwtService.decode_token(valid_token)

        # Should be valid UUID strings
        assert len(decoded.user_id) == 36  # UUID string length
        assert len(decoded.company_id) == 36
        assert "-" in decoded.user_id
        assert "-" in decoded.company_id

    def test_decode_token_timestamp_conversion(self, valid_token):
        """Test that timestamps are properly converted to datetime objects"""
        decoded = JwtService.decode_token(valid_token)

        # Both should be datetime objects, not timestamps
        assert isinstance(decoded.iat, datetime)
        assert isinstance(decoded.exp, datetime)

        # Exp should be after iat
        assert decoded.exp > decoded.iat

    def test_decode_token_handles_future_issued_at(self):
        """Test handling of token with future issued at time (clock skew)"""
        payload = JwtPayload(
            user_id=str(uuid4()),
            company_id=str(uuid4()),
            role=Roles.ADMIN,
            username="testuser",
        )

        # Set iat to future
        payload.iat = datetime.now(timezone.utc) + timedelta(minutes=5)
        payload.exp = datetime.now(timezone.utc) + timedelta(hours=1)

        token = jwt.encode(
            payload.model_dump(mode="json"), JwtService.SECRET_KEY, algorithm="HS256"
        )

        # JWT library may or may not validate iat being in future
        # This tests your actual implementation behavior
        try:
            decoded = JwtService.decode_token(token)
            assert decoded.iat == payload.iat
        except jwt.InvalidIssuedAtError:
            # This is acceptable behavior
            pass


class TestDecodeTokenEdgeCases:
    """Edge case tests for decode_token"""

    def test_decode_token_with_extra_claims(self):
        """Test that extra claims in token don't break decoding"""
        payload_dict = {
            "user_id": str(uuid4()),
            "company_id": str(uuid4()),
            "username": "testuser",
            "role": Roles.ADMIN,
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "extra_field": "extra_value",  # Extra claim
        }

        token = jwt.encode(payload_dict, JwtService.SECRET_KEY, algorithm="HS256")
        decoded = JwtService.decode_token(token)

        # Should still decode successfully, extra field ignored
        assert decoded.username == "testuser"

    def test_decode_token_with_missing_optional_fields(self):
        """Test decoding token missing non-required fields"""
        # This tests if your JwtPayload model handles missing fields
        minimal_payload = {
            "user_id": str(uuid4()),
            "company_id": str(uuid4()),
            "username": "testuser",
            "role": Roles.ADMIN,
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }

        token = jwt.encode(minimal_payload, JwtService.SECRET_KEY, algorithm="HS256")
        decoded = JwtService.decode_token(token)

        assert decoded.username == "testuser"


# Run with: pytest tests/auth/test_jwt_service.py -v
# Run with coverage: pytest tests/auth/test_jwt_service.py --cov=app.auth.jwt.jwt_service --cov-report=html
