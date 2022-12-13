import json
from base64 import urlsafe_b64decode, urlsafe_b64encode

from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15


class WePayClearSignatureVerifier:
    """The following implementation comes from the official WePay Clear documentation
    for handling their signature verification.

    https://dev.wepay.com/api/guides/notification-signatures/#python-example

    We modified some of this logic from the original to accommodate our own integration.
    """

    def __init__(self, pubkey: str):
        # Obtain and insert the WePay public key.
        self.public_key = RSA.import_key(pubkey)

    @staticmethod
    def base64url_decode(payload):
        payload_length = len(payload) % 4
        if payload_length == 2:
            payload += "=="
        elif payload_length == 3:
            payload += "="
        elif payload_length != 0:
            raise ValueError("Invalid base64 string")
        return urlsafe_b64decode(payload.encode("utf-8"))

    @staticmethod
    def base64_decode(data: str) -> str:
        return str(WePayClearSignatureVerifier.base64url_decode(data), "utf-8", "ignore")

    @staticmethod
    def base64_encode(payload: str) -> str:
        if not isinstance(payload, bytes):
            payload = payload.encode("utf-8")
        encode = urlsafe_b64encode(payload)
        return encode.decode("utf-8").rstrip("=")

    def __verify_single_signature(self, payload, sig):
        data = SHA256.new(payload.encode("utf-8"))
        try:
            pkcs1_15.new(self.public_key).verify(data, sig)
            return True
        except Exception as e:
            print(e)
            return False

    def verify_signatures(self, request_body, wepay_signature):
        try:
            # Read "wepay-signature" in the HTTP request header and Base64 decode it.
            decoded_wepay_signature = WePayClearSignatureVerifier.base64_decode(
                wepay_signature)

            # Read the request body as a string and Base64 encode it.
            base64_request_body = WePayClearSignatureVerifier.base64_encode(
                request_body)

            # Parse "wepay-signature" as a JSON array and read the elements in it.
            sig_json_array = json.loads(decoded_wepay_signature)
            for sig in sig_json_array:
                protected = sig["protected"]
                signature = sig["signature"]

                # Base64 decode the signature value.
                decoded_signature = WePayClearSignatureVerifier.base64url_decode(
                    signature)

                # Concat protected + "." + request body to get the payload.
                payload = protected + "." + base64_request_body

                # Call RSA to verify the function.
                verified = self.__verify_single_signature(
                    payload, decoded_signature)
                if verified:
                    return True
            print("Either signature or payload have invalid format")
            return False
        except Exception:
            print("WePay Clear Notification signature could not be validated")
            return False
