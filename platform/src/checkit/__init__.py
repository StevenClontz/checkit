import importlib.resources
from . import static
VERSION = importlib.resources.read_text(static, 'VERSION').strip()
