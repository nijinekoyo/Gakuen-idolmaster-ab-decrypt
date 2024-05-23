'''
Author: nijineko
Date: 2024-05-23 20:47:38
LastEditTime: 2024-05-23 21:10:14
LastEditors: nijineko
Description: 资源文件导出
FilePath: \Gakuen-idolmaster-ab-decrypt\resource\export.py
'''
import os
import shutil
import decrypt.octodb_pb2


def exportFiles(filesPath: str, outputPath: str, octodb: decrypt.octodb_pb2.Database):
    """ 导出资源文件
    :param filesPath: octo文件夹路径
    :param outputPath: 输出路径
    :param octodb: OctoDB 清单数据
    """

    resourceList: list = octodb.resourceList

    nameMap = {
        value.md5: value.name
        for value in resourceList
    }

    # 遍历所有的AssetBundle文件路径
    for dirPath, _, fileNames in os.walk(filesPath):
        for fileName in fileNames:
            # 检查文件是否存在于nameMap中
            if fileName in nameMap:
                filePath = os.path.join(dirPath, fileName)

                fileExtension = os.path.splitext(nameMap[fileName])[
                    1].split(".")[-1]
                outputFolder = os.path.join(outputPath, fileExtension)

                # 建立output文件夹
                if not os.path.exists(outputFolder):
                    os.makedirs(outputFolder)

                outputFilePath = os.path.join(outputFolder, nameMap[fileName])

                print(f"Exporting {fileName} to {outputFilePath}")

                # 复制文件
                try:
                    shutil.copy(filePath, outputFilePath)
                except Exception as e:
                    raise e
