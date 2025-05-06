import copy
import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

__encrypted = []
__javaDecoderFilePath = ""
__encryptorFileName = "MyCipher.java"
__mainKeyHex = secrets.token_bytes(16).hex()
__mainIvHex = secrets.token_bytes(16).hex()


def _getEncrypted():
    return __encrypted


def setJavaDecoderFilePath(path="src/logic/Encoding/JavaDecoder"):
    __javaDecoderFilePath = path


def getJavaDecoderFilePath():
    return os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "test",
        "output",
    )


def getEncrypted():
    return copy.deepcopy(__encrypted)


def _encode(string):
    key_hex = __mainKeyHex

    # Convert the hexadecimal key to bytes
    key = bytes.fromhex(key_hex)

    # Input string to encrypt
    input_string = string

    # Generate a random initialization vector (IV)
    iv = bytes.fromhex(__mainIvHex)

    # Create an AES cipher with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))

    # Encrypt the input string
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(input_string.encode()) + encryptor.finalize()

    # Print the IV and ciphertext in hexadecimal format
    iv_hex = __mainIvHex
    ciphertext_hex = ciphertext.hex()
    return ciphertext_hex, iv_hex, key_hex


def printAllEncoded():
    for encodedIdentifier in getEncrypted():
        encodedIdentifier.print()


def makeJavaDecoder():
    javaFileFirstPart = os.path.join(
        os.path.dirname(__file__), "JavaDecoder", "FirstPart"
    )
    javaFileSecondPart = os.path.join(
        os.path.dirname(__file__), "JavaDecoder", "SecondPart"
    )
    writePath = os.path.join(getJavaDecoderFilePath(), __encryptorFileName)
    if not os.path.exists(getJavaDecoderFilePath()):
        os.makedirs(getJavaDecoderFilePath())
    with open(javaFileFirstPart, "r") as firstPart:
        firstPartText = firstPart.read()
    with open(javaFileSecondPart, "r") as secondPart:
        secondPartText = secondPart.read()
    with open(writePath, "w") as javaFile:
        javaFile.write("")
    with open(writePath, "a") as java_file:
        java_file.write(firstPartText)
        java_file.write(f'\tprivate final String mainKeyHex = "{__mainKeyHex}";\n'
                        f"\n"
                        f'\tprivate final String mainIvHex = "{__mainIvHex}";\n\n'
                        "\tprivate MyCipher(){\n"
                        "\t\tmap = new HashMap<>();\n"
                        )
        for item in getEncrypted():
            try:
                tempString = item.identifier.name + " " + item.identifier.value
            except:
                tempString = ""
            java_file.write(

                f"\t\tmap.put(\n"
                f'\t\t"{item.cipherHex}"\n'
                f"\t\t,new ArrayList<>(Arrays.asList(\n"
                f'\t\t"{item.keyHex}","{item.ivHex}")));//{tempString} \n '
            )
        java_file.write(secondPartText)


def encodeIdentifier(identifier):
    isBuilt, encoded = __alreadyBuiltID(identifier)
    if not isBuilt:
        newEncoder = Encoder(identifier, None)
        return newEncoder
    else:
        return encoded


def encodeString(string, line, file):
    isBuilt, encoded = __alreadyBuiltString(string, line, file)
    if not isBuilt:
        newEncoder = Encoder(None, string, line, file)
        return newEncoder
    else:
        return encoded


def __alreadyBuiltID(identifier):
    for encrypted in __encrypted:
        if identifier and encrypted.identifier == identifier:
            return True, encrypted
    return False, None


def __alreadyBuiltString(string, line, file):
    for encrypted in __encrypted:
        if encrypted.string == string:
            return True, encrypted
    return False, None


class Encoder:
    def __init__(self, identifier, string, line=None, file=None):
        self.identifier = identifier
        self.string = string
        if identifier is not None:
            self.cipherHex, self.ivHex, self.keyHex = _encode(
                self.identifier.getValue()
            )
            _getEncrypted().append(self)
        else:
            self.cipherHex, self.ivHex, self.keyHex = _encode(self.string)
            self.line = line
            self.file = file
            _getEncrypted().append(self)

    def print(self):
        if self.identifier is None:
            print(self.string, self.cipherHex)
        else:
            print(self.identifier.name, self.cipherHex)