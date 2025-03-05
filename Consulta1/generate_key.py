import secrets
import base64 

clave = secrets.token_bytes(32)

clave_base64 = base64.b64encode(clave).decode('utf-8')

print(clave_base64)