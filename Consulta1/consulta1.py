import hvac

# Configurar la URL de Vault
VAULT_ADDR = "https://127.0.0.1:8200"

# Rutas de los certificados del cliente
CLIENT_CERT = "certificados/client-cert.pem"
CLIENT_KEY = "certificados/client-key.pem"

# Crear cliente de Vault
client = hvac.Client(url=VAULT_ADDR, verify=False, cert=(CLIENT_CERT, CLIENT_KEY))

# Verificar si la autenticación fue exitosa
if client.is_authenticated():
    print("Autenticación exitosa")
else:
    print("Error en la autenticación")
    exit(1)

# Obtener la clave almacenada en Vault
secret_path = "dicom"
response = client.secrets.kv.v1.read_secret(path=secret_path, mount_point="kv")

# Extraer el valor de la clave
encryption_key = response['data']['key']
print(f"Clave obtenida: {encryption_key}")
