from cryptography.fernet import Fernet

if __name__ == "__main__":
    print("This is a library \nPlease import it and not run it")

def initdecryption(KeyInfo):
    key = KeyInfo
    global cipher_suite
    cipher_suite = Fernet(key)

def encryptFile(FileName):
    with open(FileName,"rb") as f:
        Original = f.read()
    encoded_file = cipher_suite.encrypt(Original)
    with open(FileName,"wb") as f:
        f.write(encoded_file)
    return encoded_file

def decryptFile(FileName):
    with open(FileName,"rb") as f:
        Encrypted = f.read()
    decoded_file = cipher_suite.decrypt(Encrypted)
    with open(FileName,"wb") as f:
        f.write(decoded_file)
    return decoded_file
