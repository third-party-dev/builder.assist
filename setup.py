from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="thirdparty-builder-assist",
    version="0.1.1",
    description="Tool for automatically building source on save.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vincent Agriesti",
    author_email="crazychenz@gmail.com",
    url="https://github.com/third-party-dev/builder.assist",
    # In reality this could be 3.3. ... keeping this 3.7 or greater means
    # we reserve the right to use monotonic_ns() in the future. This should
    # probably never be less than 3.6 for asyncio.
    python_requires='~=3.7',
    packages=[
        "thirdparty",
        "thirdparty.builder",
        "thirdparty.builder.assist"
    ],
    entry_points={
        'console_scripts': ['assist=thirdparty.builder.assist.cli:main'],
    },
    package_dir={"": "src"},
    install_requires=[
        "inotify"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
)
