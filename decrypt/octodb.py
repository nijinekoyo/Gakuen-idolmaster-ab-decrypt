'''
Author: nijineko
Date: 2024-05-23 16:38:53
LastEditTime: 2024-05-23 18:14:04
LastEditors: nijineko
Description: octodb解密
FilePath: \Gakuen-idolmaster-ab-decrypt\decrypt\octoDB.py
'''
import hashlib
from Crypto.Cipher import AES
import decrypt.octodb_pb2
from Crypto.Util.Padding import unpad

# 常量定义
KEY = "1nuv9td1bw1udefk"
IV = "LvAUtf+tnz"


def octodbDecrypt(filepath: str) -> decrypt.octodb_pb2.Database:
    """ 解密OctoDB

    :param filepath: 加密文件路径
    :return: 解密后的 protobuf 对象
    """

    key = bytes(KEY, "utf-8")
    iv = bytes(IV, "utf-8")

    key = hashlib.md5(key).digest()
    iv = hashlib.md5(iv).digest()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 读取加密文件
    with open(filepath, "rb") as f:
        encryptedBytes = f.read()

    try:
        # 由于某种原因，加密文件的开头有一个额外的 0x01 字节
        decryptedBytes = unpad(cipher.decrypt(
            encryptedBytes[1:]), block_size=16, style="pkcs7")
    except:
        print("Failed to decrypt cache file")
        raise

    # 前16个字节是其后面的数据库的md5，跳过
    decryptedBytes = decryptedBytes[16:]
    # 将解密的字节读取到 protobuf 对象
    protoDatabase = decrypt.octodb_pb2.Database()
    protoDatabase.ParseFromString(decryptedBytes)

    return protoDatabase