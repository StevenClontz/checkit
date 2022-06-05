import setuptools

with open("checkit/static/README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

with open("checkit/static/VERSION", "r") as vf:
    VERSION = vf.read().strip()

with open("checkit/static/PYTHON_VERSION", "r") as vf:
    PYTHON_VERSION = vf.read().strip()

setuptools.setup(
    name="checkit-dashboard",
    version=VERSION,
    author="Steven Clontz",
    author_email="steven.clontz@gmail.com",
    description="Dashboard for authoring/disseminating randomized exercises",
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
    python_requires=f">={PYTHON_VERSION}",
    packages=setuptools.find_packages(),
    package_data={
        "checkit": [
            "static/*", 
            "wrapper/*",
        ],
    },
    install_requires=[
        'ipywidgets',
        'lxml',
        'latex2mathml',
        'pystache',
        'click',
    ],
    extras_require={
        'dev': [
            'build',
            'twine',
            'ipykernel',
        ]
    }
)
