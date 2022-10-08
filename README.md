<img src="https://github.com/heiheiyoyo/PyLANDrop/raw/master/LANDrop/icons/banner.png" width="300">

> Drop any files to any devices on your LAN. No need to use instant messaging for that anymore.

LANDrop is a cross-platform tool that you can use to conveniently transfer photos, videos, and other types of files to other devices on the same local network.

You can download prebuilts of LANDrop from the [official website](https://landrop.app/#downloads).

Or you can download it from PyPI by command:
```
pip install LANDrop
```
You can run it by command `landrop`


## Features

- Cross platform: when we say it, we mean it. iOS, Android, macOS, Windows, Linux, name yours.
- Ultra fast: uses your local network for transferring. Internet speed is not a limit.
- Easy to use: intuitive UI. You know how to use it when you see it.
- Secure: uses state-of-the-art cryptography algorithm. No one else can see your files.
- No cellular data: outside? No problem. LANDrop can work on your personal hotspot, without consuming cellular data.
- No compression: doesn't compress your photos and videos when sending.

## Building

The AppImage we provide as the prebuilt for Linux might not work on your machine. You can run LANDrop with python by yourself if the prebuilt doesn't work for you.

To run LANDrop:

1. Download and install the dependencies: 
    ```
    pip install -r requirements.txt
    pip install pyinstaller
    ```
2. Clone this repository
    ```
    git clone https://github.com/heiheiyoyo/PyLANDrop
    ```
3. Run the following commands
    ```
    cd PyLANDrop
    pyinstaller -F LANDrop/main.py -n LANDrop --hidden-import _cffi_backend
    ```
4. You can now run LANDrop via
    ```
    cd dist
    ./LANDrop
    ```
Or you can install the package to your site-packages
```
python setup.py install
```
then you can run it by command `landrop`