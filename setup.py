import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pins",
    version="0.0.1",
    author="Mark Sellors",
    author_email="python@5vcc.com",
    description="A simple python implementation of RStudio's pins package to work with RStudio Connect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sellorm/python-pins",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
