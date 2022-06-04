import importlib.resources

def read_resource(resource_name):
    return importlib.resources.read_text("checkit.static", resource_name)

def open_resource(resource_name):
    return importlib.resources.open_binary("checkit.static", resource_name)