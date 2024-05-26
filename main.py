'''
Author: nijineko
Date: 2024-05-23 16:37:07
LastEditTime: 2024-05-26 16:30:05
LastEditors: nijineko
Description: main
FilePath: \Gakuen-idolmaster-ab-decrypt\main.py
'''
import decrypt.octodb
import decrypt.asset_bundle
import resource.export


def main():
    octodb = decrypt.octodb.decryptOctoDB(
        "./octo/pdb/400/205000/octocacheevai")

    try:
        # 解密AssetBundle
        decrypt.asset_bundle.decryptToFile(
            "./octo", "./output/asset_bundle", octodb)

        # 导出资源文件
        resource.export.exportFiles("./octo", "./output/resource", octodb)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    main()
