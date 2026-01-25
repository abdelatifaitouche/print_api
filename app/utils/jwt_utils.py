import hashlib
import json
import base64
import hmac
from datetime import datetime, timedelta
from .payload_builder import JwtPayloadFactory
from dotenv import load_dotenv
import os

load_dotenv()


class JwtManager:
    def __init__(self):
        self.__secret_key = os.getenv("SECRET_KEY")  # needs to be loaded from env
        self.algo = "sha256"
        self.__access_exp = 36000  # needs to be loaded from env
        self.__refresh_exp = 5000000  # needs to be loaded from env
        self.__payload_factory = JwtPayloadFactory()

    def __base_64_encoding(self, data: dict) -> str:
        """
        takes a dict , turn's it into a json string and them convert it to bytes
        encode these bytes in base64urlsafe , turns it into a string and remove any padding


        the return type is an ascii to

        """
        dbytes = json.dumps(data).encode("utf-8")
        encoded_data = base64.urlsafe_b64encode(dbytes)

        encoded = encoded_data.decode("ascii").rstrip("=")

        return encoded

    def __base_64_decoding(self, data: str) -> dict:
        """
        takes a bytes string from the token,
        addes the correct padding since base64 expects the data to be
        a multiple of 4 otherwise it adds a padding (=)
        """
        padding = (4 - len(data) % 4) % 4
        data += "=" * padding
        decoded = json.loads(base64.urlsafe_b64decode(data).decode("utf-8"))
        return decoded

    def __generate_signature(self, encoded_header: str, encoded_payload: str) -> str:
        """
        takes the encoded header and payload strings(ascii chars) ,
        convert's them into bytes

        using the hmac library we generate the signature with sha256 from the hashlib.sha256()

        returns the string value in base64 url safe

        """

        message: str = f"{encoded_header}.{encoded_payload}".encode("ascii")
        signature_raw_bytes = hmac.new(
            message, self.__secret_key.encode("ascii"), hashlib.sha256
        ).digest()

        url_safe_signature = (
            base64.urlsafe_b64encode(signature_raw_bytes).decode("ascii").rstrip("=")
        )
        return url_safe_signature

    def generate_token(self, user_data: dict, is_refresh: bool = False) -> str:
        """
        Generate a jwt token based on the provided data
        needs to be more dynamic (use a builder next)
        for now, it needs the username , role and email in the payload

        and the is_refresh flag to generate the refresh token
        """

        header: dict = {"alg": "sha256", "typ": "JWT"}
        if is_refresh:
            payload: dict = self.__payload_factory.refresh_token_payload(
                user_data["username"], user_data["email"], user_data["role"]
            )
        else:
            payload: dict = self.__payload_factory.access_token_payload(
                user_data["id"],
                user_data["username"],
                user_data["email"],
                user_data["role"],
                user_data["company_id"],
            )

        encoded_header = self.__base_64_encoding(header)
        encoded_payload = self.__base_64_encoding(payload)
        signature = self.__generate_signature(encoded_header, encoded_payload)

        token = f"{encoded_header}.{encoded_payload}.{signature}"

        return token

    def verify_token(self, token: str):
        """
        recalculate the signature with our private key
         - header.payload.signature
            deconstruct each part
                use the generate signature and compare it to the sent signature
        """
        header, payload, signature = token.split(".")

        recalculated_signature = self.__generate_signature(header, payload)

        if signature != recalculated_signature:
            return False

        decoded_payload = self.__base_64_decoding(payload)

        current_time = int(datetime.utcnow().timestamp())

        if decoded_payload["exp"] < current_time:
            print("expired token")
            return False

        return True

    def get_user_from_token(self, token: str) -> dict:
        header, payload, signature = token.split(".")

        decoded_payload = self.__base_64_decoding(payload)

        return decoded_payload
