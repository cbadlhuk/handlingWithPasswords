from cryptography.fernet import Fernet
import os
import tkinter
from tkinter.filedialog import askopenfilename


def generateKey(filePath):
    try:
        key = Fernet.generate_key()
        file = open(filePath, 'wb')
        file.write(key)
        return True
    except:
        print("An error occurred during generateKey function")
        return False
    finally:
        file.close()


def readKey():
    try:
        key_path = os.path.dirname(os.path.realpath(__file__))
        key_path = key_path + "\mykey.key"
        file = open(key_path, 'rb')
        key = file.read()
        return key
    except:
        print("An error occurred during readKey function")
        return ""
    finally:
        file.close()


def encryptFile(fileToEncryptPath, fileEncryptedPath):
    try:
        auth = Fernet(readKey())

        try:
            file = open(fileToEncryptPath, 'rt')
            file_content = file.read()
        finally:
            file.close()

        text = auth.encrypt(file_content.encode('utf-8'))
        file = open(fileEncryptedPath, 'wb')
        file.write(text)
        return True
    except:
        print("An error occurred during encryptFile function")
        return False
    finally:
        file.close()


def decryptFile(filePath, option):
    try:
        auth = Fernet(readKey())
        file = open(filePath, 'rb')
        file_text = file.read()
        text = auth.decrypt(file_text)
        text = text.decode('utf-8')

        if text != "":
            if option == "script":
                return text
            else:
                x = 0
                while x < 10:
                    option = (input("Do you want to [S]ave the result to a file or [P]rint? [S] or [P]")).upper()
                    if option == "S":
                        try:
                            new_filePath = filePath[0:filePath.find("_encrypted.txt")] + "_decrypted.txt"
                            file = open(new_filePath, 'wt')
                            file.write(text)
                        finally:
                            file.close()
                    elif option == "P":
                        print(text)
                    else:
                        print("This option is not valid, please try again!")
                    break
                return True
    except:
        print("An error occurred during decryptFile function")
        return False
    finally:
        file.close()


def addGroup(filePath):
    try:
        section = input("Type the group name: ")
        section = "[" + section + "]"

        user = input("Type the username: ")
        user = "user=" + user

        password = input("Type the password: ")
        password = "password=" + password

        file_content = decryptFile(filePath, "script")
        content = section + '\n' + user + '\n' + password + "\n" + file_content

        try:
            temporary_filePath = filePath[0:filePath.find("_encrypted.txt")] + "_tempFile.txt"
            file = open(temporary_filePath, 'wt')
            file.write(content)
        finally:
            file.close()

        if encryptFile(temporary_filePath, filePath):
            os.remove(temporary_filePath)
            return True
    except:
        print("An error occurred during addGroup function")
        return False


def deleteGroup(filePath):
    try:
        file_content = decryptFile(filePath, "script")
        try:
            temporary_filePath = filePath[0:filePath.find("_encrypted.txt")] + "_tempFile.txt"
            file = open(temporary_filePath, 'wt')
            file.write(file_content)
        finally:
            file.close()

        groups = []
        try:
            file = open(temporary_filePath, 'rt')
            for line in file:
                if line[0] == "[":
                    groups.append(line)
        finally:
            file.close()

        print("Which group do you want to delete?")
        print(groups)
        section = input("Type the group name according to the presented list: ")
        section = "[" + section + "]"+'\n'

        new_lines = []
        try:
            file = open(temporary_filePath, 'rt')
            for line in file:
                if line == section:
                    file.readline()
                    file.readline()
                else:
                    new_lines.append(line)
        finally:
            file.close()

        try:
            temporary_filePath = filePath[0:filePath.find("_encrypted.txt")] + "_tempFile.txt"
            file = open(temporary_filePath, 'wt')
            file.writelines(new_lines)
        finally:
            file.close()

        if encryptFile(temporary_filePath, filePath):
            os.remove(temporary_filePath)
            return True

    except:
        print("An error occurred during deleteGroup function")
        return False


def Menu():
    print("What do you want to do?")
    print("1 - Generate the key")
    print("2 - Encrypt the file")
    print("3 - Decrypt the file")
    print("4 - Add new group")
    print("5 - Delete a group")
    print("6 - Exit")

    option = int(input("Type now: "))
    if option == 6:
        exit()

    tkinter.Tk().withdraw()
    filePath = askopenfilename()

    if option == 1:
        filePath = filePath + "\mykey.key"
        if generateKey(filePath):
            print("Your key was generated!")
            Menu()

    elif option == 2:
        fileEncryptedPath = filePath[0:filePath.find(".txt")] + "_encrypted.txt"
        if encryptFile(filePath, fileEncryptedPath):
            print("Your file " + filePath + " was encrypted as " + fileEncryptedPath + "!")
            Menu()

    elif option == 3:
        if decryptFile(filePath, "user"):
            print("Your file " + filePath + " was decrypted!")
            Menu()

    elif option == 4:
        if addGroup(filePath):
            print("Your new group was added and the file " + filePath + " was encrypted!")
            Menu()

    elif option == 5:
        if deleteGroup(filePath):
            print("Your group was deleted and the file " + filePath + " was encrypted!")
            Menu()
    else:
        print("Option invalid!")
Menu()
