from setuptools import setup


README = open("README.md").read()

setup(
    name="optionchain_stream",  
    version="0.6",
    author="OM CHOKSI",
    author_email="omchoksi108@gmail.com",
    description="Python library for live streaming option chain using DHAN Websocket",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/OMCHOKSI108/DHAN/OptionChainStream",
    packages=['optionchain_stream'],
    install_requires=["redis"],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries"
    ],
)