from setuptools import setup

long_description = open('README.md').read()

setup(
    name="python-tortilla",
    version='2.0',
    packages=["tortilla"],
    description="A Python library for dipping into Salsa",
    url="https://github.com/sunlightlabs/python-tortilla",
    author="Jeremy Carbaugh",
    author_email="jcarbaugh@sunlightfoundation.com",
    license='BSD',
    long_description=long_description,
    platforms=["any"],
    install_requires=["requests==2.2.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)