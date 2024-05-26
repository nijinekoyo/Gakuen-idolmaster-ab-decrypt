'''
Author: nijineko
Date: 2024-05-26 16:27:51
LastEditTime: 2024-05-27 00:40:11
LastEditors: nijineko
Description: AssetBundle文件导出
FilePath: \Gakuen-idolmaster-ab-decrypt\asset_bundle\export.py
'''
import json
import os
import UnityPy
from UnityPy.files.ObjectReader import ObjectReader
import UnityPy.classes
import asset_bundle.image

exportTypes = [
    'Sprite',
    'Texture2D',
    'TextAsset',
    'Shader',
    'MonoBehaviour',
    'Mesh',
    'Font',
    'AudioClip',
    'VideoClip',
]


def exportFiles(filesPath: str, outputPath: str):
    """ 导出AssetBundle文件
    :param filesPath: 解密后的AssetBundle文件存放路径
    :param outputPath: 输出路径
    """

    # 指定Unity版本
    UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.21f1"

    # 遍历所有的AssetBundle文件路径
    for dirPath, _, fileNames in os.walk(filesPath):
        index = 0
        fileNamesCount = len(fileNames)
        for fileName in fileNames:
            assetFilePath = os.path.join(dirPath, fileName)

            # 读取AssetBundle文件
            with open(assetFilePath, "rb") as assetFile:
                # 加载AssetBundle文件
                print(
                    f"({index+1}/{fileNamesCount}) Exporting {os.path.normpath(assetFilePath)}...")
                environment = UnityPy.load(assetFile)
                # 遍历所有的Object
                for object in environment.objects:
                    # 导出Object
                    exportObject(object, outputPath)
            index += 1


def exportObject(object: ObjectReader, outputPath: str):
    """ 导出Object
    :param object: ObjectReader对象
    :param outputPath: 文件输出路径
    """
    objectType = object.type.name
    objectContainer = object.container
    if objectType not in exportTypes:
        return

    # 读取文件数据
    try:
        fileData = object.read()
    except Exception as e:
        print(f"Error: {e}")
        return

    if hasattr(fileData, "name") == False or fileData.name is None or fileData.name == "":
        return

    fileName = fileData.name

    # 组成导出文件路径
    exportFilePath = os.path.join(outputPath, objectType, fileName)
    # 建立文件夹
    if not os.path.exists(os.path.dirname(exportFilePath)):
        os.makedirs(os.path.dirname(exportFilePath))

    # 导出文件
    match objectType:
        case 'Sprite':
            exportFilePath += ".png"
            fileData.image.save(exportFilePath)
        case 'Texture2D':
            exportFilePath += ".png"
            # 检查是否有图片数据
            if not os.path.exists(exportFilePath) and fileData.m_Width:
                imageData = fileData.image
                # 调整部分图片大小
                imageData = asset_bundle.image.resizeByFileName(fileName, imageData)
                imageData.save(exportFilePath)
        case 'TextAsset':
            # 检查是否存在后缀
            if not os.path.splitext(exportFilePath)[1]:
                exportFilePath += ".txt"

            # 写入文件
            with open(exportFilePath, "wb") as f:
                f.write(fileData.script)
        case 'Shader':
            exportFilePath += ".shader"
            # 写入文件
            with open(exportFilePath, "wb") as f:
                f.write(fileData.export().encode("utf8"))
        case 'MonoBehaviour':
            # 如果存在nodes，则转换为json格式储存
            if object.serialized_type.nodes:
                exportFilePath += ".json"
                # 写入文件
                try:
                    file = open(exportFilePath, "wb")
                    file.write(json.dumps(
                        object.read_typetree(),
                        indent=4,
                        ensure_ascii=False
                    ).encode("utf8"))
                # 处理`OSError`异常
                except OSError as e:
                    print(f"Error: {e}")
                except:
                    raise
                else:
                    file.close()
            else:
                exportFilePath += ".bin"
                # 写入文件
                with open(exportFilePath, "wb") as f:
                    f.write(object.raw_data)
        case 'Mesh':
            # Mesh导出到容器命名的文件夹
            if objectContainer is not None:
                exportFilePath = os.path.join(
                    outputPath, objectType, objectContainer, fileName)
                # 建立文件夹
                if not os.path.exists(os.path.dirname(exportFilePath)):
                    os.makedirs(os.path.dirname(exportFilePath))

            exportFilePath += ".obj"

            fileBuf = fileData.export()
            # 如果遇到bool类型则跳过
            if isinstance(fileBuf, bool):
                return
            # 写入文件
            with open(exportFilePath, "wt", newline="") as f:
                f.write(fileBuf)
        case 'Font':
            if fileData.m_FontData:
                if fileData.m_FontData[0:4] == b"OTTO":
                    exportFilePath += ".otf"
                else:
                    exportFilePath += ".ttf"
                # 写入文件
                with open(exportFilePath, "wb") as f:
                    f.write(fileData.m_FontData)
        case 'AudioClip':
            samples = fileData.samples
            for name, clip_data in samples.items():
                # 检查是否存在后缀
                if not os.path.splitext(name)[1]:
                    name += ".wav"

                exportFilePath = os.path.join(
                    outputPath, objectType, fileName, name)
                # 建立文件夹
                if not os.path.exists(os.path.dirname(exportFilePath)):
                    os.makedirs(os.path.dirname(exportFilePath))
                # 写入文件
                with open(exportFilePath, "wb") as f:
                    f.write(clip_data)
        case 'VideoClip':
            exportFilePath += ".mp4"
            # 写入文件
            with open(exportFilePath, "wb") as f:
                f.write(fileData.m_VideoData)
        case _:
            print(f"Unknown type: {objectType}")
            return
