'''
Author: nijineko
Date: 2024-05-26 16:38:10
LastEditTime: 2024-05-26 20:09:15
LastEditors: nijineko
Description: 导出AssetBundle文件
FilePath: \Gakuen-idolmaster-ab-decrypt\export_asset_bundle.py
'''
import asset_bundle.export


def main():
    # 导出AssetBundle文件
    asset_bundle.export.exportFiles(
        "./output/asset_bundle", "./output/asset_bundle_export")


if __name__ == '__main__':
    main()
