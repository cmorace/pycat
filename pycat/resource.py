import pyglet.resource


def set_resource_directory(path: str):
    """Set the directory to load resources from.

    path is relative to script calling `window.run()`
    """
    pyglet.resource.path = [path]
    pyglet.resource.reindex()
