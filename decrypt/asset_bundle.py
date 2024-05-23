'''
Author: nijineko
Date: 2024-05-23 17:04:07
LastEditTime: 2024-05-23 20:52:22
LastEditors: nijineko
Description: AssetBundle解密
FilePath: \Gakuen-idolmaster-ab-decrypt\decrypt\asset_bundle.py
'''
import os
import decrypt.octodb_pb2

def stringToMaskBytes(maskString: str, maskStringLength: int, bytesLength: int) -> bytes:
    maskBytes = bytearray(bytesLength)
    if maskString != 0:
        if maskStringLength >= 1:
            i = 0
            j = 0
            k = bytesLength - 1
            while maskStringLength != j:
                charJ = maskString[j]
                # 在python中必须强制转换为 Int
                charJ = int.from_bytes(charJ.encode(
                    "ascii"), byteorder='little', signed=False)
                j += 1
                maskBytes[i] = charJ
                i += 2
                # 您必须添加 &0xFF 才能在 python 中获取无符号整数，否则它将返回有符号整数
                charJ = ~charJ & 0xFF
                maskBytes[k] = charJ
                k -= 2
        if bytesLength >= 1:
            l = bytesLength
            v13 = 0x9B
            m = bytesLength
            pointer = 0
            while m:
                v16 = maskBytes[pointer]
                pointer += 1
                m -= 1
                v13 = (((v13 & 1) << 7) | (v13 >> 1)) ^ v16
            b = 0
            while l:
                l -= 1
                maskBytes[b] ^= v13
                b += 1
    return bytes(maskBytes)


def assetBundleDecrypt(input: bytes, maskString: str, offset: int = 0, streamPos: int = 0, headerLength: int = 256) -> bytes:
    """ 解密 AssetBundle文件
    :param input: 加密文件
    :param maskString: 解密密钥
    :param offset: 偏移量
    :param streamPos: 流位置
    :param headerLength: 头长度
    :return: 解密后的文件
    """

    maskStringLength = maskString.__len__()
    bytesLength = maskStringLength << 1
    buffer = bytearray(input)
    maskBytes = stringToMaskBytes(maskString, maskStringLength, bytesLength)
    i = 0
    while streamPos + i < headerLength:
        buffer[offset + i] ^= maskBytes[streamPos + i -
                                        int((streamPos + i) / bytesLength) * bytesLength]
        i += 1
    return bytes(buffer)


def assetBundleDecryptToFile(filesPath: str, outputPath: str, octodb: decrypt.octodb_pb2.Database):
    """ 解密 AssetBundle文件
    :param filesPath: octo文件夹路径
    :param outputPath: 输出路径
    :param octodb: OctoDB 清单数据
    """

    assetList: list = octodb.assetBundleList

    nameMap = {
        value.md5: value.name
        for value in assetList
    }

    # 建立output文件夹
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # AssetBundle文件头
    unityFileHead = b"\x55\x6e\x69\x74\x79"

    # 遍历所有的AssetBundle文件路径
    for dirPath, _, fileNames in os.walk(filesPath):
        for fileName in fileNames:
            filePath = os.path.join(dirPath, fileName)
            outputFilePath = os.path.join(outputPath, fileName)

            # 检查文件是否存在于nameMap中
            if fileName in nameMap:
                with open(filePath, "rb") as f:
                    encryptedABFileBytes = f.read()

                    # 检查是否被加密
                    if encryptedABFileBytes[0:5] == unityFileHead:
                        # 如果没有加密则直接写入
                        with open(outputFilePath, "wb") as outputFile:
                            outputFile.write(encryptedABFileBytes)
                    else:
                        # 解密文件
                        decryptedABFileBytes = assetBundleDecrypt(
                            encryptedABFileBytes, nameMap[fileName])
                        if decryptedABFileBytes.__len__() > 0 and decryptedABFileBytes[0:5] == unityFileHead:
                            # 解密成功，写入文件
                            with open(outputFilePath, "wb") as outputFile:
                                outputFile.write(decryptedABFileBytes)

                            print(f"Decrypted {fileName}")
                        else:
                            print(f"Failed to decrypt {fileName}")
                            raise Exception(f"Failed to decrypt {fileName}")
