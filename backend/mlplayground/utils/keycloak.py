from keycloak import KeycloakOpenID
from jose import jwt
import requests


class InvalidToken(Exception):
    ...


class Keycloak:
    def __init__(self, **kwargs):
        self.server_url = kwargs["server_url"]
        self.realm_name = kwargs["realm_name"]
        self.client_id = kwargs["client_id"]
        self.client_secret_key = kwargs.get("client_secret_key")
        self._kc = KeycloakOpenID(**kwargs)
        self.public_key = self.__build_public_key()

    def __build_public_key(self):
        return "-----BEGIN PUBLIC KEY-----\n" + self._kc.public_key() + "\n-----END PUBLIC KEY-----"

    def validate_audience(self, token):
        claims = jwt.get_unverified_claims(token)
        if claims.get("aud") != self.client_id:
            raise InvalidToken

    def validate_authorized_party(self, token, client_id):
        claims = jwt.get_unverified_claims(token)
        if claims.get("azp") != client_id:
            raise InvalidToken

    def decode_token(self, token):
        options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
        return self._kc.decode_token(token, key=self.public_key, options=options)

    def exchange_token(self, subject_token, target_aud):
        return self._kc.exchange_token(subject_token, target_aud)

    def issue_token(self, username, password, totp=None):
        return self._kc.token(username, password, totp=totp)

    def user_info(self, token):
        return self._kc.userinfo(token)

    def issue_api_token(self):
        response = requests.post(
            f"{self.server_url}realms/{self.realm_name}/api-access/token",
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret_key,
                'audience': self.client_id,
            }
        )
        return response.json()
