import setuptools

with open("requirements.txt") as fin:
    REQUIRED_PACKAGES = fin.read()

setuptools.setup(
    name='LANDrop',
    version='0.4.0',
    description='LANDrop is a cross-platform tool that you can use to conveniently transfer photos, videos, and other types of files to other devices on the same local network.',
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author='heiheiyoyo',
    author_email='543425864@qq.com',
    url='https://github.com/heiheiyoyo/PyLANDrop',
    install_requires=REQUIRED_PACKAGES,
    packages=['LANDrop'],
    license="BSD-3",
    python_requires='>=3.6',
    entry_points={'console_scripts': ['landrop = LANDrop.__main__:main']}
)
