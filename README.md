## ftool-gui

## 简介

在 macOS 上进行 frida 相关操作的图形化小工具

## 开发

```

git clone https://github.com/soft98-top/ftool-gui.git

cd ftool-gui

python -m pip install -r requirements.txt

pyinstaller --onefile --windowed --add-data "code:code" ftool-gui.py

```

## 使用

[ftool-gui: macos上的frida小工具](https://www.bilibili.com/video/BV1foHTeYEaW/?share_source=copy_web&vd_source=2d5ecb3cfaa551915a9d017370564488)

## 提示

如果在attach时遇到了`SyntaxError: unexpected character`，大概率是因为系统的智能引号功能，请在设置中搜索然后关闭，然后重新打开ftool-gui进行使用。