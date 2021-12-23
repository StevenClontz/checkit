import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

with open("platform/src/checkit/static/VERSION", "r") as vf:
    VERSION = vf.read().strip()

with open("platform/src/checkit/static/PYTHON_VERSION", "r") as vf:
    PYTHON_VERSION = vf.read().strip()

setuptools.setup(
    name="checkit-platform",
    version=VERSION,
    author="Steven Clontz",
    author_email="steven.clontz@gmail.com",
    description="Platform for authoring/disseminating randomized exercises",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/stevenclontz/checkit",
    project_urls={
        "Bug Tracker": "https://github.com/stevenclontz/checkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "platform/src"},
    packages=setuptools.find_packages(where="platform/src"),
    python_requires=f">={PYTHON_VERSION}",
    package_data={
        "checkit": ["static/*"],
    },
    install_requires=[],
    extras_require={
        'dev': [
            'build',
            'twine',
        ]
    }
)