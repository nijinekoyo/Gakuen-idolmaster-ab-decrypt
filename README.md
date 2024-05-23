# Gakuen-idolmaster-ab-decrypt
学园偶像大师(学園アイドルマスター) AssetBundle 文件解密工具

## Use
1. 安装依赖
``` shell
pip install -r requirements.txt
```
2. 以安卓系统为例，将游戏文件`/data/data/com.bandainamcoent.idolmaster_gakuen/files/Octo`拷贝到项目目录下，**注意：此步需要设备具有Root权限**
3. 执行脚本，等待解密完成
``` shell
python ./main.py
```
4. 使用其他工具解开AssetBundle打包即可获得游戏文件

## Unity Version
游戏AssetBundle包内的Unity Version被去掉了，需要人工补齐版本号，目前游戏使用的Unity版本号为`2022.3.21f1`

## Thank
1. [gkmasToolkit](https://github.com/kishidanatsumi/gkmasToolkit): 提供了解密思路
2. [gakuen-idolmaster-global-metadata-decrypt](https://github.com/chinosk6/gakuen-idolmaster-global-metadata-decrypt) [Issues #1](https://github.com/chinosk6/gakuen-idolmaster-global-metadata-decrypt/issues/1): 提供了大量的帮助