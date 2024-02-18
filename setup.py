from setuptools import find_packages, setup
from pathlib import Path

setup(
    name="sirm_spf_libs",
    packages=find_packages(
        include=[
            "sirm_spf_libs",
            "sirm_spf_libs.*",
        ],
        exclude=[
            "tests",
        ],
    ),
    version="2024.0217.1248.alpha",
    description="Basic SPF tools to work with an FPS database",
    author="Charles E Vopicka",
    install_requires=[
        "pathlib",
        "configparser",
        "pyodbc",
    ],
    setup_requires=[],
    tests_requires=[],
    test_suite="",
    license="LICENSE",
    include_package_data=True,
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
