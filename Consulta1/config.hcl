listener "tcp" {
  address = "0.0.0.0:8200"
  tls_cert_file = "certificados/vault-server.crt"
  tls_key_file = "certificados/vault-server.key"
}
storage "file" {
  path = "/vault/data"
}

disable_mlock = true
