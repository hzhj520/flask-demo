from keycloak import KeycloakOpenID
import json
import jwt
from itsdangerous import TimedSerializer as Serializer

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://10.100.192.46:8080/auth/",
                                 realm_name="keycloak-demo",
                                 client_id="app-vue",
                                 client_secret_key="fd4bf17c-3af5-41e9-8805-87bfb2a7ebec")

# Get WellKnow
config_well_know = keycloak_openid.well_know()

# Get Token
token = keycloak_openid.token("editor", "user")
# print(token)
# token = keycloak_openid.token("user", "password", totp="012345")

# # Get Userinfo
# userinfo = keycloak_openid.userinfo(token['access_token'])

# print("userinfo---------->", json.dumps(userinfo,
#       sort_keys=True, indent=4, separators=(',', ':')))


token_info = keycloak_openid.introspect(token['access_token'])

print("token_info---------->", json.dumps(token_info,
      sort_keys=True, indent=4, separators=(',', ':')))



def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = "fd4bf17c-3af5-41e9-8805-87bfb2a7ebec"

    encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    print(token["access_token"])

    payload = jwt.decode(token["access_token"], secret, algorithms=['RS256'])
    # payload = Serializer.loads(token)


    return payload

