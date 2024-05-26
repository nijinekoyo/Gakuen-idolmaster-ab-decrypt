'''
Author: nijineko
Date: 2024-05-27 00:45:52
LastEditTime: 2024-05-27 01:42:08
LastEditors: nijineko
Description: 图片处理
FilePath: \Gakuen-idolmaster-ab-decrypt\asset_bundle\image.py
'''
import re
from PIL import Image


def resize(image: Image.Image, width: int, height: int) -> Image.Image:
    """ 调整图片大小
    :param image: 图片对象
    :param width: 宽度
    :param height: 高度
    :return: 调整后的图片对象
    """
    return image.resize((width, height), Image.BICUBIC)


def resizeByFileName(fileName: str, image: Image.Image) -> Image.Image:
    """ 按照文件名调整图片大小
    :param fileName: 文件名
    :param image: 图片对象
    :return: 调整后的图片对象
    """
    pattern = r'^img_general_csprt-.*_full$'
    if re.match(pattern, fileName):
        return resize(image, 2560, 1440)
    pattern = r'^img_general_cidol-.+-thumb-landscape-large$'
    if re.match(pattern, fileName):
        return resize(image, 2560, 1440)
    pattern = r'^img_general_cidol-.+-full$'
    if re.match(pattern, fileName):
        return resize(image, 1440, 2560)
    pattern = r'^img_adv_still_.+$'
    if re.match(pattern, fileName):
        return resize(image, 1440, 2560)
    pattern = r'^img_general_comic_\d+$'
    if re.match(pattern, fileName):
        return resize(image, 1024, 768)
    
    return image
