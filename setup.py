from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        name="eeft",
        author="Ryan Hamilton",
        version="0.1.0",
        packages=find_packages(include=["eeft", "eeft.*"]),
        install_requires=["earthengine-api"],
    )
