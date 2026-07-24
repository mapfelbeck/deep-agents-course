"""Dependencies: the auth seam and shared request-scoped helpers.

Today this is a single fixed user. To enable SSO later, replace
``get_current_user`` with an OIDC/SAML validator that reads the request's
``Authorization`` header or session cookie and returns a real ``User``. No schema
or query changes are required — every row is already stamped with ``user_id``.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str


def get_current_user() -> User:
    """Return the current user. Single fixed user until SSO lands."""
    return User(id="default")
