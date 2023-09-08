import ldap
from ldap.ldapobject import SimpleLDAPObject
from loguru import logger
from logic.auth.abscract import Authenticator
from logic.utils.decorators import logging
from settings import LDAP_SERVER, LDAP_DOMAIN


class LDAPConnection:
    def __init__(self, server: str):
        self._server = server
        self._connection = None

    def __enter__(self):
        self._connection = ldap.initialize(self._server)
        logger.error(self._server)
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.unbind_s()
        self._connection = None


class LDAPAuthenticator(Authenticator):
    def __init__(self, connection: SimpleLDAPObject, username: str, password: str):
        self._connection = connection
        self._username = username
        self._password = password

    def authenticate(self) -> dict:
        try:
            self.normalize_username()
            self._connection.simple_bind_s(self._username, self._password)
            return {
                'is_auth': True
            }
        except ldap.INVALID_CREDENTIALS:
            return {
                'is_auth': False,
                'error': 'Invalid username or password'
            }
        except ldap.LDAPError as error:
            return {
                'is_auth': False,
                'error': str(error)
            }

    def normalize_username(self):
        split_username = self._username.split(',')
        if not len(split_username) >= 3:
            domain, dc = LDAP_DOMAIN.split('.')
            self._username = f"cn={self._username},dc={domain},dc={dc}"
@logging
def authenticate_ldap(username: str, password: str) -> dict:
    with LDAPConnection(LDAP_SERVER) as ldap_connection:
        authenticator = LDAPAuthenticator(ldap_connection, username, password)
        return authenticator.authenticate()
