'''
Author: nijineko
Date: 2024-05-23 16:37:07
LastEditTime: 2024-05-23 20:58:10
LastEditors: nijineko
Description: main
FilePath: \Gakuen-idolmaster-ab-decrypt\main.py
'''
from decrypt.octodb import octodbDecrypt
from decrypt.asset_bundle import assetBundleDecryptToFile
from resource.export import exportFiles


def main():
    octodb = octodbDecrypt("./octo/pdb/400/205000/octocacheevai")

    try:
        # 解密AssetBundle
        assetBundleDecryptToFile("./octo", "./output/asset_bundle", octodb)

        # 导出资源文件
        exportFiles("./octo", "./output/resource", octodb)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    main()
