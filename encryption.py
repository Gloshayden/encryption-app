from cryptography.fernet import Fernet, InvalidToken

if __name__ == "__main__":
    print("This is a library \nPlease import it and not run it")

def initdecryption(KeyInfo):
    key = KeyInfo
    global cipher_suite
    cipher_suite = Fernet(key)

def checkIfEncrypted(FileName):
    with open(FileName,"rb") as f:
        file = f.read()
    try:
        cipher_suite.decrypt(file)
        return True
    except InvalidToken:
        return False

def encryptFile(FileName):
    with open(FileName,"rb") as f:
        Original = f.read()
    encoded_file = cipher_suite.encrypt(Original)
    if checkIfEncrypted(FileName):
        return "already encrypted"
    with open(FileName,"wb") as f:
        f.write(encoded_file)
    return "encrypted"

def decryptFile(FileName):
    with open(FileName,"rb") as f:
        Encrypted = f.read()
    if not checkIfEncrypted(FileName):
        return "encrypted"
    decoded_file = cipher_suite.decrypt(Encrypted)
    with open(FileName,"wb") as f:
        f.write(decoded_file)
    return "decrypted"
