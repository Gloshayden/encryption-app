from cryptography.fernet import Fernet, InvalidToken

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
    try:
        cipher_suite.decrypt(Original)
        return "not encrypted"
    except InvalidToken:
        pass
    with open(FileName,"wb") as f:
        f.write(encoded_file)
    return "encrypted"

def decryptFile(FileName):
    with open(FileName,"rb") as f:
        Encrypted = f.read()
    try:
        decoded_file = cipher_suite.decrypt(Encrypted)
    except InvalidToken:
        return "not decrypted"
    with open(FileName,"wb") as f:
        f.write(decoded_file)
    return "decrypted"
