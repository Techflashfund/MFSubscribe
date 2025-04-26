import os
import base64
import json
import nacl.public
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .cryptic_utils import decrypt


# Load from environment variables
SIGNED_UNIQUE_REQ_ID = os.environ.get("SIGNED_UNIQUE_REQ_ID")
ENCRYPTION_PRIVATE_KEY_BASE64 = os.environ.get("ENCRYPTION_PRIVATE_KEY")

# ONDC's Staging Public Key (constant)
ONDC_PUBLIC_KEY_BASE64 = "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="

def ondc_site_verification(request):
    return HttpResponse(f"""
    <html>
        <head>
            <meta name='ondc-site-verification' content='{SIGNED_UNIQUE_REQ_ID}' />
        </head>
        <body>
            ONDC Site Verification Page
        </body>
    </html>
    """, content_type="text/html")


@csrf_exempt
def on_subscribe(request):
    if request.method == "POST":
        data = json.loads(request.body)
        encrypted_challenge = data.get("challenge")

        # Load private key from env
        private_key = nacl.public.PrivateKey(base64.b64decode(ENCRYPTION_PRIVATE_KEY_BASE64))

        # Load ONDC's public key
        peer_public_key = nacl.public.PublicKey(base64.b64decode(ONDC_PUBLIC_KEY_BASE64))

        # Create shared key
        box = nacl.public.Box(private_key, peer_public_key)
        shared_key = box.shared_key()

        # Decrypt challenge
        decrypted_challenge = decrypt(encrypted_challenge, shared_key)

        return JsonResponse({"answer": decrypted_challenge})

    return JsonResponse({"error": "Invalid request"}, status=400)
