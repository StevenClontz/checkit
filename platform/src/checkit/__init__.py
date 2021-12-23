import importlib.resources as pkg_resources
from . import static
VERSION = pkg_resources.read_text(static, 'VERSION').strip()
