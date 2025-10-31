from setuptools import setup, find_packages

setup(
    name="mac_wait",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "psutil>=5.9.0",
        "pynput>=1.7.6"
    ],
    entry_points={
        "console_scripts": [
            "mac_wait = mac_wait.main:main"  # main.py에 main() 함수 필요
        ]
    },
)
