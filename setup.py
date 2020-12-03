from setuptools import setup

setup(
    name="thirdparty.builder.assist",
    version="0.1.0",
    description="Tool for automatically building source on save.",
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
)
