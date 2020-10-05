from cryptography.fernet import Fernet
import os

def generateKey(filePath):
    try:
        key = Fernet.generate_key()
        file = open(filePath, 'wb')
        file.write(key)        
        return True
    except:
        print("An error ocurred during generateKey function")
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
        print("An error ocurred during readKey function")
        return ""
    finally:
        file.close()

def cryptFile(filePath, content):
    try:       
        auth = Fernet(readKey())        
        text = auth.encrypt(content.encode('utf-8'))
        file = open(filePath, 'wb')
        file.write(text)
        return True
    except:
        print("An error ocurred during cryptFile function")
        return False
    finally:
        file.close()

def decryptFile(filePath):
    try:
        auth = Fernet(readKey())
        file = open(filePath, 'rb')
        file_text = file.read()        
        text = auth.decrypt(file_text)        
        return text.decode('utf-8')
    except:
        print("An error ocurred during decryptFile function")
        return ""
    finally:
        file.close()

def addGroup():
    try:
        section = input("Type the section name: ")
        user = input("Type the username: ")
        password = input("Type the password: ")
        text = section + '\n' + user + '\n' + password
        return text
    except:
        print("An error ocurred during addGroup function")
        return ""

print("What do you want to do?")
print("1 - Generate the key")
print("2 - Crypto the file")
print("3 - Decrypto the file")
print("4 - Add new group")

option = int(input("Type now: "))

if option == 1:
    filePath = input("Type the location to save your key: ")
    filePath = filePath + "\mykey.key"
    if generateKey(filePath):
        print("Your key was generated!")
elif option == 2:
    fileToCryptPath = input("Type the file location to crypt: ")
    fileCryptedPath =  fileToCryptPath[0:fileToCryptPath.find(".txt")] + "_crypted.txt"

    try:
        file = open(fileToCryptPath, 'rt')
        file_content = file.read()
    finally:
        file.close()

    if cryptFile(fileCryptedPath, file_content):
        print("Your file "+ fileToCryptPath +" was crypted as "+ fileCryptedPath +"!")
elif option == 3:
    filePath = input("Type the file location: ")
    text = decryptFile(filePath)
    if text != "":
        print("Your file "+ filePath +" was decrypted!")
        option = (input("Do you want to save the result to a file? [Y] or [N]")).upper()

        if option == "Y":
            try:
                new_filePath = filePath[0:filePath.find("_crypted.txt")] + "_decrypted.txt"
                file = open(new_filePath, 'wt')
                file.write(text)                 
            finally:
                file.close()
        else:
            print(text)
elif option == 4:
    filePath = input("Type the file location: ")
    text = decryptFile(filePath)
    new_text = addGroup()
    content = text + "\n" + new_text

    if cryptFile(filePath, content):
        print("Your new section was added and the file "+ filePath +" was crypted!")
else:
    print("Option invalid!")