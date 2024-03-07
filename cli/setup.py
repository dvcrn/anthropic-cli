from setuptools import setup, find_packages

setup(
    name="anthropic-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic",
    ],
    entry_points={
        "console_scripts": [
            "anthropic-cli = cli.cli:main",
        ],
    },
)