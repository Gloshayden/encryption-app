import os, encryption, json, hashlib
import FreeSimpleGUI as sg
from cryptography.fernet import Fernet

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
    while app := True:
        files = os.listdir("files")
        layout = [  [sg.Text("Please select the file you want to encrypt or decrypt")],
                    [sg.Listbox(values=files, size=(50,20), select_mode="LISTBOX_SELECT_MODE_SINGLE", bind_return_key=True)],
                    [sg.Button("Regenerate Key", key="key"), sg.Button("Exit")]]
        window = sg.Window('Please pick a file', layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            break


if __name__ == "__main__":
    main()