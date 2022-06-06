from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="checkit-dashboard",
    install_requires=[
        "ipywidgets",
        "lxml",
        "latex2mathml",
        "pystache",
        "click",
    ],
)
