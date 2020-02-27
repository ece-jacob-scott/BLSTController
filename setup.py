import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BLSTController",
    version="0.1.1",
    author="Jacob Scott",
    author_email="jscott35@uic.edu",
    description="Main library for allowing control of BLST foot pedals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ece-jacob-scott/BLSTController",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyserial"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)