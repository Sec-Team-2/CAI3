import os
import time
import hashlib
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

def get_images(folder):
    return sorted([os.path.join(folder, f) for f in os.listdir(folder) if (f.endswith(".DCM") or f.endswith(".dcm"))])

def hash_image(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

def encrypt_image(image_path, key):
    with open(image_path, 'rb') as f:
        data = f.read()
    
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(data)
    return cipher.nonce + ciphertext  

def decrypt_image(encrypted_data, key):
    nonce = encrypted_data[:8]  
    ciphertext = encrypted_data[8:]
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ciphertext)

def process_folder(folder, key):
    images = get_images(folder)
    encryption_times, decryption_times = [], []
    altered_hashes = 0
    total_images = len(images)
    
    for image in images:
        original_hash = hash_image(image)
        
        start_enc = time.time()
        encrypted_data = encrypt_image(image, key)
        end_enc = time.time()
        
        start_dec = time.time()
        decrypted_data = decrypt_image(encrypted_data, key)
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
    print(f"  Avg Encryption Time: {avg_enc_time:.6f} sec"  )
    print(f"  Avg Decryption Time: {avg_dec_time:.6f} sec")
    print(f"  Altered Hash Percentage: {altered_percentage:.2f}%\n")

def main():
    ruta1 = "./images/500/"  
    ruta2 = "./images/1000/"  
    key = get_random_bytes(32)  
    
    print("Processing Folder 1:")
    process_folder(ruta1, key)
    print("Processing Folder 2:")
    process_folder(ruta2, key)

if __name__ == "__main__":
    main()
