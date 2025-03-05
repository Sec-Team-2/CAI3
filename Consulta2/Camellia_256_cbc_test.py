import os
import time
import hashlib
import camellia
from Crypto.Util.Padding import pad, unpad

def get_images(folder):
    return sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".dcm")])

def hash_image(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

def encrypt_image(image_path, key, iv):
    with open(image_path, 'rb') as f:
        data = f.read()

    cipher = camellia.CamelliaCipher(key=key, IV=iv, mode=camellia.MODE_CBC)
    padded_data = pad(data, camellia.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def decrypt_image(encrypted_data, key, iv):
    cipher = camellia.CamelliaCipher(key=key, IV=iv, mode=camellia.MODE_CBC)
    decrypted_padded_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_padded_data, camellia.block_size)

def process_folder(folder, key, iv):
    images = get_images(folder)
    encryption_times, decryption_times = [], []
    altered_hashes = 0
    total_images = len(images)

    for image in images:
        original_hash = hash_image(image)

        start_enc = time.time()
        encrypted_data = encrypt_image(image, key, iv)
        end_enc = time.time()

        start_dec = time.time()
        decrypted_data = decrypt_image(encrypted_data, key, iv)
        end_dec = time.time()

        encryption_times.append(end_enc - start_enc)
        decryption_times.append(end_dec - start_dec)

        new_hash = hashlib.sha256(decrypted_data).hexdigest()
        if new_hash != original_hash:
            altered_hashes += 1

    avg_enc_time = sum(encryption_times) / total_images if total_images else 0
    avg_dec_time = sum(decryption_times) / total_images if total_images else 0
    altered_percentage = (altered_hashes / total_images) * 100 if total_images else 0

    print(f"Folder: {folder}")
    print(f"  Avg Encryption Time: {avg_enc_time:.6f} sec")
    print(f"  Avg Decryption Time: {avg_dec_time:.6f} sec")
    print(f"  Altered Hash Percentage: {altered_percentage:.2f}%\n")

def main():
    ruta1 = "./images/500/"
    ruta2 = "./images/1000/"
    key = b'32_byte_key_for_camellia_256!!!'  # Clave de 32 bytes (256 bits)
    iv = b'16_byte_iv_for_cbc!'  # IV de 16 bytes

    print("Processing Folder 1:")
    process_folder(ruta1, key, iv)
    print("Processing Folder 2:")
    process_folder(ruta2, key, iv)

if __name__ == "__main__":
    main()
