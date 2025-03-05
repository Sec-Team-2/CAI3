## Consulta 1
Para la consulta 1 se ha implementado un sistema de gestión de claves criptográficas utilizando vault. Para configurar el entorno es necesario llevar a cabo los siguientes comandos.

### Configurar entorno virtual de python (recomendable)
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Instalar vault
```bash
sudo apt update
sudo apt upgrade
sudo apt install vault
```

En este punto también será necesario detener el servicio de vault en caso de haberse iniciado automáticamente.
```bash
sudo systemctl stop vault
```

### Crear directorios para almacenar los datos de vault
```bash
sudo mkdir -p /vault/data
sudo chown -R $(whoami):$(whoami) /vault/data
chmod 750 /vault/data
```

### Generar certificado CA para vault
Al ejecutar el segundo comando se solicitará que se introduzcan algunos datos. Se recomienda que se ponga la misma palabra qu se solicite. Ej: en el campo ES[] introducir ES.
```bash
cd Consulta1/certificados
openssl req -x509 -newkey rsa:4096 -keyout vault-server.key -out vault-server.crt -days 365 -nodes -config ../openssl.cnf
```

### Añadir certificados al registro de certificados autorizados en el sistema operativo
```bash
sudo cp vault-server.crt /usr/local/share/ca-certificates/vault-server.crt
sudo update-ca-certificates
```

### Iniciar vault
En una nueva terminal puesto que se dejará el proceso ejecutando (también se puede ejecutar en segundo plano)
```bash
cd Consulta1
vault server -config=config.hcl
```

### Inicializar vault
Desde la misma terminal del principio (o una nueva)
```bash
cd Consulta1
export VAULT_ADDR='https://127.0.0.1:8200'
vault operator init
```
Tras este comando ya se habrá inicializado vault, se mostrarán 5 claves y un token. Es importante guardar estas claves y el token en un lugar seguro. No obstante, vault estará sellado y habrá que desbloquearlo utilizando el siguiente comando 3 veces, cada una de ellas con una de las 5 claves generadas en el comando anterior (no importa cuales ni el orden).
```bash
vault operator unseal
```

### Iniciar sesión en vault
```bash
vault login <token_generado en el comando de init>
```

### Generar y almacenar la clave
```bash
vault secrets enable kv
python generate_key.py
```
El comando generate_key.py generará una clave criptográfica aleatoria y se mostrará por consola.
```bash
vault kv put kv/dicom key="clave_generada"
```

### Configurar uso de certificados de los clientes
```bash
cd certificados
vault auth enable cert
```
Generar un certificado para el servidor
```bash
openssl req -x509 -newkey rsa:4096 -keyout ca-key.pem -out ca-cert.pem -days 365 -nodes -subj "/CN=Vault CA"
```
Generar un certificado para el cliente
```bash
openssl req -newkey rsa:4096 -keyout client-key.pem -out client-req.pem -nodes -subj "/CN=vault-client"
openssl x509 -req -in client-req.pem -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -days 365
```
Configurar vault para que utilice el certificado de la CA
```bash
vault write auth/cert/config \
    certificate=@ca-cert.pem \
    allowed_common_names="vault-client"
```
Configurar una política de acceso
```bash
vault policy write read-secrets - <<EOF
path "kv/*" {
  capabilities = ["create", "update", "read", "list"]
}
EOF
```
Configurar vault para que utilice los certificados del cliente
```bash
vault write auth/cert/certs/all-clients \
    display_name="all-clients" \
    certificate=@ca-cert.pem \
    policies="read-secrets"
```

### Consultar la clave almacenada
```bash
cd Consulta1
python consulta1.py
```
