from cryptography.fernet import Fernet
import os
import tkinter
from enum import Enum
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
import logging

class fileType(Enum):
    fileEncrypted = 1
    fileNotEncrypted = 2

class option(Enum):
    script = 1
    user = 2

def setLog():
    logging.root.handlers = []
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename='Log.txt')

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

def generateKey(filePath):
    try:
        key = Fernet.generate_key()
        file = open(filePath, 'wb')
        file.write(key)
        return True
    except:
        logging.error("An error occurred during generateKey function")
        return False
    finally:
        logging.info("The personal key was generated")
        file.close()


def readKey():
    try:
        key_path = os.path.dirname(os.path.realpath(__file__))
        key_path = key_path + "\mykey.key"
        file = open(key_path, 'rb')
        key = file.read()
        return key
    except:
        logging.error("An error occurred during readKey function")
        return ""
    finally:
        logging.info("The key was retrieved")
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
        logging.error("An error occurred during encryptFile function")
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
            if option == option.script:
                return text
            else:
                x = 0
                while x < 10:
                    inputOption = (input("Do you want to [S]ave the result to a file or [P]rint? [S] or [P]")).upper()
                    if inputOption == "S":
                        try:
                            new_filePath = filePath[0:filePath.find("_encrypted.txt")] + "_decrypted.txt"
                            file = open(new_filePath, 'wt')
                            file.write(text)
                        finally:
                            file.close()
                    elif inputOption == "P":
                        logging.info(text)
                        print(text)
                    else:
                        logging.warning("This option is not valid, please try again!")
                    break
                return True
    except:
        logging.exception("An error occurred during decryptFile function")
        return False
    finally:
        logging.info("The file is empty")
        file.close()


def addGroup(filePath, fileType):
    try:
        section = input("Type the group name: ")
        section = "[" + section + "]"

        user = input("Type the username: ")
        user = "user=" + user

        password = input("Type the password: ")
        password = "password=" + password

        if fileType == fileType.fileEncrypted:
            file_content = decryptFile(filePath, option.script)
        else:
            file_content = ""

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
        logging.exception("An error occurred during addGroup function")
        return False


def deleteGroup(filePath):
    try:
        file_content = decryptFile(filePath, option.script)
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
        logging.exception("An error occurred during deleteGroup function")
        return False

def createFile(filePath):
    try:
        open(filePath, 'w')
        addGroup(filePath, fileType.fileNotEncrypted)
    except:
        logging.exception("An error occurred during createFile function")
        return False

def Menu():
    setLog()
    logging.info("Starting the menu")

    print("What do you want to do?")
    print("1 - Generate the key")
    print("2 - Encrypt the file")
    print("3 - Decrypt the file")
    print("4 - Add new group")
    print("5 - Delete a group")
    print("6 - Create new file")
    print("7 - Exit")

    inputOption = int(input("Type now: "))
    if inputOption == 7:
        exit()

    tkinter.Tk().withdraw()
    if inputOption != 1 and inputOption != 6:
        filePath = askopenfilename()

    if inputOption == 1:
        filePath = askdirectory()
        filePath = filePath + "\mykey.key"
        if generateKey(filePath):
            print("Your key was generated!")
            logging.info("Your key was generated!")
            Menu()

    elif inputOption == 2:
        fileEncryptedPath = filePath[0:filePath.find(".txt")] + "_encrypted.txt"
        if encryptFile(filePath, fileEncryptedPath):
            print("Your file " + filePath + " was encrypted as " + fileEncryptedPath + "!")
            logging.info("Your file " + filePath + " was encrypted as " + fileEncryptedPath + "!")
            Menu()

    elif inputOption == 3:
        if decryptFile(filePath, option.user):
            print("Your file " + filePath + " was decrypted!")
            logging.info("Your file " + filePath + " was decrypted!")
            Menu()

    elif inputOption == 4:
        if addGroup(filePath, fileType.fileEncrypted):
            print("Your new group was added and the file " + filePath + " was encrypted!")
            logging.info("Your new group was added and the file " + filePath + " was encrypted!")
            Menu()

    elif inputOption == 5:
        if deleteGroup(filePath):
            print("Your group was deleted and the file " + filePath + " was encrypted!")
            logging.info("Your group was deleted and the file " + filePath + " was encrypted!")
            Menu()
    elif inputOption == 6:
        filePath = asksaveasfilename()
        fileEncryptedPath = filePath[0:filePath.find(".txt")] + "_encrypted.txt"
        if createFile(fileEncryptedPath):
            print("Your file was created " + fileEncryptedPath + " and was encrypted!")
            logging.info("Your file was created " + fileEncryptedPath + " and was encrypted!")
            Menu()
    else:
        print("Option invalid!")
        logging.warning("Option invalid!")
Menu()
