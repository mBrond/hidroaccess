from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hidroaccess ",
    version="1.1.0",
    author="Miguel Brondani",
    author_email="brondani.miguel@gmail.com",
    description="Pacote python para facilitar o acesso a API HidroWebService",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mBrond/AccessHidroWebService",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.11",
        "requests>=2.32.3",
        "pandas>=2.2.3",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    keywords="accesshidrowebservice api water data hidroclient",
    project_urls={
        "Bug Reports": "https://github.com/mBrond/AccessHidroWebService/issues",
        "Source": "https://github.com/mBrond/AccessHidroWebService",
    },
    license="MIT",
    license_files=("LICENSE"), 
    include_package_data=True,
)