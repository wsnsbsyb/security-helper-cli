from setuptools import setup, find_packages

setup(
    name="security-cheat-cli",
    version="0.1.0",
    description="命令行安全速查表工具",
    author="你的名字",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'security-cheat=main:main',
        ],
    },
)