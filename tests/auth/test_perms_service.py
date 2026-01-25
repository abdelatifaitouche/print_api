import pytest
from unittest.mock import Mock, patch
from app.auth.permission_context import PermissionContext
from app.auth.role_perms_map import ROLE_PERMISSION
from app.enums.permissions import Permissions
from app.enums.roles import Roles


@pytest.fixture
def mock_admin():
    user = Mock()
    user.username = "abdelatif"
    user.email = "abdelatif.aitouche3@gmail.com"
    user.role = Roles.ADMIN

    return user


@pytest.fixture
def mock_user():
    user = Mock()
    user.username = "abdelatif"
    user.email = "abdelatif.aitouche3@gmail.com"
    user.role = Roles.USER
    return user


@pytest.fixture
def mock_client():
    user = Mock()
    user.username = "abdelatof"
    user.email = "abdelatif.aitouche3@gmail.com"
    user.role = Roles.CLIENT

    return user


class TestPermissionService:
    def test_admin_has_any_permissions(self, mock_admin):
        ctx: PermissionContext = PermissionContext(mock_admin)

        perms = ctx.has_any_permission(
            Permissions.CAN_READ_ALL, Permissions.CAN_CREATE_ALL
        )

        assert perms == True
