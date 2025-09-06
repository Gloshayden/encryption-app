import os, encryption, json, hashlib
import FreeSimpleGUI as sg
from cryptography.fernet import Fernet, InvalidToken

def askForPassword(password) -> bool:
    layout = [  [sg.Text("Please enter your password")],
                [sg.InputText()],
                [sg.Button('Confirm')] ]
    window = sg.Window('conform password', layout)
    event, values = window.read()
    prehash = values[0]
    window.close()
    hashedpass = hashlib.sha256(prehash.encode()).hexdigest()
    if hashedpass == password:
        return True
    else:
        return False

def main():
    if not os.path.exists("files"): os.mkdir("files")
    if not os.path.exists("settings.json"):
        layout = [  [sg.Text("please enter in a password")],
                    [sg.Text("(this will be used to decrypt files)")],
                    [sg.InputText()],
                    [sg.Button('Confirm')] ]
        window = sg.Window('Make Password', layout)
        event, values = window.read()
        password = values[0]
        window.close()
        settings = {"password":hashlib.sha256(password.encode()).hexdigest()}
        with open("settings.json","w") as file:
            json.dump(settings, file)
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key","wb") as f:
            f.write(key)

    with open("key.key","rb") as f:
        keyinfo = f.read()
    encryption.initdecryption(keyinfo)

    with open("settings.json","r") as f:
        settings = json.load(f)
    password = settings["password"]

    folder = "files"
    files = os.listdir("files")
    while True:
        layout = [  [sg.Text('Folder'), sg.In(size=(30,1), default_text=folder, focus=False, enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
                    [sg.Text("Please select the file you want to encrypt or decrypt")],
                    [sg.Listbox(values=files, size=(50,20), select_mode="LISTBOX_SELECT_MODE_SINGLE", bind_return_key=True)],
                    [sg.Button("Regenerate Key", key="key"),sg.Button("Refresh"),sg.Button("Exit")]]
        window = sg.Window('Please pick a file', layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            break

        elif event == "Refresh":
            window.close()
            continue

        elif event == "-FOLDER-":
            window.close()
            folder = values['-FOLDER-']
            try:
                files = os.listdir(folder) 
                for file in files:
                    if os.path.isdir(f"{folder}/{file}"):
                        files.remove(file)
            except FileNotFoundError:
                sg.popup("The folder Does not exist please try again")
                continue

        elif event == "key":
            window.close()
            layout = [  [sg.Text("Are you sure you want to regenerate the key?")],
                        [sg.Button("Yes"),sg.Button("No")]]
            window = sg.Window('regenerate key?', layout)
            event, values = window.read()
            if event == "Yes":
                window.close()
                PassCheck = askForPassword(password)
                if PassCheck == True:
                    os.remove("key.key")
                    key = Fernet.generate_key()
                    with open("key.key","wb") as f:
                        f.write(key)
                    with open("key.key","rb") as f:
                        keyinfo = f.read()
                        encryption.initdecryption(keyinfo)
                else:
                    sg.popup("Incorrect password")
            else:
                window.close()
                continue
            key = Fernet.generate_key()
            with open("key.key","wb") as f:
                f.write(key)
            with open("key.key","rb") as f:
                keyinfo = f.read()
                encryption.initdecryption(keyinfo)

        elif values != {0: []}:
            window.close()
            file = values[0][0]
            folder = values["-FOLDER-"]
            FileName, FileExt = os.path.splitext(file)
            FileExt = FileExt.lower()
            if FileExt == ".png" or FileExt == ".gif":
                if encryption.checkIfEncrypted(f"{folder}/{file}"):
                    layout = [  [sg.Text("What do you want to do with this file?")],
                                [sg.Text("File: " + file)],
                                [sg.Button("Encrypt"),sg.Button("Decrypt"),sg.Button("Back")]]
                else:
                    layout = [  [sg.Text("What do you want to do with this file?")],
                                [sg.Text("File: " + file)],
                                [sg.Image(f"{folder}/{file}")],
                                [sg.Button("Encrypt"),sg.Button("Decrypt"),sg.Button("Back")]]
            elif FileExt == ".txt":
                if encryption.checkIfEncrypted(f"{folder}/{file}"):
                    layout = [  [sg.Text("What do you want to do with this file?")],
                                [sg.Text("File: " + file)],
                                [sg.Button("Encrypt"),sg.Button("Decrypt"),sg.Button("Back")]]
                else:
                    layout = [  [sg.Text("What do you want to do with this file?")],
                                [sg.Text("File: " + file)],
                                [sg.Multiline(default_text=open(f"{folder}/{file}","r").read(), size=(30,5), disabled=True)],
                                [sg.Button("Encrypt"),sg.Button("Decrypt"),sg.Button("Back")]]
            else:
                layout = [  [sg.Text("What do you want to do with this file?")],
                            [sg.Text("File: " + file)],
                            [sg.Button("Encrypt"),sg.Button("Decrypt"), sg.Button("Back")]]
            window = sg.Window('Please pick an option', layout)
            event, values = window.read()
            window.close()
            if event == "Encrypt":
                result = encryption.encryptFile(f"{folder}/{file}")
                if result == "encrypted":
                    sg.popup("File encrypted")
                else:
                    sg.popup("File already encrypted")
            elif event == "Decrypt":
                PassCheck = askForPassword(password)
                if PassCheck == True:
                    result = encryption.decryptFile(f"{folder}/{file}")
                    if result == "decrypted":
                        sg.popup("File decrypted")
                    else:
                        sg.popup("File already decrypted")
                else:
                    sg.popup("Incorrect password")
                continue


if __name__ == "__main__":
    main()