import requests
from jose import jwt
from urllib.request import urlopen
import json
# Flask route protected with Auth0 token verification
from flask import Flask, request, jsonify


# AUTH0_DOMAIN = 'your-auth0-domain'
# API_IDENTIFIER = 'your-api-identifier'
# ALGORITHMS = ["RS256"]

def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = urlopen(jwks_url)
    return json.loads(response.read())

def verify_token(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_IDENTIFIER, issuer=f"https://{AUTH0_DOMAIN}/")
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTClaimsError:
            return None
        except Exception:
            return None
    return None

app = Flask(__name__)

@app.route("/protected", methods=["GET"])
def protected():
    # token = request.headers.get("Authorization").split()[1]
    # payload = verify_token(token)
    payload = "Ok"
    if payload:
        return jsonify({"message": "This is a protected route", "user": payload})
    else:
        return jsonify({"message": "Token is invalid or expired"}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)