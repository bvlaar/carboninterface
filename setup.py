from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="carboninterface",
    version="1.0",
    description="Carbon Interface Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxhumber/carboninterface",
    author="Max Humber",
    author_email="max.humber@gmail.com",
    license="MIT",
    py_modules=["carboninterface"],
    python_requires=">=3.6",
    setup_requires=["setuptools>=38.6.0"],
    install_requires=["requests>=2.23.0"]
)
