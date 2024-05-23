'''
Author: nijineko
Date: 2024-05-23 16:37:07
LastEditTime: 2024-05-23 18:13:24
LastEditors: nijineko
Description: main
FilePath: \Gakuen-idolmaster-ab-decrypt\main.py
'''
from decrypt.octodb import octodbDecrypt
from decrypt.asset_bundle import assetBundleDecryptToFile


def main():
    octodb = octodbDecrypt("./Octo/pdb/400/205000/octocacheevai")

    # 解密AssetBundle
    assetBundleDecryptToFile("./Octo/v1/400", "./output", octodb)


if __name__ == '__main__':
    main()
