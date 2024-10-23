from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def encrypt_message(message, key):
    # Create a new AES cipher
    key = hashlib.sha256(key.encode()).digest()  # Ensure key length is 32 bytes
    cipher = AES.new(key, AES.MODE_ECB)
    # Encrypt the message with padding
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    # Convert to base64 to make it easier to embed in an image
    return base64.b64encode(encrypted).decode()

def decrypt_message(encrypted_message, key):
    # Decode the base64 string
    encrypted_message = base64.b64decode(encrypted_message)
    # Create a new AES cipher
    key = hashlib.sha256(key.encode()).digest()  # Ensure key length is 32 bytes
    cipher = AES.new(key, AES.MODE_ECB)
    # Decrypt and unpad the message
    decrypted = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted.decode()

def encode_image(image_path, message, output_path, key):
    # Encrypt the message
    encrypted_message = encrypt_message(message, key)
    # Open the image
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    index = 0

    # Convert the message to a binary string
    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message)

    if len(binary_message) > width * height:
        raise ValueError("Message is too long to hide in this image.")

    # Hide the message in the least significant bits of the image
    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                pixel = list(img.getpixel((col, row)))
                # Change the LSB of the red channel
                pixel[0] = pixel[0] & ~1 | int(binary_message[index])
                encoded.putpixel((col, row), tuple(pixel))
                index += 1
            else:
                break

    # Ensure the output path has a valid extension, default to .png if none
    if not output_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        output_path += ".png"

    # Save the encoded image
    encoded.save(output_path)
    print(f"Message encoded and saved to {output_path}")

def decode_image(image_path, key):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    binary_message = ''
    
    # Extract the binary message from the image's LSBs
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            # Extract the LSB of the red channel
            binary_message += str(pixel[0] & 1)
    
    # Convert the binary message to a string
    byte_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join([chr(int(byte, 2)) for byte in byte_message if int(byte, 2) != 0])
    
    try:
        # Decrypt the message
        decrypted_message = decrypt_message(decoded_message, key)
        return decrypted_message
    except Exception as e:
        return f"Failed to decrypt message: {str(e)}"

if __name__ == "__main__":
    choice = input("Enter 'e' to encode a message or 'd' to decode a message: ").lower()
    if choice == 'e':
        image_path = input("Enter the path of the image: ")
        message = input("Enter the message to hide: ")
        output_path = input("Enter the output image path: ")
        key = input("Enter the encryption key: ")
        encode_image(image_path, message, output_path, key)
    elif choice == 'd':
        image_path = input("Enter the path of the encoded image: ")
        key = input("Enter the decryption key: ")
        hidden_message = decode_image(image_path, key)
        print(f"Hidden Message: {hidden_message}")
    else:
        print("Invalid option. Please run the script again.")
