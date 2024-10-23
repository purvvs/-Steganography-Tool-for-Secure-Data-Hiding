Steganography Tool for Secure Data Hiding

Description
This Steganography Tool allows users to securely hide encrypted messages inside images using Least Significant Bit (LSB) manipulation. The tool can both encrypt and decrypt hidden messages, ensuring that data remains secure. This project demonstrates fundamental concepts in cryptography, image processing, and data security.

Features
- **Encryption**: Uses AES encryption to secure messages before embedding them in images.
- **Steganography**: Embeds encrypted messages into the least significant bits of an image's pixels.
- **Decryption**: Extracts and decrypts the hidden message from an image.
- **Supports Multiple Image Formats**: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`

 Prerequisites
Before running the project, ensure you have the following installed:
- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Pillow**: Python Imaging Library for handling image processing.
- **PyCryptodome**: Cryptography library for encrypting and decrypting messages.



example:
encryption:
Enter 'e' to encode a message or 'd' to decode a message: e
Enter the path of the image: input_image.png
Enter the message to hide: Secret Message
Enter the output image path: encoded_image.png
Enter the encryption key: mysecurekey


decryption:
Enter 'e' to encode a message or 'd' to decode a message: d
Enter the path of the encoded image: encoded_image.png
Enter the decryption key: mysecurekey

