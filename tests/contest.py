# tests/conftest.py
import sys
from pathlib import Path
import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now you can import from app
from app.auth.jwt.jwt_service import JwtService


@pytest.fixture(autouse=True)
def setup_jwt_service():
    """Configure JWTService for testing"""
    JwtService.SECRET_KEY = "test-secret-key"
    JwtService.ACCESS_TOKEN_EXPIRE = 1
    yield
